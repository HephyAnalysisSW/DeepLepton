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
                help="Run the file on a small sample (for test purpose), bool flag set to True if used" )
args = argParser.parse_args()

#
# Logger
#
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)


logger.info("program started")
# path_pred = "/scratch-cbe/users/benjamin.wilhelmy/DeepLepton/trained/DYvsQCD_fromMax/training_20/prediction_max/"
# path_truth = "/scratch-cbe/users/maximilian.moser/DeepLepton/traindata/DYvsQCD_2016/"
# outfiles_path = "/scratch-cbe/users/benjamin.wilhelmy/DeepLepton/trained/DYvsQCD_fromMax/training_20/prediction_max/outfiles.txt"
# scratch_directory = "/scratch-cbe/users/benjamin.wilhelmy/DeepLepton/"
# path_truth = "/eos/vbc/user/benjamin.wilhelmy/DeepLepton/v1/step2/2016/muo/pt_3.5_-1/DYvsQCD/"
# path_pred = os.path.join(scratch_directory, "trained/DYvsQCD_2016_3/training_40_epoches_usw/prediction/")
# outfiles_path = os.path.join(path_pred, "benjamins_outfiles.txt")

path_truth = "/scratch-cbe/users/maximilian.moser/DeepLepton/traindata/DYvsQCD_2016/"
outfiles_path = "/scratch-cbe/users/maximilian.moser/DeepLepton/Train_DYvsQCD_notprompt/training_10/outfiles.txt"
path_pred = "/scratch-cbe/users/maximilian.moser/DeepLepton/Train_DYvsQCD_notprompt/training_10/"





# set sensible output file name s.t. one knows from which model the plot came
output_file_name = "Consistency_check_plot_max_model_"
if args.small:
    output_file_name += "small_"

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


pt_bins = np.array([0,5,7.5,10,12.5,15,17.5,20,25,30,35,40,45,50,60,75,100, 125],
                    dtype = float)
pt_bins = np.array([5, 7.5, 10, 12.5, 15, 17.5, 20, 25, 30, 35, 40, 45, 50, 60, 75, 100,
                                125, 150, 175, 200, 250, 300, 400, 500, 600, 2000], dtype=float)
# actually dxy bins...
eta_bins = np.linspace(start=-5, stop=5, num=10, endpoint=True, dtype=float)

# eta_bins = np.array(
#             [-2.5,-2.,-1.5,-1.,-0.5,0.5,1,1.5,2.,2.5],
#             dtype=float
#             )

len_classifier_pt = len(pt_bins)-1
len_classifier_eta = len(eta_bins)-1

TP_pt = np.zeros((len_classifier_pt, 2), dtype = float)
# example TP_pt[i,:] = [nr of prompt identified leps given the lep was really prompt,
#                      nr of prompt leps in reality]
# then the ratio of these two entries is the TP rate for the specified pt range

TP_eta = np.zeros((len_classifier_eta, 2), dtype = float)

FN_pt = np.zeros(len_classifier_pt, dtype = float)
# Here we only have one component since the other one is
# already stored in TP_pt[i,1] -> no need to store it twice

FN_eta = np.zeros(len_classifier_eta, dtype = float)

TN_pt = np.zeros((len_classifier_pt, 2), dtype = float)
TN_eta = np.zeros((len_classifier_eta, 2), dtype = float)

FP_pt = np.zeros(len_classifier_pt, dtype = float)
FP_eta = np.zeros(len_classifier_eta, dtype = float)

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
    while reader.run():
        r = reader.event
        for i in range(len_classifier_pt):
            if r.lep_pt < pt_bins[i+1] and pt_bins[i] < r.lep_pt:
                    # r.lep_pt                      type is float
                    # r.lep_isPromptId_Training     type is int (0 or 1)
                    # r.prob_isPrompt               type is float
                    # print("This was the first event")
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

        # Now the same thing for eta
        for i in range(len_classifier_eta):
            if r.lep_eta < eta_bins[i+1] and eta_bins[i] < r.lep_eta:
                if r.lep_isPromptId_Training:
                    TP_eta[i, 1] += 1. 
                    if r.prob_isPrompt >= threshold:
                        TP_eta[i, 0] += 1. 
                    else:
                        FN_eta[i] += 1.
                        
                else:
                    TN_eta[i, 1] += 1.
                    if r.prob_isPrompt < threshold:
                        TN_eta[i, 0] += 1. 
                    else:
                        FP_eta[i] += 1.       


# calculate sensitivity = signal efficiency
sensitivity_pt = (TP_pt[:, 0])/(TP_pt[:, 0]+FN_pt)
sensitivity_eta = TP_eta[:, 0]/(TP_eta[:, 0]+FN_eta)

# caluclate specificity
# specificity_pt = (TN_pt[:, 0])/(TN_pt[:, 0]+FP_pt)
# specificity_eta = TN_eta[:, 0]/(TN_eta[:, 0]+FP_eta)

# calculate accuracy
# accuracy_pt = (TP_pt[:, 0]+TN_pt[:, 0])/(TP_pt[:, 0]+TN_pt[:, 0]+FP_pt+FN_pt)
# accuracy_eta = (TP_eta[:, 0]+TN_eta[:, 0])/(TP_eta[:, 0]+TN_eta[:, 0]+FP_eta+FN_eta)

