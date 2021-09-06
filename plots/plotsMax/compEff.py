import ROOT
ROOT.gROOT.SetBatch(True)
from math import sqrt, cos, sin, pi, cosh
import Analysis.Tools.syncer as syncer
from RootTools.core.standard import *
import os
from copy import deepcopy
from DeepLepton.Tools.user import plot_directory
import uproot
import pandas
from sklearn.metrics import roc_curve, auc
import numpy as np
import argparse
import array
from copy import deepcopy
import sys

argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',       action='store',      default='INFO',      nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--directory', action='store')
argParser.add_argument('--small',       action='store_true',     help="Run the file on a small sample (for test purpose), bool flag set to     True if used" )
argParser.add_argument('--long',       action='store_true',     help="0-500, else 0-45" )
argParser.add_argument('--flavour',     action="store", default="muo")
argParser.add_argument('--mode', action="store")

args = argParser.parse_args()

#
# Logger
#
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)


directory = args.directory
sampleName = directory.split('/')[-2]

print(sampleName)

directoryLSTM      = "training_20" 
directoryGRU       = "training_20_GRU" 
directoryNoPfCands = "training_20_NoPfCands"
directorySimpleRNN = "training_20_SimpleRNN"





flav = args.flavour
if "2016" in directory:
    year = "2016"
elif "2017" in directory:
    year = "2017"
elif "2018" in directory:
    year = "2018"
else:
    logger.error("NO YEAR")



if flav == "muo":
    variables = ['lep_isPromptId_Training/I',
             'lep_isNonPromptId_Training/I',
             'lep_isNotPromptId_Training/I',
             'lep_isFakeId_Training/I',
             'lep_pt/F',
             'lep_eta/F',
             #'lep_probPrompt/F',
             #'lep_probNonPrompt/F',
             #'lep_probFake/F',
             #'lep_probNotPrompt/F',
             'lep_probPrompt_LSTM/F',
             'lep_probPrompt_GRU/F',
             'lep_probPrompt_SimpleRNN/F',
             'lep_probPrompt_NoCands/F',
             'lep_mvaTTH/F',
             'lep_StopsCompressed/I',
             'lep_looseId/F',
             'lep_mediumId/F',
             'lep_tightId/F',
             'lep_precut/F',
            ]
else:
    variables = ['lep_isPromptId_Training/I',
             'lep_isNonPromptId_Training/I',
             'lep_isNotPromptId_Training/I',
             'lep_isFakeId_Training/I',
             'lep_pt/F',
             'lep_eta/F',
             #'lep_probPrompt/F',
             #'lep_probNonPrompt/F',
             #'lep_probFake/F',
             #'lep_probNotPrompt/F',
             'lep_probPrompt_LSTM/F',
             'lep_probPrompt_GRU/F',
             'lep_probPrompt_SimpleRNN/F',
             'lep_probPrompt_NoCands/F',
             'lep_mvaTTH/F',
             'lep_probPrompt_LSTM/F',
             'lep_probPrompt_GRU/F',
             'lep_probPrompt_SimpleRNN/F',
             'lep_probPrompt_NoCands/F',
             'lep_StopsCompressed/I',
             'lep_precut/F',
            ]
    
pred    = []
truth   = []


if args.long:
    if flav == "muo":
        #pt_bins = np.array([3.5,5,7.5,10,12.5,15,17.5,20,25,30,35,40,45,50,60,75,100, 125, 150, 175, 200,250,300,400,500,],dtype=float)
        pt_bins = np.array([3.5,7.5,12.5,17.5,25,35,45,75,150,300,500,],dtype=float)
    else:
        #pt_bins = np.array([5,7.5,10,12.5,15,17.5,20,25,30,35,40,45,50,60,75,100, 125, 150, 175, 200,250,300,400,500,],dtype=float)
        pt_bins = np.array([5,10,15,20,30,50,100,200,500,],dtype=float)
else:
    if flav == "muo":
        #pt_bins = np.array([3.5,5,7.5,10,12.5,15,17.5,20,25,30,35,40,45],dtype=float)
        pt_bins = np.array([3.5,7.5,12.5,17.5,25,35,45],dtype=float)
    else:
        #pt_bins = np.array([5,7.5,10,12.5,15,17.5,20,25,30,35,40,45],dtype=float)
        pt_bins = np.array([5,10,15,20,30,45],dtype=float)

