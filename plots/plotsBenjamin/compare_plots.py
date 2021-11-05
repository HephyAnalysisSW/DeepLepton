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
                           
argParser.add_argument('--ncat',
                       action='store',
                       type=int,
                       required=True,
                       help="Training on how many lepton classes? (4 or 5)")

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

logger.info("Starting compare_plots.py")


# little helper class
class Struct():
    def __init__(self):
        self.struct = {"lep_feature":[], "lep_truth":[], "lep_pred_DNN":[], "lep_pred_cut":[]}
        self.keys = ["lep_feature", "lep_truth", "lep_pred_DNN", "lep_pred_cut"]

    def add_value(self, array):
        i = 0
        for key in self.keys:
            assert len(array) == 4
            self.struct[key].append(array[i])
            i += 1

    def get(self, key):
       return self.struct[key]

    def add(self, other_Struct):
        for key in self.keys:
            self.struct[key] += other_Struct.get(key)
        
    def set(self, key, a_list):
        assert key in self.keys
        assert isinstance(a_list, list)
        self.struct[key] = a_list



class Eff_Roc:
    def __init__(self,
                lep_feature="lep_pt/F",
                lep_feature_bins=np.array([3.5, 5, 10, 15, 20]),
                give_signal_eff=True,
                eff=0.9,
                preselection="lep_precut==1",
                plotting_bins=[np.linspace(start=3.5, stop=5, num=10),
                                        np.linspace(start=5, stop=10, num=10),
                                        np.linspace(start=10, stop=15, num=10),
                                        np.linspace(start=15, stop=20, num=10)],
                input_dir="/scratch-cbe/users/benjamin.wilhelmy/DeepLepton/predicted_on_sample/v6/2018/muo/pt_3.5_-1",
                output_dir=plot_directory):

        # here we save the values for the different lep_feature_bins
        self.lep_bin          = [Struct() for i in range(len(plotting_bins))]
        self.latex_string     = []

        self.lep_feature      = lep_feature
        self.lep_feature_bins = lep_feature_bins
        self.give_signal_eff  = give_signal_eff
        self.eff              = eff
        self.preselection     = preselection
        self.plotting_bins    = plotting_bins
        self.input_dir        = input_dir
        self.output_dir       = output_dir

        self.sample           = Sample.fromDirectory(name="pred", directory=self.input_dir, treeName='tree', selectionString = self.preselection)
        if args.small:
            self.sample.reduceFiles(to=4)
            x = self.output_dir.split("/")
            x[-2] += "_small"
            self.output_dir = "/".join(x)

        if os.path.isdir(self.output_dir):
            logger.info("output directory already exists.")
        else:
            logger.info("output directory does not exist, making it")
            os.makedirs(self.output_dir)

        # self.pred  = []
        # self.truth = []
        assert len(self.lep_feature_bins) != 0
        assert len(self.lep_feature_bins)-1 == len(self.plotting_bins)

        # How many lepton Classes
        self.n_classes = args.ncat
        if self.n_classes == 4:
            # only one susy class
            logger.info("please check the type of the TLeaf s")
            self.truth_vars = ["lep_isFromSUSYandHF_Training/I"]
            self.pred_vars  = ["prob_lep_isFromSUSYandHF/F"]
        elif self.n_classes == 5:
            raise(NotImplemented())
            self.truth_vars = ["lep_isFromSUSY_Training/I", "lep_isFromSUSYHF_Training/I"]
            self.pred_vars  = ["prob_isFromSUSY/F", "prob_isFromSUSYHF/F",]
        else:
            raise NotImplemented("this case for ncat is not implemented")
        
        self.variables = self.truth_vars +\
                         self.pred_vars +\
                         [self.lep_feature] +\
                         ["lep_StopsCompressed/I"]

        logger.info("read variables are {}".format(self.variables))


    def wasSignal(self, event):
        for category in self.truth_vars:
            if getattr(event, category.split('/')[0]) == 1:
                return 1
        return 0
    
    def prob_wasSignal(self, event):
        probability = 0
        for category in self.pred_vars:
            probability += getattr(event, category.split('/')[0])
        return probability

    # What says the StopsCompressed cut
    def cut_Signal(self, event):
        return getattr(event, "lep_StopsCompressed")


    def read_and_sort_for_bins(self):
        # sample = Sample.fromDirectory(name="pred", directory=self.input_dir, treeName='tree', selectionString = self.preselection)
         
        reader = self.sample.treeReader(variables=self.variables)
        reader.start()
        
        while reader.run():
            # in which lep_feature bin belons the lep?
            # append in the correct bin data in the order
            # -> ["lep_feature", "lep_truth", "lep_pred_DNN", "lep_pred_cut"]
            r = reader.event
            # i_lep_bin = 0
            lep_feature_value = getattr(r, self.lep_feature.split('/')[0])
            #print(lep_feature_value)
            for i_lep_bin, bin_edge in enumerate(self.lep_feature_bins[1:]):
                if lep_feature_value < bin_edge and \
                    lep_feature_value > self.lep_feature_bins[i_lep_bin]:

                    values = [lep_feature_value,
                                self.wasSignal(r),
                                self.prob_wasSignal(r),
                                self.cut_Signal(r)]

                    self.lep_bin[i_lep_bin].add_value(values)


    def find_nearest(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx


# self.keys = ["lep_feature", "lep_truth", "lep_pred_DNN", "lep_pred_cut"]

    def rm_nans(self, struct):
        '''remove the indices where pred is nan'''
        nans = np.isnan(np.array(struct.get("lep_pred_DNN")))

        truth = np.array(struct.get("lep_truth"))
        feature = np.array(struct.get("lep_feature"))
        cut = np.array(struct.get("lep_pred_cut"))
        pred = np.array(struct.get("lep_pred_DNN"))

        if nans.any() == True:
            logger.info("ATTENTION FOUND NANS IN PREDICTION...REMOVING THEM, BE CAREFUL")
            logger.debug("with values: feature, truth, pred, cut = {}, {}, {}, {}".format(feature[nans], truth[nans], pred[nans], cut[nans]))

        truth = truth[np.logical_not(nans)]
        pred = pred[np.logical_not(nans)]
        cut = cut[np.logical_not(nans)]
        feature = feature[np.logical_not(nans)]

        struct.set("lep_truth",    list(truth))
        struct.set("lep_feature",  list(feature))
        struct.set("lep_pred_DNN", list(pred))
        struct.set("lep_pred_cut", list(cut))
        # return [list(truth), list(pred)]

    def rm_nans_from_lists(self, truth, pred, cut):
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


    def fromStruct_make_plot(self):
        # self.plotdata = [{} for i in range(len(self.lep_bin))]
        for j, struct in enumerate(self.lep_bin):
            # logger.debug("printing lep_truth = {} \n printing lep_pred_DNN = {}".format(struct.get("lep_truth"),
            #                                                                             struct.get("lep_pred_DNN")))
            
            if args.logLevel == "DEBUG":
                tmps = struct.get("lep_pred_DNN")
                # tmps = np.array(tmps, dtype=np.float64)
                logger.debug("tmp types {}".format(type(tmps[0])))
                for tmp in tmps:
                    if not((tmp >= 0) and (tmp<=1)):
                        logger.debug("Found invalid value ?! {}".format(tmp))

            self.rm_nans(struct)
            print("The {}th struct".format(j))
            print("Values of the struct: \n truth: {} \n pred: {}".format(self.lep_bin[j].get("lep_truth"), self.lep_bin[j].get("lep_pred_DNN")))

            fpr_dnn, tpr_dnn, thresholds_dnn = roc_curve(struct.get("lep_truth"), struct.get("lep_pred_DNN"), drop_intermediate=False)
            
            fpr_stopsComp, tpr_stopsComp, thresholds_stopsComp = roc_curve(struct.get("lep_truth"), struct.get("lep_pred_cut"), drop_intermediate=False)
            # get the threshold for given efficiency:
            if self.give_signal_eff:
                i           = self.find_nearest(tpr_dnn, self.eff)
                i_stopsComp = self.find_nearest(tpr_stopsComp, self.eff)
            else:
                i           = self.find_nearest(fpr_dnn, self.eff) 
                i_stopsComp = self.find_nearest(fpr_stopsComp, self.eff)

            threshold = thresholds_dnn[i]
            roc_ptys = [i, fpr_dnn, tpr_dnn, thresholds_dnn, fpr_stopsComp, tpr_stopsComp, thresholds_stopsComp]
            # make the roc curve...
            self.plot_roc_curve(fpr_dnn, tpr_dnn, fpr_stopsComp, tpr_stopsComp,
                            tpr_dnn[i], fpr_dnn[i],
                            threshold, 
                            os.path.join(self.output_dir,
                                    self.lep_feature.split("/")[0],
                                    "roc_curve_{}.png".format(self.lep_feature_bins[j+1])))

            print("made the new roc_curve in {}".format(os.path.join(self.output_dir,
                                    self.lep_feature.split("/")[0],
                                    "roc_curve_{}.png".format(self.lep_feature_bins[j+1]))))
            self.latex_string.append([self.lep_feature_bins[j],
                                      self.lep_feature_bins[j+1],
                                      tpr_dnn[i],
                                      tpr_stopsComp[i_stopsComp],
                                      fpr_dnn[i],
                                      fpr_stopsComp[i_stopsComp],
                                      threshold,
                                      ])
            # def __init__(self, x_bins, lep_feature = "lep_pt", structur, THRESHOLD):
            logger.info("Creating HistoData_handler with {} leptons".format(len(struct.get("lep_feature"))))
            data = HistoData_handler(x_bins=self.plotting_bins[j],
                                     lep_feature=self.lep_feature.split('/')[0], 
                                     structur=struct, 
                                     THRESHOLD=threshold,
                                     output_dir = self.output_dir,
                                     roc_ptys=roc_ptys)
            logger.info("rading data and fill the histos")
            data.reading() # read and fill the histos
            logger.info("making the eff plots...")
            data.calc_eff_backeff_and_plot() # cal eff and backeff and plot it
            logger.info("Done...")
        if error:
            raise ValueError()
    def make_roc_curve(self):
        pred     = []
        truth    = []
        cut_pred = []

        # sample = Sample.fromDirectory(name="pred", directory=self.input_dir, treeName='tree', selectionString = self.preselection)
       
        reader = self.sample.treeReader(variables=self.variables)
        reader.start()
        
        while reader.run():
            r = reader.event
            pred.append(self.prob_wasSignal(r))
            truth.append(self.wasSignal(r))
            cut_pred.append(self.cut_Signal(r))

        logger.info("Making roc curve...")
        [truth, pred, cut_pred] = self.rm_nans_from_lists(truth, pred, cut_pred)
        fpr, tpr, thresholds = roc_curve(truth, pred, drop_intermediate=False)
        fpr_cut, tpr_cut, thrsh_cut = roc_curve(truth, cut_pred, drop_intermediate=False) 
        if self.give_signal_eff:
            i = self.find_nearest(tpr, self.eff)   
        else:
            i = self.find_nearest(fpr, self.eff) 
        global_threshold = thresholds[i]
        global_eff       = tpr[i]
        global_backeff   = fpr[i]
        #os.path.join(self.output_dir, 'roc_curve.png'))
        self.plot_roc_curve(fpr, tpr, fpr_cut, tpr_cut,
                            global_eff, global_backeff,
                            global_threshold, 
                            os.path.join(self.output_dir, 'roc_curve.png'))
        # print("plot_roc_curve WORKED!!!!!!!!!!!!!!!!!!!!!")

    def plot_roc_curve(self, fpr, tpr, fpr_cut, tpr_cut, 
                        global_eff, global_backeff,
                        global_threshold, outname):
        c1 = ROOT.TCanvas("c1", "L", 200,100,1000,1000)
        c1.SetTitle("ROC-Curve")
        
        gr1 = ROOT.TGraph(len(fpr), array.array('d', fpr), array.array('d', tpr))
        gr1.GetXaxis().SetTitle("False Positive Rate")
        gr1.GetYaxis().SetTitle("True Positive Rate")
        # gr1.SetLineWidth(2)
        gr1.GetXaxis().SetLimits(0,1)
        gr1.GetYaxis().SetLimits(0,1)
        gr1.SetTitle("ROC-Curve")
        gr1.SetMarkerStyle(1)
        gr1.SetLineColor(1)

        gr2 = ROOT.TGraph(len(fpr_cut), array.array('d', fpr_cut), array.array('d', tpr_cut))
        gr2.GetXaxis().SetTitle("False Positive Rate")
        gr2.GetYaxis().SetTitle("True Positive Rate")
        # gr1.SetLineWidth(2)
        gr2.GetXaxis().SetLimits(0,1)
        gr2.GetYaxis().SetLimits(0,1)
        gr2.SetTitle("StopsCompressed - cut based")
        gr2.SetMarkerStyle(1)
        gr2.SetLineColor(2)

        gr_point = ROOT.TGraph(1, array.array('d', [global_backeff]), array.array('d', [global_eff]))
        gr_point.SetMarkerStyle(3)
        gr_point.SetMarkerSize(4)
        gr_point.SetMarkerColor(3)
        gr_point.SetTitle("TPR = {:0.2e} FPR = {:0.2e} Threshold = {:0.2e}".format(global_eff, global_backeff, global_threshold))



        mg = ROOT.TMultiGraph()
        mg.SetTitle("ROC-Curve; False Positive Rate; True Positive Rate")
        mg.Add(gr1)
        mg.Add(gr2)
        mg.Add(gr_point)
        mg.Draw("ALP")
        c1.BuildLegend()
        # TODO: output path handling
        # if args.special_output_path:
        #     plot_sub_dir = args.special_output_path
        # else:
        #     plot_sub_dir = path_pred.split('/')[-2]
        c1.Print(outname) #os.path.join(self.output_dir, 'roc_curve.png'))


    def copy(self):
        from shutil import copyfile
        index="/mnt/hephy/cms/benjamin.wilhelmy/www/index.php"
        print(os.path.join(self.output_dir, "index.php"))
        print("/".join(self.output_dir.split("/")[:-1]))
        print(os.path.join(self.output_dir, self.lep_feature, "index.php"))
        copyfile(index, os.path.join(self.output_dir, "index.php")) 
        copyfile(index, os.path.join("/".join(self.output_dir.split("/")[:-1]), "index.php"))
        copyfile(index, os.path.join(self.output_dir, self.lep_feature.split("/")[0], "index.php"))
   


    def make_latex_table(self):
        with open(os.path.join(self.output_dir,
                                self.lep_feature.split("/")[0])+".txt", 'w') as latex:
            latex.write("\\begin{center} \n")
            latex.write("\\begin{tabular}{||c| c c c||} \n")
            latex.write("\\hline \n")
            latex.write("{}".format(self.lep_feature.split("/")[0].split("_")[0])) 
            latex.write("\_{")
            latex.write("{}".format(self.lep_feature.split("/")[0].split("_")[1]))
            latex.write("} & $\\epsilon _S$ & $\\epsilon _B$ & Threshold \\\ [1.0ex] \n")
            latex.write("\\hline \n")
            for values in self.latex_string:
                latex.write("{}-{} & ".format(values[0], values[1]))
                latex.write("{:.2f}\\% ({:.2f}) & ".format(100.0*values[2], 100.0*values[3]))
                latex.write("{:.2f}\\% ({:.2f}) & ".format(100.0*values[4], 100.0*values[5]))
                latex.write("{} \\\ [0.5ex] \n".format(values[6]))
                latex.write("\\hline \n")
            latex.write("\\end{tabular} \n")
            latex.write("\\end{center}")









class HistoData_handler:
# roc_ptys = [i, fpr_dnn, tpr_dnn, thresholds_dnn, fpr_stopsComp, tpr_stopsComp, thresholds_stopsComp]

    def __init__(self, x_bins, structur, THRESHOLD, roc_ptys, output_dir, lep_feature = "lep_pt"):
        self.TP = {"x":[]} 
        self.TN = {"x":[]}
        self.FP = {"x":[]}
        self.FN = {"x":[]}

        self.h_tp = {"x":np.zeros(len(x_bins)-1)}
        self.h_tn = {"x":np.zeros(len(x_bins)-1)}
        self.h_fp = {"x":np.zeros(len(x_bins)-1)}
        self.h_fn = {"x":np.zeros(len(x_bins)-1)}

        # max length of list of tuples before making histogram to save memory
        self.n_max      = 1e6
        self.x_bins     = x_bins
        self.structur   = deepcopy(structur)
        self.THRESHOLD  =THRESHOLD
        self.x          = lep_feature 
        self.roc_ptys   = roc_ptys
        self.output_dir = output_dir

        # for reading samples
        #self.variables = self.labels + self.prob_labels + [x+"/F", y+"/F"] # [x+"/F", y+"/F"]

        # needed for checking the length of TP, TN, ... and making histos
        self.categories = [(self.TP, self.h_tp), (self.TN, self.h_tn), (self.FP, self.h_fp), (self.FN, self.h_fn)]
        
        if args.ncat == 4:
            logger.info("check if the type in the prediction rootfile is D or F!")
            self.labels = ["lep_isPromptId_Training/I",
                      "lep_isNonPromptId_Training/I",
                      "lep_isFakeId_Training/I",
                      "lep_isFromSUSYandHF_Training/I"]
        
            self.prob_labels = ["prob_isPrompt/F",
                           "prob_isNonPrompt/F",
                           "prob_isFake/F",
                           "prob_lep_isFromSUSYandHF/F"]
        
            # define what is signal the rest is background
            self.signal = {"Training":['lep_isFromSUSYandHF_Training'],
                      "prob":['prob_lep_isFromSUSYandHF']}
        
        elif args.ncat == 5:
            logger.info("check if TLeafes have type F or D !!!")
            raise(NotImplemented("correct type ??"))
            self.labels = ["lep_isPromptId_Training/I",
                      "lep_isNonPromptId_Training/I",
                      "lep_isFakeId_Training/I",
                      "lep_isFromSUSY_Training/I",
                      "lep_isFromSUSYHF_Training/I"]
            
            self.prob_labels = ["prob_isPrompt/F",
                           "prob_isNonPrompt/F",
                           "prob_isFake/F",
                           "prob_isFromSUSY/F",
                           "prob_isFromSUSYHF/F"]
        
            self.signal = {"Training":['lep_isFromSUSY_Training', 'lep_isFromSUSYHF_Training'],
                      "prob":['prob_isFromSUSY', 'prob_isFromSUSYHF']}
        
        else:
            raise NotImplemented("ncat in (4,5)")


   
    # for category in categories
    def make_histo(self, category):
        # category[1] is h_..
        logger.debug("histox before {}".format(category[1]["x"]))
        category[1]["x"] += np.histogram(category[0]["x"], self.x_bins)[0]
        category[0]["x"] = []
        logger.debug("histo after {}".format(category[1]["x"]))
        return category
    
    # for calculating efficiency and background eff
    def divide_histo(self, hist_a, hist_b):
        assert(len(hist_a) == len(hist_b))
        tmp = np.zeros(len(hist_a))
        for i in range(len(hist_a)):
            if hist_b[i]:
                tmp[i] = hist_a[i]/hist_b[i]
            else:
                logger.info("A bin was empty -> consider other binning")
                tmp[i] = -1
        return tmp
    
    def reading(self): 
        # should later work with threshold beeing array_like
        logger.info("found {} leptons passing selection".format(len(self.structur.get("lep_feature"))))
        for i in range(len(self.structur.get("lep_feature"))):
        # self.struct = {"lep_feature":[], "lep_truth":[], "lep_pred_DNN":[], "lep_pred_cut":[]}
            if self.structur.get("lep_truth")[i]: # if lepton is signal
                if self.structur.get("lep_pred_DNN")[i]>=self.THRESHOLD: # event_classified_signal
                    self.TP["x"].append(self.structur.get("lep_feature")[i])
                else:
                    self.FN["x"].append(self.structur.get("lep_feature")[i])
            else: # the lepton is not signal
                if self.structur.get("lep_pred_DNN")[i]>=self.THRESHOLD: # event_classified_signal
                    self.FP["x"].append(self.structur.get("lep_feature")[i])
                else:
                    self.TN["x"].append(self.structur.get("lep_feature")[i])
            
            for category in self.categories:
                if len(category[0]["x"]) >= self.n_max:
                    logger.info("make a temporal histogram to save mem")
                    category=self.make_histo(category)
                    #category[0]["x"] = []
                    #category[0]["y"] = []
            
        # take the last events in histogram
        for category in self.categories:
            category=self.make_histo(category)
            # category[0]["x"] = []
            # category[0]["y"] = []
        
        
        logger.info("Done making histos for a lep_feature bin...")

    def calc_eff_backeff_and_plot(self):
    # calculate sensitivity = signal efficiency
        self.sensitivity_x = self.divide_histo(self.h_tp["x"], self.h_tp["x"] + self.h_fn["x"])
        self.back_eff_x    = self.divide_histo(self.h_fp["x"], self.h_tn["x"] + self.h_fp["x"])

        self._plot(color=1)

    # The pt plot:
    # gr1 = ROOT.TGraph(len_classifier_pt, array.array("d", plot_x_bins), array.array("d", efficiency_pt))
    def _plot(self, color): #, fillcolor):
        # make the dot in the middle of the bin ...
        shift_bins = True
        mybins = np.zeros(len(self.x_bins)-1)
        if shift_bins == True:
            for i in range(len(mybins)):
                mybins[i] = (self.x_bins[i]+self.x_bins[i+1])/2.
        else:
            mybins = deepcopy(self.x_bins)[:-1] 
        print(len(mybins))
        print((self.sensitivity_x))
        gr1 = ROOT.TGraph(len(mybins),
                            array.array("d", mybins),
                            array.array("d", self.sensitivity_x))
    
        gr2 = ROOT.TGraph(len(mybins),
                            array.array("d", mybins),
                            array.array("d", self.back_eff_x))
        
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
        mg.SetTitle("Binary Classification Tests in {}".format(self.x))
        mg.Draw("APL")  # set everything before Draw, exept axis stuff
        mg.GetXaxis().SetTitle(self.x)
        # mg.GetYaxis().SetLimits(0, 1)
        mg.SetMinimum(0)
        mg.SetMaximum(1)
        c1.BuildLegend(0.7, 0.4, 1, 0.6)
        # TODO: ...
        #roc_ptys = [i, fpr_dnn, tpr_dnn, thresholds_dnn, fpr_stopsComp, tpr_stopsComp, thresholds_stopsComp]
        eff = self.roc_ptys[2][i]
        backeff = self.roc_ptys[1][i]


        if os.path.isdir(os.path.join(self.output_dir, "{}/".format(self.x))):
            logger.info("feature directory already exists")
        else:
            os.mkdir(os.path.join(self.output_dir, "{}".format(self.x)))

        c1.Print(os.path.join(self.output_dir,
                              "{}".format(self.x),
                              "Efficiency_plt_{}_e_be_thr_".format(mybins[0])+ "{:0.2e}_{:0.2e}_{:0.2e}.png".format(eff, backeff, self.THRESHOLD)))
        
        logger.info("Succesfully plotted {} plot".format(self.x))




##############################################
input_dir  = args.input_dir
#"/scratch-cbe/users/benjamin.wilhelmy/DeepLepton/predicted_on_sample/v4/2018/muo/pt_3.5_-1/Stop250-dm10-006/"

output_dir = os.path.join(plot_directory, args.outfilespath)
#os.path.join(plot_directory, "Training_v4", "training_on_unbalanced_data_only4lep_classes_dxy_weighted_Keras-loss_20eps_0.1dropout", "vsStopsCompressed", "Stop250-dm10-006")


Lep_Pt = Eff_Roc(lep_feature="lep_pt/F",
        lep_feature_bins=np.array([3.5, 5, 10, 15, 20, 40]), 
        give_signal_eff=True,
        eff=0.9,
        preselection="lep_precut==1",
        plotting_bins=[np.linspace(start=3.5, stop=5, num=10),
                                np.linspace(start=5, stop=10, num=10),
                                np.linspace(start=10, stop=15, num=10),
                                np.linspace(start=15, stop=20, num=10),
                                np.linspace(start=20, stop=40, num=10)],
        input_dir=input_dir,
        output_dir=output_dir)

Lep_dxy = Eff_Roc(lep_feature="lep_dxy/F",
        lep_feature_bins=np.array([-3.0, -0.1, -0.005, 0.005, 0.1, 3]), 
        give_signal_eff=True,
        eff=0.9,
        preselection="lep_precut==1",
        plotting_bins=[np.linspace(start=-3.0, stop=-0.1, num=5),
                                np.linspace(start=-0.1, stop=-0.005, num=5),
                                np.linspace(start=-0.005, stop=0.005, num=20),
                                np.linspace(start=0.005, stop=0.1, num=5),
                                np.linspace(start=0.1, stop=3, num=5)],
        input_dir=input_dir,
        output_dir=output_dir)


logger.info("read and sort for bins...")
Lep_dxy.read_and_sort_for_bins()
logger.info("from struct make plots...")
Lep_dxy.fromStruct_make_plot()
# logger.info("make roc curve...")
# Lep_dxy.make_roc_curve()
Lep_dxy.copy()
Lep_dxy.make_latex_table()
del Lep_dxy

logger.info("read and sort for bins...")
Lep_Pt.read_and_sort_for_bins()
logger.info("from struct make plots...")
Lep_Pt.fromStruct_make_plot()
# logger.info("make roc curve...")
# Lep_Pt.make_roc_curve()
Lep_Pt.copy()
Lep_Pt.make_latex_table()
logger.info("deleting Lep_Pt to save mem...")





