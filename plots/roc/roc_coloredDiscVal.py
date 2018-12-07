# Standard imports
import ROOT
import array
import os
from ROOT import gStyle

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',           default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--small',              action='store_true',                help='Run only on a small subset of the data?', )
argParser.add_argument('--plot_directory',     action='store',           default='deepLepton')
argParser.add_argument('--ptMin',              action='store',      type=int,     default=5)
argParser.add_argument('--ptMax',              action='store',      type=int,     default=25)
argParser.add_argument('--flat',               action='store_true',                 help='Run on flat ntuple data?', )
argParser.add_argument('--flatSample',         action='store',           default='TTJets_Muons_balanced_pt5toInf_2016')

argParser.add_argument('--year',               action='store', type=int, choices=[2016,2017],   default=2016,   help="Which year?")
argParser.add_argument('--flavour',            action='store', type=str, choices=['ele','muo'], default='muo',  help="Which Flavour?")
argParser.add_argument('--testData',           action='store', type=int, choices=[0,1],         default=1,      help="plot test or train data?")
argParser.add_argument('--lumi_weight',        action='store', type=int, choices=[0,1],         default=1,      help="apply lumi weight?")
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

event_selection = "(1)"

#signal and background sample

if args.flat:
    from DeepLepton.samples.flat_training_samples import *

    nMax = 2 if args.flat else -1
    
    flat_sampleInfo = vars()[args.flatSample]
    flat_files, predict_files = get_flat_files( flat_sampleInfo['flat_directory'], flat_sampleInfo['predict_directory' if args.testData else 'predict_directory_trainData'])
    flat_sample = get_flat_sample( flat_sampleInfo['training_name'], flat_sampleInfo['sample_name'], flat_files, predict_files )

    sig_sample = flat_sample
    bkg_sample = flat_sample

    training_name = flat_sample.name
    sample_name   = flat_sample.texName

else:
    data_directory = "/afs/hephy.at/data/rschoefbeck02/cmgTuples/"
    postProcessing_directory = "deepLepton_v1/inclusive"
    from DeepLepton.samples.cmgTuples_deepLepton_Summer16_mAODv2_postProcessed import *

    sig_sample = TTJets_DiLepton
    bkg_sample = TTJets_SingleLepton
    training_name = 'TTJets_Muons_20181013'
    sample_name   = 'TTJets_Muons'

    if args.small:
        TTJets_DiLepton.reduceFiles( to = 1 )
        TTJets_SingleLepton.reduceFiles( to = 1 )
        #DY.reduceFiles( to = 1 )
        #QCD.reduceFiles( to = 1 )

# truth categories
prompt_selection    = "(abs(lep_mcMatchId)==6||abs(lep_mcMatchId)==23||abs(lep_mcMatchId)==24||abs(lep_mcMatchId)==25||abs(lep_mcMatchId)==37)"
nonPrompt_selection = "(!(abs(lep_mcMatchId)==6||abs(lep_mcMatchId)==23||abs(lep_mcMatchId)==24||abs(lep_mcMatchId)==25||abs(lep_mcMatchId)==37))&&(abs(lep_mcMatchAny)==4||abs(lep_mcMatchAny)==5)"
fake_selection      = "(!(abs(lep_mcMatchId)==6||abs(lep_mcMatchId)==23||abs(lep_mcMatchId)==24||abs(lep_mcMatchId)==25||abs(lep_mcMatchId)==37))&&(!(abs(lep_mcMatchAny)==4||abs(lep_mcMatchAny)==5))"

# lepton preselection
loose_id = "abs(lep_pdgId)==13&&lep_pt>5&&abs(lep_eta)<2.4&&lep_miniRelIso<0.4&&lep_sip3d<8&&abs(lep_dxy)<0.05&&abs(lep_dz)<0.1&&lep_pfMuonId&&lep_mediumMuonId"
#loose_id = "abs(lep_pdgId)==13&&lep_miniRelIso<0.5"

# pt selection
ptBinning = 5.
ptBins    = int((args.ptMax-args.ptMin)/ptBinning)
kinematic_selections = [
                        {"name":                         "pt{ptMin}to{ptMax}".format(ptMin = int(args.ptMin + i*ptBinning), ptMax = int(args.ptMin + (i+1)*ptBinning) if args.ptMin + (i+1)*ptBinning<args.ptMax else args.ptMax), 
                         "selectionString": "lep_pt>{ptMin}&&lep_pt<={ptMax}".format(ptMin = args.ptMin + i*ptBinning, ptMax = args.ptMin + (i+1)*ptBinning if args.ptMin + (i+1)*ptBinning<args.ptMax else args.ptMax)}
                         for i in xrange(ptBins)
                       ]