eta_bins = np.array(
            [-2.5,-2.,-1.5,-1.,-0.5,0.5,1,1.5,2.,2.5, 3.2],
            dtype=float
            )

pt_truth  = [[] for i in range(len(pt_bins))]
eta_truth = [[] for i in range(len(eta_bins))]

pt_pred_LSTM      = [[] for i in range(len(pt_bins))]
pt_pred_GRU       = [[] for i in range(len(pt_bins))]
pt_pred_SimpleRNN = [[] for i in range(len(pt_bins))]
pt_pred_NoCands   = [[] for i in range(len(pt_bins))]

eta_pred_LSTM      = [[] for i in range(len(eta_bins))]
eta_pred_GRU       = [[] for i in range(len(eta_bins))]
eta_pred_SimpleRNN = [[] for i in range(len(eta_bins))]
eta_pred_NoCands   = [[] for i in range(len(eta_bins))]

pt_pred_tth   = [[] for i in range(len(pt_bins))]

pt_pred_stops = [[] for i in range(len(pt_bins))]
    
selectionString = "lep_precut==1.&&lep_genPartFlav!=15"


if args.mode == "TOP":
    Sample = Sample.fromDirectory(
                            name="Sample",
                            directory=directory,
                            treeName='tree',
                            selectionString=selectionString)
    
elif args.mode == 'DYvsQCD':
    import os
    dirs = os.listdir( directory )
    directoriesDY  = [os.path.join(directory, d)  for d in dirs if "DY"  in d]
    directoriesQCD = [os.path.join(directory, d)  for d in dirs if "QCD" in d]
    
    directories = directoriesDY + directoriesQCD
    Sample  = Sample.fromDirectory('DY',  directory=directories,  treeName='tree', selectionString=selectionString)

#if args.small:
#    Sample.reduceFiles(to=1)

reader = Sample.treeReader(variables=variables)
reader.start()

counter = 0
while reader.run():
    r = reader.event
    
    #lep_probPrompt              = r.lep_probPrompt
    #prob_isNonPrompt            = r.prob_isNonPrompt
    #prob_isFake                 = r.prob_isFake
    lep_isPromptId_Training     = r.lep_isPromptId_Training
    lep_isNonPromptId_Training  = r.lep_isNonPromptId_Training
    lep_isFakeId_Training       = r.lep_isFakeId_Training
    lep_pt                      = r.lep_pt
    lep_eta                     = r.lep_eta
    lep_mvaTTH                  = r.lep_mvaTTH
    lep_StopsCompressed         = r.lep_StopsCompressed
    
    lep_probPrompt_LSTM         = r.lep_probPrompt_LSTM
    lep_probPrompt_GRU          = r.lep_probPrompt_GRU 
    lep_probPrompt_SimpleRNN    = r.lep_probPrompt_SimpleRNN 
    lep_probPrompt_NoCands      = r.lep_probPrompt_NoCands 
    
    for i, pt in enumerate(pt_bins):
        if lep_pt < pt:
            pt_pred_LSTM[i-1].append(lep_probPrompt_LSTM)
            pt_pred_GRU[i-1].append(lep_probPrompt_GRU)
            pt_pred_SimpleRNN[i-1].append(lep_probPrompt_SimpleRNN)
            pt_pred_NoCands[i-1].append(lep_probPrompt_NoCands)

            pt_truth[i-1].append(lep_isPromptId_Training)
            pt_pred_tth[i-1].append(lep_mvaTTH)
            pt_pred_stops[i-1].append(lep_StopsCompressed)
            break 
    #for i in range(len(pt_bins)):
    #    if lep_pt > pt_bins[i] and lep_pt < pt_bins[i+1]:
    #        pt_pred[i].append(lep_probPrompt)
    #        pt_truth[i].append(lep_isPromptId_Training)
    #        pt_pred_tth[i].append(lep_mvaTTH)
    #        pt_pred_stops[i].append(lep_StopsCompressed)
    #        break 
            
    
    counter += 1
    if args.small:
        if counter > 1000000:
            break
# Plot logic here


