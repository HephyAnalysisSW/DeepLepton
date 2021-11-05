import ROOT
ROOT.gROOT.SetBatch(True)
from math import sqrt, cos, sin, pi, cosh
from RootTools.core.standard import *
import os
from copy import deepcopy
import Analysis.Tools.syncer as syncer
import time
from DeepLepton.Tools.user import plot_directory
import argparse

argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',
                action='store',
                default='INFO',
                nargs='?',
                choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'],
                help="Log level for logging")

argParser.add_argument('--small',
                action='store_true',
                help="Run the file on a small sample (for test purpose), bool flag set to True if used" )

argParser.add_argument('--normalize',
                        action='store_true',
                        help="If True all histos will have the same area (The same as the 4th histo)")

argParser.add_argument('--path', action='store', required=True, help="Path to root files to plot")

argParser.add_argument('--ncat',
                        action='store',
                        required=True,
                        type = int,
                        help="how many lepton classes (4 or 5)?")


args = argParser.parse_args()



#
# Logger
#
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

logger.info("starting plot.py")

redirector = "root://eos.grid.vbc.ac.at/"

directory = args.path
sample_name = "data"

t0 = time.time()
data_sample = Sample.fromDirectory(
        sample_name,
        directory = directory,
        # redirector=redirector,
        treeName  = "tree",
        selectionString = "lep_precut==1"
        )

logger.info("%i files", len(data_sample.files))

small_nfiles = 10
if args.small:
    logger.info("start shuffeling samples")
    list_of_samples = data_sample.split(n=10, shuffle = True)
    data_sample = Sample.combine(name=data_sample.name, samples=list_of_samples)
    logger.info("done shuffeling")
    data_sample.reduceFiles( to = small_nfiles )

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
                  #"lep_isFromSUSYandHF_Training/I",
                 ]

# copy samples:

samplePrompt               = deepcopy(data_sample)
samplePrompt.setSelectionString("lep_precut==1 && lep_isPromptId_Training==1")
samplePrompt.texName       = "Prompt"
samplePrompt.Name          = "Prompt"
samplePrompt.style         = styles.lineStyle(ROOT.kBlack)

sampleNonPrompt            = deepcopy(data_sample)
sampleNonPrompt.setSelectionString("lep_precut==1 && lep_isNonPromptId_Training==1")
sampleNonPrompt.texName    = "NonPrompt"
sampleNonPrompt.Name       = "NonPrompt"
sampleNonPrompt.style      = styles.lineStyle(ROOT.kBlue)

sampleFake                 = deepcopy(data_sample)
sampleFake.setSelectionString("lep_precut==1 && lep_isFakeId_Training==1")
sampleFake.texName         = "Fake"
sampleFake.Name            = "Fake"
sampleFake.style           = styles.lineStyle(ROOT.kGreen + 1)

if args.ncat == 5: 
    sampleSUSY                 = deepcopy(data_sample)
    sampleSUSY.setSelectionString("lep_precut==1 && lep_isFromSUSY_Training==1") #lep_isFromSUSY_Training/I
    sampleSUSY.texName         = "FromSUSY"
    sampleSUSY.Name            = "FromSUSY"
    sampleSUSY.style           = styles.lineStyle(ROOT.kRed)
    
    sampleSUSYHF                 = deepcopy(data_sample)
    sampleSUSYHF.setSelectionString("lep_precut==1 && lep_isFromSUSYHF_Training==1")
    sampleSUSYHF.texName         = "FromSUSYHF"
    sampleSUSYHF.Name            = "FromSUSYHF"
    sampleSUSYHF.style           = styles.lineStyle(ROOT.kMagenta)


    stack = Stack([samplePrompt], [sampleNonPrompt], [sampleFake], [sampleSUSY], [sampleSUSYHF])

elif args.ncat == 4: 
    sampleSUSY                 = deepcopy(data_sample)
    sampleSUSY.setSelectionString("lep_precut==1 && lep_isFromSUSYandHF_Training==1") #lep_isFromSUSY_Training/I
    sampleSUSY.texName         = "FromSUSY"
    sampleSUSY.Name            = "FromSUSY"
    sampleSUSY.style           = styles.lineStyle(ROOT.kRed)

    read_variables += ["lep_StopsCompressed/I", "lep_precut/F", "lep_probPrompt/F",
                        "lep_probNonPrompt/F", "lep_probFake/F", "prob_lep_isFromSUSYandHF/F"]

    sampleStopsCompressed = deepcopy(data_sample)
    sampleStopsCompressed.setSelectionString("lep_precut==1 && lep_StopsCompressed==1")
    sampleStopsCompressed.texName         = "isStopsCompressed"
    sampleStopsCompressed.Name            = "isStopsCompressed"
    sampleStopsCompressed.style           = styles.lineStyle(ROOT.kMagenta)

    stack = Stack([samplePrompt], 
                    [sampleNonPrompt], 
                    [sampleFake], 
                    [sampleSUSY], 
                    [sampleStopsCompressed])

