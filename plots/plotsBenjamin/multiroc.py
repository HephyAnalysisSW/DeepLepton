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



path_truth = "/eos/vbc/user/maximilian.moser/DeepLepton/v2/step2/2016/muo/pt_3.5_-1/DYvsQCD/"
outfiles_path = "/scratch-cbe/users/maximilian.moser/DeepLepton/Train/training_test2/outfiles.txt"
path_pred_list = ["/scratch-cbe/users/maximilian.moser/DeepLepton/Train/training_test2/",
             "/scratch-cbe/users/maximilian.moser/DeepLepton/Train/training_test3/",
             "/scratch-cbe/users/maximilian.moser/DeepLepton/Train/training_test4/",
             "/scratch-cbe/users/maximilian.moser/DeepLepton/Train/training_test5/"]
  

variables = ["prob_isPrompt/F", "lep_isPromptId_Training/I"]

fpr = {}
tpr = {}
for path_pred in path_pred_list:
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
            pred.append(r.prob_isPrompt)
            truth.append(r.lep_isPromptId_Training)
         
    fpr[path_pred], tpr[path_pred], _ = roc_curve(truth, pred)


gr1 = ROOT.TGraph(len(fpr[path_pred_list[0]]), array.array('d', fpr[path_pred_list[0]]), array.array('d', tpr[path_pred_list[0]]))
gr2 = ROOT.TGraph(len(fpr[path_pred_list[1]]), array.array('d', fpr[path_pred_list[1]]), array.array('d', tpr[path_pred_list[1]]))
gr3 = ROOT.TGraph(len(fpr[path_pred_list[2]]), array.array('d', fpr[path_pred_list[2]]), array.array('d', tpr[path_pred_list[2]]))
gr4 = ROOT.TGraph(len(fpr[path_pred_list[3]]), array.array('d', fpr[path_pred_list[3]]), array.array('d', tpr[path_pred_list[3]]))

gr1.SetLineColorAlpha(ROOT.kBlue, 0.8)
gr2.SetLineColorAlpha(ROOT.kRed, 0.8)
gr3.SetLineColorAlpha(ROOT.kGreen, 0.8)
gr4.SetLineColorAlpha(ROOT.kMagenta+3, 0.8)

gr1.SetLineWidth(2)
gr2.SetLineWidth(2)
gr3.SetLineWidth(2)
gr4.SetLineWidth(2)
"""
gr1.SetTitle("T1")

c1 = ROOT.TCanvas("c1", "L", 200,100,1000,1000)

c1.SetTitle("ROC-Curve Comparison")

gr1.GetXaxis().SetTitle("False Positive Rate")
gr1.GetYaxis().SetTitle("True Positive Rate")

gr1.GetXaxis().SetLimits(0,1)
gr1.GetYaxis().SetLimits(0,1)
gr1.SetTitle("ROC-Curve")

gr1.Draw()
gr2.Draw("same")
gr3.Draw("same")

c1.Print(os.path.join(plot_directory, 'roc/roc_comp1.png'))
c1.BuildLegend()
"""
c1 = ROOT.TCanvas("c1", "L", 200,100,1000,1000)

gr1.SetTitle("Training Dense, standard network")
gr2.SetTitle("Default Network")
gr3.SetTitle("Smaller Dense start, larger dense end")
gr4.SetTitle("Big dense charged, larger dense end")

mg = ROOT.TMultiGraph()
mg.Add(gr1)
mg.Add(gr2)
mg.Add(gr3)
mg.Add(gr4)

mg.SetTitle("ROC-Curve Comparison")

mg.Draw("AL") # set everything before Draw, exept axis stuff

mg.GetXaxis().SetTitle("False Positive Rate")
mg.GetYaxis().SetTitle("True Positive Rate")

mg.GetXaxis().SetLimits(0,1)
mg.GetYaxis().SetLimits(0,1)


c1.BuildLegend()

c1.Print(os.path.join(plot_directory, 'roc/roc_comp1.png'))



