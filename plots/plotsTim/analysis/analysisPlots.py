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

from math                         import sqrt, cos, sin, pi, cosh, log, exp
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
argParser.add_argument('--selection',          action='store',      default='lep_CR_tt2l-jet_CR_tt2l-lower_met-dilepOS-ht_met-filters' )#'lep_CR_tt2l-jet_CR_tt2l-lower_met-dilepOSmumu-ht_met-filters' )#'lep_CR_tt2l-jet_CR_tt2l-met200-dilepOS-ht_met-filters' )  #'lep_CR_DY-dilepOS-met200' )   #'lep_CR_tt2l-jet_CR_tt2l-met200' )   #default='dilepZmass-dilepSelSFOS-njet2p-btag0p' ) #default = 'dilepSelOS-njet2p-btag2p', )  #default='dilepSel-njet2p-btag1p' )        default='dilepSel-njet2p-btag2p' )   default='njet2p-btag2p-met300')
argParser.add_argument('--signal',             action='store',      default=None,            nargs='?', choices=[None, "SMS"], help="Add signal to plot")
#argParser.add_argument('--leptonpreselection', action='store',      default='Sum$(lep_pt>10&&abs(lep_pdgId)==13)>=1')
argParser.add_argument('--leptonpreselection', action='store',      default='1')#default='(Sum$(abs(lep_pdgId)==11)+Sum$(abs(lep_pdgId)==13))>=2')
argParser.add_argument('--region',             action='store',      choices=['low_tt2l','high_tt2l','low_DY','high_DY','low_sig', 'med_sig', 'high_sig'], required=True  )
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

selection_dict = {"low_tt2l":"lep_CR_tt2l_mumu-jet_CR_tt2l-lower_met-dilepOS-filters", 
                "high_tt2l":"lep_CR_tt2l-jet_CR_tt2l-met200-dilepOS-filters", 
                "low_DY": "lep_CR_DY_mumu-jet_CR_DY-dilepOSmumuDY-lower_met-filters", 
                "high_DY":"lep_CR_DY_all-jet_CR_DY-dilepOS-met200-filters", 
                "low_sig":"lep_SR_mu-jet_SR-lower_met-filters", 
                "med_sig":"lep_SR_all-jet_SR-med_met-filters", 
                #"high_sig":"lep_SR_all_DL_bgr-jet_SR-met300-filters" } 
                "high_sig":"lep_SR_all-jet_SR-met300-filters" } 
args.selection = selection_dict[args.region]
print(args.selection)

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
    if "sig" in args.region:
        mc             = [ DY, TTJets_DiLepton, VV, TTJets_SingleLepton, WJets,]
    else:
        mc             = [ DY, TTJets_DiLepton, VV,]
for sample in mc: sample.style = styles.fillStyle(sample.color)


if args.signal == "SMS":
    data_directory = '/afs/hephy.at/data/cms03/DeepLepton/results/'
    postProcessing_directory = "deepLepton_v5/dilep/" 
    from DeepLepton.samples.cmgTuples_deepLepton_Summer16_mAODv2_postProcessed import *
    SMS_T2tt                 = SMS_T2tt_lowerpt
#    SMS_T2tt                 = SMS_T2tt_350_20
    #SMS_T2tt.style           = styles.lineStyle( ROOT.kBlack, width=3 )
    SMS_T2tt.style           = styles.lineStyle( ROOT.kRed, width=3 )
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
    event.jets           = filter( isAnalysisJet, filter( lambda j:j['pt']>25 and j['id'], [getObjDict(event, 'jet_', jetVars, i) for i in range(int(getVarValue(event, 'njet')))] ) )
    #event.jets   = filter( isAnalysisJet, event.jets )
    event.b_jets = filter( lambda j: isAnalysisJet(j) and isBJet(j), event.jets )
    
    event.ht25 = sum([jet['pt'] for jet in event.jets]) 
    event.weight *= (event.ht25>100)
    event.weight = event.weight*((event.met_pt/event.ht25)>0.6)*((event.met_pt/event.ht25)<1.4) if event.ht25!=0. else 0.

sequence.append( getJets ) 

if args.region=="high_tt2l" or args.region=="low_tt2l":
    mu_selector = muonSelector('ControlRegion_tt2l', args.year)  
    ele_selector = eleSelector('ControlRegion_tt2l', args.year)  
