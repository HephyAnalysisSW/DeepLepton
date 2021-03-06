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
argParser.add_argument('--small',       action='store_true',     help="Run the file on a small sample (for test purpose), bool flag set to     True if used" )
args = argParser.parse_args()

#
# Logger
#
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

#/Train_testpeak/training/

path_truth = "/scratch-cbe/users/maximilian.moser/DeepLepton/v2/step2/2016/muo/pt_3.5_-1/Top/"
outfiles_path = "/scratch-cbe/users/maximilian.moser/DeepLepton/Train_Top_2016/training_20/outfiles.txt"
path_pred = "/scratch-cbe/users/maximilian.moser/DeepLepton/Train_Top_2016/training_20/"

#path_truth = "/scratch-cbe/users/maximilian.moser/DeepLepton/traindata/DYvsQCD_2016/"
#outfiles_path = "/scratch-cbe/users/maximilian.moser/DeepLepton/Train_DYvsQCD_rH/training_40/last/outfiles.txt"
#path_pred = "/scratch-cbe/users/maximilian.moser/DeepLepton/Train_DYvsQCD_rH/training_40/last/"



variables = ["prob_isPrompt/F", "prob_isNonPrompt/F", "prob_isFake/F", "lep_isPromptId_Training/I", "lep_isNonPromptId_Training/I", "lep_isFakeId_Training/I", "lep_pt/F", "lep_eta/F"]

# read outfiles
logger.info('Getting filenames')
files_truth = []
files_pred  = []

for f in open(outfiles_path, "r"):
    if ".root" in f:
        if f.endswith("\n"):
            ff = f[:-1]
        truth_file   = ff[5:]
        f_pred  = os.path.join(path_pred, ff)
        f_truth = os.path.join(path_truth, truth_file)
        files_pred.append(f_pred)
        files_truth.append(f_truth)
        if args.small:
            break

pred    = []
truth   = []

pt_bins = np.array([
                3.5,5,7.5,10,12.5,15,17.5,20,25,30,35,40,45,50,60,75,100, 125],dtype=float)
                #125,150,175,200,250,300,400,500,
                #600,2000],dtype=float)
eta_bins = np.array(
            [-2.5,-2.,-1.5,-1.,-0.5,0.5,1,1.5,2.,2.5, 3.2],
            dtype=float
            )

pt_truth  = [[] for i in range(len(pt_bins))]
eta_truth = [[] for i in range(len(eta_bins))]

pt_pred   = [[] for i in range(len(pt_bins))]
eta_pred  = [[] for i in range(len(eta_bins))]



for i in range(len(files_truth)):
    logger.info("Reading Sample %i of %i"%(i+1, len(files_truth)))
    
    SampleTruth = Sample.fromFiles("truth", files_truth[i], treeName='tree')
    SamplePred  = Sample.fromFiles("pred", files_pred[i], treeName='tree')
    Sample = deepcopy(SampleTruth)
    Sample.addFriend(SamplePred, treeName='tree')
    
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

        if lep_isNonPromptId_Training == 1.:
            continue
    
        for i, pt in enumerate(pt_bins):
            if lep_pt < pt:
                pt_pred[i-1].append(prob_isPrompt)
                pt_truth[i-1].append(lep_isPromptId_Training)
                break 
       
        for i, eta in enumerate(eta_bins):
            if lep_eta < eta:
                eta_pred[i-1].append(prob_isPrompt)
                eta_truth[i-1].append(lep_isPromptId_Training)
                break

# Plot logic here

def find_nearest_index(a, a0):
    "Element in nd array `a` closest to the scalar value `a0`"
    idx = np.abs(np.asarray(a) - a0).argmin()
    return idx #a.flat[idx]

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

def search_best_threshhold(pred, truth, bins, target):
    threshholds = []
    signal_eff = []
    back_eff = []
    threshholds = np.linspace (0.01, 0.3, 1000)

    for t in threshholds:
        s, b = get_efficiencies(pred, truth, bins, t)
        signal_eff.append(s)
        back_eff.append(b)
    
    final_sig_eff = []
    final_back_eff = []
    
    for i in range(len(bins)):
        idx = find_nearest_index([x[i] for x in back_eff], target)
        final_sig_eff.append(signal_eff[idx][i])
        final_back_eff.append(back_eff[idx][i])

    return final_sig_eff, final_back_eff

for target in [0.02, 0.05]:
    pt_signal_eff , pt_background_eff = search_best_threshhold(pt_pred, pt_truth, pt_bins, target)

    gr1 = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_signal_eff))
    gr2 = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_background_eff))

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

    mg.GetXaxis().SetTitle("lepton pt")
    mg.GetYaxis().SetTitle("efficiency")

    mg.GetYaxis().SetLimits(0,1)

    c1.BuildLegend(0.7,0.4, 1, 0.6)
    c1.Print(os.path.join(plot_directory, 'Efficiency_muo_Top_2016_flat/pt_flat_background_{}.png'.format(str(target))))
    '''
    # eta
    eta_signal_eff , eta_background_eff = get_efficiencies(eta_pred, eta_truth, eta_bins, threshhold)

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
    c1.Print(os.path.join(plot_directory, 'Efficiency_muo_Top_2016/eta_flat_background_{}.png'.format(str(threshhold))))
'''

