###########
# imports #
###########

# Standard imports
import ROOT
import os
from array import array
from copy import deepcopy
import math

# RootTools
from RootTools.core.standard import *

# DeepLepton
from DeepLepton.Tools.helpers import getObjDict, getCollection
from DeepLepton.samples.flat_training_samples import *

# User specific 
from DeepLepton.Tools.user import plot_directory
plot_directory_=os.path.join(plot_directory, 'DeepLepton')
plot_directory=plot_directory_

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',           default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--small',              action='store_true',                help='Run only on a small subset of the data?', )
argParser.add_argument('--plot_directory',     action='store',           default='deepLepton')
argParser.add_argument('--ptMin',              action='store',      type=int,     default=25)
argParser.add_argument('--ptMax',              action='store',      type=int,     default=0)
argParser.add_argument('--flat',               action='store_true',                 help='Run on flat ntuple data?', )
argParser.add_argument('--flatSample',         action='store',           default='TTJets_Muons_balanced_pt5toInf_2016')

argParser.add_argument('--year',               action='store', type=int, choices=[2016,2017],   default=2016,   help="Which year?")
argParser.add_argument('--flavour',            action='store', type=str, choices=['ele','muo'], default='muo',  help="Which Flavour?")
argParser.add_argument('--testData',           action='store_true',      help="plot test or train data?")
argParser.add_argument('--looseId',            action='store_true',      help="plot data with looseId preselection?")
argParser.add_argument('--trainingClasses',    action='store', type=str, choices=['fullClasses','simpleClasses','noTraining'], default='fullClasses',  help="Which lepton classes, select no training for input data plots?")


#argParser.add_argument('--selection',          action='store',      default='dilepOS-njet3p-btag1p-onZ')
args = argParser.parse_args()

# Logger
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

# adapted from RootTools (added fillstyle)
def fillStyle( color, style, lineColor = ROOT.kBlack, errors = False):
    def func( histo ):
        lc = lineColor if lineColor is not None else color
        histo.SetLineColor( lc )
        histo.SetMarkerSize( 0 )
        histo.SetMarkerStyle( 0 )
        histo.SetMarkerColor( lc )
        histo.SetFillColor( color )
        histo.SetFillStyle( style)
        histo.drawOption = "hist"
        if errors: histo.drawOption+='E'
        return 
    return func


##############################
# load samples and variables #
##############################

maxN = -1
if args.small:
    maxN = 2

#get flat sample
if args.flat:

    sampleInfo = vars()[args.flatSample]
    flat_files, predict_files = get_flat_files( sampleInfo['flat_directory'], sampleInfo['predict_directory' if args.testData else 'predict_directory_trainData'], maxN)
    sample = get_flat_sample( sampleInfo['training_name'], sampleInfo['sample_name'], flat_files, predict_files )

else:
    print "FIXME: implement full events first."

# variables to read
flat_variables = get_flat_variables(args.trainingClasses)

#########################
# define plot structure #
#########################

plotDate=sampleInfo["training_date"]

leptonFlavour=[]
ecalTypes=[]

if args.flavour=="ele":
    sampleEle=sample
    leptonFlavour = {"Name":"Electron", "ShortName":"ele", "pdgId":11, "sample":sample, "selectionString": "abs(lep_pdgId)==11", "date":plotDate}
    ecalTypes.append({"Name":"All", "selectionString": "abs(lep_etaSc)>=0."})
    ecalTypes.append({"Name":"EndCap", "selectionString": "abs(lep_etaSc)>1.479"})
    ecalTypes.append({"Name":"Barrel", "selectionString": "abs(lep_etaSc)<=1.479"})

if args.flavour=="muo":
    sampleMuo=sample
    leptonFlavour = {"Name":"Muon", "ShortName":"muo", "pdgId":13, "sample":sample, "selectionString": "abs(lep_pdgId)==13", "date":plotDate}
    ecalTypes.append({"Name":"All", "selectionString": "abs(lep_eta)>=0."})

# pt selection
kinematic_selection = "lep_pt>{ptMin}".format(ptMin = args.ptMin) if args.ptMax==0 else "lep_pt>{ptMin}&&lep_pt<={ptMax}".format(ptMin = args.ptMin, ptMax = args.ptMax)
kinematic_selection_name = "pt{ptMin}to{ptMax}".format(ptMin = args.ptMin, ptMax = 'Inf' if args.ptMax==0 else args.ptMax)

