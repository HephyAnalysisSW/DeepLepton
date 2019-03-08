#!/usr/bin/env python
''' Analysis script for standard plots
'''
#
# Standard imports and batch mode
#
import ROOT, os
ROOT.gROOT.SetBatch(True)
import itertools
import copy

from math                         import sqrt, cos, sin, pi, cosh
from RootTools.core.standard      import *
from DeepLepton.Tools.user            import plot_directory
from DeepLepton.Tools.helpers         import deltaR, deltaPhi, getObjDict, getVarValue
from DeepLepton.Tools.objectSelection import getFilterCut, isAnalysisJet, isBJet, getAllLeptons, leptonVars, muonSelector, lepton_branches_data, lepton_branches_mc
from DeepLepton.Tools.cutInterpreter  import cutInterpreter

#
# Arguments
# 
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',      default='INFO',          nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--noData',             action='store_true', default=False,           help='also plot data?')
argParser.add_argument('--year',               action='store',      default=2016,            choices = [2016, 2017], type=int, help='2016 or 2017?',)
argParser.add_argument('--reduceMC',           action='store',      default=1,               type=int, help='Reduce MC sample by a factor?',)
argParser.add_argument('--eta_min',            action='store',      default=0.,                                      type=float, help='eta min for binning',)
argParser.add_argument('--eta_max',            action='store',      default=2.5,                                     type=float, help='eta max for binning',)
argParser.add_argument('--small',                                   action='store_true',     help='Run only on a small subset of the data?', )
argParser.add_argument('--tag',                                     action='store_true',     help='Plot tags?', )
argParser.add_argument('--trainingInput',                           action='store_true',     help='Plot training inputs without pfCands?', )
argParser.add_argument('--pfCandInput',                             action='store_true',     help='Plot only pfCand inputs?', )
argParser.add_argument('--plot_directory',     action='store',      default='DeepLepton')
argParser.add_argument('--sampleSelection',    action='store',      choices=['DY','TT'], default='TT'  )
argParser.add_argument('--data',               action='store',      type=str, default='Run2016'  )
argParser.add_argument('--selection',          action='store',      default='njet1p-btag1p')
args = argParser.parse_args()

#
# Logger
#
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

args.plot_directory += "_"+args.sampleSelection
if args.small:                        args.plot_directory += "_small"
if args.year == 2017:                 args.plot_directory += "_Run2017"
if args.noData:                       args.plot_directory += "_noData"
args.plot_directory = os.path.join( args.plot_directory, args.data+'_reducedMC'+str(args.reduceMC), 'eta_{eta_min}to{eta_max}'.format(eta_min = args.eta_min, eta_max = args.eta_max) )
#
# Make samples, will be searched for in the postProcessing directory
#

if args.year == 2017:
    pass
    #postProcessing_directory = "TopEFT_PP_2017_v14/dilep"
    #data_directory           = "/afs/hephy.at/data/dspitzbart02/cmgTuples"  
    #from DeepLepton.samples.cmgTuples_Data25ns_92X_Run2017_postProcessed import *
    #from DeepLepton.samples.cmgTuples_Summer17_92X_mAODv2_postProcessed import *

    #SingleElectron_data = SingleElectron_Run2017
    #SingleMuon_data     = SingleMuon_Run2017
    #SingleEleMu_data    = SingleEleMu_Run2017
else:
    data_directory           = "/afs/hephy.at/data/rschoefbeck01/cmgTuples/"  
    postProcessing_directory = "deepLepton_v7/singlelep" 
    from DeepLepton.samples.cmgTuples_Data25ns_80X_07Aug17_postProcessed import *
    data_directory           = "/afs/hephy.at/data/rschoefbeck01/cmgTuples/"  
    postProcessing_directory = "deepLepton_v7/singlelep" 
    from DeepLepton.samples.cmgTuples_deepLepton_Summer16_mAODv2_postProcessed import *

    DoubleMuon_data     = vars()['DoubleMuon_'+args.data]
    data_sample         = DoubleMuon_data
# backgrounds / mc
if args.year == 2017:
    mc             = [ ]
else:
    mc             = [ DY, TTJets_DiLepton, TTJets_SingleLepton,]

for sample in mc: sample.style = styles.fillStyle(sample.color)