elif args.region=="high_DY" or args.region=="low_DY":
    mu_selector = muonSelector('ControlRegion_DY', args.year)  
    ele_selector = eleSelector('ControlRegion_DY', args.year)
elif args.region=="low_sig" or args.region=="med_sig" or args.region=="high_sig": 
    mu_selector = muonSelector('SR_T2tt', args.year)  
    ele_selector = eleSelector('SR_T2tt', args.year)  


def make_analysisVariables( event, sample ):
    all_leptons = getAllLeptons( event, leptonVars , collection = "lep")
    #all_leptons = sorted(all_leptons, key = lambda lep: -lep['pt'])
    all_leptons.sort(key = lambda lep: -lep['pt'])
    muons = filter( lambda l: abs(l['pdgId']) == 13 and mu_selector(l), all_leptons ) 
    electrons = filter( lambda l: abs(l['pdgId']) == 11 and ele_selector(l), all_leptons )
    
    event.nlep_selected = len(muons) + len(electrons)
    selected_lep = muons + electrons
    
    event.leadingLep_pt = all_leptons[0]['pt'] if len(all_leptons) >= 1 else float('nan')
    
    #if event.nlep_selected == 2 and selected_lep[0]['pdgId']*selected_lep[1]['pdgId']<0 :  #higher
    #if event.nlep_selected == 2 and selected_lep[0]['pdgId']==-selected_lep[1]['pdgId'] :   #lower

    if args.region=="high_tt2l" or args.region=="med_sig" or args.region=="high_sig":
        condition = (event.nlep_selected == 2 and selected_lep[0]['pdgId']*selected_lep[1]['pdgId']<0)
    elif args.region=="low_tt2l" or args.region=="low_sig":
        condition = (event.nlep_selected == 2 and selected_lep[0]['pdgId']==-selected_lep[1]['pdgId'])
    elif args.region=="low_DY": 
        condition = (event.nlep_selected == 2 and selected_lep[0]['pdgId']==-selected_lep[1]['pdgId'] and (selected_lep[0]['pt']>20  or (selected_lep[0]['ip3d']>0.01 and selected_lep[1]['ip3d']>0.01) or (selected_lep[0]['sip3d']>2 and selected_lep[1]['sip3d']>2)))
    elif args.region=="high_DY": 
        condition = (event.nlep_selected == 2 and selected_lep[0]['pdgId']*selected_lep[1]['pdgId']<0 and (selected_lep[0]['pt']>20  or (selected_lep[0]['ip3d']>0.01 and selected_lep[1]['ip3d']>0.01) or (selected_lep[0]['sip3d']>2 and selected_lep[1]['sip3d']>2)))

    
    if condition:
        selected_lep = sorted(selected_lep, key = lambda lep: -lep['pt'])         
        lep_1, lep_2 = selected_lep 
           
        event.leadingLep_pt = lep_1['pt']        
 
        l_1 = ROOT.TLorentzVector()
        l_1.SetPtEtaPhiM(lep_1['pt'], lep_1['eta'], lep_1['phi'], 0 )
        l_2 = ROOT.TLorentzVector()
        l_2.SetPtEtaPhiM(lep_2['pt'], lep_2['eta'], lep_2['phi'], 0 )
        ll = l_1 + l_2
 
        event.ptll = ll.Pt() 
        event.mll = ll.M()         
        mt1 = sqrt( 2*lep_1["pt"]*event.met_pt*( 1 - cos( lep_1['phi'] - event.met_phi ) )) 
        mt2 = sqrt( 2*lep_2["pt"]*event.met_pt*( 1 - cos( lep_2['phi'] - event.met_phi ) )) 
        #event.mt_min = min(mt1, mt2)

        v1 = event.met_pt * sin( event.met_phi - lep_2["phi"]  ) / ( lep_1["pt"] * sin( lep_1["phi"] - lep_2["phi"] ) )
        v2 = event.met_pt * sin( lep_1["phi"] - event.met_phi  ) / ( lep_2["pt"] * sin( lep_1["phi"] - lep_2["phi"] ) )
        v1 += 1
        v2 += 1
        #print("v1: ", v1)
        #print("v2: ", v2)
        #angle1 = pi if v1<0. else 0.
        #angle2 = pi if v2<0. else 0.
                             
       
        tau_1 = ROOT.TLorentzVector()
        tau_2 = ROOT.TLorentzVector() 
        
        if v1<0:
            tau_1.SetPtEtaPhiM( lep_1['pt']*abs(v1), -lep_1['eta'], lep_1['phi']+pi, 1.77682 )
        else:
            tau_1.SetPtEtaPhiM( lep_1['pt']*abs(v1), lep_1['eta'], lep_1['phi'], 1.77682 )
        if v2<0:
            tau_2.SetPtEtaPhiM( lep_2['pt']*abs(v2), -lep_2['eta'], lep_2['phi']+pi, 1.77682 ) 
        else:
            tau_2.SetPtEtaPhiM( lep_2['pt']*abs(v2), lep_2['eta'], lep_2['phi'], 1.77682 ) 
        tautau = tau_1 + tau_2
        event.mtautau = tautau.M() 
        if v1<0 or v2<0:
            event.mtautau *= -1
        #print(event.mtautau)

        vec = ROOT.TVector2( event.met_pt * cos(event.met_phi), event.met_pt * sin(event.met_phi) )
        for lep in all_leptons:
            if abs(lep['pdgId']) == 13:
                vec += ROOT.TVector2( lep['pt'] * cos(lep['phi']), lep['pt'] * sin(lep['phi']) )
        event.met_musubtracted = vec.Mod()

    else:
        event.ptll = float('nan')
        event.mll =  float('nan')
        event.mt_min = float('nan')
        event.mtautau = float('nan')
        event.leadingLep_pt = float('nan')
        event.weight = 0.
        mt1 = float('nan')
        mt2 = float('nan') 
        event.met_musubtracted = float('nan')
    
    event.weight *= (event.mll < 50.)*(event.mll > 4.)  # only for same flavour??
    if event.nlep_selected==2 and selected_lep[0]['pdgId']==-selected_lep[1]['pdgId']: 
        event.weight *= (event.mll<9. or event.mll>10.5)
    event.ptll *= (event.ptll > 3.)
    
    
    if args.region=="low_DY" or args.region=="high_DY":
        event.weight *= (mt1 < 70.)*(mt2 < 70.)
        event.weight *= (0. < event.mtautau < 160.)
        if args.region=="high_DY":
            event.weight *= (event.met_musubtracted > 125.)
    else:
        event.weight *= (0 > event.mtautau or 160. < event.mtautau) 
        #event.weight *= (160. < event.mtautau) 
        event.weight *= (0 > event.mtautau or 160. < event.mtautau) 
        event.weight *= (event.met_musubtracted > 125.) 
   
    if not 'low' in args.region: 
        if event.nlep_selected==2:
            if selected_lep[0]['pdgId']==-selected_lep[1]['pdgId'] and abs(selected_lep[0]['pdgId'])==13:
                event.weight = event.met_musubtracted>125.
            else: 
                event.weight = event.met_musubtracted>200.
                

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
    plot_directory_ = os.path.join(plot_directory, 'analysisPlots3', args.plot_directory, ("log" if log else "lin"), args.selection)#+"_DL_WP2")
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

