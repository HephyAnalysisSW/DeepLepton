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



path_truth = "/scratch-cbe/users/maximilian.moser/DeepLepton/traindata/DYvsQCD_2016/"
outfiles_path = "/scratch-cbe/users/maximilian.moser/DeepLepton/Train100/training_test10/outfiles.txt"
path_pred = "/scratch-cbe/users/maximilian.moser/DeepLepton/Train100/training_test10/"

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

pt_bins = [3.5, 10, 20, 40, 50, 200, 1000]
eta_bins = [0, 1, 2, 3]

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


threshhold = 0.5

pt_signal_eff = []
pt_background_eff = []

for i in range(len(pt_bins)-1): # iterate through bins
    true_signal = 0
    false_signal = 0
    true_background = 0
    false_background = 0
    n_signal = 0
    n_background = 0

    for j in range(len(pt_truth[i])):
        if pt_pred[i][j] > threshhold:
            if pt_truth[i][j] == 1:
                true_signal += 1
                n_signal += 1
            else:
                false_signal += 1
                n_background += 1
        else:
            if pt_truth[i][j] == 1:
                false_background += 1
                n_signal += 1
            else:
                true_background += 1
                n_background += 1
    
    #print("true_signal{}, false_signal {}, true_background {}, false_background {}, n_signal {}, n_background {}".format(true_signal, false_signal, true_background, false_background, n_signal, n_background))
    signal_eff = true_signal / float(n_signal) 
    background_eff = false_background / float(n_background)
    #print('bin {}-{}, signal_eff {}, background_eff {}'.format(pt_bins[i], pt_bins[i+1], signal_eff, background_eff))
    pt_signal_eff.append(signal_eff)
    pt_background_eff.append(background_eff)









