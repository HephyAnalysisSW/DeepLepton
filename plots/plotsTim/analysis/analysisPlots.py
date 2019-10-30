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
from DeepLepton.Tools.objectSelection import getFilterCut, isAnalysisJet, isBJet, getAllLeptons, leptonVars, eleSelector, muonSelector, lepton_branches_data, lepton_branches_mc
from DeepLepton.Tools.cutInterpreter  import cutInterpreter
from DeepLepton.Tools.triggerSelector_deepLepton_analysis import triggerSelector
#
# Arguments
# 
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',      default='INFO',          nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--noData',             action='store_true', default=False,           help='also plot data?')
argParser.add_argument('--year',               action='store',      default=2016,            choices = [2016, 2017], type=int, help='2016 or 2017?',)
argParser.add_argument('--reduceMC',           action='store',      default=1,               type=int, help='Reduce MC sample by a factor?',)
argParser.add_argument('--small',                                   action='store_true',     help='Run only on a small subset of the data?', )
argParser.add_argument('--plot_directory',     action='store',      default='DeepLepton')
argParser.add_argument('--sampleSelection',    action='store',      choices=['DY','TT'], default='TT'  )
argParser.add_argument('--data',               action='store',      type=str, default='Run2016'  )
argParser.add_argument('--selection',          action='store',      default='lep_CR_tt2l-jet_CR_tt2l-lower_met-dilepOSmumu-ht_met' )  #'lep_CR_tt2l-jet_CR_tt2l-met200-dilepOS-ht_met' )   #'lep_CR_DY-dilepOS-met200' )   #'lep_CR_tt2l-jet_CR_tt2l-met200' )   #default='dilepZmass-dilepSelSFOS-njet2p-btag0p' ) #default = 'dilepSelOS-njet2p-btag2p', )  #default='dilepSel-njet2p-btag1p' )        default='dilepSel-njet2p-btag2p' )   default='njet2p-btag2p-met300')
argParser.add_argument('--signal',             action='store',      default=None,            nargs='?', choices=[None, "SMS"], help="Add signal to plot")
#argParser.add_argument('--leptonpreselection', action='store',      default='Sum$(lep_pt>10&&abs(lep_pdgId)==13)>=1')
argParser.add_argument('--leptonpreselection', action='store',      default='1')#default='(Sum$(abs(lep_pdgId)==11)+Sum$(abs(lep_pdgId)==13))>=2')
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
args.plot_directory = os.path.join( args.plot_directory, args.data+'_reducedMC'+str(args.reduceMC) )

## reduce files homogenous
#def reduceFiles( self, factor = 1, to = None ):
#    ''' Reduce number of files in the sample
#    '''
#    len_before = len(self.files)
#    norm_before = self.normalization
#
#    if factor!=1:
#        #self.files = self.files[:len_before/factor]
#        self.files = self.files[0::factor]
#        if len(self.files)==0:
#            raise helpers.EmptySampleError( "No ROOT files for sample %s after reducing by factor %f" % (self.name, factor) )
#    elif to is not None:
#        if to>=len(self.files):
#            return
#        self.files = self.files[:to]
#    else:
#        return
#
#    # Keeping track of reduceFile factors
#    factor = len(self.files)/float(len_before)
#    if hasattr(self, "reduce_files_factor"):
#        self.reduce_files_factor *= factor
#    else:
#        self.reduce_files_factor = factor
#    self.normalization = factor*self.normalization if self.normalization is not None else None
#
#    logger.info("Sample %s: Reduced number of files from %i to %i. Old normalization: %r. New normalization: %r. factor: %3.3f", self.name, len_before, len(self.files), norm_before, self.normalization, factor)
#
#    return

#
# Make samples, will be searched for in the postProcessing directory
#

#if args.year == 2017:
#    raise NotImplementedError
    #postProcessing_directory = "TopEFT_PP_2017_v14/dilep"
    #data_directory           = "/afs/hephy.at/data/dspitzbart02/cmgTuples"  
    #from DeepLepton.samples.cmgTuples_Data25ns_92X_Run2017_postProcessed import *
    #from DeepLepton.samples.cmgTuples_Summer17_92X_mAODv2_postProcessed import *

    #SingleElectron_data = SingleElectron_Run2017
    #SingleMuon_data     = SingleMuon_Run2017
    #SingleEleMu_data    = SingleEleMu_Run2017
