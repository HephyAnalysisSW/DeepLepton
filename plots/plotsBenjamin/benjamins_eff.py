import ROOT

# this enables batch mode -> pyroot will not display any graphics
ROOT.gROOT.SetBatch(True)

# automatic sync with cernbox, ...
import Analysis.Tools.syncer as syncer
from RootTools.core.standard import *
import os
from copy import deepcopy
from DeepLepton.Tools.user import plot_directory
# import uproot
import argparse
import sys
import numpy as np
import array


argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',
                action='store',
                default='INFO',
                nargs='?',
                choices=['CRITICAL',
                        'ERROR',
                        'WARNING',
                        'INFO',
                        'DEBUG',
                        'TRACE',
                        'NOTSET'],
                help="Log level for logging")

argParser.add_argument('--small',
                action='store_true',
                help="Run the file on a small sample (for test purpose), bool flag set to     True if used" )
args = argParser.parse_args()

#
# Logger
#
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)


logger.info("program started")
# TODO: take the paths from plot_directory
scratch_directory = "/scratch-cbe/users/benjamin.wilhelmy/DeepLepton/"
path_truth = "/eos/vbc/user/benjamin.wilhelmy/DeepLepton/v1/step2/2016/muo/pt_3.5_-1/DYvsQCD/"
path_pred = os.path.join(scratch_directory, "trained/DYvsQCD_2016_3/training_20_epoches/prediction/")
outfiles_path = os.path.join(path_pred, "outfiles.txt")



variables = ["prob_isPrompt/F", "lep_isPromptId_Training/I", "lep_pt/F", "lep_eta/F"]

# read outfiles
logger.info('Getting filenames')
files_truth = []
files_pred  = []


# read in the the root file names
for f in open(outfiles_path, "r"):
    if ".root" in f:
        if f.endswith("\n"):
            ff = f[:-1]
        else:
            ff = f
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
                0,5,7.5,10,12.5,15,17.5,20,25,30,35,40,45,50,60,75,100], dtype = float)
                #125,150,175,200,250,300,400,500,
                #600,2000],dtype=float)
#np.geomspace(3.5, 250, 50) #[3.5, 4, 5, 6, 7, 8, 10, 20, 40, 50, 100, 200, 1000]
eta_bins = np.array(
            [-2.5,-2.,-1.5,-1.,-0.5,0.5,1,1.5,2.,2.5],
            dtype=float
            )

# pt_truth  = [[] for i in range(len(pt_bins))]
# eta_truth = [[] for i in range(len(eta_bins))]
# 
# pt_pred   = [[] for i in range(len(pt_bins))]
# eta_pred  = [[] for i in range(len(eta_bins))]

len_classifier_pt = len(pt_bins)-1
len_classifier_eta = len(eta_bins)-1

TP_pt = np.zeros((len_classifier_pt, 2), dtype = float)
# example TP_pt[i,:] = [nr of prompt identified leps given the lep was really prompt,
#                      nr of prompt leps in reality]
# then the ratio of these two entries is the TP rate for the specified pt range

TP_eta = np.zeros(len_classifier_eta, dtype = float)

FN_pt = np.zeros(len_classifier_pt, dtype = float)
# Here we only have one component since the other one is
# already stored in TP_pt[i,1] -> no need to store it twice

FN_eta = np.zeros(len_classifier_eta, dtype = float)

TN_pt = np.zeros((len_classifier_pt, 2), dtype = float)
TN_eta = np.zeros(len_classifier_eta, dtype = float)

FP_pt = np.zeros(len_classifier_pt, dtype = float)
FP_eta = np.zeros(len_classifier_eta, dtype = float)
# print(files_truth)
# print(files_pred)

# set threshold
threshold = 0.5

for i in range(len(files_truth)):
    logger.info("Reading Sample %i of %i"%(i+1, len(files_truth)))
    
    SampleTruth = Sample.fromFiles("truth", files_truth[i], treeName='tree')
    SamplePred  = Sample.fromFiles("pred", files_pred[i], treeName='tree')
    Sample = deepcopy(SampleTruth)
    Sample.addFriend(SamplePred, treeName='tree')
    
    reader = Sample.treeReader(variables=variables)
    reader.start()
    stop = False
    while reader.run():
        r = reader.event
        if stop:
            break
        for i in range(len(pt_bins)-1):
            if r.lep_pt < pt_bins[i+1] and pt_bins[i] < r.lep_pt:
                    # r.lep_pt                      type is float
                    # r.lep_isPromptId_Training     type is int (0 or 1)
                    # r.prob_isPrompt               type is float
                    # print("This was the first event")
                        # stop = True
                if r.lep_isPromptId_Training:
                    TP_pt[i, 1] += 1. 
                    if r.prob_isPrompt >= threshold:
                        TP_pt[i, 0] += 1. 
                    else:
                        FN_pt[i] += 1.
                        
                else:
                    TN_pt[i, 1] += 1.
                    if r.prob_isPrompt < threshold:
                        TN_pt[i, 0] += 1. 
                    else:
                        FP_pt[i] += 1.

        # TODO the same for eta