def get_efficiencies(pred, truth, bins, threshhold):
    signal_eff = []
    background_eff = []
    for pr, tr in zip(pred, truth):
        
        true_signal      = 0.
        false_background = 0.
        total_signal     = 0.
        total_background = 0.
        for p, t in zip(pr, tr):
            if t > 0.5:
                total_signal += 1.
                if p > threshhold:
                    true_signal += 1.

            elif t < 0.5:
                total_background += 1.
                if p > threshhold:
                    false_background += 1.
            else:
                sys.exit(1)
        if total_signal >= 1:
            sig_eff = true_signal / total_signal
            #print("sig_eff", sig_eff)
        else:
            sig_eff = 0.5 # no pts in this region
        if total_background >= 1:
            back_eff = false_background / total_background
        else:
            back_eff = 0.5 # no pts in this region
        
        signal_eff.append(sig_eff)
        background_eff.append(back_eff)
    return signal_eff, background_eff


pt_signal_eff_tth    , pt_background_eff_tth   = get_efficiencies(pt_pred_tth, pt_truth, pt_bins, 0.9)
pt_signal_eff_stops , pt_background_eff_stops = get_efficiencies(pt_pred_stops, pt_truth, pt_bins, 0.5) # is 0 or 1

for t in [0.9,0.91,0.92,0.95, 0.96, 0.97, 0.98,  0.99,0.991,0.992,0.993,  0.994, 0.995, 0.996, 0.997, 0.998, 0.999, 0.9983, 0.9985, 0.9987, 0.9988, 0.9989, 0.999]:
    pt_signal_eff_LSTM,      pt_background_eff_LSTM      = get_efficiencies(pt_pred_LSTM,      pt_truth, pt_bins, t)
    pt_signal_eff_GRU,       pt_background_eff_GRU       = get_efficiencies(pt_pred_GRU,       pt_truth, pt_bins, t)
    pt_signal_eff_SimpleRNN, pt_background_eff_SimpleRNN = get_efficiencies(pt_pred_SimpleRNN, pt_truth, pt_bins, t)
    pt_signal_eff_NoCands,   pt_background_eff_NoCands   = get_efficiencies(pt_pred_NoCands,   pt_truth, pt_bins, t)
     
    gr1_LSTM      = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_signal_eff_LSTM))
    gr2_LSTM      = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_background_eff_LSTM))
    gr1_GRU       = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_signal_eff_GRU))
    gr2_GRU       = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_background_eff_GRU))
    gr1_SimpleRNN = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_signal_eff_SimpleRNN))
    gr2_SimpleRNN = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_background_eff_SimpleRNN))
    gr1_NoCands   = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_signal_eff_NoCands))
    gr2_NoCands   = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_background_eff_NoCands))

    gr3 = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_signal_eff_tth))
    gr4 = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_background_eff_tth))
    
    gr5 = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_signal_eff_stops))
    gr6 = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_background_eff_stops))


    gr1_LSTM.SetLineColorAlpha(ROOT.kBlue, 1)
    gr2_LSTM.SetLineColorAlpha(ROOT.kRed, 1)
    gr1_GRU.SetLineColorAlpha(ROOT.kBlue+4, 1)
    gr2_GRU.SetLineColorAlpha(ROOT.kRed+3, 1)
    gr1_SimpleRNN.SetLineColorAlpha(ROOT.kBlue-1, 1)
    gr2_SimpleRNN.SetLineColorAlpha(ROOT.kRed-2, 1)
    gr1_NoCands.SetLineColorAlpha(ROOT.kYellow+3, 1)
    gr2_NoCands.SetLineColorAlpha(ROOT.kCyan-1, 1)
    
    gr3.SetLineColorAlpha(ROOT.kCyan+1, 1)
    gr4.SetLineColorAlpha(ROOT.kMagenta+2, 1)
    gr5.SetLineColorAlpha(ROOT.kGreen+2, 1)
    gr6.SetLineColorAlpha(ROOT.kYellow+1, 1)

    gr1_LSTM.SetMarkerStyle(34)
    gr2_LSTM.SetMarkerStyle(34)
    gr1_GRU.SetMarkerStyle(34)
    gr2_GRU.SetMarkerStyle(34)
    gr1_SimpleRNN.SetMarkerStyle(34)
    gr2_SimpleRNN.SetMarkerStyle(34)
    gr1_NoCands.SetMarkerStyle(34)
    gr2_NoCands.SetMarkerStyle(34)
    gr3.SetMarkerStyle(34)
    gr4.SetMarkerStyle(34)
    gr5.SetMarkerStyle(34)
    gr6.SetMarkerStyle(34)

    c1 = ROOT.TCanvas("c1", "L", 200,100,1000,1000)
    
    c1.SetGrid()
    
    gr1_LSTM.SetTitle("Signal Efficiency DeepLepton LSTM")
    gr2_LSTM.SetTitle("Background Efficiency DeepLepton LSTM")
    gr1_GRU.SetTitle("Signal Efficiency DeepLepton GRU")
    gr2_GRU.SetTitle("Background Efficiency DeepLepton GRU")
    gr1_SimpleRNN.SetTitle("Signal Efficiency DeepLepton SimpleRNN")
    gr2_SimpleRNN.SetTitle("Background Efficiency DeepLepton SimpleRNN")
    gr1_NoCands.SetTitle("Signal Efficiency DeepLepton NoCands")
    gr2_NoCands.SetTitle("Background Efficiency DeepLepton NoCands")
    
    gr3.SetTitle("Signal Efficiency TTH")
    gr4.SetTitle("Background Efficiency TTH")
    gr5.SetTitle("Signal Efficiency StopsCompressed")
    gr6.SetTitle("Background Efficiency StopsCompressed")

    mg = ROOT.TMultiGraph()

    mg.Add(gr1_LSTM)
    mg.Add(gr2_LSTM)
    mg.Add(gr1_GRU)
    mg.Add(gr2_GRU)
    mg.Add(gr1_SimpleRNN)
    mg.Add(gr2_SimpleRNN)
    mg.Add(gr1_NoCands)
    mg.Add(gr2_NoCands)
    
    mg.Add(gr3)
    mg.Add(gr4)
    mg.Add(gr5)
    mg.Add(gr6)

    mg.SetTitle("Signal and Background Efficiency")
    
    mg.Draw("APL") # set everything before Draw, exept axis stuff

    mg.GetXaxis().SetTitle("lepton pt")
    mg.GetYaxis().SetTitle("efficiency")

    mg.GetYaxis().SetLimits(0,1)

    c1.BuildLegend(0.7,0.4, 1, 0.6)
    
    try:
        os.mkdir(os.path.join(plot_directory, 'Efficiency_muo_Top_2016_{}/'))
    except:
        pass
    c1.Print(os.path.join(plot_directory, 'Efficiency_Comp_{}_{}_{}_{}/pt_background_{}_{}-{}.png'.format(flav,args.mode,year, sampleName, t, 3.5, str(pt_bins[-1]))))

