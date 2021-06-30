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
import sys

argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',       action='store',      default='INFO',      nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--directory', action='store')
argParser.add_argument('--small',       action='store_true',     help="Run the file on a small sample (for test purpose), bool flag set to     True if used" )
argParser.add_argument('--long',       action='store_true',     help="0-500, else 0-45" )
argParser.add_argument('--flavour', action='store')
args = argParser.parse_args()

#
# Logger
#
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)


directory = args.directory

#variables = ["prob_isPrompt/F", "prob_isNonPrompt/F", "prob_isFake/F", "lep_isPromptId_Training/I", "lep_isNonPromptId_Training/I", "lep_isFakeId_Training/I", "lep_pt/F", "lep_eta/F"]
variables = ['lep_isPromptId_Training/I',
             'lep_isNonPromptId_Training/I',
             'lep_isNotPromptId_Training/I',
             'lep_isFakeId_Training/I',
             'lep_pt/F',
             'lep_eta/F',
             'lep_probPrompt/F',
             'lep_probNonPrompt/F',
             'lep_probFake/F',
             'lep_probNotPrompt/F',
             'lep_mvaTTH/F',]

if args.flavour == 'muo':
    variables += ['lep_StopsCompressed/I',
             'lep_looseId/F',
             'lep_mediumId/F',
             'lep_tightId/F',
             'lep_precut/F'] 


pred    = []
truth   = []

if args.flavour == 'muo':
    if args.long:
        pt_bins = np.array([
                3.5,5,7.5,10,12.5,15,17.5,20,25,30,35,40,45,50,60,75,100,
                125, 125,150,175,200,250,300,400,500],dtype=float)
    else:
        pt_bins = np.array([
                3.5,5,7.5,10,12.5,15,17.5,20,25,30,35,40,45,],dtype=float)
elif args.flavour == 'ele':
    if args.long:
        pt_bins = np.array([
                5,7.5,10,12.5,15,17.5,20,25,30,35,40,45,50,60,75,100,
                125, 125,150,175,200,250,300,400,500],dtype=float)
    else:
        pt_bins = np.array([
                5,7.5,10,12.5,15,17.5,20,25,30,35,40,45],dtype=float)
    

eta_bins = np.array(
            [-2.5,-2.,-1.5,-1.,-0.5,0.5,1,1.5,2.,2.5, 3.2],
            dtype=float
            )

pt_truth  = [[] for i in range(len(pt_bins))]
eta_truth = [[] for i in range(len(eta_bins))]

pt_pred   = [[] for i in range(len(pt_bins))]
eta_pred  = [[] for i in range(len(eta_bins))]

pt_pred_tth   = [[] for i in range(len(pt_bins))]
pt_pred_stops = [[] for i in range(len(pt_bins))]
    
Sample = Sample.fromDirectory(
                            name="Sample",
                            directory=directory,
                            treeName='tree',
                            selectionString="lep_precut==1.&&lep_genPartFlav!=15")

#if args.small:
#    Sample.reduceFiles(to=1)
 
reader = Sample.treeReader(variables=variables)
reader.start()

counter = 0
while reader.run():
    r = reader.event
    
    lep_probPrompt              = r.lep_probPrompt
    #prob_isNonPrompt            = r.prob_isNonPrompt
    #prob_isFake                 = r.prob_isFake
    lep_isPromptId_Training     = r.lep_isPromptId_Training
    lep_isNonPromptId_Training  = r.lep_isNonPromptId_Training
    lep_isFakeId_Training       = r.lep_isFakeId_Training
    lep_pt                      = r.lep_pt
    lep_eta                     = r.lep_eta
    lep_mvaTTH                  = r.lep_mvaTTH
    
    if args.flavour == 'muo':
        lep_precut = r.lep_precut
        lep_StopsCompressed = r.lep_StopsCompressed

    for i, pt in enumerate(pt_bins):
        if lep_pt < pt:
            pt_pred[i-1].append(lep_probPrompt)
            pt_truth[i-1].append(lep_isPromptId_Training)
            pt_pred_tth[i-1].append(lep_mvaTTH)
            break 
    
    counter += 1
    if args.small:
        if counter > 6000000:
            break
