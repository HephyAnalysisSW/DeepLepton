import ROOT
ROOT.gROOT.SetBatch(True)
import Analysis.Tools.syncer as syncer
from RootTools.core.standard import *
import os
from copy import deepcopy
from DeepLepton.Tools.user import plot_directory
import uproot
from sklearn.metrics import roc_curve, auc
import numpy as np
import argparse
import array
from copy import deepcopy

argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--outfilespath',
                       action='store', 
                       required=True,
                       type=str,
                       help="Path of outfiles.txt generated by prediction")

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
                       help="Run the file on a small sample (for test purpose)\
                           , bool flag set to     True if used" )
                           
argParser.add_argument('--ncat',
                       action='store',
                       type=int,
                       required=True,
                       help="Training on how many lepton classes? (4 or 5)")

argParser.add_argument('--special_output_path',
                        action='store',
                        default="",
                        help="path for output if one doesnt want the deault one" )
args = argParser.parse_args()

#
# Logger
#
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

logger.info("Starting roc.py")
# take this vars from parser -> make roc.sh
# path_truth = "/eos/vbc/user/maximilian.moser/DeepLepton/v2/step2/2016/muo/pt_3.5_-1/DYvsQCD/"
outfiles_path = args.outfilespath
# path_pred = "/scratch-cbe/users/maximilian.moser/DeepLepton/Train/training_test2/"
path_pred = os.path.dirname(outfiles_path)

n_classes = args.ncat
if n_classes == 4:
    # only one susy class
    logger.info("please check the type of the TLeaf s")
    truth_vars = ["lep_isFromSUSYandHF_Training/D"]
    pred_vars = ["prob_lep_isFromSUSYandHF/D"]
elif n_classes == 5:
    raise(NotImplemented())
    truth_vars = ["lep_isFromSUSY_Training/F", "lep_isFromSUSYHF_Training/F"]
    pred_vars = ["prob_isFromSUSY/F", "prob_isFromSUSYHF/F",]
else:
    raise NotImplemented("this case for ncat is not implemented")

variables = truth_vars + pred_vars

def wasSignal(event, truth_vars):
    for category in truth_vars:
        if getattr(event, category.split('/')[0]) == 1:
            return 1
    return 0

def prob_wasSignal(event, pred_vars):
    probability = 0
    for category in pred_vars:
        probability += getattr(event, category.split('/')[0])
    return probability


# read outfiles
logger.info('Getting filenames')
files_pred  = []
# print("outfiles path is {}".format(outfiles_path))
# print("path pred is {}".format(path_pred))
for f in open(outfiles_path, "r"):
    if ".root" in f:
        if f.endswith("\n"):
            ff = f[:-1]
        # truth_file   = ff[5:]
        # print("ff is {}".format(ff))
        f_pred  = os.path.join(path_pred, ff)
        # f_truth = os.path.join(path_truth, truth_file)
        files_pred.append(f_pred)
        # files_truth.append(f_truth)
        if args.small:
            break
# print("my predict files are {}".format(files_pred))
if len(files_pred) == 0:
    raise "No files found!"

pred    = []
truth   = []

for i in range(len(files_pred)):
    logger.info("Reading Sample %i of %i"%(i+1, len(files_pred)))
    logger.debug("Reading File {}".format(files_pred[i]))    
# =============================================================================
#     SampleTruth = Sample.fromFiles("truth", files_truth[i], treeName='tree')
#     SamplePred  = Sample.fromFiles("pred", files_pred[i], treeName='tree')
#     Sample = deepcopy(SampleTruth)
#     Sample.addFriend(SamplePred, treeName='tree')
# =============================================================================
    Sample = Sample.fromFiles("pred", files_pred[i], treeName='tree')

    reader = Sample.treeReader(variables=variables)
    reader.start()

    while reader.run():
        r = reader.event
        pred.append(prob_wasSignal(r, pred_vars))
        truth.append(wasSignal(r, truth_vars))

assert(truth != [])

logger.info("Making roc curve...")
# int(tprint("truth, pred:")
# int(tprint(truth)
# int(tprint(pred)

# a function to remove nans from pred
def rm_nans(truth, pred):
    '''remove the indices where pred is nan'''
    nans = np.isnan(np.array(pred))
    truth = np.array(truth)
    pred = np.array(pred)
    truth = truth[np.logical_not(nans)]
    pred = pred[np.logical_not(nans)]
    truth = list(truth)
    pred = list(pred)

# rm_nans(truth, pred)
# logger.info("removed nans")


fpr, tpr, thresholds = roc_curve(truth, pred, drop_intermediate=False)
# set a fpr point
workpoints = [0.01, 0.05, 0.1]


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx
work_index = [find_nearest(fpr, wp) for wp in workpoints]
work_tpr = [tpr[i] for i in work_index]
work_thresholds = [thresholds[i] for i in work_index]

# heuristics...
best_ratio = tpr/(fpr+0.01)
best_ratio = best_ratio[np.logical_not(np.isinf(best_ratio))]
best_index = best_ratio.argmax()
print("best ratio value is {}".format(best_ratio[best_index]))
print("with threshold = {}".format(thresholds[best_index]))
workpoints.append(fpr[best_index])
work_tpr.append(tpr[best_index])
work_thresholds.append(thresholds[best_index])

# add the 0.5 threshold:
tmp_i = find_nearest(thresholds, 0.5)
workpoints.append(fpr[tmp_i])
work_tpr.append(tpr[tmp_i])
work_thresholds.append(thresholds[tmp_i])


print("fpr points = {}".format(workpoints))
print("tpr points = {}".format(work_tpr))
print("thresh points = {}".format(work_thresholds))


logger.info("plotting...")
c1 = ROOT.TCanvas("c1", "L", 200,100,1000,1000)
c1.SetTitle("ROC-Curve")

gr = ROOT.TGraph(len(fpr), array.array('d', fpr), array.array('d', tpr))
gr.GetXaxis().SetTitle("False Positive Rate")
gr.GetYaxis().SetTitle("True Positive Rate")
#gr.SetLineWidth(2)
gr.GetXaxis().SetLimits(0,1)
gr.GetYaxis().SetLimits(0,1)
gr.SetTitle("ROC-Curve")
gr.SetMarkerStyle(1)

mg = ROOT.TMultiGraph()
mg.SetTitle("ROC-Curve; False Positive Rate; True Positive Rate")
mg.Add(gr)

# plot workpoints
colors = list(range(1,9))
colors.remove(2)
colors.remove(5)
#colors.extend(range(3,10))
for i in range(len(workpoints)):
    gr_point = ROOT.TGraph(1, array.array('d', [workpoints[i]]), array.array('d', [work_tpr[i]]))
    gr_point.SetMarkerStyle(3)
    gr_point.SetMarkerSize(4)
    gr_point.SetMarkerColor(colors[i])
    gr_point.SetTitle("Threshold = {:0.2e}".format(work_thresholds[i]))
    mg.Add(gr_point)

mg.Draw("ALP")
c1.BuildLegend()
if args.special_output_path:
    plot_sub_dir = args.special_output_path
else:
    plot_sub_dir = path_pred.split('/')[-2]
c1.Print(os.path.join(plot_directory, "Training_v4", plot_sub_dir ,'roc_curve.png'))

logger.info("saving workpoints")
np.save("workpoints/thresholds_{}.npy".format(plot_sub_dir), np.array(work_thresholds))
np.save("workpoints/tpr points_{}.npy".format(plot_sub_dir), np.array(work_tpr))
np.save("workpoints/fpr points_{}.npy".format(plot_sub_dir), np.array(workpoints))