# ROC Curves

def numcheck(arr):
    rm = []
    for i, a in enumerate(arr):
        if a > 1:
            rm.append(i)
            print('too large {}',format(i))
        elif a < 0:
            rm.append(i)
            print('too small {}'.format(i))
        if np.isnan(a):
            print('is nan {}'.format(i))
            rm.append(i)
    return rm


# bin as key
results_lstm      = {}
results_gru       = {}
results_simplernn = {}
results_nocands   = {}
results_tth       = {}
results_stops     = {}

for truths, pred_lstm, pred_gru, pred_simplernn, pred_nocands, pred_tth, pred_stops, pt_bin in zip(pt_truth, pt_pred_LSTM, pt_pred_GRU, pt_pred_SimpleRNN, pt_pred_NoCands, pt_pred_tth, pt_pred_stops, pt_bins):
    if pt_bin == pt_bins[-1]:
        continue
    #pred_dl = []
    #truths = []
    #pred_tth = []
    #pred_stops = []
    #for i in range(2):
    #    pred_dl += pt_pred[i]
    #    pred_tth += pt_pred_tth[i]
    #    pred_stops += pt_pred_stops[i]
    #    truths += pt_truth[i]


    for i, t in enumerate(truths):
        if t > 1:
            print('is 1 at position {}'.format(i))
            break
    from sklearn.metrics import roc_curve, auc
     
    rm_indices = numcheck(pred_lstm)
    truths2 = truths[:]
    for i in reversed(rm_indices):
        truths2.pop(i)
        pred_lstm.pop(i)
    fpr_lstm,      tpr_lstm,      thr_lstm      = roc_curve(truths2, pred_lstm)
    
    rm_indices = numcheck(pred_gru)
    truths2 = truths[:]
    for i in reversed(rm_indices):
        truths2.pop(i)
        pred_gru.pop(i)
    fpr_gru,       tpr_gru,       thr_gru       = roc_curve(truths2, pred_gru)
    
    rm_indices = numcheck(pred_simplernn)
    truths2 = truths[:]
    for i in reversed(rm_indices):
        truths2.pop(i)
        pred_simplernn.pop(i)
    fpr_simplernn, tpr_simplernn, thr_simplernn = roc_curve(truths2, pred_simplernn)
    
    rm_indices = numcheck(pred_nocands)
    truths2 = truths[:]
    for i in reversed(rm_indices):
        truths2.pop(i)
        pred_nocands.pop(i)
    fpr_nocands,   tpr_nocands,   thr_nocands   = roc_curve(truths2, pred_nocands)
    
    fpr_tth,       tpr_tth,       thr_tth       = roc_curve(truths, pred_tth)
    fpr_stops,     tpr_stops,     thr_stops     = roc_curve(truths, pred_stops)
    
    results_lstm[pt_bin]      = [fpr_lstm, tpr_lstm, thr_lstm]    
    results_gru[pt_bin]       = [fpr_gru, tpr_gru, thr_gru]    
    results_simplernn[pt_bin] = [fpr_simplernn, tpr_simplernn, thr_simplernn]    
    results_nocands[pt_bin]   = [fpr_nocands, tpr_nocands, thr_nocands]    
    results_tth[pt_bin]       = [fpr_tth, tpr_tth, thr_tth]    
    results_stops[pt_bin]     = [fpr_stops, tpr_stops, thr_stops]    

    gr1_lstm      = ROOT.TGraph(len(fpr_lstm), array.array('d', fpr_lstm), array.array('d', tpr_lstm))
    gr1_gru       = ROOT.TGraph(len(fpr_gru), array.array('d', fpr_gru), array.array('d', tpr_gru))
    gr1_simplernn = ROOT.TGraph(len(fpr_simplernn), array.array('d', fpr_simplernn), array.array('d', tpr_simplernn))
    gr1_nocands   = ROOT.TGraph(len(fpr_nocands), array.array('d', fpr_nocands), array.array('d', tpr_nocands))
    gr2           = ROOT.TGraph(len(fpr_tth), array.array('d', fpr_tth), array.array('d', tpr_tth))
    gr3           = ROOT.TGraph(len(fpr_stops), array.array('d', fpr_stops), array.array('d', tpr_stops))
    
    gr1_lstm.SetLineColorAlpha(ROOT.kBlue, 0.8)
    gr1_gru.SetLineColorAlpha(ROOT.kPink+10, 0.8)
    gr1_simplernn.SetLineColorAlpha(ROOT.kCyan, 0.8)
    gr1_nocands.SetLineColorAlpha(ROOT.kBlack, 0.8)
    gr2.SetLineColorAlpha(ROOT.kRed, 0.8)
    gr3.SetLineColorAlpha(ROOT.kGreen, 0.8)
    
    gr1_lstm.SetLineWidth(2)
    gr1_gru.SetLineWidth(2)
    gr1_simplernn.SetLineWidth(2)
    gr1_nocands.SetLineWidth(2)
    gr2.SetLineWidth(2)
    gr3.SetLineWidth(2)
    
    c1 = ROOT.TCanvas("c1", "L", 200,100,1000,1000)
    gr1_lstm.SetTitle("Deep Lepton LSTM")
    gr1_gru.SetTitle("Deep Lepton GRU")
    gr1_simplernn.SetTitle("Deep Lepton SimpleRNN")
    gr1_nocands.SetTitle("Deep Lepton NoCands")
    gr2.SetTitle("TTH")
    gr3.SetTitle("Stops Compressed")
    
    mg = ROOT.TMultiGraph()
    mg.Add(gr1_lstm)
    mg.Add(gr1_gru)
    mg.Add(gr1_simplernn)
    mg.Add(gr1_nocands)
    mg.Add(gr2)
    mg.Add(gr3)
    
    mg.SetTitle("ROC-Curve Comparison {}".format(pt_bin))
     
    mg.Draw("AL")
    mg.GetXaxis().SetTitle("False Positive Rate")
    mg.GetYaxis().SetTitle("True Positive Rate")
    
    mg.GetXaxis().SetLimits(0,1)
    mg.GetYaxis().SetLimits(0,1)
    
    c1.BuildLegend()
    c1.Print(os.path.join(plot_directory, 'Efficiency_Comp_{}_{}_{}_{}/pt_roc_{}.png'.format(flav, args.mode,year, sampleName, pt_bin)))

    