#PF Candidates
pfCand_plot_binning = {
                'neutral'  : {'mult': [21,0,20],'sumPt': [50,0,25] },
                'charged'  : {'mult': [71,0,70],'sumPt': [50,0,100]}, 
                'photon'   : {'mult': [41,0,40],'sumPt': [50,0,50] }, 
                'electron' : {'mult': [21,0,20],'sumPt': [50,0,25] }, 
                'muon'     : {'mult': [21,0,20],'sumPt': [50,0,25] },
             }
pfCand_flavors = pfCand_plot_binning.keys()


####################################
# loop over samples and draw plots #
####################################

loose_id = "abs(lep_pdgId)==13&&lep_pt>5&&abs(lep_eta)<2.4&&lep_miniRelIso<0.4&&lep_sip3d<8&&abs(lep_dxy)<0.05&&abs(lep_dz)<0.1&&lep_pfMuonId&&lep_mediumMuonId"
preselectionString= loose_id if args.looseId else "abs(lep_pdgId)==13&&lep_pt>5" 

#define class samples
if args.trainingClasses in ['fullClasses', 'noTrainingIDs']:
    samplePrompt    = deepcopy(sample)
    sampleNonPrompt = deepcopy(sample)
    sampleFake      = deepcopy(sample)

    samplePrompt.setSelectionString("(lep_isPromptId_Training==1&&"+preselectionString+")")
    sampleNonPrompt.setSelectionString("(lep_isNonPromptId_Training==1&&"+preselectionString+")")
    sampleFake.setSelectionString("(lep_isFakeId_Training==1&&"+preselectionString+")")

    samplePrompt.name    = "Prompt"
    sampleNonPrompt.name = "NonPrompt"
    sampleFake.name      = "Fake"

    samplePrompt.texName    = "Prompt"
    sampleNonPrompt.texName = "NonPrompt"
    sampleFake.texName      = "Fake"

    samplePrompt.style    = fillStyle(color=ROOT.kCyan, style=3004, lineColor=ROOT.kCyan)
    sampleNonPrompt.style = fillStyle(color=ROOT.kBlue, style=3004, lineColor=ROOT.kBlue)
    sampleFake.style      = fillStyle(color=ROOT.kGray, style=3004, lineColor=ROOT.kGray)

    # Define stack
    mc    = [samplePrompt,sampleNonPrompt,sampleFake]  # A full example would be e.g. mc = [ttbar, ttz, ttw, ...]
    stack = Stack(mc) # A full example would be e.g. stack = Stack( mc, [data], [signal1], [signal2] ) -> Samples in "mc" are stacked in the plot

if args.trainingClasses=='simpleClasses':
    samplePrompt    = deepcopy(sample)
    sampleNotPrompt = deepcopy(sample)

    samplePrompt.setSelectionString("(lep_isPromptId_Training==1&&"+preselectionString+")")
    sampleNotPrompt.setSelectionString("(lep_isNotPromptId_Training==1&&"+preselectionString+")")

    samplePrompt.name    = "Prompt"
    sampleNotPrompt.name = "NotPrompt"

    samplePrompt.texName    = "Prompt"
    sampleNotPrompt.texName = "NotPrompt"

    samplePrompt.style    = fillStyle(color=ROOT.kCyan, style=3004, lineColor=ROOT.kCyan)
    sampleNotPrompt.style = fillStyle(color=ROOT.kGray+2, style=3004, lineColor=ROOT.kGray+2)

    # Define stack
    mc    = [samplePrompt,sampleNotPrompt]  # A full example would be e.g. mc = [ttbar, ttz, ttw, ...]
    stack = Stack(mc) # A full example would be e.g. stack = Stack( mc, [data], [signal1], [signal2] ) -> Samples in "mc" are stacked in the plot

