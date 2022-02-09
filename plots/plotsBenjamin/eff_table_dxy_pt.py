import ROOT
ROOT.gROOT.SetBatch(True)
# import Analysis.Tools.syncer as syncer
from RootTools.core.standard import *
import os
from copy import deepcopy
from DeepLepton.Tools.user import plot_directory
import uproot
from sklearn.metrics import roc_curve, auc
import numpy as np
import argparse
import array
import sys


argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--outfilespath',
                       action='store', 
                       #required=True,
                       type=str,
                       help="Output path, without the Tools.user plot_directory!")

argParser.add_argument('--input_dir',
                        action='store',
                        required=True,
                        type=str,
                        help="Path to predicted root files (onsample)")

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
                           
# argParser.add_argument('--ncat',
#                        action='store',
#                        type=int,
#                        required=True,
#                        help="Training on how many lepton classes? (4 or 5)")

# argParser.add_argument('--special_output_path',
#                         action='store',
#                         default="",
#                         help="path for output if one doesnt want the deault one" )
args = argParser.parse_args()

#
# Logger
#
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def rm_nans_from_lists(truth, pred, cut):
    '''remove the indices where pred is nan'''
    nans = np.isnan(np.array(pred))
    if nans.any() == True:
        logger.info("ATTENTION FOUND NANS IN PREDICTION...REMOVING THEM, BE CAREFUL")
    truth = np.array(truth)
    truth = truth[np.logical_not(nans)]
    cut   = np.array(cut)
    cut   = cut[np.logical_not(nans)]
    pred = np.array(pred)
    pred = pred[np.logical_not(nans)]
    return [list(truth), list(pred), list(cut)]

class Bin(object):
    def __init__(self, pt_l, pt_u, dxy_l, dxy_u):
        '''giving upper and lower bin edges'''
        self.bin_pt_l = pt_l
        self.bin_pt_u = pt_u
        self.bin_dxy_l = dxy_l
        self.bin_dxy_u = dxy_u
        self.s = []
        self.p = []
        self.c = []
    def add_value(self, was_signal, prob_signal, cut_signal):
        self.s.append(was_signal)
        self.p.append(prob_signal)
        self.c.append(cut_signal)
    def get_signal(self):
        return self.s
    def get_prob(self):
        return self.p
    def get_cut(self):
        return self.c
    def __mk_roc(self):
        self.s, self.p, self.c = rm_nans_from_lists(self.s, self.p, self.c)
        if len(self.s) == 0:
            logger.info("{} was empty".format(self))
            self.empty = True
            self.fpr_dnn = None
            self.fpr_cut = None
            self.threshold = None
            self.threshold_cut = None
            self.tpr_dnn = None
            self.tpr_cut = None
        elif self.s.count(1)<=2:
            logger.info("The following bin has no/one/two signal muons: {}\n".format(self))
            try:
                self.fpr_dnn, self.tpr_dnn, self.threshold = roc_curve(self.s, self.p)
                self.fpr_cut, self.tpr_cut, self.threshold_cut = roc_curve(self.s, self.c, drop_intermediate=True)
                self.empty = False
            except Exception as e:
                print(e)
                logger.info("Exception bec. no signal muons in bin setting all no None...")
                self.fpr_dnn = None
                self.fpr_cut = None
                self.threshold = None
                self.threshold_cut = None
                self.tpr_dnn = None
                self.tpr_cut = None
                self.empty = True

        else:
            self.fpr_dnn, self.tpr_dnn, self.threshold = roc_curve(self.s, self.p)
            self.fpr_cut, self.tpr_cut, self.threshold_cut = roc_curve(self.s, self.c, drop_intermediate=True)
            self.empty = False
            # except Exception as e:
            #     print(e)
            #     logger.info("signal: {}".format(self.s))
            #     logger.info("prob:   {}".format(self.p))
    def get_eff(self):
        self.__mk_roc()
        if self.empty:
            self.t_dnn = None
            self.s_eff_dnn = self.tpr_dnn
            self.b_eff_dnn = self.fpr_dnn

            self.s_eff_cut = self.tpr_cut
            self.b_eff_cut = self.fpr_cut
        else:
            dnn_i = find_nearest(self.tpr_dnn, 0.9)
            self.t_dnn = self.threshold[dnn_i]
            self.s_eff_dnn = self.tpr_dnn[dnn_i]
            self.b_eff_dnn = self.fpr_dnn[dnn_i]

            self.s_eff_cut = self.tpr_cut[1]
            self.b_eff_cut = self.fpr_cut[1]
        return {"s_eff_dnn": self.s_eff_dnn, "b_eff_dnn":self.b_eff_dnn, "dnn_threshold":self.t_dnn,
                "s_eff_cut": self.s_eff_cut, "b_eff_cut":self.b_eff_cut}
    def get_roc_dnn(self):
        return [self.fpr_dnn, self.tpr_dnn, self.threshold]
    def get_roc_cut(self):
        return [self.fpr_cut, self.tpr_cut, self.threshold_cut]
    def print_me(self):
        string1 = "pt=[{} -- {}], dxy=[{} -- {}]".format(self.bin_pt_l, self.bin_pt_u, self.bin_dxy_l, self.bin_dxy_u)
        try:
            string2 = "E_s: {:.3f}, ({:.3f})".format(self.s_eff_dnn, self.s_eff_cut)
            string3 = "E_b: {:.3f}, ({:.3f})".format(self.b_eff_dnn, self.b_eff_cut)
        except:
            try:
                string2 = "E_s: {:.5s}, ({:.5s})".format(self.s_eff_dnn, self.s_eff_cut)
                string3 = "E_b: {:.3f}, ({:.3f})".format(self.b_eff_dnn, self.b_eff_cut)
            except ValueError as v:
                string2 = "E_s: {:.5s}, ({:.5s})".format(self.s_eff_dnn, self.s_eff_cut)
                string3 = "E_b: {:.5s}, ({:.5s})".format(self.b_eff_dnn, self.b_eff_cut)

        print("{:<45}".format(string1)+"{:23}".format(string2)+"{:23}".format(string3))
    def __repr__(self):
        return "Bin(pt=[{} -- {}], dxy=[{} -- {}]) containing {} elements".format(\
                            self.bin_pt_l, self.bin_pt_u, self.bin_dxy_l, self.bin_dxy_u, len(self.s))