# Read variables and sequences
#
deepLepton_input_branches = "jetBTagDeepCSV/F,mvaTTV/F,rho/F,innerTrackChi2/F,miniRelIsoCharged/F,miniRelIsoNeutral/F,lostOuterHits/I,trackerLayers/I,pixelLayers/I,trackerHits/I,innerTrackValidHitFraction/F,jetDR/F,edxy/F,edz/F,ip3d/F,edxy/F,edz/F,ip3d/F,jetPtRatiov1/F,jetPtRelv1/F,jetPtRatiov2/F,jetPtRelv2/F,ptErrTk/F,segmentCompatibility/F,isGlobalMuon/I,chi2LocalPosition/F,chi2LocalMomentum/F,globalTrackChi2/F,caloCompatibility/F,trkKink/F,deepLepton_prompt/F,deepLepton_nonPrompt/F,deepLepton_fake/F,glbTrackProbability/F,nStations/F,iLepGood/I" 
deepLepton_vars           = map( lambda s:s.split('/')[0], deepLepton_input_branches.split(',') )
read_variables =   ["weight/F",
                    "evt/l", "run/I", "lumi/I",
                    "jet[pt/F,eta/F,phi/F,btagCSV/F,id/I,btagDeepCSV/F]", "njet/I", 'nJetSelected/I',
                    "nlep/I",  "lep[%s,%s]"%(lepton_branches_data,deepLepton_input_branches),
                    "met_pt/F", "met_phi/F", "metSig/F", "ht/F", "nBTag/I", 
                   ]

sequence = []

def getJets( event, sample ):
    jetVars              = ['eta','pt','phi','btagCSV','id', 'btagDeepCSV']
    event.jets           = filter( lambda j:j['pt']>30 and j['id'], [getObjDict(event, 'jet_', jetVars, i) for i in range(int(getVarValue(event, 'njet')))] )

    event.jets   = filter( isAnalysisJet, event.jets )
    event.b_jets = filter( lambda j: isAnalysisJet(j) and isBJet(j), event.jets )

sequence.append( getJets )

loose_mu_selector = muonSelector( "loose", args.year)
tight_mu_selector = muonSelector( "tight_2l", args.year)

def getLeptons( event, sample ):
    all_leptons = getAllLeptons( event, leptonVars + deepLepton_vars, collection = "lep")
    loose_muons = filter( lambda l: abs(l['pdgId']) == 13 and loose_mu_selector(l), all_leptons )

    #tight_muons = filter( tight_mu_selector, loose_muons )
    #print len(loose_muons), len( tight_muons )
    
    # take first two 
    event.l1, event.l2 = ( loose_muons + [None, None] ) [:2]
    if event.l1 is not None: event.l1['tight'] = tight_mu_selector(event.l1)
    if event.l2 is not None: event.l2['tight'] = tight_mu_selector(event.l2)

    if event.l1 is not None and event.l2 is not None and (event.l1['tight'] or event.l2['tight']):
        event.tp_mll = sqrt(2*event.l1['pt']*event.l2['pt']*(cosh(event.l1['eta']-event.l2['eta']) - cos(event.l1['phi']-event.l2['phi'])))
    else:
        event.tp_mll = float('nan')

    #sample selection
    DY = ( abs( event.tp_mll - 91.2 ) < 15 )
    TT = ( event.tp_mll > 20 and abs( event.tp_mll - 91.2 ) > 15 )
    event.tp_selection = vars()[args.sampleSelection]

    # loop over both possibilities
    for tag, probe, postfix in [ 
            [ event.l1, event.l2, '1'], 
            [ event.l2, event.l1, '2'] ]:
        # require tight tag
        if tag is not None and probe is not None and tag['tight']: 
            # recall probe and tag in potentially two configurations
            setattr( event, "tag_%s"%postfix, tag )
            setattr( event, "probe_%s"%postfix, probe )
        else:
            setattr( event, "tag_%s"%postfix, None )
            setattr( event, "probe_%s"%postfix, None )

    #print len(filter( tight_mu_selector, loose_muons )), event.probe_1, event.probe_2

    #event.leptons           = filter( lambda j:j['pt']>30 and j['id'], [getObjDict(event, 'lepton_', leptonVars, i) for i in range(int(getVarValue(event, 'nlepton')))] )
    #event.leptons   = filter( isAnalysisLepton, event.leptons )
    #event.b_leptons = filter( lambda j: isAnalysisLepton(j) and isBLepton(j), event.leptons )

sequence.append( getLeptons )

