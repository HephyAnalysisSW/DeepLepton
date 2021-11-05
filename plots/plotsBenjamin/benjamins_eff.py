import RootTools.core.logger as logger_rt
import DeepLepton.Tools.logger as logger
import array
import numpy as np
import sys
import argparse
from DeepLepton.Tools.user import plot_directory
from copy import deepcopy
import os
from RootTools.core.standard import *
import Analysis.Tools.syncer as syncer
# automatic sync with cernbox, ...
import ROOT

# this enables batch mode -> pyroot will not display any graphics
ROOT.gROOT.SetBatch(True)

# import uproot


argParser = argparse.ArgumentParser(description="Argument parser")
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
                           ,bool flag set to True if used")
                           
argParser.add_argument('--pathpred',
                       action='store',
                       required=True,
                       type=str,
                       help="Path to prediction root files")

# argParser.add_argument('--pathtruth',
#                        action='store',
#                        required=True,
#                        type=str,
#                        help="Path to Truth root files")

argParser.add_argument('--outfilespath',
                       action='store',
                       default="outfiles.txt",
                       type=str,
                       help="Path of the outfiles.txt generated by prediction.\
                           Default: join(pathpred, outfiles.txt)")

argParser.add_argument('--ncat',
                       action='store',
                       required=True,
                       type=int,
                       help="Training on how many lepton classes? (4 or 5)")

argParser.add_argument('--special_output_path',
                        action='store',
                        default="",
                        help="path for output if one doesnt want the deault one" )

args = argParser.parse_args()

#
# Logger
#
logger = logger.get_logger(args.logLevel, logFile=None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile=None)


logger.info("starting benjamins_eff.py")

path_pred = args.pathpred
if args.special_output_path:
    subdir = args.special_output_path
else:
    subdir = path_pred.split('/')[-2]

if args.outfilespath == "outfiles.txt":
    path_outfiles = os.path.join(path_pred, args.outfilespath)
else:
    path_outfiles = args.outfilespath


output_file_name ="Efficiency_plots_" 
# "first_real_training_on_unbalanced_data_no_removes_0.1_dropout_20epochs_prediction_model_epoch2_"

if args.small:
    output_file_name += "small_"

if args.ncat == 4:
    logger.info("check if the type in the prediction rootfile is D or F!")
    labels = ["lep_isPromptId_Training/D",
              "lep_isNonPromptId_Training/D",
              "lep_isFakeId_Training/D",
              "lep_isFromSUSYandHF_Training/D"]

    prob_labels = ["prob_isPrompt/D",
                   "prob_isNonPrompt/D",
                   "prob_isFake/D",
                   "prob_lep_isFromSUSYandHF/D"]

    # define what is signal the rest is background
    signal = {"Training":['lep_isFromSUSYandHF_Training'],
              "prob":['prob_lep_isFromSUSYandHF']}

elif args.ncat == 5:
    logger.info("check if TLeafes have type F or D !!!")
    raise(NotImplemented("correct type ??"))
    labels = ["lep_isPromptId_Training/F",
              "lep_isNonPromptId_Training/F",
              "lep_isFakeId_Training/F",
              "lep_isFromSUSY_Training/F",
              "lep_isFromSUSYHF_Training/F"]
    
    prob_labels = ["prob_isPrompt/F",
                   "prob_isNonPrompt/F",
                   "prob_isFake/F",
                   "prob_isFromSUSY/F",
                   "prob_isFromSUSYHF/F"]

    signal = {"Training":['lep_isFromSUSY_Training', 'lep_isFromSUSYHF_Training'],
              "prob":['prob_isFromSUSY', 'prob_isFromSUSYHF']}

else:
    raise NotImplemented("ncat in (4,5)")

x = "lep_pt"
y = "lep_dxy"

# for reading samples
variables = labels + prob_labels + [x+"/D", y+"/D"] # [x+"/F", y+"/F"]




# read outfiles
logger.info('Getting filenames')
# files_truth = []
files_pred = []