# Plot logic here

def find_nearest_index(a, a0):
    "Element in nd array `a` closest to the scalar value `a0`"
    idx = np.abs(np.asarray(a) - a0).argmin()
    return idx

def get_efficiencies(pred, truth, bins, threshhold):
    signal_eff = []
    background_eff = []
    for pr, tr in zip(pred, truth):
        
        true_signal      = 0.
        false_background = 0.
        total_signal     = 0.
        total_background = 0.
        for p, t in zip(pr, tr):
            if t > 0.5:
                total_signal += 1.
                if p > threshhold:
                    true_signal += 1.

            elif t < 0.5:
                total_background += 1.
                if p > threshhold:
                    false_background += 1.
            else:
                sys.exit(1)
        if total_signal >= 1:
            sig_eff = true_signal / total_signal
            #print("sig_eff", sig_eff)
        else:
            sig_eff = 0.5 # no pts in this region
        if total_background >= 1:
            back_eff = false_background / total_background
        else:
            back_eff = 0.5 # no pts in this region
        
        signal_eff.append(sig_eff)
        background_eff.append(back_eff)
    return signal_eff, background_eff

def search_best_threshhold(pred, truth, bins, target):
    threshholds = []
    signal_eff = []
    back_eff = []
    if args.small:
        N=100
    else:
        N=200
    threshholds = np.linspace(0.98, 1, N)

    counter = 1
    for t in threshholds:
        logger.info('Evaluationg for threshhold {} of {}'.format(counter, len(threshholds)))
        s, b = get_efficiencies(pred, truth, bins, t)
        signal_eff.append(s)
        back_eff.append(b)
        counter += 1    

    final_sig_eff = []
    final_back_eff = []
    final_threshhold = []
    for i in range(len(bins)):
        if bins[i] < target[2]:
            newTarget = target[0]
        else:
            newTarget = target[1]
            
        idx = find_nearest_index([x[i] for x in back_eff], newTarget)
        print('index', idx)
        final_sig_eff.append(signal_eff[idx][i])
        final_back_eff.append(back_eff[idx][i])
        final_threshhold.append(threshholds[idx])

    return final_sig_eff, final_back_eff, final_threshhold
    
def get_eta_threshhold(eta_pred, eta_truth, threshholds):
    pass

target = [0.05, 0.01, 7.5] # Target1, Target2, TargetCut

pt_signal_eff , pt_background_eff, threshholds = search_best_threshhold(pt_pred, pt_truth, pt_bins, target)
pt_signal_eff_tth    , pt_background_eff_tth   = get_efficiencies(pt_pred_tth, pt_truth, pt_bins, 0.9)

gr1 = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_signal_eff))
gr2 = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_background_eff))

gr3 = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_signal_eff_tth))
gr4 = ROOT.TGraph(len(pt_bins)-1, array.array("d", pt_bins[:-1]), array.array("d", pt_background_eff_tth))


gr1.SetLineColorAlpha(ROOT.kBlue, 1)
gr2.SetLineColorAlpha(ROOT.kRed, 1)
gr3.SetLineColorAlpha(ROOT.kBlue+3, 1)
gr4.SetLineColorAlpha(ROOT.kRed+3, 1)

gr1.SetMarkerStyle(34)
gr2.SetMarkerStyle(34)
gr3.SetMarkerStyle(34)
gr4.SetMarkerStyle(34)

c1 = ROOT.TCanvas("c1", "L", 200,100,1000,1000)

c1.SetGrid()

gr1.SetTitle("Signal Efficiency DeepLepton")
gr2.SetTitle("Background Efficiency DeepLepton")
gr3.SetTitle("Signal Efficiency TTH")
gr4.SetTitle("Background Efficiency TTH")

mg = ROOT.TMultiGraph()

mg.Add(gr1)
mg.Add(gr2)
mg.Add(gr3)
mg.Add(gr4)

mg.SetTitle("Signal and Background Efficiency")