# DeepLepton
# candidates
read_variables.append( VectorTreeVariable.fromString('DL_pfCand_neutral[pt/F,eta/F,phi/F,dxy_pf/F,dz_pf/F,puppiWeight/F,fromPV/F,selectedLeptons_mask/I]', nMax=200 )) # default nMax is 100
read_variables.append( VectorTreeVariable.fromString('DL_pfCand_charged[pt/F,eta/F,phi/F,dxy_pf/F,dz_pf/F,puppiWeight/F,dzAssociatedPV/F,fromPV/F,selectedLeptons_mask/I]', nMax=500 )) # default nMax is 100
read_variables.append( VectorTreeVariable.fromString('DL_pfCand_photon[pt/F,eta/F,phi/F,dxy_pf/F,dz_pf/F,puppiWeight/F,fromPV/F,selectedLeptons_mask/I]', nMax=200 )) # default nMax is 100
read_variables.append( VectorTreeVariable.fromString('DL_pfCand_electron[pt/F,eta/F,phi/F,dxy_pf/F,dz_pf/F,pdgId/I,selectedLeptons_mask/I]', nMax=50 )) # default nMax is 100
read_variables.append( VectorTreeVariable.fromString('DL_pfCand_muon[pt/F,eta/F,phi/F,dxy_pf/F,dz_pf/F,pdgId/I,selectedLeptons_mask/I]', nMax=50 )) # default nMax is 100
read_variables.append( VectorTreeVariable.fromString('DL_SV[pt/F,eta/F,phi/F,chi2/F,ndof/F,dxy/F,edxy/F,ip3d/F,eip3d/F,sip3d/F,cosTheta/F,jetPt/F,jetEta/F,jetDR/F,maxDxyTracks/F,secDxyTracks/F,maxD3dTracks/F,secD3dTracks/F,selectedLeptons_mask/I]', nMax=200 )) # default nMax is 100
read_variables.extend( map( TreeVariable.fromString, ["nDL_pfCand_neutral/I", "nDL_pfCand_charged/I", "nDL_pfCand_photon/I", "nDL_pfCand_electron/I", "nDL_pfCand_muon/I", "nDL_SV/I"]) )

#PF Candidates flavors and binning
pfCand_plot_binning = {
                'neutral'  : {'mult': [21,0,20],'sumPt': [25,0,25]  },
                'charged'  : {'mult': [71,0,70],'sumPt': [50,0,100] },
                'photon'   : {'mult': [41,0,40],'sumPt': [50,0,50]  },
                'electron' : {'mult': [21,0,20],'sumPt': [25,0,25]  },
                'muon'     : {'mult': [21,0,20],'sumPt': [25,0,25]  },
             }
pfCand_flavors = pfCand_plot_binning.keys()
SV_plot_binning = {
                'sv'       : {'mult': [6,0,5],'sumPt': [25,0,30]    },
             }


from TopEFT.Tools.DeepLeptonReader import evaluator
import numpy as np
def deepLepton(event, sample ):
    # set the event
    evaluator.setEvent( event)
    features_normalized = np.array( [ evaluator.prepare_features_normalized( "lep", i_lep ) for i_lep in range(event.nlep) ], dtype=np.float32 )

    for l in [event.l1, event.l2]:
        if l is not None:
            if l['iLepGood'] >= 0:
                l['candidates'] = evaluator.pf_candidates_for_lepton( "lep", l['iLepGood'], maskName = "selectedLeptons" )

                #pfCands
                for flavor in pfCand_flavors:
                    cands = l['candidates'][flavor]
                    #print len(cands), cands
                    l['pfCands_mult_%s'%flavor]  = len( cands )
                    l['pfCands_sumPt_%s'%flavor] = sum( [ c['pfCand_{fl}_pt_ptRelSorted'.format(fl=flavor)] for c in cands ], 0. )
                    #setattr( event, l['pfCands_mult_%s'%flavor], len( cands ) )
                    #setattr( event, l['pfCands_sumPt_%s'%flavor], sum( [ c['pfCand_{fl}_pt_ptRelSorted'.format(fl=flavor)] for c in cands ], 0. ) )

                #SV
                cands = l['candidates']['SV']
                l['sv_mult']  = len( cands )
                l['sv_sumPt'] = sum( [ c['SV_pt_ptSorted'] for c in cands ], 0. )                

            else:
                l['candidates'] = None
                for flavor in pfCand_flavors:
                    l['pfCands_mult_%s'%flavor]  = None 
                    l['pfCands_sumPt_%s'%flavor] = None
                    #setattr( event, l['pfCands_mult_%s'%flavor], None ) 
                    #setattr( event, l['pfCands_sumPt_%s'%flavor], None )
                l['sv_mult']  = None
                l['sv_sumPt'] = None              

            
    #if event.tag_2 is not None:   print event.tag_2['candidates']
    #if event.probe_2 is not None: print event.probe_2['candidates']