tr = triggerSelector(args.year) 
if 'low' in args.region: 
    triggerSelection = tr.getSelection("MET")
else:
    triggerSelection = tr.getSelection("MET_high")

print(triggerSelection)

if not args.noData:
    data_sample.setSelectionString([getFilterCut(isData=True, year=args.year), cutInterpreter.cutString(args.selection) , triggerSelection])
    data_sample.name           = "data"
    data_sample.style          = styles.errorStyle(ROOT.kBlack)
    lumi_scale                 = data_sample.lumi/1000
    data_sample.read_variables = ["nlep/I",  "lep[%s]"%(lepton_branches_data) ]

#print('lumi scale: ', lumi_scale)

if args.noData: lumi_scale = 35.9
weight_ = lambda event, sample: event.weight

for sample in mc + signals:
    sample.scale          = lumi_scale
    sample.read_variables = ["reweightPU36fb/F", "reweightBTagDeepCSV_SF/F", "nlep/I",  "lep[%s]"%(lepton_branches_mc) ]
    sample.weight         = lambda event, sample: event.reweightBTagDeepCSV_SF*event.reweightPU36fb*(1 if args.small else args.reduceMC)
  
    #sample.read_variables = ['reweightTopPt/F','reweightDilepTriggerBackup/F','reweightLeptonSF/F','reweightBTag_SF/F','reweightPU36fb/F', 'nTrueInt/F', 'reweightLeptonTrackingSF/F']
    #sample.weight         = lambda event, sample: event.reweightTopPt*event.reweightBTag_SF*event.reweightLeptonSF*event.reweightDilepTriggerBackup*event.reweightPU36fb*event.reweightLeptonTrackingSF
    #print("Trigger selection: ", tr.getSelection("MET")) 
    if sample in mc:
        
        sample.setSelectionString([getFilterCut(isData=False, year=args.year), cutInterpreter.cutString(args.selection), triggerSelection])# , args.leptonpreselection])
    elif sample in signals:
        signal_normalization = 1234.35/lumi_scale
        sample.weight         = lambda event, sample: signal_normalization*event.reweightBTagDeepCSV_SF*event.reweightPU36fb*(1 if args.small else args.reduceMC)
        sample.setSelectionString([getFilterCut(isData=False, year=args.year), cutInterpreter.cutString(args.selection), cutInterpreter.cutString('T2tt_350_20')])# , args.leptonpreselection])
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