# now make a flat pt background plot:

def get_nearest_index(arr, val):
    array = np.asarray(arr)
    idx = (np.abs(array - val)).argmin()
    return idx
    



targets = [0.01, 0.02, 0.05, 0.1]

efficiencies_lstm = {}
efficiencies_gru = {}
efficiencies_simplernn = {}
efficiencies_nocands = {}


for pt_bin in pt_bins[:-1]:
    fpr_lstm, tpr_lstm, thr_lstm                = results_lstm[pt_bin]
    fpr_gru, tpr_gru, thr_gru                   = results_gru[pt_bin]
    fpr_simplernn, tpr_simplernn, thr_simplernn = results_simplernn[pt_bin]
    fpr_nocands, tpr_nocands, thr_nocands       = results_nocands[pt_bin]
    fpr_tth, tpr_tth, thr_tth                   = results_tth[pt_bin]
    fpr_stops, tpr_stops, thr_stops             = results_stops[pt_bin]
    
    #print(fpr_dl, tpr_dl, thr_dl)
    #print(1)
    #print(fpr_tth, tpr_tth, thr_tth)
    #print(2)
    #print(fpr_stops, tpr_stops, thr_stops)

    # get sig_eff and thr for lstm:
    efficiencies = {}
    for target in targets:
        index = get_nearest_index(fpr_lstm, target)
        signal_eff = tpr_lstm[index]
        background_eff = fpr_lstm[index]
        threshhold = thr_lstm[index]
        efficiencies[target] = [signal_eff, background_eff, threshhold, target, pt_bin]
    efficiencies_lstm[pt_bin] = efficiencies
    # get sig_eff and thr for gru:
    efficiencies = {}
    for target in targets:
        index = get_nearest_index(fpr_gru, target)
        signal_eff = tpr_gru[index]
        background_eff = fpr_gru[index]
        threshhold = thr_gru[index]
        efficiencies[target] = [signal_eff, background_eff, threshhold, target, pt_bin]
    efficiencies_gru[pt_bin] = efficiencies
    # get sig_eff and thr for simplernn:
    efficiencies = {}
    for target in targets:
        index = get_nearest_index(fpr_simplernn, target)
        signal_eff = tpr_simplernn[index]
        background_eff = fpr_simplernn[index]
        threshhold = thr_simplernn[index]
        efficiencies[target] = [signal_eff, background_eff, threshhold, target, pt_bin]
    efficiencies_simplernn[pt_bin] = efficiencies
    # get sig_eff and thr for nocands:
    efficiencies = {}
    for target in targets:
        index = get_nearest_index(fpr_nocands, target)
        signal_eff = tpr_nocands[index]
        background_eff = fpr_nocands[index]
        threshhold = thr_nocands[index]
        efficiencies[target] = [signal_eff, background_eff, threshhold, target, pt_bin]
    efficiencies_nocands[pt_bin] = efficiencies


