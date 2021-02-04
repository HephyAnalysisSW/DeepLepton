import ROOT
ROOT.gROOT.SetBatch(True)
from math import sqrt, cos, sin, pi, cosh
from RootTools.core.standard import *
import os
from copy import deepcopy

# StopsDilepton
#from DeepLepton.Tools.user import plot_directory
plot_directory = "/users/maximilian.moser/Plots/lep_pt"

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',       action='store',      default='INFO',      nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--plot_directory', action='store',      default='FourMuonInvariantMass')
argParser.add_argument('--small',       action='store_true',                                                                        help="Run the file on a small sample (for test purpose), bool flag set to True if used" )
args = argParser.parse_args()



#
# Logger
#
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

directory = [
        "/scratch-cbe/users/robert.schoefbeck/DeepLepton/v1/step2/2016/muo/pt_5_-1/DYvsQCD/",
        ]

data_sample = Sample.fromDirectory(
        "step2",
        #directory = "/scratch-cbe/users/maximilian.moser/DeepLepton/v1_small/step1/2016/muo/Fake/pt_5_-1/DYJetsToLL_M50_LO/", 
        directory = directory,
        treeName  = "tree"
        )

if args.small:
    data_sample.reduceFiles( to = 1 )

# copy samples:

samplePrompt               = deepcopy(data_sample)
samplePrompt.setSelectionString("lep_isPromptId_Training==1")
samplePrompt.legendText    = "Prompt"
samplePrompt.style         = styles.lineStyle(ROOT.kBlack)

sampleNonPrompt            = deepcopy(data_sample)
sampleNonPrompt.setSelectionString("lep_isNonPromptId_Training==1")
sampleNonPrompt.legendText = "NonPrompt"
sampleNonPrompt.style      = styles.lineStyle(ROOT.kBlue)

sampleFake                 = deepcopy(data_sample)
sampleFake.setSelectionString("lep_isFakeId_Training==1")
sampleFake.legendText      = "Fake"
sampleFake.style           = styles.lineStyle(ROOT.kGreen)


read_variables = [
                  "lep_pt/F",
		  "lep_eta/F",
                 ]


stack = Stack([samplePrompt, sampleNonPrompt, sampleFake])

# Use some defaults
Plot.setDefaults(stack = stack)

plots = []


plots.append(Plot(name      = "lep_pt",
                  texX      = 'p_{T}(l)', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_pt,
                  binning   = [100,0,200],                  
                  ))

plots.append(Plot(name      = "lep_eta",
                  texX      = 'eta', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_eta,
                  binning   = [100,0,3],
                  ))

plotting.fill(plots, read_variables = read_variables)

for plot in plots:
    plotting.draw(plot, 
                  plot_directory = plot_directory, #os.path.join(plot_directory, args.plot_directory),
                  ratio          = None, 
                  logX           = False, 
                  logY           = True,
                  sorting        = True, 
                  yRange         = (1.0, "auto"),
                  #legend         = "auto"
                  #drawObjects    = drawObjects( )
                                              )