#elif args.year == 2016:
#    #data_directory           = "/afs/hephy.at/data/rschoefbeck01/cmgTuples/"  
#    data_directory           = "/afs/hephy.at/data/cms02/cmgTuples/"  
#    postProcessing_directory = "deepLepton_v7/singlelep" 
#    from DeepLepton.samples.cmgTuples_Data25ns_80X_07Aug17_postProcessed import *
#    #data_directory           = "/afs/hephy.at/data/rschoefbeck01/cmgTuples/"  
#    data_directory           = "/afs/hephy.at/data/cms02/cmgTuples/"  
#    postProcessing_directory = "deepLepton_v7/singlelep" 
#    from DeepLepton.samples.cmgTuples_deepLepton_Summer16_mAODv2_postProcessed import *
#    
#    DoubleMuon_data     = vars()['DoubleMuon_'+args.data]
#    data_sample         = DoubleMuon_data
# backgrounds / mc

if args.year == 2017:
    raise NotImplementedError
elif args.year == 2016:
    data_directory = '/afs/hephy.at/data/cms03/DeepLepton/results/'
    #postProcessing_directory = "deepLepton_v5/dilep_small/"    # small 
    postProcessing_directory = "deepLepton_v5/dilep/" 
    from DeepLepton.samples.cmgTuples_Data25ns_80X_07Aug17_postProcessed import *
    data_directory = '/afs/hephy.at/data/cms03/DeepLepton/results/'
    #postProcessing_directory = "deepLepton_v5/dilep_small/" 
    postProcessing_directory = "deepLepton_v5/dilep/" 
    from DeepLepton.samples.cmgTuples_deepLepton_Summer16_mAODv2_postProcessed import *    
    
    MET_data     = vars()['MET_'+args.data]
    data_sample         = MET_data

if args.year == 2017:
    raise NotImplementedError 
    mc             = [ ]
elif args.year == 2016:
    mc              = [ TTJets_DiLepton, DY, VV,]
    #mc             = [ DY, TTJets_DiLepton, VV,]
    #mc             = [ DY, TTJets_DiLepton, VV, TTJets_SingleLepton, WJets,]
    #mc             = [ DY, TTJets_DiLepton, TTJets_SingleLepton,]

for sample in mc: sample.style = styles.fillStyle(sample.color)


if args.signal == "SMS":
    data_directory = '/afs/hephy.at/data/cms03/DeepLepton/results/'
    postProcessing_directory = "deepLepton_v5/dilep_small/" 
    from DeepLepton.samples.cmgTuples_deepLepton_Summer16_mAODv2_postProcessed import *
    SMS_T2tt                 = SMS_T2tt
    SMS_T2tt.style           = styles.lineStyle( ROOT.kBlack, width=3 )
    signals = [ SMS_T2tt,]
else:
    signals = []


# Read variables and sequences
#
deepLepton_input_branches = "jetBTagDeepCSV/F,mvaTTV/F,rho/F,innerTrackChi2/F,miniRelIsoCharged/F,miniRelIsoNeutral/F,lostOuterHits/I,trackerLayers/I,pixelLayers/I,trackerHits/I,innerTrackValidHitFraction/F,jetDR/F,edxy/F,edz/F,ip3d/F,edxy/F,edz/F,ip3d/F,jetPtRatiov1/F,jetPtRelv1/F,jetPtRatiov2/F,jetPtRelv2/F,ptErrTk/F,segmentCompatibility/F,isGlobalMuon/I,chi2LocalPosition/F,chi2LocalMomentum/F,globalTrackChi2/F,caloCompatibility/F,trkKink/F,deepLepton_prompt/F,deepLepton_nonPrompt/F,deepLepton_fake/F,glbTrackProbability/F,nStations/I,iLepGood/I" 
deepLepton_vars           = map( lambda s:s.split('/')[0], deepLepton_input_branches.split(',') )
read_variables =   ["weight/F",
                    "evt/l", "run/I", "lumi/I",
                    "jet[pt/F,eta/F,phi/F,btagCSV/F,id/I,btagDeepCSV/F]", "njet/I", 'nJetSelected/I',
                    #"nlep/I",  "lep[%s,%s]"%(lepton_branches_data,deepLepton_input_branches),
                    "met_pt/F", "met_phi/F", "metSig/F", "ht/F", "nBTag/I", #"lep_deepLepton_prompt/F", #"lep_deepLepton_fake/F", "lep_deepLepton_nonPrompt/F", 
                   ]


