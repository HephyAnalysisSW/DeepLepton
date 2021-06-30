import ROOT
ROOT.gROOT.SetBatch(True)
from math import sqrt, cos, sin, pi, cosh
from RootTools.core.standard import *
import os
from copy import deepcopy

import Analysis.Tools.syncer as syncer

import time

# StopsDilepton
from DeepLepton.Tools.user import plot_directory
#plot_directory = "/users/maximilian.moser/Plots/lep_pt"

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',       action='store',      default='INFO',      nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
#argParser.add_argument('--plot_directory', action='store',      default='FourMuonInvariantMass')
argParser.add_argument('--small',       action='store_true',                                                                        help="Run the file on a small sample (for test purpose), bool flag set to True if used" )
argParser.add_argument('--mode', action='store', default='Top' ) 
argParser.add_argument('--directory', action='store' )
args = argParser.parse_args()



#
# Logger
#
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

redirector = "root://eos.grid.vbc.ac.at/"

if not args.directory:
    directory = [
            "/scratch-cbe/users/maximilian.moser/DeepLepton/predicted/v3/muo/pt_3.5_-1/TT_pow/"
        ]
else:
    directory = args.directory

flav = "muo" if "muo" in directory else "ele"

if args.mode == 'Top':
    data_sample = Sample.fromDirectory(
        "Predicted",
        directory = directory,
        treeName  = "tree",
        selectionString = "lep_genPartFlav!=15&&lep_precut==1"
        )
    if args.small:
        data_sample.reduceFiles( to = 4 )

elif args.mode == 'DYvsQCD':
    import os
    dirs = os.listdir( directory )
    directoriesDY  = [os.path.join(directory, d)  for d in dirs if "DY"  in d]
    directoriesQCD = [os.path.join(directory, d)  for d in dirs if "QCD" in d]
    
    # TODO: weight the samples
    sampleDY  = Sample.fromDirectory('DY',  directory=directoriesDY,  treeName='tree', selectionString='lep_isPromptId_Training==1&&lep_genPartFlav!=15&&lep_precut==1')
    sampleQCD = Sample.fromDirectory('QCD', directory=directoriesQCD, treeName='tree', selectionString='lep_isPromptId_Training==0&&lep_genPartFlav!=15&&lep_precut==1')
    if args.small:
        sampleDY.reduceFiles( to = 4 )
        sampleQCD.reduceFiles( to = 4 )
#logger.info("%i files", len(data_sample.files))


# copy samples:
wp = 0.995 # Working Point

# As Signal
if args.mode == "Top":
    samplePrompt               = deepcopy(data_sample)
    sampleNonPrompt            = deepcopy(data_sample)
    sampleFake                 = deepcopy(data_sample)

elif args.mode == "DYvsQCD":
    samplePrompt    = deepcopy(sampleDY)
    sampleNonPrompt = deepcopy(sampleQCD)
    sampleFake      = deepcopy(sampleQCD)

samplePrompt.addSelectionString("lep_isPromptId_Training==1")
samplePrompt.texName       = "Prompt"
samplePrompt.Name          = "Prompt"
samplePrompt.style         = styles.lineStyle(ROOT.kRed)

sampleNonPrompt.addSelectionString("lep_isNonPromptId_Training==1")
sampleNonPrompt.texName    = "NonPrompt"
sampleNonPrompt.Name       = "NonPrompt"
sampleNonPrompt.style      = styles.lineStyle(ROOT.kBlue)

sampleFake.addSelectionString("lep_isFakeId_Training==1")
sampleFake.texName         = "Fake"
sampleFake.Name            = "Fake"
sampleFake.style           = styles.lineStyle(ROOT.kGreen)


read_variables = [
                  "lep_pt/F",
		          "lep_eta/F",
                  "lep_phi/F",
                  "lep_pdgId/F",
                  "lep_mediumId/F",
                  "lep_miniPFRelIso_all/F",
                  "lep_pfRelIso03_all/F",
                  "lep_sip3d/F",
                  "lep_dxy/F",
                  "lep_dz/F",
                  "lep_charge/F",
                  "lep_dxyErr/F",
                  "lep_dzErr/F",
                  "lep_ip3d/F",
                  "lep_jetPtRelv2/F",
                  "lep_jetRelIso/F",
                  "lep_miniPFRelIso_chg/F",
                  "lep_mvaLowPt/F",
                  "lep_nStations/F",
                  "lep_nTrackerLayers/F",
                  "lep_pfRelIso03_all/F",
                  "lep_pfRelIso03_chg/F",
                  "lep_pfRelIso04_all/F",
                  "lep_ptErr/F",
                  "lep_segmentComp/F",
                  "lep_tkRelIso/F",
                  "lep_tunepRelPt/F",
                  "lep_genPartFlav/F",
                  "npfCand_charged/I",
                  "npfCand_neutral/I",
                  "npfCand_photon/I",
                  "npfCand_electron/I",
                  "npfCand_muon/I",
                  "nSV/I",
                  "lep_mvaTTH/F",
                  "lep_StopsCompressed/F",
                  "lep_probPrompt/F",
                  "lep_probNonPrompt/F",
                  "lep_probFake/F",
                   ]


stack = Stack([samplePrompt], [sampleNonPrompt], [sampleFake])

# Use some defaults
Plot.setDefaults(stack = stack)

plots = []


plots.append(Plot(name      = "Discriminator_of_Prompt",
                  texX      = 'Prompt Discriminator', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_probPrompt,
                  binning   = [100,0,1],
                  ))
plots.append(Plot(name      = "Discriminator_of_NonPrompt",
                  texX      = 'NonPrompt Discriminator', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_probNonPrompt,
                  binning   = [100,0,1],
                  ))
plots.append(Plot(name      = "Discriminator_of_Fake",
                  texX      = 'Fake Discriminator', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_probFake,
                  binning   = [100,0,1],
                  ))

plotting.fill(plots, read_variables = read_variables)

for plot in plots:
    plotting.draw(plot, 
                  plot_directory = os.path.join(plot_directory, "2016_{}_{}_Input_{}".format(flav, args.mode, directory.split("/")[-2])),#args.plot_directory),
                  ratio          = None, 
                  logX           = False, 
                  logY           = True,
                  sorting        = True,
                  scaling        = {0:0, 1:0, 2:0}, 
                  yRange         = (1.0, "auto"),
                  #legend         = "auto"
                  #drawObjects    = drawObjects( )
                  copyIndexPHP   = True,
                  extensions     = ["png", "pdf", "root"]
                                              )

#logger.info("%f s per file, %f total", (time.time()-t0)/len(data_sample.files), time.time()-t0)