sequence.append( deepLepton )


# Text on the plots
#
def drawObjects( plotData, dataMCScale, lumi_scale ):
    tex = ROOT.TLatex()
    tex.SetNDC()
    tex.SetTextSize(0.04)
    tex.SetTextAlign(11) # align right
    lines = [
      (0.15, 0.95, 'CMS Preliminary' if plotData else 'CMS Simulation'), 
      (0.45, 0.95, 'L=%3.1f fb{}^{-1} (13 TeV) Scale %3.2f'% ( lumi_scale, dataMCScale ) ) if plotData else (0.45, 0.95, 'L=%3.1f fb{}^{-1} (13 TeV)' % lumi_scale)
    ]
    return [tex.DrawLatex(*l) for l in lines] 

def drawPlots(plots, dataMCScale):
  for log in [False, True]:
    plot_directory_ = os.path.join(plot_directory, 'analysisPlots', args.plot_directory, ("log" if log else "lin"), args.selection)
    for plot in plots:
      if not max(l[0].GetMaximum() for l in plot.histos): 
        logger.warning( "Empty plot! Do nothing" )
        continue # Empty plot
        
      plotting.draw(plot,
	    plot_directory = plot_directory_,
	    ratio = {'yRange':(0.1,1.9)} if not args.noData else None,
	    logX = False, logY = log, sorting = True,
	    yRange = (0.03, "auto") if log else (0.001, "auto"),
	    scaling = {},
	    legend = [ (0.15,0.9-0.03*sum(map(len, plot.histos)),0.9,0.9), 2],
	    drawObjects = drawObjects( not args.noData, dataMCScale , lumi_scale ),
        copyIndexPHP = True
      )

#
# Loop over channels
#
yields     = {}
allPlots   = {}

data_sample.setSelectionString([getFilterCut(isData=True, year=args.year)])
data_sample.name           = "data"
data_sample.style          = styles.errorStyle(ROOT.kBlack)
lumi_scale                 = data_sample.lumi/1000

if args.noData: lumi_scale = 35.9
weight_ = lambda event, sample: event.weight*event.tp_selection

for sample in mc:
  sample.scale          = lumi_scale
  sample.read_variables = ["reweightPU36fb/F", "reweightBTagDeepCSV_SF/F",]
  sample.weight         = lambda event, sample: event.reweightBTagDeepCSV_SF*event.reweightPU36fb*(1 if args.small else args.reduceMC)
  #sample.read_variables = ['reweightTopPt/F','reweightDilepTriggerBackup/F','reweightLeptonSF/F','reweightBTag_SF/F','reweightPU36fb/F', 'nTrueInt/F', 'reweightLeptonTrackingSF/F']
  #sample.weight         = lambda event, sample: event.reweightTopPt*event.reweightBTag_SF*event.reweightLeptonSF*event.reweightDilepTriggerBackup*event.reweightPU36fb*event.reweightLeptonTrackingSF
  sample.setSelectionString([getFilterCut(isData=False, year=args.year)])
  if args.reduceMC!=1:
    sample.reduceFiles( factor = args.reduceMC )

if not args.noData:
  stack = Stack(mc, data_sample)
else:
  stack = Stack(mc)

if args.small:
    for sample in stack.samples:
        sample.reduceFiles( to = 2 )

# Use some defaults
Plot.setDefaults(stack = stack, weight = staticmethod( weight_ ), selectionString = cutInterpreter.cutString(args.selection), addOverFlowBin=None)

plots = []