sequence = []

def getJets( event, sample ):
    jetVars              = ['eta','pt','phi','btagCSV','id', 'btagDeepCSV']
    event.jets           = filter( isAnalysisJet, filter( lambda j:j['pt']>30 and j['id'], [getObjDict(event, 'jet_', jetVars, i) for i in range(int(getVarValue(event, 'njet')))] ) )
    #event.jets   = filter( isAnalysisJet, event.jets )
    event.b_jets = filter( lambda j: isAnalysisJet(j) and isBJet(j), event.jets )
    
    event.ht25 = sum([jet['pt'] for jet in event.jets]) 

sequence.append( getJets ) 

mu_selector = muonSelector('ControlRegion_tt2l', args.year)  
ele_selector = eleSelector('ControlRegion_tt2l', args.year)  

def make_analysisVariables( event, sample ):
    all_leptons = getAllLeptons( event, leptonVars , collection = "lep")
    #all_leptons = sorted(all_leptons, key = lambda lep: -lep['pt'])
    all_leptons.sort(key = lambda lep: -lep['pt'])
    muons = filter( lambda l: abs(l['pdgId']) == 13 and mu_selector(l), all_leptons ) 
    electrons = filter( lambda l: abs(l['pdgId']) == 11 and ele_selector(l), all_leptons )
    #leptons = soft_muons + soft_electrons
   # leptons = all_leptons
    #print(type(soft_muons), type(soft_electrons), type(leptons)) 
    #event.nlep_selected = len(all_leptons)   
    
    event.nlep_selected = len(muons) + len(electrons)
    selected_lep = muons + electrons
    #print("selected leptons: ", leptons)
    
    event.leadingLep_pt = all_leptons[0]['pt'] if len(all_leptons) >= 1 else float('nan')
    
    if event.nlep_selected == 2:
        #leptons = sorted(leptons.items(), key = lambda l:(l[1], l[0]))        
        #all_leptons = sorted(all_leptons, key = lambda lep: -lep['pt'])         
        selected_lep = sorted(selected_lep, key = lambda lep: -lep['pt'])         
        #lep_1, lep_2 = all_leptons[:1] 
        lep_1, lep_2 = selected_lep 
           
        #event.leadingLep_pt = lep_1['pt']        
 
        l_1 = ROOT.TLorentzVector()
        l_1.SetPtEtaPhiM(lep_1['pt'], lep_1['eta'], lep_1['phi'], 0 )
        l_2 = ROOT.TLorentzVector()
        l_2.SetPtEtaPhiM(lep_2['pt'], lep_2['eta'], lep_2['phi'], 0 )
        ll = l_1 + l_2
 
        event.ptll = ll.Pt() 
        event.mll = ll.M()         
        #print(event.mll)        
        mt1 = sqrt( 2*lep_1["pt"]*event.met_pt*( 1 - cos( lep_1['phi'] - event.met_phi ) )) 
        mt2 = sqrt( 2*lep_2["pt"]*event.met_pt*( 1 - cos( lep_2['phi'] - event.met_phi ) )) 
        event.mt_min = min(mt1, mt2)

        v1 = event.met_pt * sin( event.met_phi - lep_2["phi"]  ) / ( lep_1["pt"] * sin( lep_1["phi"] - lep_2["phi"] ) )
        v2 = event.met_pt * sin( lep_1["phi"] - event.met_phi  ) / ( lep_2["pt"] * sin( lep_1["phi"] - lep_2["phi"] ) )
        v1 += 1
        v2 += 1
        #print(v1, v2)
        tau_1 = ROOT.TLorentzVector()
        tau_2 = ROOT.TLorentzVector() 
        tau_1.SetPtEtaPhiM( lep_1['pt']*v1, lep_1['eta'], lep_1['phi'], 1.77682 )
        tau_2.SetPtEtaPhiM( lep_2['pt']*v2, lep_2['eta'], lep_2['phi'], 1.77682 ) 
        tautau = tau_1 + tau_2
        event.mtautau = tautau.M() 

    else:
        event.ptll = float('nan')
        event.mll =  float('nan')
        event.mt_min = float('nan')
        event.mtautau = float('nan')
    #print ROOT.gDirectory.GetList().ls()
    
    vec = ROOT.TVector2( event.met_pt * cos(event.met_phi), event.met_pt * sin(event.met_phi) )
    for lep in all_leptons:
        if abs(lep['pdgId']) == 13:
            vec += ROOT.TVector2( lep['pt'] * cos(lep['phi']), lep['pt'] * sin(lep['phi']) )
    event.met_musubtracted = vec.Mod()

    
    event.weight *= (event.mll < 50)*(event.mll > 4)*(event.mll<9 or event.mll>10.5)
    #if not (event.mll<9 or event.mll>10.5): event.weight = 0.
    event.ptll *= (event.ptll > 3)
    event.weight *= (0 > event.mtautau or 160 < event.mtautau) 
    event.weight *= (event.met_musubtracted > 125) 
    
    #event.weight *= (0. < event.mtautau < 160.) 
    #event.weight *= (event.mt_min < 70.)
    #print(event.mll)