kinematic_selections.append({"name": "pt25toInf", "selectionString": "lep_pt>25"})

#relative lumi weight
weightString = 'lumi_scaleFactor1fb' if args.lumi_weight else '1'

# lepton Ids
deepLepton = {"name":"deepLepton", "var":"prob_lep_isPromptId_Training" if args.flat else "lep_deepLepton_prompt",      "color":ROOT.kGreen+2, "thresholds":[ i/10000. for i in range(0,10000)]}
mvaTTV     = {"name":"TTV",        "var":"lep_mvaTTV",                                                                  "color":ROOT.kGray+1,  "thresholds":[ i/10000. for i in range(-10000,10001)]}
mvaTTH     = {"name":"TTH",        "var":"lep_mvaTTH",                                                                  "color":ROOT.kGray,    "thresholds":[ i/100. for i in range(-100,101)]}

lepton_ids = [
    #mvaTTH, 
    mvaTTV,
    deepLepton,
]


# get signal efficiency
for kinematic_selection in kinematic_selections:
    for lepton_id in lepton_ids:
        logger.info( "At id %s", lepton_id["name"] )
        selectionString = "&&".join( [ kinematic_selection["selectionString"], loose_id,  prompt_selection ] )
        print selectionString
        ref                    = sig_sample.getYieldFromDraw( selectionString = selectionString, weightString = weightString) 
        lepton_id["sig_h_eff"] = sig_sample.get1DHistoFromDraw(     lepton_id["var"], lepton_id["thresholds"], selectionString = selectionString, weightString = weightString, binningIsExplicit = True )
        lepton_id["sig_h_eff"].Scale( 1./ref['val'])


        selectionString = "&&".join( [ kinematic_selection["selectionString"], loose_id,  "(!("+prompt_selection+"))" ] )
        print selectionString
        ref                    = bkg_sample.getYieldFromDraw( selectionString = selectionString, weightString = weightString )
        lepton_id["bkg_h_eff"] = bkg_sample.get1DHistoFromDraw( lepton_id["var"], lepton_id["thresholds"], selectionString = selectionString, weightString = weightString, binningIsExplicit = True )
        lepton_id["bkg_h_eff"].Scale( 1./ref['val'])

    #    e_S = 0.
    #    e_B = 0
    #    for i_b in reversed(range( 0, lepton_id["sig_h_eff"].GetNbinsX() + 1 )):
    #        print i_b, lepton_id["sig_h_eff"].Integral(i_b, lepton_id["sig_h_eff"].GetNbinsX() + 1), lepton_id["bkg_h_eff"].Integral(i_b, lepton_id["bkg_h_eff"].GetNbinsX() + 1)
        lepton_id["sig_eff" ] = [ lepton_id["sig_h_eff"].Integral(i_b, lepton_id["sig_h_eff"].GetNbinsX() + 1) for i_b in range( 0, lepton_id["sig_h_eff"].GetNbinsX() + 1 )] 
        lepton_id["bkg_eff" ] = [ lepton_id["bkg_h_eff"].Integral(i_b, lepton_id["bkg_h_eff"].GetNbinsX() + 1) for i_b in range( 0, lepton_id["bkg_h_eff"].GetNbinsX() + 1 )] 

        lepton_id["roc_"+kinematic_selection["name"]] = ROOT.TGraph(len(lepton_id["bkg_eff" ]), array.array('d', lepton_id["bkg_eff" ]), array.array('d', lepton_id["sig_eff" ]))
        lepton_id["roc_"+kinematic_selection["name"]].SetLineColor( lepton_id['color'] )

