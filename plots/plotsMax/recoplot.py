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

t0 = time.time()

if args.mode == 'Top':
    data_sample = Sample.fromDirectory(
        "Predicted",
        directory = directory,
        treeName  = "tree",
        selectionString="lep_precut==1",
        )
    if args.small:
        data_sample.reduceFiles( to = 4 )

elif args.mode == 'DYvsQCD':
    import os
    dirs = os.listdir( directory )
    directoriesDY  = [os.path.join(directory, d)  for d in dirs if "DY"  in d]
    directoriesQCD = [os.path.join(directory, d)  for d in dirs if "QCD" in d]
    
    # TODO: weight the samples
    sampleDY  = Sample.fromDirectory('DY',  directory=directoriesDY,
                                        treeName='tree',
                                        selectionString='lep_isPromptId_Training==1',
                                        weightString="luminosity*genWeight*xsec(sample) / Sum(genWeights)")
    sampleQCD = Sample.fromDirectory('QCD', directory=directoriesQCD,
                                        treeName='tree',
                                        selectionString='lep_isPromptId_Training==0',
                                        weightString="luminosity*genWeight*xsec(sample) / Sum(genWeights)")
    data_sample = Sample.combine("Predicted", [sampleDY])
    if args.small:
        sampleDY.reduceFiles( to = 4 )
        sampleQCD.reduceFiles( to = 4 )

logger.info("%i files", len(data_sample.files))


# copy samples:
wp = 0.993 # Working Point

# As Signal
if args.mode == 'Top':
    samplePromptSig               = deepcopy(data_sample)
    sampleNonPromptSig            = deepcopy(data_sample)
    sampleFakeSig                 = deepcopy(data_sample)
    samplePromptBack              = deepcopy(data_sample)
    sampleNonPromptBack           = deepcopy(data_sample)
    sampleFakeBack                = deepcopy(data_sample)
elif args.mode == 'DYvsQCD':
    samplePromptSig    = deepcopy(sampleDY)
    sampleNonPromptSig = deepcopy(sampleQCD)
    sampleFakeSig      = deepcopy(sampleQCD)
    samplePromptBack   = deepcopy(sampleDY)
    sampleNonPromptBack= deepcopy(sampleQCD)
    sampleFakeBack     = deepcopy(sampleQCD)

samplePromptSig.addSelectionString("lep_isPromptId_Training==1&&lep_probPrompt>{}".format(wp))
samplePromptSig.texName       = "Prompt as Signal"
samplePromptSig.Name          = "Prompt asSignal"
samplePromptSig.style         = styles.lineStyle(ROOT.kRed)

sampleNonPromptSig.addSelectionString("lep_isNonPromptId_Training==1&&lep_probPrompt>{}".format(wp))
sampleNonPromptSig.texName    = "NonPrompt as Signal"
sampleNonPromptSig.Name       = "NonPrompt as Signal"
sampleNonPromptSig.style      = styles.lineStyle(ROOT.kBlue)

sampleFakeSig.addSelectionString("lep_isFakeId_Training==1&&lep_probPrompt>{}".format(wp))
sampleFakeSig.texName         = "Fake as Signal"
sampleFakeSig.Name            = "Fake as Signal"
sampleFakeSig.style           = styles.lineStyle(ROOT.kGreen)

# As Background
samplePromptBack               = deepcopy(data_sample)
samplePromptBack.addSelectionString("lep_isPromptId_Training==1&&lep_probPrompt<{}".format(wp))
samplePromptBack.texName       = "Prompt as Background"
samplePromptBack.Name          = "Prompt as Background"
samplePromptBack.style         = styles.lineStyle(ROOT.kOrange)

sampleNonPromptBack            = deepcopy(data_sample)
sampleNonPromptBack.addSelectionString("lep_isNonPromptId_Training==1==1&&lep_probPrompt<{}".format(wp))
sampleNonPromptBack.texName    = "NonPrompt as Background"
sampleNonPromptBack.Name       = "NonPrompt as Background"
sampleNonPromptBack.style      = styles.lineStyle(ROOT.kOrange+7)

sampleFakeBack                 = deepcopy(data_sample)
sampleFakeBack.addSelectionString("lep_isFakeId_Training==1==1&&lep_probPrompt<{}".format(wp))
sampleFakeBack.texName         = "Fake as Background"
sampleFakeBack.Name            = "Fake as Background"
sampleFakeBack.style           = styles.lineStyle(ROOT.kAzure+7)


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
                 ]


stack = Stack([samplePromptSig], [sampleNonPromptSig], [sampleFakeSig], [samplePromptBack], [sampleNonPromptBack], [sampleFakeBack])

# Use some defaults
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
                  binning   = [100,0,20],
                  ))

plots.append(Plot(name      = "lep_pfRelIso03_all",
                  texX      = 'pfRelIso03_all', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_pfRelIso03_all,
                  binning   = [100,0,20],
                  ))

plots.append(Plot(name      = "lep_sip3d",
                  texX      = 'sip3d', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_sip3d,
                  binning   = [100,0,5000],
                  ))

plots.append(Plot(name      = "lep_dxy",
                  texX      = 'dxy', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_dxy,
                  binning   = [100,-5,5],# -0.05,0.05
                  ))

plots.append(Plot(name      = "lep_dxy_zoom",
                  texX      = 'dxy', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_dxy,
                  binning   = [100,-0.05,0.05],# -5,5
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
                  binning   = [100,0,1],
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
                  binning   = [100,0,30],
                  ))

plots.append(Plot(name      = "lep_miniPFRelIso_chg",
                  texX      = 'miniPFRelIso_chg', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_miniPFRelIso_chg,
                  binning   = [100,0,15],
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
                  binning   = [100,0,30],
                  ))

plots.append(Plot(name      = "lep_pfRelIso03_chg",
                  texX      = 'pfRelIso03_chg', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_pfRelIso03_chg,
                  binning   = [100,0,30],
                  ))

plots.append(Plot(name      = "lep_pfRelIso04_all",
                  texX      = 'pfRelIso04_all', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_pfRelIso04_all,
                  binning   = [100,0,30],
                  ))

plots.append(Plot(name      = "lep_ptErr",
                  texX      = 'ptErr', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_ptErr,
                  binning   = [100,0,40],
                  ))

plots.append(Plot(name      = "lep_segmentComp",
                  texX      = 'segmentComp', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_segmentComp,
                  binning   = [100,0,1],
                  ))

plots.append(Plot(name      = "lep_tkRelIso",
                  texX      = 'tkRelIso', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_tkRelIso,
                  binning   = [100,0,40],
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

plotting.fill(plots, read_variables = read_variables)

for plot in plots:
    plotting.draw(plot, 
                  plot_directory = os.path.join(plot_directory, "2016_muo_{}_Input_{}".format(args.mode, directory.split("/")[-2])),#args.plot_directory),
                  ratio          = None, 
                  logX           = False, 
                  logY           = True,
                  sorting        = True,
                  scaling        = {0:3, 1:3, 2:3, 3:3, 4:3, 5:3}, 
                  yRange         = (1.0, "auto"),
                  #legend         = "auto"
                  #drawObjects    = drawObjects( )
                  copyIndexPHP   = True,
                  extensions     = ["png", "pdf", "root"]
                                              )

logger.info("%f s per file, %f total", (time.time()-t0)/len(data_sample.files), time.time()-t0)