sequence.append( make_analysisVariables )


# DeepLepton
# candidates
read_variables.append( VectorTreeVariable.fromString('DL_pfCand_neutral[pt/F,eta/F,phi/F,dxy_pf/F,dz_pf/F,puppiWeight/F,fromPV/F,selectedLeptons_mask/I]', nMax=200 )) # default nMax is 100
read_variables.append( VectorTreeVariable.fromString('DL_pfCand_charged[pt/F,eta/F,phi/F,dxy_pf/F,dz_pf/F,puppiWeight/F,dzAssociatedPV/F,fromPV/F,selectedLeptons_mask/I]', nMax=500 )) # default nMax is 100
read_variables.append( VectorTreeVariable.fromString('DL_pfCand_photon[pt/F,eta/F,phi/F,dxy_pf/F,dz_pf/F,puppiWeight/F,fromPV/F,selectedLeptons_mask/I]', nMax=200 )) # default nMax is 100
read_variables.append( VectorTreeVariable.fromString('DL_pfCand_electron[pt/F,eta/F,phi/F,dxy_pf/F,dz_pf/F,pdgId/I,selectedLeptons_mask/I]', nMax=50 )) # default nMax is 100
read_variables.append( VectorTreeVariable.fromString('DL_pfCand_muon[pt/F,eta/F,phi/F,dxy_pf/F,dz_pf/F,pdgId/I,selectedLeptons_mask/I]', nMax=50 )) # default nMax is 100
read_variables.append( VectorTreeVariable.fromString('DL_SV[pt/F,eta/F,phi/F,chi2/F,ndof/F,dxy/F,edxy/F,ip3d/F,eip3d/F,sip3d/F,cosTheta/F,jetPt/F,jetEta/F,jetDR/F,maxDxyTracks/F,secDxyTracks/F,maxD3dTracks/F,secD3dTracks/F,selectedLeptons_mask/I]', nMax=200 )) # default nMax is 100
read_variables.extend( map( TreeVariable.fromString, ["nDL_pfCand_neutral/I", "nDL_pfCand_charged/I", "nDL_pfCand_photon/I", "nDL_pfCand_electron/I", "nDL_pfCand_muon/I", "nDL_SV/I"]) )