else:
    stack = Stack([samplePrompt], [sampleNonPrompt], [sampleFake])

logger.info("copied samples successfully")



# Use some defaults
# This is a static memberfunc
Plot.setDefaults(stack = stack)

plots = []

plots.append(Plot(name      = "lep_pt",
                  texX      = 'p_{T}(l)', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_pt,
                  binning   = [100,0,210],                  
                  ))

plots.append(Plot(name      = "lep_eta",
                  texX      = 'eta', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_eta,
                  binning   = [100,0,3],
                  ))

plots.append(Plot(name      = "lep_phi",
                  texX      = 'phi', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_phi,
                  binning   = [100,0,4],
                  ))

plots.append(Plot(name      = "lep_pdgId",
                  texX      = 'pdgId', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_pdgId,
                  binning   = [100,0,20],
                  ))

plots.append(Plot(name      = "lep_mediumId",
                  texX      = 'mediumId', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_mediumId,
                  binning   = [100,0,5],
                  ))

plots.append(Plot(name      = "lep_miniPFRelIso_all",
                  texX      = 'miniPFRelIso_all', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_miniPFRelIso_all,
                  binning   = [100,0,1],
                  ))

plots.append(Plot(name      = "lep_pfRelIso03_all",
                  texX      = 'pfRelIso03_all', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_pfRelIso03_all,
                  binning   = [100,0,1],
                  ))

plots.append(Plot(name      = "lep_sip3d",
                  texX      = 'sip3d', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_sip3d,
                  binning   = [100,0,5000],
                  ))

plots.append(Plot(name      = "lep_dxy",
                  texX      = 'dxy', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_dxy,
                  binning   = [100,-5,5],# -5, 5
                  ))

plots.append(Plot(name      = "lep_dxy_zoom", #zoom
                  texX      = 'dxy', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_dxy,
                  binning   = [100,-0.05,0.05],# -0.05,0.05
                  ))

plots.append(Plot(name      = "lep_dz",
                  texX      = 'dz', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_dz,
                  binning   = [100,-50,50], # -0.1,0.1
                  ))

plots.append(Plot(name      = "lep_dz_zoom",
                  texX      = 'dz', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_dz,
                  binning   = [100,-1,1], # -0.1,0.1
                  ))

plots.append(Plot(name      = "lep_charge",
                  texX      = 'charge', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_charge,
                  binning   = [100,-2,2],
                  ))

plots.append(Plot(name      = "lep_dxyErr",
                  texX      = 'dxyErr', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_dxyErr,
                  binning   = [100,0,10], # 1
                  ))

plots.append(Plot(name      = "lep_dzErr",
                  texX      = 'dzErr', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_dzErr,
                  binning   = [100,0,15],
                  ))

plots.append(Plot(name      = "lep_ip3d",
                  texX      = 'ip3d', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_ip3d,
                  binning   = [100,-1,30],
                  ))

plots.append(Plot(name      = "lep_jetPtRelv2",
                  texX      = 'jetPtRelv2', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_jetPtRelv2,
                  binning   = [100,-10,300],
                  ))

plots.append(Plot(name      = "lep_jetRelIso",
                  texX      = 'jetRelIso', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_jetRelIso,
                  binning   = [100,0,1],
                  ))

plots.append(Plot(name      = "lep_miniPFRelIso_chg",
                  texX      = 'miniPFRelIso_chg', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_miniPFRelIso_chg,
                  binning   = [100,0,1],
                  ))

plots.append(Plot(name      = "lep_mvaLowPt",
                  texX      = 'mvaLowPt', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_mvaLowPt,
                  binning   = [100,0,1],
                  ))

plots.append(Plot(name      = "lep_nStations",
                  texX      = 'nStations', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_nStations,
                  binning   = [100,0,10],
                  ))

plots.append(Plot(name      = "lep_nTrackerLayers",
                  texX      = 'nTrackerLayers', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_nTrackerLayers,
                  binning   = [20,0,20],
                  ))

plots.append(Plot(name      = "lep_pfRelIso03_all",
                  texX      = 'pfRelIso03_all', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_pfRelIso03_all,
                  binning   = [100,0,1],
                  ))

plots.append(Plot(name      = "lep_pfRelIso03_chg",
                  texX      = 'pfRelIso03_chg', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_pfRelIso03_chg,
                  binning   = [100,0,1],
                  ))

plots.append(Plot(name      = "lep_pfRelIso04_all",
                  texX      = 'pfRelIso04_all', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_pfRelIso04_all,
                  binning   = [100,0,1],
                  ))