# calculate efficiency
# efficiency_pt = (sensitivity_pt+specificity_pt+accuracy_pt)/3
# efficiency_eta = (sensitivity_eta+specificity_eta+accuracy_eta)/3

# calculate background eff
back_eff_pt = FP_pt / (TN_pt[:, 0] + FP_pt)
back_eff_eta = FP_eta / (TN_eta[:, 0] + FP_eta)

# shif the pt_bin values such that the point lies in the middle of the bin
plot_pt_bins = np.zeros(len_classifier_pt)
for i in range(len_classifier_pt):
    plot_pt_bins[i] = (pt_bins[i+1]+pt_bins[i])/2

# shif the eta_bin values such that the point lies in the middle of the bin
plot_eta_bins = np.zeros(len_classifier_eta)
for i in range(len_classifier_eta):
    plot_eta_bins[i] = (eta_bins[i+1]+eta_bins[i])/2

# The pt plot:
# gr1 = ROOT.TGraph(len_classifier_pt, array.array("d", plot_pt_bins), array.array("d", efficiency_pt))
gr2 = ROOT.TGraph(len_classifier_pt, array.array("d", plot_pt_bins), array.array("d", sensitivity_pt))
# gr3 = ROOT.TGraph(len_classifier_pt, array.array("d", plot_pt_bins), array.array("d", specificity_pt))
# gr4 = ROOT.TGraph(len_classifier_pt, array.array("d", plot_pt_bins), array.array("d", accuracy_pt))
gr5 = ROOT.TGraph(len_classifier_pt, array.array("d", plot_pt_bins), array.array("d", back_eff_pt))

# gr1.SetLineColorAlpha(ROOT.kBlue, 1)
gr2.SetLineColorAlpha(ROOT.kRed, 1)
# gr3.SetLineColorAlpha(3, 1) #green
# gr4.SetLineColorAlpha(5, 1) #yellow
gr5.SetLineColorAlpha(6, 1) #violet 

# gr1.SetMarkerStyle(34)
gr2.SetMarkerStyle(34)
# gr3.SetMarkerStyle(34)
# gr4.SetMarkerStyle(34)
gr5.SetMarkerStyle(34)


c1 = ROOT.TCanvas("c1", "L", 200,100,1000,1000)

c1.SetGrid()

# gr1.SetTitle("Efficiency")
gr2.SetTitle("Signal Efficiency")
# gr3.SetTitle("Specificity")
# gr4.SetTitle("Accuracy")
gr5.SetTitle("Background Efficiency")

mg = ROOT.TMultiGraph()

# mg.Add(gr1)
mg.Add(gr2)
# mg.Add(gr3)
# mg.Add(gr4)
mg.Add(gr5)

mg.SetTitle("Binary Classification Tests in p_t")

mg.Draw("APL") # set everything before Draw, exept axis stuff

mg.GetXaxis().SetTitle("lepton pt")
# mg.GetYaxis().SetTitle("efficiency")

mg.GetYaxis().SetLimits(0,1)

c1.BuildLegend(0.7,0.4, 1, 0.6)
c1.Print(os.path.join(plot_directory, 'Efficiency/'+output_file_name +'pt.png'))

logger.info("Succesfully plotted pt plot")

# The eta plot:

# gr1 = ROOT.TGraph(len_classifier_eta, array.array("d", plot_eta_bins), array.array("d", efficiency_eta))
gr2 = ROOT.TGraph(len_classifier_eta, array.array("d", plot_eta_bins), array.array("d", sensitivity_eta))
# gr3 = ROOT.TGraph(len_classifier_eta, array.array("d", plot_eta_bins), array.array("d", specificity_eta))
# gr4 = ROOT.TGraph(len_classifier_eta, array.array("d", plot_eta_bins), array.array("d", accuracy_eta))
gr5 = ROOT.TGraph(len_classifier_eta, array.array("d", plot_eta_bins), array.array("d", back_eff_eta))

# gr1.SetLineColorAlpha(ROOT.kBlue, 1)
gr2.SetLineColorAlpha(ROOT.kRed, 1)
# gr3.SetLineColorAlpha(3, 1) #green
# gr4.SetLineColorAlpha(5, 1) #yellow
gr5.SetLineColorAlpha(6, 1) #violet 

# gr1.SetMarkerStyle(34)
gr2.SetMarkerStyle(34)
# gr3.SetMarkerStyle(34)
# gr4.SetMarkerStyle(34)
gr5.SetMarkerStyle(34)


c1 = ROOT.TCanvas("c1", "L", 200,100,1000,1000)

c1.SetGrid()

# gr1.SetTitle("Efficiency")
gr2.SetTitle("Signal Efficiency")
# gr3.SetTitle("Specificity")
# gr4.SetTitle("Accuracy")
gr5.SetTitle("Background Efficiency")

mg = ROOT.TMultiGraph()

# mg.Add(gr1)
mg.Add(gr2)
# mg.Add(gr3)
# mg.Add(gr4)
mg.Add(gr5)

mg.SetTitle("$Binary \t Classification \\ Tests\quad in \\ \eta; lepton\\ \eta$")

mg.Draw("APL") # set everything before Draw, exept axis stuff

mg.GetYaxis().SetLimits(0,1)

c1.BuildLegend(0.7,0.4, 1, 0.6)
c1.Print(os.path.join(plot_directory, 'Efficiency/'+output_file_name+'eta.png'))