# get the right signal efficiencies:
swap_back_eff = 15 # 2nd target, 0th target, swap at 3rd bin
loose_target_index = 1
tight_target_index = 0
pt_signal_eff_lstm = []
pt_background_eff_lstm = []
pt_signal_eff_gru = []
pt_background_eff_gru = []
pt_signal_eff_simplernn = []
pt_background_eff_simplernn = []
pt_signal_eff_nocands = []
pt_background_eff_nocands = []

for pt_bin in pt_bins[:-1]:
    if pt_bin <= swap_back_eff:
        target = targets[loose_target_index]
    else:
        target = targets[tight_target_index]
    
    sig_eff_lstm  = efficiencies_lstm[pt_bin][target][0]
    back_eff_lstm = efficiencies_lstm[pt_bin][target][1]    
    sig_eff_gru  = efficiencies_gru[pt_bin][target][0]
    back_eff_gru = efficiencies_gru[pt_bin][target][1]    
    sig_eff_simplernn  = efficiencies_simplernn[pt_bin][target][0]
    back_eff_simplernn = efficiencies_simplernn[pt_bin][target][1]    
    sig_eff_nocands  = efficiencies_nocands[pt_bin][target][0]
    back_eff_nocands = efficiencies_nocands[pt_bin][target][1]    

    pt_signal_eff_lstm.append(sig_eff_lstm)
    pt_background_eff_lstm.append(back_eff_lstm) 
    pt_signal_eff_gru.append(sig_eff_gru)
    pt_background_eff_gru.append(back_eff_gru) 
    pt_signal_eff_simplernn.append(sig_eff_simplernn)
    pt_background_eff_simplernn.append(back_eff_simplernn) 
    pt_signal_eff_nocands.append(sig_eff_nocands)
    pt_background_eff_nocands.append(back_eff_nocands) 

