# Standard imports
import ROOT
import array
import os

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',      default='INFO',          nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--small',                                   action='store_true',     help='Run only on a small subset of the data?', )
argParser.add_argument('--plot_directory',     action='store',      default='deepLepton')
argParser.add_argument('--flat',                                    action='store_true',     help='Run on flat ntuple data?', )
#argParser.add_argument('--selection',          action='store',      default='dilepOS-njet3p-btag1p-onZ')
args = argParser.parse_args()

# DeepLepton
from DeepLepton.Tools.user import plot_directory

# Logger
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

#RootTools
from RootTools.core.standard import *

#Samples
data_directory = "/afs/hephy.at/data/rschoefbeck02/cmgTuples/"
postProcessing_directory = "deepLepton_v1/inclusive"
from DeepLepton.samples.cmgTuples_deepLepton_Summer16_mAODv2_postProcessed import *
from DeepLepton.samples.flat_training_samples import training_20181026

if args.small:
    TTJets_DiLepton.reduceFiles( to = 1 )
    TTJets_SingleLepton.reduceFiles( to = 1 )
    #DY.reduceFiles( to = 1 )
    #QCD.reduceFiles( to = 1 )
    training_20181026.reduceFiles( to = 1 )

event_selection = "(1)"

#signal and background sample

if args.flat:
    sig_sample = training_20181026
    bkg_sample = training_20181026
else:
    sig_sample = TTJets_DiLepton
    bkg_sample = TTJets_SingleLepton

# truth categories
prompt_selection    = "(abs({lep}_mcMatchId)==6||abs({lep}_mcMatchId)==23||abs(lep_mcMatchId)==24||abs(lep_mcMatchId)==25||abs(lep_mcMatchId)==37)".format( lep = "lep")
nonPrompt_selection = "(!(abs(lep_mcMatchId)==6||abs(lep_mcMatchId)==23||abs(lep_mcMatchId)==24||abs(lep_mcMatchId)==25||abs(lep_mcMatchId)==37))&&(abs(lep_mcMatchAny)==4||abs(lep_mcMatchAny)==5)"
fake_selection      = "(!(abs(lep_mcMatchId)==6||abs(lep_mcMatchId)==23||abs(lep_mcMatchId)==24||abs(lep_mcMatchId)==25||abs(lep_mcMatchId)==37))&&(!(abs(lep_mcMatchAny)==4||abs(lep_mcMatchAny)==5))"

# lepton preselection
loose_id = "abs(lep_pdgId)==13&&lep_pt>5&&abs(lep_eta)<2.4&&lep_miniRelIso<0.4&&lep_sip3d<8&&abs(lep_dxy)<0.05&&abs(lep_dz)<0.1&&lep_pfMuonId&&lep_mediumMuonId"
#loose_id = "abs(lep_pdgId)==13&&lep_miniRelIso<0.5"

# pt selection
kinematic_selection = "lep_pt>25"

# lepton Ids
deepLepton = {"name":"deepLepton", "var":"prob_lep_isPromptId_Training" if args.flat else "lep_deepLepton_prompt",      "color":ROOT.kGreen, "thresholds":[ i/10000. for i in range(0,10000)]}
mvaTTV     = {"name":"TTV",        "var":"lep_mvaTTV",                                                                  "color":ROOT.kBlue,  "thresholds":[ i/100. for i in range(-100,101)]}
mvaTTH     = {"name":"TTH",        "var":"lep_mvaTTH",                                                                  "color":ROOT.kRed,   "thresholds":[ i/100. for i in range(-100,101)]}

lepton_ids = [
    deepLepton,
    mvaTTV,
    mvaTTH, 
]

# get signal efficiency
for lepton_id in lepton_ids:
    logger.info( "At id %s", lepton_id["name"] )
    selectionString = "&&".join( [ kinematic_selection, loose_id,  prompt_selection ] )
    print selectionString
    ref                    = sig_sample.getYieldFromDraw( selectionString = selectionString ) 
    lepton_id["sig_h_eff"] = sig_sample.get1DHistoFromDraw(     lepton_id["var"], lepton_id["thresholds"], selectionString = selectionString, binningIsExplicit = True )
    lepton_id["sig_h_eff"].Scale( 1./ref['val'])


    selectionString = "&&".join( [ kinematic_selection, loose_id,  "(!("+prompt_selection+"))" ] )
    print selectionString
    ref                    = bkg_sample.getYieldFromDraw( selectionString = selectionString ) 
    lepton_id["bkg_h_eff"] = bkg_sample.get1DHistoFromDraw( lepton_id["var"], lepton_id["thresholds"], selectionString = selectionString, binningIsExplicit = True )
    lepton_id["bkg_h_eff"].Scale( 1./ref['val'])

#    e_S = 0.
#    e_B = 0
#    for i_b in reversed(range( 0, lepton_id["sig_h_eff"].GetNbinsX() + 1 )):
#        print i_b, lepton_id["sig_h_eff"].Integral(i_b, lepton_id["sig_h_eff"].GetNbinsX() + 1), lepton_id["bkg_h_eff"].Integral(i_b, lepton_id["bkg_h_eff"].GetNbinsX() + 1)
    lepton_id["sig_eff" ] = [ lepton_id["sig_h_eff"].Integral(i_b, lepton_id["sig_h_eff"].GetNbinsX() + 1) for i_b in range( 0, lepton_id["sig_h_eff"].GetNbinsX() + 1 )] 
    lepton_id["bkg_eff" ] = [ lepton_id["bkg_h_eff"].Integral(i_b, lepton_id["bkg_h_eff"].GetNbinsX() + 1) for i_b in range( 0, lepton_id["bkg_h_eff"].GetNbinsX() + 1 )] 

    lepton_id["roc"]      = ROOT.TGraph(len(lepton_id["bkg_eff" ]), array.array('d', lepton_id["bkg_eff" ]), array.array('d', lepton_id["sig_eff" ]))
    lepton_id["roc"].SetLineColor( lepton_id['color'] ) 

c = ROOT.TCanvas() 
option = "L"
same    ="A"
for lepton_id in lepton_ids:
    #lepton_id["roc"].GetXaxis().SetRangeUser(0.01, 1)
    lepton_id["roc"].GetXaxis().SetTitle("bkg eff")
    lepton_id["roc"].GetYaxis().SetTitle("sig eff")
    lepton_id["roc"].GetXaxis().SetLimits(0.01, 1)
    lepton_id["roc"].GetHistogram().SetMaximum(1)
    lepton_id["roc"].GetHistogram().SetMinimum(0)
    lepton_id["roc"].Draw(option+same)
    same = "same"

c.SetLogx()
c.Print(os.path.join( plot_directory, "DeepLepton", "roc.png") )
