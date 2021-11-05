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
#argParser.add_argument('--plot_directory', action='store',      default='FourMuonInvariantMass')
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

logger.info("starting plot.py")

redirector = "root://eos.grid.vbc.ac.at/"

subdirs = ["Fake/", "FromSUSY/", "FromSUSYHF/", "NonPrompt/", "Prompt/"]
# dietrich_step1_files = "/eos/vbc/user/dietrich.liko/DeepLepton/v0/step1/2017/muo/"
# directory = [os.path.join(dietrich_step1_files, subdir, "pt_3.5_-1/CompSUSY/") for subdir in subdirs]
# directory = [
        # "/eos/vbc/user/benjamin.wilhelmy/DeepLepton/v1/step2/2016/muo/pt_3.5_-1/DYvsQCD/",
        # "/eos/vbc/user/benjamin.wilhelmy/DeepLepton/v1_compr_stop/step1/2017/muo/NonPrompt/pt_3_-1/stopCompr/Sample_0/",
        # "/eos/vbc/user/benjamin.wilhelmy/DeepLepton/v1_compr_stop/step1/2017/muo/Prompt/pt_3_-1/stopCompr/Sample_0/",
        # "/eos/vbc/user/benjamin.wilhelmy/DeepLepton/v1_compr_stop/step1/2017/muo/Fake/pt_3_-1/stopCompr/Sample_0/"
        #"/eos/vbc/user/dietrich.liko/DeepLepton/v0/step1/2017/muo/FromSUSYHF/pt_3.5_-1/CompSUSY/
#        ]
directory = args.path
t0 = time.time()
data_sample = Sample.fromDirectory(
        "step2",
        directory = directory,
        treeName  = "tree"
        )

logger.info("%i files", len(data_sample.files))

small_nfiles = 10
if args.small:
    data_sample.reduceFiles( to = small_nfiles )

# copy samples:



if args.ncat == 5: 
    sampleLHS               = deepcopy(data_sample)
    sampleLHS.setSelectionString("prob_isFromSUSY<0.4")
    sampleLHS.texName       = "Prob SUSY < 0.4"
    sampleLHS.Name          = "Prob SUSY < 0.4"
    sampleLHS.style         = styles.lineStyle(ROOT.kBlack)
    
    sampleRHS            = deepcopy(data_sample)
    sampleRHS.setSelectionString("prob_isFromSUSY>=0.4")
    sampleRHS.texName    = "Prob SUSY >= 0.4"
    sampleRHS.Name       = "Prob SUSY >= 0.4"
    sampleRHS.style      = styles.lineStyle(ROOT.kBlue)


    stack = Stack([sampleLHS], [sampleRHS])
elif args.ncat == 4: 
    sampleLHS               = deepcopy(data_sample)
    sampleLHS.setSelectionString("prob_lep_isFromSUSYandHF<0.5")
    sampleLHS.texName       = "Prob SUSY < 0.5"
    sampleLHS.Name          = "Prob SUSY < 0.5"
    sampleLHS.style         = styles.lineStyle(ROOT.kBlack)
    
    sampleRHS            = deepcopy(data_sample)
    sampleRHS.setSelectionString("prob_lep_isFromSUSYandHF>=0.5")
    sampleRHS.texName    = "Prob SUSY >= 0.5"
    sampleRHS.Name       = "Prob SUSY >= 0.5"
    sampleRHS.style      = styles.lineStyle(ROOT.kBlue)

    stack = Stack([sampleLHS], [sampleRHS])
logger.info("copied samples successfully")
logger.info("\n please check if TLeaf has the right type F or D check code it makes a difference!")

read_variables =[
            'lep_pt/F',                   # 0 
            'lep_eta/F',                  # 1
            'lep_phi/F',                  # 2
            'lep_mediumId/F',             # 3
            'lep_miniPFRelIso_all/F',     # 4
            'lep_sip3d/F',                # 5
            'lep_dxy/F',                  # 6
            'lep_dz/F',
            'lep_charge/F',
            'lep_dxyErr/F',
            'lep_dzErr/F',
            'lep_ip3d/F',
            'lep_jetPtRelv2/F',
            'lep_jetRelIso/F',
            'lep_miniPFRelIso_chg/F',
            'lep_mvaLowPt/F',
            'lep_nStations/F',
            'lep_nTrackerLayers/F',
            'lep_pfRelIso03_all/F',
            'lep_pfRelIso03_chg/F',
            'lep_pfRelIso04_all/F',
            'lep_ptErr/F',
            'lep_segmentComp/F',
            'lep_tkRelIso/F',
            'lep_tunepRelPt/F', ]

# this is needed since prediction TLeafes have type D!
if args.ncat == 4:
    read_variables = ["lep_pt/D",
		          "lep_eta/D",
                  "lep_phi/D",
                  "lep_mediumId/D",
                  "lep_miniPFRelIso_all/D",
                  "lep_sip3d/D",
                  "lep_dxy/D",
                  "lep_dz/D",
                  "lep_charge/D",
                  "lep_dxyErr/D",
                  "lep_dzErr/D",
                  "lep_ip3d/D",
                  "lep_jetPtRelv2/D",
                  "lep_jetRelIso/D",
                  "lep_miniPFRelIso_chg/D",
                  "lep_mvaLowPt/D",
                  "lep_nStations/D",
                  "lep_nTrackerLayers/D",
                  "lep_pfRelIso03_all/D",
                  "lep_pfRelIso03_chg/D",
                  "lep_pfRelIso04_all/D",
                  "lep_ptErr/D",
                  "lep_segmentComp/D",
                  "lep_tkRelIso/D",
                  "lep_tunepRelPt/D",]