# make plot:
logger.info("Making final plot")
 
gr1_lstm = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_signal_eff_lstm))
gr2_lstm = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_background_eff_lstm))
gr1_gru = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_signal_eff_gru))
gr2_gru = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_background_eff_gru))
gr1_simplernn = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_signal_eff_simplernn))
gr2_simplernn = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_background_eff_simplernn))
gr1_nocands = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_signal_eff_nocands))
gr2_nocands = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_background_eff_nocands))

gr3 = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_signal_eff_tth))
gr4 = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_background_eff_tth))
    
gr5 = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_signal_eff_stops))
gr6 = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_background_eff_stops))


gr1_lstm.SetLineColorAlpha(ROOT.kBlue, 1)
gr2_lstm.SetLineColorAlpha(ROOT.kRed, 1)
gr1_gru.SetLineColorAlpha(ROOT.kBlue+4, 1)
gr2_gru.SetLineColorAlpha(ROOT.kRed+3, 1)
gr1_simplernn.SetLineColorAlpha(ROOT.kBlue-1, 1)
gr2_simplernn.SetLineColorAlpha(ROOT.kRed-2, 1)
gr1_nocands.SetLineColorAlpha(ROOT.kYellow+3, 1)
gr2_nocands.SetLineColorAlpha(ROOT.kCyan-1, 1)

gr3.SetLineColorAlpha(ROOT.kCyan+1, 1)
gr4.SetLineColorAlpha(ROOT.kMagenta+2, 1)
gr5.SetLineColorAlpha(ROOT.kGreen+2, 1)
gr6.SetLineColorAlpha(ROOT.kYellow+1, 1)

gr1_lstm.SetMarkerStyle(34)
gr2_lstm.SetMarkerStyle(34)
gr1_gru.SetMarkerStyle(34)
gr2_gru.SetMarkerStyle(34)
gr1_simplernn.SetMarkerStyle(34)
gr2_simplernn.SetMarkerStyle(34)
gr1_nocands.SetMarkerStyle(34)
gr2_nocands.SetMarkerStyle(34)
gr3.SetMarkerStyle(34)
gr4.SetMarkerStyle(34)
gr5.SetMarkerStyle(34)
gr6.SetMarkerStyle(34)

c1 = ROOT.TCanvas("c1", "L", 200,100,1000,1000)
    
c1.SetGrid()
    
gr1_lstm.SetTitle("Signal Efficiency DeepLepton LSTM")
gr2_lstm.SetTitle("Background Efficiency DeepLepton LSTM")
gr1_gru.SetTitle("Signal Efficiency DeepLepton GRU")
gr2_gru.SetTitle("Background Efficiency DeepLepton GRU")
gr1_simplernn.SetTitle("Signal Efficiency DeepLepton SimpleRNN")
gr2_simplernn.SetTitle("Background Efficiency DeepLepton SimpleRNN")
gr1_nocands.SetTitle("Signal Efficiency DeepLepton NoCands")
gr2_nocands.SetTitle("Background Efficiency DeepLepton NoCands")
gr3.SetTitle("Signal Efficiency TTH")
gr4.SetTitle("Background Efficiency TTH")
gr5.SetTitle("Signal Efficiency StopsCompressed")
gr6.SetTitle("Background Efficiency StopsCompressed")

mg = ROOT.TMultiGraph()

mg.Add(gr1_lstm)
mg.Add(gr2_lstm)
mg.Add(gr1_gru)
mg.Add(gr2_gru)
mg.Add(gr1_simplernn)
mg.Add(gr2_simplernn)
mg.Add(gr1_nocands)
mg.Add(gr2_nocands)
mg.Add(gr3)
mg.Add(gr4)
mg.Add(gr5)
mg.Add(gr6)