# print(TP_pt)
# print(TN_pt)
# print(FP_pt)
# print(FN_pt)

# calculate sensitivity
sensitivity_pt = (TP_pt[:, 0])/(TP_pt[:, 0]+FN_pt)

# caluclate specificity
specificity_pt = (TN_pt[:, 0])/(TN_pt[:, 0]+FP_pt)

# calculate accuracy
accuracy_pt = (TP_pt[:, 0]+TN_pt[:, 0])/(TP_pt[:, 0]+TN_pt[:, 0]+FP_pt+FN_pt)

# calculate efficiency
efficiency_pt = (sensitivity_pt+specificity_pt+accuracy_pt)/3

# print((TP_pt[:, 0] + FN_pt)/(TN_pt[:, 0] + FP_pt))


# print(TP_pt[:, 0] + FN_pt)
# print("This was true prompt")
# print(TN_pt[:, 0] + FP_pt)
# print(sensitivity_pt)
# print(specificity_pt)
# print(accuracy_pt)
# print(efficiency_pt)

# TODO shif the pt_bin values to (pt_bins[i+1]-pt_bins)[i])/2

gr1 = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[1:]), array.array("d", efficiency_pt))
gr2 = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[1:]), array.array("d", sensitivity_pt))
gr3 = ROOT.TGraph(len_classifier_pt, array.array("d", pt_bins[1:]), array.array("d", specificity_pt))
gr4 = ROOT.TGraph(len_classifier_pt, array.array("d", pt_bins[1:]), array.array("d", accuracy_pt))

gr1.SetLineColorAlpha(ROOT.kBlue, 1)
gr2.SetLineColorAlpha(ROOT.kRed, 1)
gr3.SetLineColorAlpha(3, 1) #green
gr4.SetLineColorAlpha(5, 1) #yellow

gr1.SetMarkerStyle(34)
gr2.SetMarkerStyle(34)
gr3.SetMarkerStyle(34)
gr4.SetMarkerStyle(34)


c1 = ROOT.TCanvas("c1", "L", 200,100,1000,1000)

c1.SetGrid()

gr1.SetTitle("Efficiency")
gr2.SetTitle("Sensitivity")
gr3.SetTitle("Specificity")
gr4.SetTitle("Accuracy")

mg = ROOT.TMultiGraph()

mg.Add(gr1)
mg.Add(gr2)
mg.Add(gr3)
mg.Add(gr4)

mg.SetTitle("Binary Classification Tests")

mg.Draw("APL") # set everything before Draw, exept axis stuff

mg.GetXaxis().SetTitle("lepton pt")
mg.GetYaxis().SetTitle("efficiency")

mg.GetYaxis().SetLimits(0,1)

c1.BuildLegend(0.7,0.4, 1, 0.6)
c1.Print(os.path.join(plot_directory, 'Efficiency/test_pt_small.png'))

logger.info("Succesfully plotted")







































# eta
#     eta_signal_eff , eta_background_eff = get_efficiencies(eta_pred, eta_truth, eta_bins, threshhold, background=False)
# 
#     gr1 = ROOT.TGraph(len(eta_bins)-1, array.array("d", eta_bins[:-1]), array.array("d", eta_signal_eff))
#     gr2 = ROOT.TGraph(len(eta_bins)-1, array.array("d", eta_bins[:-1]), array.array("d", eta_background_eff))
# 
#     gr1.SetLineColorAlpha(ROOT.kBlue, 1)
#     gr2.SetLineColorAlpha(ROOT.kRed, 1)
# 
#     gr1.SetMarkerStyle(34)
#     gr2.SetMarkerStyle(34)
# 
#     c1 = ROOT.TCanvas("c1", "L", 200,100,1000,1000)
# 
#     c1.SetGrid()
# 
#     gr1.SetTitle("Signal Efficiency")
#     gr2.SetTitle("Background Efficiency")
# 
#     mg = ROOT.TMultiGraph()
# 
#     mg.Add(gr1)
#     mg.Add(gr2)
# 
#     mg.SetTitle("Signal and Background Efficiency")
# 
#     mg.Draw("APL") # set everything before Draw, exept axis stuff
# 
#     mg.GetXaxis().SetTitle("lepton eta")
#     mg.GetYaxis().SetTitle("efficiency")
# 
#     mg.GetYaxis().SetLimits(0,1)
# 
#     c1.BuildLegend(0.7,0.4, 1, 0.6)
#     c1.Print(os.path.join(plot_directory, 'Efficiency/eta_flat_background_{}.png'.format(str(threshhold))))
# 