# read in the the root file names
for f in open(path_outfiles, "r"):
    if ".root" in f:
        if f.endswith("\n"):
            ff = f[:-1]
        else:
            ff = f
        # cuts off pred_
        truth_file = ff[5:]
        f_pred = os.path.join(path_pred, ff)
        # f_truth = os.path.join(path_truth, truth_file)
        files_pred.append(f_pred)
        # files_truth.append(f_truth)
        if args.small:
            break


filenames_pred = []
if files_pred == []:
    print("searched in: {}".format(path_outfiles))
    raise AssertionError("no root files found")
for fname in files_pred:
    filenames_pred.append(os.path.basename(fname))
logger.debug("In directory {} \n found files: {}".format(os.path.dirname(files_pred[0]), filenames_pred))
# x_bins = np.array([0,5,7.5,10,12.5,15,17.5,20,25,30,35,40,45,50,60,75,100, 125],
#                     dtype = float)

# we only have leps from susy and susyhf with lep_pt up to 60, not more...
# x_bins = np.array([5, 7.5, 10, 12.5, 15, 17.5, 20, 25, 30, 35, 40, 45, 50, 60],
#                   dtype=float)

# pt bins
x_bins = np.linspace(start=3.5, stop=40, num=15, endpoint=True, dtype=float)
# actually dxy bins...
y_bins = np.linspace(start=-5, stop=5, num=15, endpoint=True, dtype=float)

# y_bins = np.array(
#             [-2.5,-2.,-1.5,-1.,-0.5,0.5,1,1.5,2.,2.5],
#             dtype=float
#             )



# complicated enough for a class
THRESHOLD = np.load("workpoints/thresholds_{}.npy".format(subdir))
# THRESHOLD = np.append(THRESHOLD, [0.5])
print(THRESHOLD)
n_thres = len(THRESHOLD)
TP = []
TN = []
FP = []
FN = []
h_tp = []
h_tn = []
h_fp = []
h_fn = []
for i in range(n_thres):
    TP.append({"x":[], "y":[]})
    TN.append({"x":[], "y":[]})
    FP.append({"x":[], "y":[]})
    FN.append({"x":[], "y":[]})

    h_tp.append({"x":np.zeros(len(x_bins)-1), "y":np.zeros(len(y_bins)-1)})
    h_tn.append({"x":np.zeros(len(x_bins)-1), "y":np.zeros(len(y_bins)-1)})
    h_fp.append({"x":np.zeros(len(x_bins)-1), "y":np.zeros(len(y_bins)-1)})
    h_fn.append({"x":np.zeros(len(x_bins)-1), "y":np.zeros(len(y_bins)-1)})

# TP = {"x":[], "y":[]}
# TN = {"x":[], "y":[]}
# FP = {"x":[], "y":[]}
# FN = {"x":[], "y":[]}


# max length of list of tuples before making histogram to save memory
n_max = 1e6

# initialize histograms with zeros
# h_tp = {"x":np.zeros(len(x_bins)-1), "y":np.zeros(len(y_bins)-1)}
# h_tn = {"x":np.zeros(len(x_bins)-1), "y":np.zeros(len(y_bins)-1)}
# h_fp = {"x":np.zeros(len(x_bins)-1), "y":np.zeros(len(y_bins)-1)}
# h_fn = {"x":np.zeros(len(x_bins)-1), "y":np.zeros(len(y_bins)-1)}

# needed for checking the length of TP, TN, ... and making histos
categories = [(TP, h_tp), (TN, h_tn), (FP, h_fp), (FN, h_fn)]

# for category in categories
def make_histo(category):
    # category[1] is h_..
    n = len(category[0]) #len(TP)
    logger.debug("histox before {}".format(category[1][0]["x"]))
    for i in range(n):
        category[1][i]["x"] += np.histogram(category[0][i]["x"], x_bins)[0]
        category[1][i]["y"] += np.histogram(category[0][i]["y"], y_bins)[0]
        category[0][i]["x"] = []
        category[0][i]["y"] = []
    logger.debug("histo after {}".format(category[1][0]["x"]))
    return category

# for calculating efficiency and background eff
def divide_histo(hist_a, hist_b):
    assert(len(hist_a) == len(hist_b))
    tmp = np.zeros(len(hist_a))
    for i in range(len(hist_a)):
        if hist_b[i]:
            tmp[i] = hist_a[i]/hist_b[i]
        else:
            logger.info("A bin was empty -> consider other binning")
            tmp[i] = -1
    return tmp