mg.SetTitle("Signal and Background Efficiency")
    
mg.Draw("APL") # set everything before Draw, exept axis stuff

mg.GetXaxis().SetTitle("lepton pt")
mg.GetYaxis().SetTitle("efficiency")

mg.GetYaxis().SetLimits(0,1)

c1.BuildLegend(0.7,0.4, 1, 0.6)
    
try:
    os.mkdir(os.path.join(plot_directory, 'Efficiency_muo_Top_2016_{}/'))
except:
    pass
c1.Print(os.path.join(plot_directory, 'Efficiency_Comp_{}_{}_{}_{}/pt_flat_background_{}_{}-{}.png'.format(flav,args.mode, year, sampleName, t, 3.5, str(pt_bins[-1]))))

















dosomethingtostop()

# Re read the files and +1 the right eta bin, according to to the threshhold (pt)
true_signal      = [0. for i in range(len(eta_bins))]
false_background = [0. for i in range(len(eta_bins))]
total_signal     = [0. for i in range(len(eta_bins))]
total_background = [0. for i in range(len(eta_bins))]


    
reader = Sample.treeReader(variables=variables)
reader.start()
while reader.run():
    r = reader.event
    
    prob_isPrompt               = r.prob_isPrompt
    prob_isNonPrompt            = r.prob_isNonPrompt
    prob_isFake                 = r.prob_isFake
    lep_isPromptId_Training     = r.lep_isPromptId_Training
    lep_isNonPromptId_Training = r.lep_isNonPromptId_Training
    lep_isFakeId_Training      = r.lep_isFakeId_Training
    lep_pt                      = r.lep_pt
    lep_eta                     = r.lep_eta

    #if lep_isNonPromptId_Training == 1.:
    #    continue
    for i, pt, t in zip(range(len(pt_bins)), pt_bins, threshholds):
        #print(lep_pt, pt)
        if lep_pt < pt: # right pt bin
            #print("in right pt bin")
            for j, eta in enumerate(eta_bins):
                if lep_eta < eta: # right eta bin
                    #print('in right eta bin')
                    if lep_isPromptId_Training == 1:
                        total_signal[j] += 1.
                        if prob_isPrompt > t:
                            true_signal[j] += 1.
                    else:
                        total_background[j] += 1.
                        if prob_isPrompt > t:
                            false_background[j] += 1.
                    break
            break
    
# calculate efficiencies:
eta_signal_eff = []
eta_background_eff = []

print(total_signal, true_signal, total_background, false_background)

for tots, trus, totb, falb in zip(total_signal, true_signal, total_background, false_background):
    try:
        eta_signal_eff.append(trus / tots)
    except:
        eta_signal_eff.append(0.5)
    try:
        eta_background_eff.append(falb / totb)
    except:
        eta_background_eff.append(0.5)
# eta
#eta_signal_eff , eta_background_eff = get_efficiencies(eta_pred, eta_truth, eta_bins, threshhold)

gr1 = ROOT.TGraph(len(eta_bins)-1, array.array("d", eta_bins[:-1]), array.array("d", eta_signal_eff))
gr2 = ROOT.TGraph(len(eta_bins)-1, array.array("d", eta_bins[:-1]), array.array("d", eta_background_eff))

gr1.SetLineColorAlpha(ROOT.kBlue, 1)
gr2.SetLineColorAlpha(ROOT.kRed, 1)

gr1.SetMarkerStyle(34)
gr2.SetMarkerStyle(34)

c1 = ROOT.TCanvas("c1", "L", 200,100,1000,1000)

c1.SetGrid()

gr1.SetTitle("Signal Efficiency")
gr2.SetTitle("Background Efficiency")

mg = ROOT.TMultiGraph()

mg.Add(gr1)
mg.Add(gr2)

mg.SetTitle("Signal and Background Efficiency")

mg.Draw("APL") # set everything before Draw, exept axis stuff

mg.GetXaxis().SetTitle("lepton eta")
mg.GetYaxis().SetTitle("efficiency")

mg.GetYaxis().SetLimits(0,1)

c1.BuildLegend(0.7,0.4, 1, 0.6)
c1.Print(os.path.join(plot_directory, 'Efficiency_muo_Top_2016_TT_pow/eta_flat_background_{}.png'.format(str(target))))

print('threshholds:', threshholds)