for ecalType in ecalTypes:
        
    # Set some defaults -> these need not be specified below for each plot
    weight = staticmethod(lambda event, sample: 1.)  # could be e.g. weight = lambda event, sample: event.weight
    selectionString = "("+kinematic_selection+"&&"+ecalType["selectionString"]+")" # could be a complicated cut
    Plot.setDefaults(stack = stack, weight = weight, selectionString = selectionString, addOverFlowBin='upper')
    plotname=""
    # Sequence
    sequence = []

    def make_sumPt( event, sample ):
        for flavor in pfCand_flavors:
            cands = getCollection( event, 'pfCand_%s'%flavor, ['pt_ptRelSorted'], 'npfCand_%s'%flavor )
            #print cands
            setattr( event, 'mult_%s'%flavor, len( cands ) )
            setattr( event, 'sumPt_%s'%flavor, sum( [ c['pt_ptRelSorted'] for c in cands ], 0. ) )
    sequence.append( make_sumPt )

    #def print_mcmatchId( event, sample ):
    #    if isNonPrompt(event) and event.lep_mvaIdSpring16<0.3 and sample==sample:
    #        print event.lep_mcMatchId

    #def print_class( event, sample ):
    #    assert isPrompt(event) + isNonPrompt(event) + isFake(event)==1, "Should never happen!"

    #    print event.lep_isPromptId, event.lep_isNonPromptId, event.lep_isFakeId, event.lep_mcMatchId, event.lep_mcMatchAny, isPrompt(event), isNonPrompt(event), isFake(event), event.lep_pdgId
    #    #print "Fill", event.lep_isPromptId if ((isPrompt(event) and sample==samplePrompt) or (isNonPrompt(event) and sample==sampleNonPrompt) or (isFake(event) and sample==sampleFake)) else float('nan')
    #    #print "Fill2", (isPrompt(event) and sample==samplePrompt),(isNonPrompt(event) and sample==sampleNonPrompt),(isFake(event) and sample==sampleFake)
    ##sequence.append(print_class)

    # Start with an empty list
    plots = []
    # Add plots

    #Lepton Classes
    plots.append(Plot(name=plotname+'ClassPrompt',
        texX = 'isPrompt', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_isPromptId_Training,
        binning=[2,0,1],
    ))
    plots.append(Plot(name=plotname+'ClassNonPrompt',
        texX = 'isNonPrompt', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_isNonPromptId_Training,
        binning=[2,0,1],
    ))
    plots.append(Plot(name=plotname+'ClassFake',
        texX = 'isFake', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_isFakeId_Training,
        binning=[2,0,1],
    ))
    
    if args.trainingClasses=='fullClasses' and args.looseId:
        plots.append(Plot(name=plotname+'DL_prob_isPrompt',
            texX = 'DL_prob_isPrompt', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.prob_lep_isPromptId_Training,
            binning=[33,0,1],
        ))
        plots.append(Plot(name=plotname+'DL_prob_isNonPrompt',
            texX = 'DL_prob_isNonPrompt', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.prob_lep_isNonPromptId_Training,
            binning=[33,0,1],
        ))
        plots.append(Plot(name=plotname+'DL_prob_isFake',
            texX = 'DL_prob_isFake', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.prob_lep_isFakeId_Training,
            binning=[33,0,1],
        ))

    if args.trainingClasses=='simpleClasses' and args.looseId:
        plots.append(Plot(name=plotname+'DL_prob_isPrompt',
            texX = 'DL_prob_isPrompt', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.prob_lep_isPromptId_Training,
            binning=[33,0,1],
        ))
        plots.append(Plot(name=plotname+'DL_prob_isNotPrompt',
            texX = 'DL_prob_isNotPrompt', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.prob_lep_isNotPromptId_Training,
            binning=[33,0,1],
        ))

    #Training Variables
    plots.append(Plot(name=plotname+'pt',
        texX = 'pt', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_pt,
        binning=[100,0,500],
    ))
    plots.append(Plot(name=plotname+'eta',
        texX = 'eta', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_eta,
        binning=[60,-3.2,3.2],
    ))
    plots.append(Plot(name=plotname+'phi',
        texX = 'phi', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_phi,
        binning=[60,-3.2,3.2],
    ))
    plots.append(Plot(name=plotname+'rho',
        texX = 'rho', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_rho,
        binning=[80,0,50],
    ))
    plots.append(Plot(name=plotname+'innerTrackChi2',
        texX = 'innerTrackChi2', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_innerTrackChi2,
        binning=[50,0,10],
    ))
    plots.append(Plot(name=plotname+'relIso03',
        texX = 'relIso03', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_relIso03,
        binning=[90,0,0.5],
    ))
    plots.append(Plot(name=plotname+'relIso04',
        texX = 'relIso04', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_relIso04,
        binning=[90,0,1.0],
    ))
    plots.append(Plot(name=plotname+'miniRelIso',
        texX = 'miniRelIso', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_miniRelIso,
        binning=[90,0,0.5],
    ))
    plots.append(Plot(name=plotname+'lostOuterHits',
        texX = 'lostOuterHits', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_lostOuterHits,
        binning=[16,0,15],
    ))
    plots.append(Plot(name=plotname+'lostInnerHits',
        texX = 'lostInnerHits', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_lostHits,
        binning=[16,0,15],
    ))

    plots.append(Plot(name=plotname+'trackerLayers',
        texX = 'trackerLayers', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_trackerLayers,
        binning=[16,0,15],
    ))
    plots.append(Plot(name=plotname+'pixelLayers',
        texX = 'pixelLayers', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_pixelLayers,
        binning=[16,0,15],
    ))
    plots.append(Plot(name=plotname+'trackerHits',
        texX = 'trackerHits', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_trackerHits,
        binning=[16,0,15],
    ))
    plots.append(Plot(name=plotname+'innerTrackValidHitFraction',
        texX = 'innerTrackValidHitFraction', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_innerTrackValidHitFraction,
        binning=[50,0.9,1.0],
    ))
    plots.append(Plot(name=plotname+'jetDR',
        texX = 'jetDR', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_jetDR,
        binning=[50,0,0.2],
    ))
    plots.append(Plot(name=plotname+'dxy',
        texX = 'dxy', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_dxy,
        binning=[50,-0.03,0.03] if leptonFlavour["Name"]=="Muon" else [50,-0.15,0.15],
    ))
    plots.append(Plot(name=plotname+'dz',
        texX = 'dz', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_dz,
        binning=[50,-0.1,0.1] if leptonFlavour["Name"]=="Muon" else [50,-0.25,0.25],
    ))
    plots.append(Plot(name=plotname+'errorDxy',
        texX = 'errorDxy', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_edxy,
        binning=[50,0,0.008],
    ))
    plots.append(Plot(name=plotname+'errorDz',
        texX = 'errorDz', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_edz,
        binning=[50,0,0.02],
    ))
    plots.append(Plot(name=plotname+'d3DwrtPV',
        texX = 'd3DwrtPV', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_ip3d,
        binning=[50,0,0.05],
    ))
    plots.append(Plot(name=plotname+'significanceD3DwrtPV',
        texX = 'significanceD3DwrtPV', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_sip3d,
        binning=[100,0,20],
    ))
    plots.append(Plot(name=plotname+'effectiveArea03',
        texX = 'EffectiveArea03', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_EffectiveArea03,
        binning=[100,0,0.1] if leptonFlavour["Name"]=="Muon" else [300,0,0.3],
    ))
    plots.append(Plot(name=plotname+'jetPtRatiov1',
        texX = 'pt(lepton)/pt(nearestJet)', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_jetPtRatiov1,
        binning=[50,0,1.25],
    ))
    plots.append(Plot(name=plotname+'jetPtRatiov2',
        texX = 'pt(lepton)/[rawpt(jet-PU-lep)*L2L3Res+pt(lepton)]', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_jetPtRatiov2,
        binning=[50,0,1.25],
    ))
    plots.append(Plot(name=plotname+'jetPtRelv1',
        texX = 'lepPtTransverseToJetAxisV1', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_jetPtRelv1,
        binning=[50,0,15],
    ))
    plots.append(Plot(name=plotname+'jetPtRelv2',
        texX = 'lepPtTransverseToJetAxisV1', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_jetPtRelv2,
        binning=[50,0,40],
    ))
    plots.append(Plot(name=plotname+'ptErrTk',
        texX = 'ptErrorTrack', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_ptErrTk,
        binning=[50,0,20],
    ))

    plots.append(Plot(name=plotname+'nTrueInt',
        texX = 'nTrueInt', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.nTrueInt,
        binning=[60,0,60],
    ))
    plots.append(Plot(name=plotname+'MVA_TTH',
        texX = 'mvaTTH', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_mvaTTH, 
        binning=[30,-1,1],
    ))
    plots.append(Plot(name=plotname+'MVA_TTV',
        texX = 'mvaTTV', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_mvaTTV, 
        binning=[30,-1,1],
    ))


    plots.append(Plot(name=plotname+'jetBTagCSV',
        texX = 'jetBTagCSV', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_jetBTagCSV, 
        binning=[30,0,1],
    ))
    plots.append(Plot(name=plotname+'jetBTagDeepCSV',
        texX = 'jetBTagDeepCSV', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_jetBTagDeepCSV, 
        binning=[30,0,1],
    ))
    #plots.append(Plot(name=plotname+'jetBTagDeepCSVCvsB',
    #    texX = 'jetBTagDeepCSVCvsB', texY = 'Number of Events',
    #    attribute = lambda lepton, sample: lepton.lep_jetBTagDeepCSVCvsB, 
    #    binning=[30,0,1],
    #))
    #plots.append(Plot(name=plotname+'jetBTagDeepCSVCvsL',
    #    texX = 'jetBTagDeepCSVCvsL', texY = 'Number of Events',
    #    attribute = lambda lepton, sample: lepton.lep_jetBTagDeepCSVCvsL, 
    #    binning=[30,0,1],
    #))

    #PF Cands
    for flavor in pfCand_flavors:
        plots.append(Plot(name='pfCands_mult_%s'%flavor,
            texX = 'mult_%s'%flavor, texY = 'Number of Events',
            attribute = "mult_%s"%flavor,
            binning=pfCand_plot_binning[flavor]['mult'],
        ))
        plots.append(Plot(name='pfCands_sumPt_%s'%flavor,
            texX = 'sumPt_%s'%flavor, texY = 'Number of Events',
            attribute = "sumPt_%s"%flavor,
            binning=pfCand_plot_binning[flavor]['sumPt'],
        ))

    #Electron specific
    if leptonFlavour["Name"]=="Electron":

        plots.append(Plot(name=plotname+'etaSc',
            texX = 'etaSc', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.lep_etaSc,
            binning=[60,-3,3],
        ))
        plots.append(Plot(name=plotname+'sigmaIetaIeta',
            texX = 'sigmaIetaIeta', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.lep_sigmaIEtaIEta,
            binning=[30,0,0.06],
        ))
        plots.append(Plot(name=plotname+'full5x5SigmaIetaIeta',
            texX = 'full5x5_sigmaIetaIeta', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.lep_full5x5_sigmaIetaIeta,
            binning=[30,0,0.06],
        ))
        plots.append(Plot(name=plotname+'dEtaInSeed',
            texX = 'dEtaInSeed', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.lep_dEtaInSeed,
            binning=[20,-0.04,0.04],
        ))
        plots.append(Plot(name=plotname+'dPhiScTrkIn',
            texX = 'dPhiScTrkIn', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.lep_dPhiScTrkIn,
            binning=[30,-0.3,0.3],
        ))
        plots.append(Plot(name=plotname+'dEtaScTrkIn',
            texX = 'dEtaScTrkIn', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.lep_dEtaScTrkIn,
            binning=[50,-1,1],
        ))
        plots.append(Plot(name=plotname+'eInvMinusPInv',
            texX = '|1/E-1/p|', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.absEInvMinusPInv,
            binning=[30,0,0.20],
        ))
        plots.append(Plot(name=plotname+'convVeto',
            texX = 'convVeto', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.lep_convVeto,
            binning=[2,0,1],
        ))
        plots.append(Plot(name=plotname+'hadronicOverEm',
            texX = 'hadronicOverEm', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.lep_hadronicOverEm,
            binning=[30,0,0.15],
        ))
        plots.append(Plot(name=plotname+'r9',
            texX = 'r9', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.lep_r9,
            binning=[100,0,1],
        ))
    #Muon specific
    if leptonFlavour["Name"]=="Muon":
        
        plots.append(Plot(name=plotname+'segmentCompatibility',
            texX = 'segmentCompatibility', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.lep_segmentCompatibility,
            binning=[10,0,1],
        ))
        plots.append(Plot(name=plotname+'muonInnerTrkRelErr',
            texX = 'muonInnerTrkRelErr', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.lep_muonInnerTrkRelErr,
            binning=[50,0,0.1],
        ))
        plots.append(Plot(name=plotname+'isGlobalMuon',
            texX = 'isGlobalMuon', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.lep_isGlobalMuon,
            binning=[2,0,1],
        ))
        plots.append(Plot(name=plotname+'chi2LocalPosition',
            texX = 'chi2LocalPosition', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.lep_chi2LocalPosition,
            binning=[50,0,20],
        ))
        plots.append(Plot(name=plotname+'chi2LocalMomentum',
            texX = 'chi2LocalMomentum', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.lep_chi2LocalMomentum,
            binning=[50,0,50],
        ))
        plots.append(Plot(name=plotname+'gobalTrackChi2',
            texX = 'gobalTrackChi2', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.lep_globalTrackChi2,
            binning=[50,0,5],
        ))
        plots.append(Plot(name=plotname+'gobalTrackProb',
            texX = 'gobalTrackProb', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.lep_glbTrackProbability,
            binning=[50,0,15],
        ))
        plots.append(Plot(name=plotname+'caloCompatibility',
            texX = 'caloCompatibility', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.lep_caloCompatibility,
            binning=[50,0,1],
        ))
        plots.append(Plot(name=plotname+'trkKink',
            texX = 'trkKink', texY = 'Number of Events',
            attribute = lambda lepton, sample: lepton.lep_trkKink,
            binning=[100,0,200],
        ))
    #other Variables
    plots.append(Plot(name=plotname+'mcMatchId',
        texX = 'mcMatchId', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_mcMatchId,
        binning=[61,-30,30],
    ))
    plots.append(Plot(name=plotname+'mcMatchAny',
        texX = 'mcMatchAny', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_mcMatchAny,
        binning=[61,-30,30],
    ))
    plots.append(Plot(name=plotname+'pdgId',
        texX = 'pdgId', texY = 'Number of Events',
        attribute = lambda lepton, sample: lepton.lep_pdgId,
        binning=[61,-30,30],
    ))
    

    #plots.append(Plot( name = "fancy_variable",
    #    texX = 'Number of tracker hits squared', texY = 'Number of Events',
    #    attribute = lambda event, sample: event.fancy_variable, # <--- can use any 'event' attribute, including the ones we define in 'sequence'    binning=[30,0,900],
    #))


    # Fill everything.
    plotting.fill(plots, read_variables = flat_variables, sequence = sequence)

    #
    # Helper: Add text on the plots
    #
    def drawObjects( plotData, dataMCScale, lumi_scale ):
        tex = ROOT.TLatex()
        tex.SetNDC()
        tex.SetTextSize(0.04)
        tex.SetTextAlign(11) # align right
        lines = [
          (0.25, 0.95, 'TestData' if args.testData else 'TrainData'),
          (0.55, 0.95, kinematic_selection_name+" "+ecalType["Name"]+" "+leptonFlavour["Name"]+"s")
        ]
        return [tex.DrawLatex(*l) for l in lines]

    # Draw a plot and make it look nice-ish
    def drawPlots(plots, dataMCScale):
      for log in [False, True]:
        plot_directory_ = (os.path.join(
                                        plot_directory,
                                        sampleInfo['sample_name'],
                                        sampleInfo['training_date'] if args.trainingClasses!='noTraining' else 'noTraining',                
                                        'TestData' if args.testData else 'TrainData',
                                        'histograms', kinematic_selection_name + "_"+ecalType["Name"]+('_looseIdSelection' if args.looseId else '_noSelection'), ("log" if log else "lin")
                                        ))
        for plot in plots:
          #if not max(l[0].GetMaximum() for l in plot.histos): continue # Empty plot
          
          plotting.draw(plot,
            plot_directory = plot_directory_,
            #ratio = {'yRange':(0.1,1.9)} if not args.noData else None,
            logX = False, logY = log, sorting = True,
            yRange = (0.03, "auto") if log else (0.001, "auto"),
            scaling = {},
            legend = [ (0.15,0.9-0.03*sum(map(len, plot.histos)),0.9,0.9), 2],
            drawObjects = drawObjects( False, dataMCScale , lumi_scale = -1 ),
            copyIndexPHP = True
          )


    # Draw the plots
    drawPlots(plots, dataMCScale = -1)