logger.info("Starting eff_table_dxy_pt.py")

truth_vars = ["lep_isFromSUSYandHF_Training/I"]
pred_vars = ["prob_lep_isFromSUSYandHF/F"]
variables = truth_vars + pred_vars + ["lep_dxy/F", "lep_pt/F", "lep_pfRelIso03_all/F"]
input_dir = args.input_dir 
preselection="abs(lep_eta) < 2.4 && lep_looseId"
pt_bins  = np.array([3.5, 5, 10, 20, 30])
dxy_bins = np.array([-3.0, -1.0, -0.5, -0.05, -0.005, 0.005, 0.05, 0.5, 1.0, 3.0])

# logger.info("constructing sample")
sample = Sample.fromDirectory(name="pred",
                                directory=input_dir,
                                treeName='tree',
                                selectionString = preselection)


# output_dir = "" set me 
if args.small:
    sample.reduceFiles(to=4)
    # TODO adjust if small the output dir


def wasSignal(event):
    for category in truth_vars:
        if getattr(event, category.split('/')[0]) == 1:
            return 1
    return 0

def prob_wasSignal(event):
    probability = 0
    for category in pred_vars:
        probability += getattr(event, category.split('/')[0])
    return probability

# What says the StopsCompressed cut
def cut_Signal(event):
    pt = getattr(event, "lep_pt")
    reliso = getattr(event, "lep_pfRelIso03_all")
    # this is done in the preselection...
    # abs_eta = abs(getattr(event, "lep_eta"))
    # loose_id = getattr(event, "lep_looseId")
    if pt <= 25:
        if (reliso*pt) < 5.0:
            return 1
        else:
            return 0
    else:
        if reliso < 0.2:
            return 1
        else:
            return 0

reader = sample.treeReader(variables=variables)
reader.start()
# table = [[[]]*(len(pt_bins1)-1)]*(len(dxy_bins)-1)
# table = np.zeros((len(pt_bins)-1, len(dxy_bins)-1))
table = []
for i in range(len(pt_bins)-1):
    for j in range(len(dxy_bins)-1):
        table.append(Bin(pt_bins[i], pt_bins[i+1], dxy_bins[j], dxy_bins[j+1]))
# for i in range(len(table)):
#     print(i, table[i])
# logger.info("Prepared the bins: {}".format(table))

short = False
short_breaker = 300000
short_cnt = 0
while reader.run():
    # in which lep_feature bin belons the lep?
    # append in the correct bin data in the order
    # -> ["lep_feature", "lep_truth", "lep_pred_DNN", "lep_pred_cut"]
    r = reader.event
    # i_lep_bin = 0
    pt = getattr(r, "lep_pt")
    dxy = getattr(r, "lep_dxy")

    # logger.info("pt={}, dxy={}".format(pt, dxy))
    for i, pt_b in enumerate(pt_bins[1:]):
        if pt <= pt_b:
            for j, dxy_b in enumerate(dxy_bins[1:]):
                if dxy <= dxy_b:
                    table[i*(len(pt_bins)-1)+j].add_value(wasSignal(r),
                                                            prob_wasSignal(r),
                                                            cut_Signal(r))

                    # logger.info("pt_b = {}, dxy_b = {}, {}".format(\
                    #                         pt_b, dxy_b, table[i*(len(dxy_bins)-1)+j]))
                    break
                else:
                    pass
            break
    short_cnt += 1
    if short and short_cnt>= short_breaker:
        break
map(lambda b: b.get_eff(), table)
for a_bin in table:
    # a_bin.get_eff()
    a_bin.print_me()
    # print("\t {}".format(zip(a_bin.s, a_bin.p)))
