##PF Candidates flavors and binning
#pfCand_plot_binning = {
#                'neutral'  : {'mult': [21,0,20],'sumPt': [25,0,25]  },
#                'charged'  : {'mult': [71,0,70],'sumPt': [50,0,100] },
#                'photon'   : {'mult': [41,0,40],'sumPt': [50,0,50]  },
#                'electron' : {'mult': [21,0,20],'sumPt': [25,0,25]  },
#                'muon'     : {'mult': [21,0,20],'sumPt': [25,0,25]  },
#             }
#pfCand_flavors = pfCand_plot_binning.keys()
#SV_plot_binning = {
#                'sv'       : {'mult': [6,0,5],'sumPt': [25,0,30]    },
#             }


#from TopEFT.Tools.DeepLeptonReader import evaluator
#import numpy as np
#def deepLepton(event, sample ):
#    # set the event
#    evaluator.setEvent( event )
#    features_normalized = np.array( [ evaluator.prepare_features_normalized( "lep", i_lep ) for i_lep in range(event.nlep) ], dtype=np.float32 )
#
#    for l in [event.l1, event.l2]:
#        if l is not None:
#            if l['iLepGood'] >= 0:
#                l['candidates'] = evaluator.pf_candidates_for_lepton( "lep", l['iLepGood'], maskName = "selectedLeptons" )
#
#                #pfCands
#                for flavor in pfCand_flavors:
#                    cands = l['candidates'][flavor]
#                    #print len(cands), cands
#                    l['pfCands_mult_%s'%flavor]  = len( cands )
#                    l['pfCands_sumPt_%s'%flavor] = sum( [ c['pfCand_{fl}_pt_ptRelSorted'.format(fl=flavor)] for c in cands ], 0. )
#                    #setattr( event, l['pfCands_mult_%s'%flavor], len( cands ) )
#                    #setattr( event, l['pfCands_sumPt_%s'%flavor], sum( [ c['pfCand_{fl}_pt_ptRelSorted'.format(fl=flavor)] for c in cands ], 0. ) )
#
#                #SV
#                cands = l['candidates']['SV']
#                l['sv_mult']  = len( cands )
#                l['sv_sumPt'] = sum( [ c['SV_pt_ptSorted'] for c in cands ], 0. )                
#
#            else:
#                l['candidates'] = None
#                for flavor in pfCand_flavors:
#                    l['pfCands_mult_%s'%flavor]  = None 
#                    l['pfCands_sumPt_%s'%flavor] = None
#                    #setattr( event, l['pfCands_mult_%s'%flavor], None ) 
#                    #setattr( event, l['pfCands_sumPt_%s'%flavor], None )
#                l['sv_mult']  = None
#                l['sv_sumPt'] = None              
#
#            
#    #if event.tag_2 is not None:   print event.tag_2['candidates']
#    #if event.probe_2 is not None: print event.probe_2['candidates']
#
#sequence.append( deepLepton )


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
    plot_directory_ = os.path.join(plot_directory, 'analysisPlots', args.plot_directory, ("log" if log else "lin"), args.selection+"wTrigger")
    for plot in plots:
      #print(plot.histos)
      #print(l for l in plot.histos)
      #print(l[0] for l in plot.histos)
      if not max(l[0].GetMaximum() for l in plot.histos): 
     
      #print( i for i in (l for l in plot.histos)  ) 
      #if not any([i.GetMaximum() for i in (l[:] for l in plot.histos)]):     #      [k for k in [l for l in plot.histos]])]): 
      #if not any([i.GetMaximum() for i in [l for l in plot.histos]]): 
      #if not max(k.GetMaximum() for k in [i for i in [l for l in plot.histos]]): 
        logger.warning( "Empty plot! Do nothing" )
        continue # Empty plot
        
      plotting.draw(plot,
	    plot_directory = plot_directory_,
	    ratio = {'yRange':(0.1,1.9)} if not args.noData else None,
	    logX = False, logY = log, sorting = True,
	    yRange = (0.03, "auto") if log else (0.001, "auto"),
	    #scaling = {0:1} if not args.noData else {},
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

if not args.noData:
    data_sample.setSelectionString([getFilterCut(isData=True, year=args.year), cutInterpreter.cutString(args.selection) , args.leptonpreselection])
    data_sample.name           = "data"
    data_sample.style          = styles.errorStyle(ROOT.kBlack)
    lumi_scale                 = data_sample.lumi/1000
    data_sample.read_variables = ["nlep/I",  "lep[%s]"%(lepton_branches_data) ]

if args.noData: lumi_scale = 35.9
weight_ = lambda event, sample: event.weight

for sample in mc + signals:
    sample.scale          = lumi_scale
    sample.read_variables = ["reweightPU36fb/F", "reweightBTagDeepCSV_SF/F", "nlep/I",  "lep[%s]"%(lepton_branches_mc) ]
    sample.weight         = lambda event, sample: event.reweightBTagDeepCSV_SF*event.reweightPU36fb*(1 if args.small else args.reduceMC)
  
    tr = triggerSelector(args.year) 
    #sample.read_variables = ['reweightTopPt/F','reweightDilepTriggerBackup/F','reweightLeptonSF/F','reweightBTag_SF/F','reweightPU36fb/F', 'nTrueInt/F', 'reweightLeptonTrackingSF/F']
    #sample.weight         = lambda event, sample: event.reweightTopPt*event.reweightBTag_SF*event.reweightLeptonSF*event.reweightDilepTriggerBackup*event.reweightPU36fb*event.reweightLeptonTrackingSF
    #print("Trigger selection: ", tr.getSelection("MET")) 
    sample.setSelectionString([getFilterCut(isData=False, year=args.year), cutInterpreter.cutString(args.selection) , args.leptonpreselection, tr.getSelection("MET")])
    if args.reduceMC!=1:
        sample.reduceFiles( factor = args.reduceMC )

if not args.noData:
  stack = Stack(mc, data_sample)
else:
  stack = Stack(mc)

stack.extend( [ [s] for s in signals ] )

if args.small:
    for sample in stack.samples:
        sample.reduceFiles( to = 2 )

# Use some defaults
Plot.setDefaults(stack = stack, weight = staticmethod( weight_ ), selectionString = cutInterpreter.cutString(args.selection) +"&&"+args.leptonpreselection, addOverFlowBin=None)

plots = []


plots.append(Plot(
    texX = 'E_{T}^{miss} (GeV)', texY = 'Number of Events / 30 GeV',
    attribute = TreeVariable.fromString( "met_pt/F" ),
    binning=[450/25,0,450],
))

plots.append(Plot(
  texX = 'p_{T}(leading lepton) (GeV)', texY = 'Number of Events / 5 GeV',
  name = 'leadingLep_pt', attribute = lambda event, sample: event.leadingLep_pt,
  binning=[25,0,150],
))

plots.append(Plot(
  texX = 'm_{ll} (GeV)', texY = 'Number of Events / 5 GeV',
  name = 'mll', attribute = lambda event, sample: event.mll,
  binning=[10,4,50],
))

#plots.append(Plot(
#  texX = 'm_{\\tau\\tau} (GeV)', texY = 'Number of Events / 5 GeV',
#  name = 'mtautau', attribute = lambda event, sample: event.mtautau,
#  binning=[200/5,0,200],
#))

plots.append(Plot(
  texX = 'H_{T} (GeV)', texY = 'Number of Events / 50 GeV',
  name = 'ht25', attribute = lambda event, sample: event.ht25, 
  binning=[700/50,0,700],
))




#plots.append(Plot(
#  texX = 'deepLepton_prompt', texY = 'Number of Events / 5 GeV',
#  name = 'deep Lepton prompt', attribute = lambda event, sample: event.lep_deepLepton_prompt,
#  #attribute = TreeVariable.fromString( "lep_deepLepton_prompt/F" ), 
#  binning=[20,0,1],
#))

plotting.fill(plots, read_variables = read_variables, sequence = sequence, max_events = 30000 if args.small else -1)

dataMCScale = -1
drawPlots(plots, dataMCScale)

logger.info( "Done with prefix %s and selectionString %s", args.selection, cutInterpreter.cutString(args.selection) )