if args.region=="high_tt2l" or args.region=="low_tt2l":
    plots.append(Plot(
        texX = 'E_{T}^{miss} (GeV)', texY = 'Number of Events / 25 GeV',
        attribute = TreeVariable.fromString( "met_pt/F" ),
        binning=[450/25,0,450],
    ))
    
    plots.append(Plot(
      texX = 'p_{T}(leading lepton) (GeV)', texY = 'Number of Events / 5 GeV',
      name = 'leadingLep_pt', attribute = lambda event, sample: event.leadingLep_pt,
      binning=[25,0,150],
    ))
    
    plots.append(Plot(
      texX = 'm_{ll} (GeV)', texY = 'Number of Events / 4.6 GeV',
      name = 'mll', attribute = lambda event, sample: event.mll,
      binning=[10,4,50],
    ))
    
    plots.append(Plot(
      texX = 'H_{T} (GeV)', texY = 'Number of Events / 50 GeV',
      name = 'ht25', attribute = lambda event, sample: event.ht25, 
      binning=[700/50,0,700],
    ))

elif args.region=="high_DY" or args.region=="low_DY":
    plots.append(Plot(
        texX = 'E_{T}^{miss} (GeV)', texY = 'Number of Events / 25 GeV',
        name = 'met_pt', attribute = lambda event, sample: event.met_musubtracted,
        binning=[450/25,0,450],
    ))
    
    plots.append(Plot(
      texX = 'p_{T}(leading lepton) (GeV)', texY = 'Number of Events / 6 GeV',
      name = 'leadingLep_pt', attribute = lambda event, sample: event.leadingLep_pt,
      binning=[150/6,0,150],
    ))
    
    plots.append(Plot(
      texX = 'm_{ll} (GeV)', texY = 'Number of Events / 4.6 GeV',
      name = 'mll', attribute = lambda event, sample: event.mll,
      binning=[10,4,50],
    ))
    
    plots.append(Plot(
      texX = 'm_{\\tau\\tau} (GeV)', texY = 'Number of Events / 10 GeV',
      name = 'mtautau', attribute = lambda event, sample: event.mtautau,
      binning=[205/10,-5,200],
    ))

elif args.region=="low_sig" or args.region=="med_sig" or args.region=="high_sig":
    binning_SR = [5,12,20,30]
    plots.append(Plot(
      texX = 'p_{T}(leading lepton) (GeV)', texY = 'Number of Events',
      name = 'leadingLep_pt', attribute = lambda event, sample: event.leadingLep_pt,
      binning=Binning.fromThresholds(binning_SR),
    ))



#plots.append(Plot(
#  texX = 'm_{\\tau\\tau} (GeV)', texY = 'Number of Events / 5 GeV',
#  name = 'mtautau', attribute = lambda event, sample: event.mtautau,
#  binning=[200/5,0,200],
#))

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

