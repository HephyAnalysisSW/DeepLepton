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



path_truth = "/eos/vbc/user/maximilian.moser/DeepLepton/v1/step2/2016/muo/pt_3.5_-1/DYvsQCD/"
outfiles_path = "/scratch-cbe/users/maximilian.moser/DeepLepton/Train/training_dense3/outfiles.txt"
path_pred = "/scratch-cbe/users/maximilian.moser/DeepLepton/Train/training_dense3/"

variables = ["prob_isPrompt/F", "lep_isPromptId_Training/I"]

# read outfiles
logger.info('Getting filenames')
files_truth = []
files_pred  = []

for f in open(outfiles_path, "r"):
    if ".root" in f:
        if f.endswith("\n"):
            ff = f[:-1]
        truth_file   = ff[5:]
        files_pred.append(os.path.join(path_pred, ff))
        files_truth.append(os.path.join(path_truth, truth_file))

logger.info('Reading Samples')

SampleTruth = Sample.fromFiles("truth", files_truth, treeName='tree')
SamplePred  = Sample.fromFiles("pred", files_pred, treeName='tree')

logger.info('Friending Samples')
Sample = deepcopy(SampleTruth)
Sample.addFriend(SamplePred, treeName='tree')


logger.info('Start Reader')
reader = Sample.treeReader(variables=variables)

reader.start()
counter = 0
pred    = []
truth   = []
while reader.run():
    r = reader.event
    pred.append(r.prob_isPrompt)
    truth.append(r.lep_isPromptId_Training)

logger.info('End Reader')

fpr, tpr, _ = roc_curve(truth, pred)

gr = ROOT.TGraph(len(fpr), array.array('d', fpr), array.array('d', tpr))
c1 = ROOT.TCanvas("c1", "L", 200,10,600,400)
gr.Draw()
c1.SaveAs(os.path.join(plot_directory, 'roc_test.png'))