# Use some defaults
Plot.setDefaults(stack = stack)

plots = []

plots.append(Plot(name      = "lep_pt_predict_data",
                  texX      = 'p_{T}(l)', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_pt,
                  binning   = [100,0,210],                  
                  ))
plots.append(Plot(name      = "lep_eta_predict_data",
                  texX      = 'eta', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_eta,
                  binning   = [100,0,3],
                  ))

plots.append(Plot(name      = "lep_phi_predict_data",
                  texX      = 'phi', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_phi,
                  binning   = [100,0,4],
                  ))


plots.append(Plot(name      = "lep_mediumId_predict_data",
                  texX      = 'mediumId', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_mediumId,
                  binning   = [100,0,5],
                  ))

plots.append(Plot(name      = "lep_miniPFRelIso_all_predict_data",
                  texX      = 'miniPFRelIso_all', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_miniPFRelIso_all,
                  binning   = [100,0,20],
                  ))

plots.append(Plot(name      = "lep_sip3d_predict_data",
                  texX      = 'sip3d', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_sip3d,
                  binning   = [100,0,5000],
                  ))

plots.append(Plot(name      = "lep_dxy_predict_data",
                  texX      = 'dxy', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_dxy,
                  binning   = [100,-5,5],# -5,5
                  ))

plots.append(Plot(name      = "lep_dxy_zoom_predict_data",
                  texX      = 'dxy', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_dxy,
                  binning   = [100,-0.05,0.05],# -5,5
                  ))

plots.append(Plot(name      = "lep_dz_predict_data",
                  texX      = 'dz', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_dz,
                  binning   = [100,-50,50], # -0.1,0.1
                  ))

plots.append(Plot(name      = "lep_dz_zoom_predict_data",
                  texX      = 'dz', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_dz,
                  binning   = [100,-1,1], # -0.1,0.1
                  ))

plots.append(Plot(name      = "lep_charge_predict_data",
                  texX      = 'charge', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_charge,
                  binning   = [100,-2,2],
                  ))

plots.append(Plot(name      = "lep_dxyErr_predict_data",
                  texX      = 'dxyErr', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_dxyErr,
                  binning   = [100,0,1],
                  ))

plots.append(Plot(name      = "lep_dzErr_predict_data",
                  texX      = 'dzErr', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_dzErr,
                  binning   = [100,0,15],
                  ))

plots.append(Plot(name      = "lep_ip3d_predict_data",
                  texX      = 'ip3d', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_ip3d,
                  binning   = [100,-1,30],
                  ))

plots.append(Plot(name      = "lep_jetPtRelv2_predict_data",
                  texX      = 'jetPtRelv2', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_jetPtRelv2,
                  binning   = [100,-10,300],
                  ))

plots.append(Plot(name      = "lep_jetRelIso_predict_data",
                  texX      = 'jetRelIso', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_jetRelIso,
                  binning   = [100,0,30],
                  ))

plots.append(Plot(name      = "lep_miniPFRelIso_chg_predict_data",
                  texX      = 'miniPFRelIso_chg', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_miniPFRelIso_chg,
                  binning   = [100,0,15],
                  ))

plots.append(Plot(name      = "lep_mvaLowPt_predict_data",
                  texX      = 'mvaLowPt', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_mvaLowPt,
                  binning   = [100,-1,1],
                  ))

plots.append(Plot(name      = "lep_nStations_predict_data",
                  texX      = 'nStations', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_nStations,
                  binning   = [100,0,10],
                  ))

plots.append(Plot(name      = "lep_nTrackerLayers_predict_data",
                  texX      = 'nTrackerLayers', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_nTrackerLayers,
                  binning   = [20,0,20],
                  ))

plots.append(Plot(name      = "lep_pfRelIso03_all_predict_data",
                  texX      = 'pfRelIso03_all', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_pfRelIso03_all,
                  binning   = [100,0,30],
                  ))

plots.append(Plot(name      = "lep_pfRelIso03_chg_predict_data",
                  texX      = 'pfRelIso03_chg', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_pfRelIso03_chg,
                  binning   = [100,0,30],
                  ))

plots.append(Plot(name      = "lep_pfRelIso04_all_predict_data",
                  texX      = 'pfRelIso04_all', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_pfRelIso04_all,
                  binning   = [100,0,30],
                  ))

plots.append(Plot(name      = "lep_ptErr_predict_data",
                  texX      = 'ptErr', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_ptErr,
                  binning   = [100,0,40],
                  ))

plots.append(Plot(name      = "lep_segmentComp_predict_data",
                  texX      = 'segmentComp', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_segmentComp,
                  binning   = [50,0,1],
                  ))

plots.append(Plot(name      = "lep_tkRelIso_predict_data",
                  texX      = 'tkRelIso', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_tkRelIso,
                  binning   = [100,0,40],
                  ))

plots.append(Plot(name      = "lep_tunepRelPt_predict_data",
                  texX      = 'tunepRelPt', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_tunepRelPt,
                  binning   = [100,0,50],
                  ))


plotting.fill(plots, read_variables = read_variables)
if args.normalize:
        scaling = {0:1}
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

if args.special_output_path:
    subdir = args.special_output_path
else:
    subdir = directory.split('/')[-2]
output_path = os.path.join(plot_directory,
                      'Training_v6',
                      subdir,
                      "Investigating_training_with_features_plots" + ("_small" if args.small else "") + \
                      ("_normalized" if args.normalize else ""))

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

logger.info("%f s per file, %f total", (time.time()-t0)/len(sampleLHS.files), time.time()-t0)