mg.Draw("APL") # set everything before Draw, exept axis stuff

mg.GetXaxis().SetTitle("lepton pt")
mg.GetYaxis().SetTitle("efficiency")

mg.GetYaxis().SetLimits(0,1)

c1.BuildLegend(0.7,0.4, 1, 0.6)
c1.Print(os.path.join(plot_directory, 'Efficiency_muo_Top_2016_TT_pow/pt_flat_background{}.png'.format("" if not args.long else "_long")))

print(threshholds) 
dosomethingtostop()

# Re read the files and +1 the right eta bin, according to to the threshhold (pt)
true_signal      = [0. for i in range(len(eta_bins))]
false_background = [0. for i in range(len(eta_bins))]
total_signal     = [0. for i in range(len(eta_bins))]
total_background = [0. for i in range(len(eta_bins))]


    
reader = Sample.treeReader(variables=variables)
reader.start()
while reader.run():
    r = reader.event
    
    prob_isPrompt               = r.prob_isPrompt
    prob_isNonPrompt            = r.prob_isNonPrompt
    prob_isFake                 = r.prob_isFake
    lep_isPromptId_Training     = r.lep_isPromptId_Training
    lep_isNonPromptId_Training = r.lep_isNonPromptId_Training
    lep_isFakeId_Training      = r.lep_isFakeId_Training
    lep_pt                      = r.lep_pt
    lep_eta                     = r.lep_eta

    #if lep_isNonPromptId_Training == 1.:
    #    continue
    for i, pt, t in zip(range(len(pt_bins)), pt_bins, threshholds):
        #print(lep_pt, pt)
        if lep_pt < pt: # right pt bin
            #print("in right pt bin")
            for j, eta in enumerate(eta_bins):
                if lep_eta < eta: # right eta bin
                    #print('in right eta bin')
                    if lep_isPromptId_Training == 1:
                        total_signal[j] += 1.
                        if prob_isPrompt > t:
                            true_signal[j] += 1.
                    else:
                        total_background[j] += 1.
                        if prob_isPrompt > t:
                            false_background[j] += 1.
                    break
            break
    
# calculate efficiencies:
eta_signal_eff = []
eta_background_eff = []

print(total_signal, true_signal, total_background, false_background)

for tots, trus, totb, falb in zip(total_signal, true_signal, total_background, false_background):
    try:
        eta_signal_eff.append(trus / tots)
    except:
        eta_signal_eff.append(0.5)
    try:
        eta_background_eff.append(falb / totb)
    except:
        eta_background_eff.append(0.5)
# eta
#eta_signal_eff , eta_background_eff = get_efficiencies(eta_pred, eta_truth, eta_bins, threshhold)

gr1 = ROOT.TGraph(len(eta_bins)-1, array.array("d", eta_bins[:-1]), array.array("d", eta_signal_eff))
gr2 = ROOT.TGraph(len(eta_bins)-1, array.array("d", eta_bins[:-1]), array.array("d", eta_background_eff))

gr1.SetLineColorAlpha(ROOT.kBlue, 1)
gr2.SetLineColorAlpha(ROOT.kRed, 1)

gr1.SetMarkerStyle(34)
gr2.SetMarkerStyle(34)

c1 = ROOT.TCanvas("c1", "L", 200,100,1000,1000)

c1.SetGrid()

gr1.SetTitle("Signal Efficiency")
gr2.SetTitle("Background Efficiency")

mg = ROOT.TMultiGraph()

mg.Add(gr1)
mg.Add(gr2)

mg.SetTitle("Signal and Background Efficiency")

mg.Draw("APL") # set everything before Draw, exept axis stuff

mg.GetXaxis().SetTitle("lepton eta")
mg.GetYaxis().SetTitle("efficiency")

mg.GetYaxis().SetLimits(0,1)

c1.BuildLegend(0.7,0.4, 1, 0.6)
c1.Print(os.path.join(plot_directory, 'Efficiency_muo_Top_2016_TT_pow/eta_flat_background_{}.png'.format(str(target))))

print('threshholds:', threshholds)
