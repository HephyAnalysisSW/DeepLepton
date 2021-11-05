import ROOT
ROOT.gROOT.SetBatch(True)
from RootTools.core.standard import *
import os
from copy import deepcopy
import Analysis.Tools.syncer as syncer
import time
from DeepLepton.Tools.user import plot_directory
import argparse

argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',       action='store',      default='INFO',      nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
#argParser.add_argument('--plot_directory', action='store',      default='FourMuonInvariantMass')
argParser.add_argument('--small',       action='store_true',                                                                        help="Run the file on a small sample (for test purpose), bool flag set to True if used" )
argParser.add_argument('--pathpred', action='store', help="path to the predicted rootfiles" )
argParser.add_argument('--normalize',
                        action='store_true',
                        default=False,
                        help="If True all histos will have the same area (The same as the 4th histo)")

argParser.add_argument('--ncat',
                        action='store',
                        required=True,
                        type = int,
                        help="how many lepton classes (4 or 5)?")

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

directory = args.pathpred
if args.special_output_path:
    subdir = args.special_output_path
else:
    subdir = directory.split('/')[-2]

t0 = time.time()
data_sample = Sample.fromDirectory(
        "Predicted",
        directory = directory,
        treeName  = "tree"
        )
if args.small:
    data_sample.reduceFiles( to = 4 )

    
   #  sampleDY  = Sample.fromDirectory('DY',  directory=directoriesDY,  treeName='tree', selectionString='lep_isPromptId_Training==1&&lep_genPartFlav!=15')
   #  sampleQCD = Sample.fromDirectory('QCD', directory=directoriesQCD, treeName='tree', selectionString='lep_isPromptId_Training==0&&lep_genPartFlav!=15')
   #  data_sample = Sample.combine("Predicted", [sampleDY])
   #  if args.small:
   #      sampleDY.reduceFiles( to = 4 )
   #      sampleQCD.reduceFiles( to = 4 )

logger.info("%i files", len(data_sample.files))


# copy samples:
# wp = 0.993 # Working Point


samplePrompt               = deepcopy(data_sample)
samplePrompt.addSelectionString("lep_isPromptId_Training==1")
samplePrompt.texName       = "Prompt"
samplePrompt.Name          = "Prompt"
samplePrompt.style         = styles.lineStyle(ROOT.kBlack)

sampleNonPrompt            = deepcopy(data_sample)
sampleNonPrompt.addSelectionString("lep_isNonPromptId_Training==1")
sampleNonPrompt.texName    = "NonPrompt"
sampleNonPrompt.Name       = "NonPrompt"
sampleNonPrompt.style      = styles.lineStyle(ROOT.kBlue)

sampleFake                 = deepcopy(data_sample)
sampleFake.addSelectionString("lep_isFakeId_Training==1")
sampleFake.texName         = "Fake"
sampleFake.Name            = "Fake"
sampleFake.style           = styles.lineStyle(ROOT.kGreen+1)

if args.ncat == 5:
    sampleSUSY                 = deepcopy(data_sample)
    sampleSUSY.addSelectionString("lep_isFromSUSY_Training==1")
    sampleSUSY.texName         = "Susy"
    sampleSUSY.Name            = "Susy"
    sampleSUSY.style           = styles.lineStyle(ROOT.kRed)
    
    sampleSUSYHF                 = deepcopy(data_sample)
    sampleSUSYHF.addSelectionString("lep_isFromSUSYHF_Training==1")
    sampleSUSYHF.texName         = "SusyHF"
    sampleSUSYHF.Name            = "SusyHF"
    sampleSUSYHF.style           = styles.lineStyle(ROOT.kMagenta)
    logger.info("check if the prediction TLeafes have type F or D")
    raise(NotImplemented("usually predictdata has type D not F look at ncat==4"))
    read_variables = ["prob_isPrompt/F",
               "prob_isNonPrompt/F",
               "prob_isFake/F",
               "prob_isFromSUSY/F",
               "prob_isFromSUSYHF/F"]

    stack = Stack([samplePrompt], [sampleNonPrompt], [sampleFake], [sampleSUSY], [sampleSUSYHF])

elif args.ncat == 4: 
    sampleSUSY                 = deepcopy(data_sample)
    sampleSUSY.addSelectionString("lep_isFromSUSYandHF_Training==1")
    sampleSUSY.texName         = "Susy"
    sampleSUSY.Name            = "Susy"
    sampleSUSY.style           = styles.lineStyle(ROOT.kRed)

    read_variables = ["prob_isPrompt/D",
                      "prob_isNonPrompt/D",
                      "prob_isFake/D",
                      "prob_lep_isFromSUSYandHF/D"]

    stack = Stack([samplePrompt], [sampleNonPrompt], [sampleFake], [sampleSUSY])

else:
    raise NotImplemented("not implemented")
# labels = ["lep_isPromptId_Training/F",
#           "lep_isNonPromptId_Training/F",
#           "lep_isFakeId_Training/F",
#           "lep_isFromSUSY_Training/F",
#           "lep_isFromSUSYHF_Training/F"]



# Use some defaults
Plot.setDefaults(stack = stack)

plots = []


plots.append(Plot(name      = "Discriminator_of_Prompt",
                  texX      = 'Prompt Discriminator', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.prob_isPrompt,
                  binning   = [100,-0.05,1.05],
                  ))
plots.append(Plot(name      = "Discriminator_of_NonPrompt",
                  texX      = 'NonPrompt Discriminator', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.prob_isNonPrompt,
                  binning   = [100,-0.05,1.05],
                  ))
plots.append(Plot(name      = "Discriminator_of_Fake",
                  texX      = 'Fake Discriminator', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.prob_isFake,
                  binning   = [100,-0.05,1.05],
                  ))

if args.ncat == 4: 
    plots.append(Plot(name      = "Discriminator_of_SUSY",
                  texX      = 'SUSY Discriminator', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.prob_lep_isFromSUSYandHF,
                  binning   = [100,-0.05,1.05],
                  ))

elif args.ncat == 5:
    plots.append(Plot(name      = "Discriminator_of_SUSYHF",
                      texX      = 'SUSYHF Discriminator', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.prob_isFromSUSYHF,
                      binning   = [100,-0.05,1.05],
                      ))

    plots.append(Plot(name      = "Discriminator_of_SUSY",
                  texX      = 'SUSY Discriminator', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.prob_isFromSUSY,
                  binning   = [100,-0.05,1.05],
                  ))

plotting.fill(plots, read_variables = read_variables)

if args.normalize:
    logger.info("Normalizing... you really want this?")
    if args.ncat == 5:
        scaling = {0:3, 1:3, 2:3, 4:3}
    elif args.ncat == 4:
        scaling = {0:3, 1:3, 2:3}
else:
    scaling = {}

for plot in plots:
    plotting.draw(plot, 
                  plot_directory = os.path.join(plot_directory, 'Training_v6', subdir),
                  ratio          = None, 
                  logX           = False, 
                  logY           = True,
                  sorting        = True,
                  scaling        = scaling, 
                  yRange         = (1.0, "auto"),
                  #legend         = "auto"
                  #drawObjects    = drawObjects( )
                  copyIndexPHP   = True,
                  extensions     = ["png", "pdf", "root"]
                                              )

logger.info("%f s per file, %f total", (time.time()-t0)/len(data_sample.files), time.time()-t0)
