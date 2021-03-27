import ROOT
ROOT.gROOT.SetBatch(True)
from math import sqrt, cos, sin, pi, cosh
from RootTools.core.standard import *
import os
from copy import deepcopy
import Analysis.Tools.syncer as syncer
from DeepLepton.Tools.user import plot_directory
import uproot
import pandas
from sklearn.metrics import roc_curve, auc
import numpy as np
import argparse
import array


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



path_truth = "/eos/vbc/user/maximilian.moser/DeepLepton/v1/step2/2016/muo/pt_3.5_-1/DYvsQCD/"
outfiles_path = "/scratch-cbe/users/maximilian.moser/DeepLepton/Train/training_dense3/outfiles.txt"
path_pred = "/scratch-cbe/users/maximilian.moser/DeepLepton/Train/training_dense3/"

# read outfiles

vars_pred  = ["prob_isPrompt"] #["prob_isPrompt", "prob_isNonPrompt", "prob_isFake"] #"prob_isPrompt:prob_isNonPrompt:prob_isFake:lep_pt:lep_eta:f5:f6:f7"
vars_truth = ["lep_isPromptId_Training"] #["lep_isPromptId_Training", "lep_isNonPromptId_Training", "lep_isFakeId_Training"]#lep_isPromptId_Training:lep_isNonPromptId_Training:lep_isFakeId_Training
var = ["prob_isPrompt", "lep_pt"] # lep_pt is actually the truth variable, somehow predict.py messes this up
outfiles = []
files = []

isPrompt = []
probPrompt = []

for f in open(outfiles_path, "r"):
    if ".root" in f:
        if f.endswith("\n"):
            ff = f[:-1]
        outfiles.append(ff)
        truth_file   = ff[5:]
        upfile_pred  = uproot.open(os.path.join(path_pred, ff))
        upfile_truth = uproot.open(os.path.join(path_truth, truth_file))

        #df_pred  = upfile_pred['tree'].pandas.df(branches=vars_pred)
        #df_truth = upfile_truth['tree'].pandas.df(branches=vars_truth)
        df  = upfile_pred['tree'].pandas.df(branches=var)
        #print(df)
        probPrompt += list(np.array(df.values)[:,0].flat)
        isPrompt   += list(np.array(df.values)[:,1].flat)
        #print(len(probPrompt))
        #print(len(isPrompt))
fpr, tpr, _ = roc_curve(isPrompt, probPrompt)

print(fpr)
print(tpr)

gr = ROOT.TGraph(len(fpr), array.array('d', fpr), array.array('d', tpr))