plots.append(Plot(name      = "lep_ptErr",
                  texX      = 'ptErr', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_ptErr,
                  binning   = [100,0,40],
                  ))

plots.append(Plot(name      = "lep_segmentComp",
                  texX      = 'segmentComp', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_segmentComp,
                  binning   = [50,0,1],
                  ))

plots.append(Plot(name      = "lep_tkRelIso",
                  texX      = 'tkRelIso', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_tkRelIso,
                  binning   = [100,0,1],
                  ))

plots.append(Plot(name      = "lep_tunepRelPt",
                  texX      = 'tunepRelPt', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_tunepRelPt,
                  binning   = [100,0,50],
                  ))

plots.append(Plot(name      = "lep_genPartFlav",
                  texX      = 'genPartFlav', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_genPartFlav,
                  binning   = [100,0,10],
                  ))

plots.append(Plot(name      = "npfCand_charged",
                  texX      = 'npfCand_charged', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.npfCand_charged,
                  binning   = [80,0,80],
                  ))

plots.append(Plot(name      = "npfCand_neutral",
                  texX      = 'npfCand_neutral', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.npfCand_neutral,
                  binning   = [20,0,20],
                  ))

plots.append(Plot(name      = "npfCand_photon", 
                  texX      = 'npfCand_photon', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.npfCand_photon,     
                  binning   = [40,0,40],
                  ))

plots.append(Plot(name      = "npfCand_electron",
                  texX      = 'npfCand_electron', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.npfCand_electron,      
                  binning   = [10,0,10],
                  ))

plots.append(Plot(name      = "npfCand_muon",
                  texX      = 'npfCand_muon', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.npfCand_muon,   
                  binning   = [10,0,10],
                  ))

plots.append(Plot(name      = "nSV",
                  texX      = 'nSV', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.nSV,
                  binning   = [10,0,20],
                  ))

plots.append(Plot(name      = "lep_preselection",
                  texX      = 'Preselection StopsCompressed', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_precut,
                  binning   = [100,-0.1, 1.1],
                  ))

plots.append(Plot(name      = "lep_isStopsCompressed",
                  texX      = 'lep_isStopsCompressed', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_StopsCompressed,
                  binning   = [100,-0.1, 1.1],
                  ))
                  
plots.append(Plot(name      = "lep_probFake",
                  texX      = 'Probability Fake', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_probFake,
                  binning   = [100,-0.1, 1.1],
                  ))

plots.append(Plot(name      = "lep_probPrompt",
                  texX      = 'Probability Prompt', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_probPrompt,
                  binning   = [100,-0.1, 1.1],
                  ))

plots.append(Plot(name      = "lep_probNonPrompt",
                  texX      = 'Probability NonPrompt', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_probNonPrompt,
                  binning   = [100,-0.1, 1.1],
                  ))

if args.ncat == 4:
    plots.append(Plot(name      = "lep_probisFromSUSYandHF",
                      texX      = 'Probability isFromSUSYandHF', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.prob_lep_isFromSUSYandHF,
                      binning   = [100,-0.1, 1.1],
                      ))
else:
    raise NotImplemented()



logger.info("filling plots")
plotting.fill(plots, read_variables = read_variables)
logger.info("done filling plots")
if args.normalize:
    if args.ncat == 5:
        scaling = {0:3, 1:3, 2:3, 4:3}
    elif args.ncat == 4: 
        scaling = {0:3, 1:3, 2:3}
else:
    scaling = {}
years = ["2016", "2017", "2018"]
year = []
for i in years:
    if i in directory:
        year.append(i)
if len(year)==1:
    logger.info("Found the year of the sample in directory, will use it for naming the outputfile")
    useyear = True
else:
    logger.info("Did not find a unique year in directory, the outputfile will not contain the year")
    useyear = False

output_path = os.path.join(plot_directory, 
                        "preselection_STop2vsTTbar",
                        "v9_unbalanced"+\
                        ("_args_small_nfiles_{} ".format(small_nfiles) if args.small else "")+\
                        ("_"+year[0] if useyear else "")+\
                        ("_normalized" if args.normalize else "")+\
                        ("_small" if "small" in directory else ""))#args.plot_directory),

logger.info("The output path is {}".format(output_path))
# if not os.path.isdir(output_path):
#     os.makedirs(output_path)
logger.info("making the plots")
for plot in plots:
    plotting.draw(plot, 
                  plot_directory = output_path, 
                  ratio          = None, 
                  scaling        = scaling,  
                  logX           = False, 
                  logY           = True,
                  sorting        = True, 
                  yRange         = (1.0, "auto"),
                  #legend         = "auto"
                  #drawObjects    = drawObjects( )
                  copyIndexPHP   = True,
                  extensions     = ["png", "pdf", "root"]
                                              )

logger.info("%f s per file, %f total", (time.time()-t0)/len(samplePrompt.files), time.time()-t0)
