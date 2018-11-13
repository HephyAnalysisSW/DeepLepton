# Standard imports
import ROOT
import array
import os
from ROOT import gStyle

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
from DeepLepton.samples.flat_training_samples import flat_sample

if args.small:
    TTJets_DiLepton.reduceFiles( to = 1 )
    TTJets_SingleLepton.reduceFiles( to = 1 )
    #DY.reduceFiles( to = 1 )
    #QCD.reduceFiles( to = 1 )
    flat_sample.reduceFiles( to = 1 )

event_selection = "(1)"

#signal and background sample

if args.flat:
    sig_sample = flat_sample
    bkg_sample = flat_sample
    training_name = flat_sample.name
    sample_name   = flat_sample.texName
else:
    sig_sample = TTJets_DiLepton
    bkg_sample = TTJets_SingleLepton
    training_name = 'TTJets_Muons_20181013'
    sample_name   = 'TTJets_Muons'

# truth categories
prompt_selection    = "(abs({lep}_mcMatchId)==6||abs({lep}_mcMatchId)==23||abs(lep_mcMatchId)==24||abs(lep_mcMatchId)==25||abs(lep_mcMatchId)==37)".format( lep = "lep")
nonPrompt_selection = "(!(abs(lep_mcMatchId)==6||abs(lep_mcMatchId)==23||abs(lep_mcMatchId)==24||abs(lep_mcMatchId)==25||abs(lep_mcMatchId)==37))&&(abs(lep_mcMatchAny)==4||abs(lep_mcMatchAny)==5)"
fake_selection      = "(!(abs(lep_mcMatchId)==6||abs(lep_mcMatchId)==23||abs(lep_mcMatchId)==24||abs(lep_mcMatchId)==25||abs(lep_mcMatchId)==37))&&(!(abs(lep_mcMatchAny)==4||abs(lep_mcMatchAny)==5))"

# lepton preselection
loose_id = "abs(lep_pdgId)==13&&lep_pt>5&&abs(lep_eta)<2.4&&lep_miniRelIso<0.4&&lep_sip3d<8&&abs(lep_dxy)<0.05&&abs(lep_dz)<0.1&&lep_pfMuonId&&lep_mediumMuonId"
#loose_id = "abs(lep_pdgId)==13&&lep_miniRelIso<0.5"

# pt selection
kinematic_selection = "lep_pt>25"
#kinematic_selection = "lep_pt>15&&lep_pt<=25"
#kinematic_selection = "lep_pt>5&&lep_pt<=15"
#kinematic_selection = "lep_pt>10&&lep_pt<=15"

# lepton Ids
deepLepton = {"name":"deepLepton", "var":"prob_lep_isPromptId_Training" if args.flat else "lep_deepLepton_prompt",      "color":ROOT.kGreen+2, "thresholds":[ i/100000. for i in range(0,100000)]}
mvaTTV     = {"name":"TTV",        "var":"lep_mvaTTV",                                                                  "color":ROOT.kGray+1,  "thresholds":[ i/1000. for i in range(-1000,1001)]}
mvaTTH     = {"name":"TTH",        "var":"lep_mvaTTH",                                                                  "color":ROOT.kGray,    "thresholds":[ i/1000. for i in range(-1000,1001)]}

lepton_ids = [
    mvaTTH, 
    mvaTTV,
    deepLepton,
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

gStyle.SetOptTitle(0)
c = ROOT.TCanvas()
option = "L"
same    ="A"
for lepton_id in lepton_ids:
    #lepton_id["roc"].GetXaxis().SetRangeUser(0.01, 1)
    lepton_id["roc"].GetXaxis().SetTitle("bkg eff")
    lepton_id["roc"].GetYaxis().SetTitle("sig eff")
    lepton_id["roc"].GetXaxis().SetLimits(0.01, 1)
    lepton_id["roc"].GetHistogram().SetMaximum(1.01)
    lepton_id["roc"].GetHistogram().SetMinimum(0.60)
    lepton_id["roc"].SetLineWidth(2)
    lepton_id["roc"].SetFillStyle(0)
    lepton_id["roc"].SetFillColor(0)
    lepton_id["roc"].SetMarkerColor(lepton_id["color"])
    lepton_id["roc"].SetTitle(lepton_id["name"])
    lepton_id["roc"].Draw(option+same)
    same = "same"

header = [
            {'text': ROOT.TPaveLabel(.00,0.93,.20,1.0,   "CMS preliminary",                                                                                                                      "nbNDC"), 'font': 30  },
            {'text': ROOT.TPaveLabel(.20,0.93,1.0,1.0,   "TestData: {sample}, {kin}    Training: {training}".format( sample = sample_name, kin = kinematic_selection, training = training_name), "nbNDC"), 'font': 130 },
            {'text': ROOT.TPaveLabel(.00,0.91,1.0,0.929, "preselection: {preselect}".format( preselect = loose_id ),                                                                             "nbNDC"), 'font': 130 },
         ]

for line in header:
    line['text'].SetFillColor(gStyle.GetTitleFillColor())
    line['text'].SetTextFont(line['font'])
    line['text'].Draw()

c.SetLogx()
c.BuildLegend(0.6,0.12,0.9,0.22)

directory = os.path.join( plot_directory, "DeepLepton", sample_name )
if not os.path.exists(directory):
    os.makedirs(directory)
c.Print(os.path.join( directory, "{plot_name}_{kin}_roc.png".format( plot_name = training_name, kin = kinematic_selection ) ))