# checks if the event is signal(True) or background(False)
def event_is_signal(event, signal):
    global labels
    signal_labels = signal["Training"]
    for signal_label in signal["Training"]:
        # print("debuging event is signal: signal_label={}, attr={}".format(signal_label, getattr(event, signal_label)))
        if getattr(event, signal_label) == 1:
            #logger.debug("event is signal: {}, {}".format(getattr(event, labels[3].split('/')[0]),
            #                                                getattr(event, labels[4].split('/')[0])))
            return True
    #logger.debug("event is not signal: {}, {}, {}".format(getattr(event, labels[0].split('/')[0]),
    #                                                        getattr(event, labels[1].split('/')[0]), 
    #                                                        getattr(event, labels[2].split('/')[0])))
    return False

def event_classified_signal(event, signal, THRESHOLD):
    signal_prob = 0
    for prediction_label in signal["prob"]:
        signal_prob += getattr(event, prediction_label)
        # print("event classified signal = {}".format(getattr(event, prediction_label)))
    # logger.debug("event classifying: signal prob={} \n prompt={}, nonpromt={}, fake={}, susy={}, susyhf={}".format(\
    #             signal_prob,
    #             getattr(event, prob_labels[0].split('/')[0]),
    #             getattr(event, prob_labels[1].split('/')[0]),
    #             getattr(event, prob_labels[2].split('/')[0]),
    #             getattr(event, prob_labels[3].split('/')[0]),
    #             getattr(event, prob_labels[4].split('/')[0])))
    if signal_prob >= THRESHOLD:

        return True
    else: 
        return False

# should later work with threshold beeing array_like
for i in range(len(files_pred)):
    logger.info("Reading Sample %i of %i" % (i+1, len(files_pred)))
    logger.debug("Filename {}".format(os.path.basename(files_pred[i])))

    # SampleTruth = Sample.fromFiles("truth", files_truth[i], treeName='tree')
    # SamplePred = Sample.fromFiles("pred", files_pred[i], treeName='tree')
    # Sample = deepcopy(SampleTruth)
    # Sample.addFriend(SamplePred, treeName='tree')
    Sample = Sample.fromFiles("pred", files_pred[i], treeName='tree')

    reader = Sample.treeReader(variables=variables)
    reader.start()
    while reader.run():
        r = reader.event
        if event_is_signal(r, signal):
            for i, threshold in enumerate(THRESHOLD):
                if event_classified_signal(r, signal, threshold):
                    TP[i]["x"].append(getattr(r, x))
                    TP[i]["y"].append(getattr(r, y))
                else:
                    FN[i]["x"].append(getattr(r, x))
                    FN[i]["y"].append(getattr(r, y))
        else:
            for i, threshold in enumerate(THRESHOLD):
                if event_classified_signal(r, signal, threshold):
                    FP[i]["x"].append(getattr(r, x))
                    FP[i]["y"].append(getattr(r, y))
                else:
                    TN[i]["x"].append(getattr(r, x))
                    TN[i]["y"].append(getattr(r, y))
        
        for category in categories:
            if len(category[0][0]["x"]) >= n_max:
                logger.info("make a temporal histogram to save mem")
                category=make_histo(category)
                #category[0]["x"] = []
                #category[0]["y"] = []
        
    # take the last events in histogram
    for category in categories:
        category=make_histo(category)
        # category[0]["x"] = []
        # category[0]["y"] = []


logger.info("done reading, calc eff and back_eff")
# calculate sensitivity = signal efficiency
sensitivity_x = []
sensitivity_y = []
back_eff_x = []
back_eff_y = []
for i in range(n_thres):
    sensitivity_x.append(divide_histo(h_tp[i]["x"], h_tp[i]["x"] + h_fn[i]["x"]))
    sensitivity_y.append(divide_histo(h_tp[i]["y"], h_tp[i]["y"] + h_fn[i]["y"]))
    back_eff_x.append(divide_histo(h_fp[i]["x"], h_tn[i]["x"] + h_fp[i]["x"]))
    back_eff_y.append(divide_histo(h_fp[i]["y"], h_tn[i]["y"] + h_fp[i]["y"]))