if args.trainingInput and not args.tag:

    plots.append(Plot(
      name = 'nVtxs', texX = 'vertex multiplicity', texY = 'Number of Events',
      attribute = TreeVariable.fromString( "nVert/I" ),
      binning=[50,0,50],
    ))

    plots.append(Plot(
        texX = 'E_{T}^{miss} (GeV)', texY = 'Number of Events / 20 GeV',
        attribute = TreeVariable.fromString( "met_pt/F" ),
        binning=[400/20,0,400],
    ))

    plots.append(Plot(
        texX = '#phi(E_{T}^{miss})', texY = 'Number of Events / 20 GeV',
        attribute = TreeVariable.fromString( "met_phi/F" ),
        binning=[10,-pi,pi],
    ))

    plots.append(Plot(
        texX = 'm(tag, probe)', texY = 'Number of Events',
        name = "tp_mll",
        attribute = lambda event, sample: event.tp_mll if event.tp_selection else float('nan'),
        binning=[50,0,150],
    ))

    plots.append(Plot(
      texX = 'N_{jets}', texY = 'Number of Events',
      attribute = TreeVariable.fromString( "nJetSelected/I" ),
      binning=[5,2.5,7.5],
    ))

    plots.append(Plot(
      texX = 'p_{T}(leading jet) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'jet1_pt', attribute = lambda event, sample: event.jets[0]['pt'] if len(event.jets)>0 and event.tp_selection else float('nan'),
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = 'p_{T}(2nd leading jet) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'jet2_pt', attribute = lambda event, sample: event.jets[1]['pt'] if len(event.jets)>1 and event.tp_selection else float('nan'),
      binning=[600/30,0,600],
    ))

#getter for tp_variables
def getter( tag_or_probe, postfix, variable ):
    def att_getter( event, sample ):
        if not event.tp_selection:
            #print "vetoed!", event.tp_mll 
            return float('nan')
        l = getattr( event, "%s_%s"%( tag_or_probe, postfix ) )
        if l is not None and abs(l['eta'])>=args.eta_min and abs(l['eta'])<args.eta_max:
            return l[variable]
        return float('nan')
    return att_getter

#pt, eta, etaSc, phi, pdgId, tightId, tightCharge, miniRelIso, relIso03, relIso04, sip3d, mediumMuonId, pfMuonId, lostHits, convVeto, dxy, dz, hadronicOverEm, dEtaScTrkIn, 
#dPhiScTrkIn, eInvMinusPInv, full5x5_sigmaIetaIeta, etaSc, mvaTTH, matchedTrgObj1Mu, matchedTrgObj1El, muonInnerTrkRelErr, chargeConsistency, trackMult, 
#miniRelIsoCharged, miniRelIsoNeutral, jetPtRelv2, jetPtRelv1, jetPtRatiov2, jetPtRatiov1, relIso03, jetBTagDeepCSV, segmentCompatibility, mvaIdSpring16, 
#eleCutId_Spring2016_25ns_v1_ConvVetoDxyDz, mvaIdFall17noIso, edxy, edz, ip3d, sip3d, innerTrackChi2, innerTrackValidHitFraction, ptErrTk, rho, jetDR, 
#trackerLayers, pixelLayers, trackerHits, lostHits, lostOuterHits, glbTrackProbability, isGlobalMuon, chi2LocalPosition, chi2LocalMomentum, globalTrackChi2, 
#trkKink, caloCompatibility, nStations, mvaTTV, cleanEle, ptCorr, isGenPrompt, FO_4l, FO_3l, FO_SS, tight_4l, tight_3l, tight_SS, 
#deepLepton_prompt, deepLepton_nonPrompt, deepLepton_fake, 

