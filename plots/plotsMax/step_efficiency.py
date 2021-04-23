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

path_truth = "/scratch-cbe/users/maximilian.moser/DeepLepton/traindata/DYvsQCD_2016/"
outfiles_path = "/scratch-cbe/users/maximilian.moser/DeepLepton/Train_DYvsQCD_rH/training_40/outfiles.txt"
path_pred = "/scratch-cbe/users/maximilian.moser/DeepLepton/Train_DYvsQCD_rH/training_40/"

#path_truth = "/scratch-cbe/users/maximilian.moser/DeepLepton/traindata/DYvsQCD_2016/"
#outfiles_path = "/scratch-cbe/users/maximilian.moser/DeepLepton/Train_DYvsQCD_rH/training_40/last/outfiles.txt"
#path_pred = "/scratch-cbe/users/maximilian.moser/DeepLepton/Train_DYvsQCD_rH/training_40/last/"



variables = ["prob_isPrompt/F", "lep_isPromptId_Training/I", "lep_pt/F", "lep_eta/F"]

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
                5,7.5,10,12.5,15,17.5,20,25,30,35,40,45,50,60,75,100], dtype = float)
                #125,150,175,200,250,300,400,500,
                #600,2000],dtype=float)
#np.geomspace(3.5, 250, 50) #[3.5, 4, 5, 6, 7, 8, 10, 20, 40, 50, 100, 200, 1000]
eta_bins = np.array(
            [-2.5,-2.,-1.5,-1.,-0.5,0.5,1,1.5,2.,2.5],
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
        
        counter = 0
        for pt in pt_bins:
            if r.lep_pt < pt:
                pt_truth[counter-1].append(r.lep_isPromptId_Training)
                pt_pred[counter-1].append(r.prob_isPrompt)
                break
            counter+=1
        
        counter = 0
        for eta in eta_bins:
            if r.lep_eta > eta:
                eta_truth[counter-1].append(r.lep_isPromptId_Training)
                eta_pred[counter-1].append(r.prob_isPrompt)
                break
            counter+=1

# Plot logic here

def find_nearest_index(a, a0):
    "Element in nd array `a` closest to the scalar value `a0`"
    idx = np.abs(np.asarray(a) - a0).argmin()
    return idx #a.flat[idx]

def get_efficiencies(pred, truth, bins, threshhold, background=True):
    signal_eff = []
    background_eff = []
    
    for i in range(len(pt_bins)-1):
        true_signal = 0
        false_signal = 0
        true_background = 0
        false_background = 0

        for j in range(len(pt_truth[i])):
            if pt_pred[i][j] > threshhold:
                if pt_truth[i][j] == 1:
                    true_signal += 1
                else:
                    false_signal += 1
            else:
                if pt_truth[i][j] == 1:
                    false_background += 1
                else:
                    true_background += 1
                
        signal_eff.append(true_signal / float(true_signal + false_background)) 
        background_eff.append(false_signal / float(true_background + false_signal))
    return signal_eff, background_eff


for threshhold in np.linspace(0.01, 0.2, 50):#[0.01, 0.02, 0.03, 0.04, 0.05, 0.06]:

    pt_signal_eff , pt_background_eff = get_efficiencies(pt_pred, pt_truth, pt_bins, threshhold, background=False)

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
    c1.Print(os.path.join(plot_directory, 'Efficiency/pt_flat_background_{}.png'.format(str(threshhold))))

    # eta
    eta_signal_eff , eta_background_eff = get_efficiencies(eta_pred, eta_truth, eta_bins, threshhold, background=False)

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
    c1.Print(os.path.join(plot_directory, 'Efficiency/eta_flat_background_{}.png'.format(str(threshhold))))

"""
# eta plot
sys.exit(0)

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

mg.GetXaxis().SetTitle("lepton eta")
mg.GetYaxis().SetTitle("efficiency")

mg.GetYaxis().SetLimits(0,1)

c1.BuildLegend(0.7,0.4, 1, 0.6)
c1.Print(os.path.join(plot_directory, 'Efficiency/eta_0.2.png'))

"""