# sensitivity_x = divide_histo(h_tp["x"], h_tp["x"] + h_fn["x"])
# sensitivity_y = divide_histo(h_tp["y"], h_tp["y"] + h_fn["y"])
# logger.info("eff x {}".format(sensitivity_x))
# logger.info("eff y {}".format(sensitivity_y))
# 
# # calculate background eff
# back_eff_x = divide_histo(h_fp["x"], h_tn["x"] + h_fp["x"])
# back_eff_y = divide_histo(h_fp["y"], h_tn["y"] + h_fp["y"])
# logger.info("back_eff x {}".format(back_eff_x))
# logger.info("back_eff y {}".format(back_eff_y))

# with open(os.path.join(plot_directory, 'Training', subdir, "raw_back_and_eff.txt"), "w") as f:
#     f.write("Eff x, y: \n")
#     f.write("{}".format(sensitivity_x))
#     f.write('\n')
#     f.write("{}".format(sensitivity_y))
#     f.write('\n')
#     f.write("Back_eff x, y: \n")
#     f.write("{}".format(back_eff_x))
#     f.write('\n')
#     f.write("{}".format(back_eff_y))

# The pt plot:
# gr1 = ROOT.TGraph(len_classifier_pt, array.array("d", plot_x_bins), array.array("d", efficiency_pt))
def plot(bins, sensitivity, back_eff, feature_name, threshold, color): #, fillcolor):
    '''feature_name is either x or y as string'''
    # make the dot in the middle of the bin ...
    shift_bins = True
    mybins = np.zeros(len(bins)-1)
    if shift_bins == True:
        for i in range(len(bins)-1):
            mybins[i] = (bins[i]+bins[i+1])/2.
    else:
        mybins = deepcopy(bins)[:-1] 

    gr1 = ROOT.TGraph(len(bins)-1,
                        array.array("d", mybins),
                        array.array("d", sensitivity))

    gr2 = ROOT.TGraph(len(bins)-1,
                        array.array("d", mybins),
                        array.array("d", back_eff))
    
    # signal green
    gr1.SetLineColor(color)
    gr1.SetMarkerStyle(34)
    gr1.SetTitle("Signal Efficiency")
    gr1.SetMaximum(1)
    gr1.SetMinimum(0)
    gr1.SetFillColor(color)
    # back red
    gr2.SetLineColor(2)
    gr2.SetFillColor(2)
    gr2.SetMarkerStyle(34)
    gr2.SetMaximum(1)
    gr2.SetMinimum(0)
    gr2.SetTitle("Background Efficiency")

    # setup canvas
    c1 = ROOT.TCanvas("c1", "L", 200, 100, 1000, 1000)
    c1.SetGrid()

    mg = ROOT.TMultiGraph()
    mg.Add(gr1)
    mg.Add(gr2)
    mg.SetTitle("Binary Classification Tests in {}".format(feature_name))
    mg.Draw("APL")  # set everything before Draw, exept axis stuff
    mg.GetXaxis().SetTitle(feature_name)
    # mg.GetYaxis().SetLimits(0, 1)
    mg.SetMinimum(0)
    mg.SetMaximum(1)
    c1.BuildLegend(0.7, 0.4, 1, 0.6)
    c1.Print(os.path.join(plot_directory,
                          'Training_v6',
                          subdir,
                          output_file_name + "{}_{:0.2e}.png".format(feature_name, threshold)))
    
    logger.info("Succesfully plotted {} plot".format(feature_name))

logger.info("start plotting")
# make the plots
#fillcolors = [30, 38, 42, 40, ROOT.kCyan-2]
colors = list(range(1,9))
colors.remove(2)
colors.remove(5)
for i in range(n_thres):
    print(colors[i])
    plot(x_bins, sensitivity_x[i], back_eff_x[i], x, THRESHOLD[i], colors[i]) #, fillcolors[i])
    plot(y_bins, sensitivity_y[i], back_eff_y[i], y, THRESHOLD[i], colors[i]) #, fillcolors[i])
    