if args.trainingInput:
    tp_variables = [
    #training variables
        #global lepton variables
        [ 'pt',                         [600/10,0,600], 'p_{T} (GeV)' ],
        [ 'eta',                        [25,-2.5,2.5],  '#eta' ],
        [ 'rho',                        [40,0,40],      '#rho' ],
        [ 'innerTrackChi2',             [40,0,10],      'innerTrackChi2' ],
        [ 'relIso03',                   [50,0,0.5],     'relIso03' ],
        [ 'miniRelIsoCharged',          [50,0,0.5],     'miniRelIsoCharged' ],
        [ 'miniRelIsoNeutral',          [50,0,0.5],     'miniRelIsoNeutral' ],
        [ 'lostOuterHits',              [16,0,15],      'lostOuterHits' ],
        [ 'lostHits',                   [16,0,15],      'lostHits' ],
        [ 'trackerLayers',              [16,0,15],      'trackerLayers' ],
        [ 'pixelLayers',                [16,0,15],      'pixelLayers' ],
        [ 'trackerHits',                [16,0,15],      'trackerHits' ],
        [ 'innerTrackValidHitFraction', [40,0.9,1.0],   'innerTrackValidHitFraction' ],
        [ 'jetDR',                      [40,0,0.1],     'jetDR' ],
        [ 'dxy',                        [40,-0.15,0.15],'dxy' ],
        [ 'dz',                         [40,-0.25,0.25],'dz' ],
        [ 'edxy',                       [40,0,0.008],   'edxy' ],
        [ 'edz',                        [40,0,0.02],    'edz' ],
        [ 'ip3d',                       [40,0,0.04],     'ip3d' ],
        [ 'sip3d',                      [40,0,8],       'sip3d' ],
        [ 'jetPtRatiov1',               [40,0,1],       'jetPtRatiov1' ],
        [ 'jetPtRatiov2',               [40,0,1.25],    'jetPtRatiov2' ],
        [ 'jetPtRelv1',                 [40,0,7],       'jetPtRelv1' ],
        [ 'jetPtRelv2',                 [40,0,20],      'jetPtRelv2' ],
        [ 'ptErrTk',                    [40,0,50],      'ptErrTk' ],
        [ 'jetBTagDeepCSV',             [30,0,1],       'jetBTagDeepCSV' ],
        #muon specific variables
        [ 'segmentCompatibility',       [10,0,1],       'segmentCompatibility' ],
        [ 'muonInnerTrkRelErr',         [40,0,0.05],    'muonInnerTrkRelErr' ],
        [ 'isGlobalMuon',               [2,0,1],        'isGlobalMuon' ],
        [ 'chi2LocalPosition',          [20,0,10],      'chi2LocalPosition' ],
        [ 'chi2LocalMomentum',          [40,0,30],      'chi2LocalMomentum' ],
        [ 'globalTrackChi2',            [40,0,3],       'globalTrackChi2' ],
        [ 'caloCompatibility',          [40,0,1],       'caloCompatibility' ],
        [ 'trkKink',                    [40,0,200],     'trkKink' ],
        #other variables
        [ 'phi',                        [50,-3.2,3.2],  '#phi' ],
        [ 'deepLepton_prompt',          [50,0,1],      'deepLepton_prompt' ],
        [ 'deepLepton_nonPrompt',       [50,0,1],      'deepLepton_nonPrompt' ],
        [ 'deepLepton_fake',            [50,0,1],      'deepLepton_fake' ],
        [ 'mvaTTV',                     [50,-1,1],     'mvaTTV' ],
    ]
else:
    tp_variables = []

if args.pfCandInput:
    #add pfCand variables
    for flavor in pfCand_flavors:
        pfCand_variables = ['mult', 'sumPt']
        for variable in pfCand_variables:
            tp_variables.append(['pfCands_%s_%s'%(variable,flavor), pfCand_plot_binning[flavor][variable], '%s_%s'%(variable,flavor)])
    #add SV variables
    SV_variables = ['mult', 'sumPt']
    for variable in SV_variables:
        tp_variables.append(['sv_%s'%variable, SV_plot_binning['sv'][variable], 'sv_%s'%variable])

var_names = [var[0] for var in tp_variables]
assert len(var_names)==len(list(set(var_names))), "tp variable names not unique!!!!"

tp_plots = []
tp_pairs = {}
for variable, binning, texX in tp_variables:
    tp_pairs[ (variable,  texX )] = {}
    #for tag_or_probe in [ 'tag', 'probe' ]:
    for tag_or_probe in [ 'tag' if args.tag else 'probe' ]:
        for postfix in ['1', '2']:
            tp_plots.append(Plot(
              texX = tag_or_probe+' '+texX, 
              texY = 'Number of Events',
              name = '%s_%s_%s'%( tag_or_probe, postfix, variable ),
              attribute = getter( tag_or_probe, postfix, variable ),
              binning   = binning,
            ))
        tp_pairs[ ( variable, texX )][ tag_or_probe ] = tp_plots[-2:]

plotting.fill(plots + tp_plots, read_variables = read_variables, sequence = sequence, max_events = 30000 if args.small else -1)

tp_draw_plots = []
for i_variable, (variable, binning, texX) in enumerate(tp_variables):
    #for tag_or_probe in [ 'tag', 'probe' ]:
    for tag_or_probe in [ 'tag' if args.tag else 'probe' ]:
        plot      = tp_pairs[ ( variable, texX )][ tag_or_probe ][0]
        plot_1    = tp_pairs[ ( variable, texX )][ tag_or_probe ][1]
        plot.name = '%s_%s'%( tag_or_probe, variable )
        for i_s, s in enumerate(plot_1.histos):
            for i_h, h in enumerate(s):
                h.Add( plot_1.histos[i_s][i_h] )
        tp_draw_plots.append( plot )

dataMCScale = -1
drawPlots(plots + tp_draw_plots, dataMCScale)

logger.info( "Done with prefix %s and selectionString %s", args.selection, cutInterpreter.cutString(args.selection) )