gStyle.SetOptTitle(0)
c = ROOT.TCanvas()
option   = "P"
same     = "A"
marker   = {}
latex    = {}
for lepton_id in lepton_ids:
    latexPos = 0.65
    for kinematic_selection in kinematic_selections:
        marker.update({kinematic_selection["name"]+lepton_id["name"]: []})
        latex.update({kinematic_selection["name"]+lepton_id["name"]: []})
        #lepton_id["roc"].GetXaxis().SetRangeUser(0.01, 1)
        lepton_id["roc_"+kinematic_selection["name"]].GetXaxis().SetTitle("bkg eff")
        lepton_id["roc_"+kinematic_selection["name"]].GetYaxis().SetTitle("sig eff")
        lepton_id["roc_"+kinematic_selection["name"]].GetXaxis().SetLimits(0.01, 1)
        lepton_id["roc_"+kinematic_selection["name"]].GetHistogram().SetMaximum(1.01)
        lepton_id["roc_"+kinematic_selection["name"]].GetHistogram().SetMinimum(0.60)
        lepton_id["roc_"+kinematic_selection["name"]].SetLineWidth(0)
        lepton_id["roc_"+kinematic_selection["name"]].SetFillStyle(0)
        lepton_id["roc_"+kinematic_selection["name"]].SetFillColor(0)
        lepton_id["roc_"+kinematic_selection["name"]].SetMarkerStyle(1)
        lepton_id["roc_"+kinematic_selection["name"]].SetMarkerColor(lepton_id["color"])
        lepton_id["roc_"+kinematic_selection["name"]].SetTitle(lepton_id["name"]+'_'+kinematic_selection["name"])
        lepton_id["roc_"+kinematic_selection["name"]].Draw(option+same)
        same = "same"
        n=lepton_id["roc_"+kinematic_selection["name"]].GetN()
        x=ROOT.Double(0)
        y=ROOT.Double(0)
        p=1
        counter = 0
        for i in xrange(n):
            lepton_id["roc_"+kinematic_selection["name"]].GetPoint(i,x,y)
            #color = 1+int(lepton_id["thresholds"][i]*lepton_id["thresholds"][i]*lepton_id["thresholds"][i]*lepton_id["thresholds"][i]*50 + 0.5) + 50
            discVal = lepton_id["thresholds"][i] if lepton_id["name"]=="deepLepton" else (lepton_id["thresholds"][i]+1.)/2.
            color = 1+int((discVal**p)*50 + 0.5) + 50
            color = color if color<=99 else 2
            if y>0.60 and x>0.01:
                marker[kinematic_selection["name"]+lepton_id["name"]].append( ROOT.TMarker(x,y,6 if lepton_id["name"]=="deepLepton" else 1) )
                marker[kinematic_selection["name"]+lepton_id["name"]][i].SetMarkerColor(color)
                marker[kinematic_selection["name"]+lepton_id["name"]][i].Draw()
            if y < latexPos and counter == 0:
                latex[kinematic_selection["name"]+lepton_id["name"]] = ROOT.TLatex(x,y, kinematic_selection["name"])
                latex[kinematic_selection["name"]+lepton_id["name"]].SetTextSize(0.020)
                latex[kinematic_selection["name"]+lepton_id["name"]].SetTextFont(42)
                latex[kinematic_selection["name"]+lepton_id["name"]].SetTextAlign(21)
                latex[kinematic_selection["name"]+lepton_id["name"]].SetTextColor(lepton_id["color"])
                latex[kinematic_selection["name"]+lepton_id["name"]].Draw()
                counter += 1
                latexPos += 0.05
header = [
            {'text': ROOT.TPaveLabel(.00,0.93,.20,1.0,   "CMS preliminary",                                                                                                                      "nbNDC"), 'font': 30  },
            {'text': ROOT.TPaveLabel(.20,0.93,1.0,1.0,   "TestData: {sample}, pt{ptMin}to{ptMax}    Training: {training}".format( sample = sample_name, ptMin = args.ptMin, ptMax = args.ptMax, training = training_name), "nbNDC"), 'font': 130 },
            {'text': ROOT.TPaveLabel(.00,0.91,1.0,0.929, "preselection: {preselect}".format( preselect = loose_id ),                                                                             "nbNDC"), 'font': 130 },
         ]

for line in header:
    line['text'].SetFillColor(gStyle.GetTitleFillColor())
    line['text'].SetTextFont(line['font'])
    line['text'].Draw()

c.SetLogx()
#color legend
leg = ROOT.TLegend(0.8,0.12,1.0,0.80)
leg.SetHeader("color legend")
leg.SetNColumns(2)
m=[]
for i in xrange(50):
    m.append( ROOT.TMarker(1.,1.,7) )
    color = 1+int((lepton_id["thresholds"][i*200]**p)*50 + 0.5) + 50
    color = color if color<=99 else 2
    m[i].SetMarkerColor(color)
    m[i].Draw
    legTxt = "x > {xVal}".format(xVal=lepton_id["thresholds"][i*200])
    leg.AddEntry(m[i], legTxt, "p")
leg.Draw()
#c.BuildLegend(0.6,0.12,0.9,0.22)

if args.flat:
    directory = os.path.join(   plot_directory, "DeepLepton", 
                                flat_sampleInfo['sample_name'],
                                flat_sampleInfo['training_date'],
                                'TestData' if args.testData else 'TrainData',
                                'roc',
                            )
else:
    directory = os.path.join( plot_directory, "DeepLepton" ) 

if not os.path.exists(directory):
    os.makedirs(directory)
c.Print(os.path.join( directory, "roc_colored_{lepid}_discriminator_{lumi}.png".format( lepid = lepton_id["name"], lumi = 'lumi' if args.lumi_weight else 'noLumi' )))
