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
args = argParser.parse_args()



#
# Logger
#
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

redirector = "root://eos.grid.vbc.ac.at/"

directory = [
        #"/eos/vbc/user/maximilian.moser/DeepLepton/v2/step2/2016/muo/pt_3.5_-1/DYvsQCD/",
        "/scratch-cbe/users/maximilian.moser/DeepLepton/v2/step2/2016/ele/pt_5_-1/Top/"
        ]

t0 = time.time()
data_sample = Sample.fromDirectory(
        "step2",
        #directory = "/scratch-cbe/users/maximilian.moser/DeepLepton/v1_small/step1/2016/muo/Fake/pt_5_-1/DYJetsToLL_M50_LO/", 
        directory = directory,
        treeName  = "tree"
        )

logger.info("%i files", len(data_sample.files))

if args.small:
    data_sample.reduceFiles( to = 4 )

# copy samples:

samplePrompt               = deepcopy(data_sample)
samplePrompt.setSelectionString("lep_isPromptId_Training==1")
samplePrompt.texName       = "Prompt"
samplePrompt.Name          = "Prompt"
samplePrompt.style         = styles.lineStyle(ROOT.kBlack)

sampleNonPrompt            = deepcopy(data_sample)
sampleNonPrompt.setSelectionString("lep_isNonPromptId_Training==1")
sampleNonPrompt.texName    = "NonPrompt"
sampleNonPrompt.Name       = "NonPrompt"
sampleNonPrompt.style      = styles.lineStyle(ROOT.kBlue)

sampleFake                 = deepcopy(data_sample)
sampleFake.setSelectionString("lep_isFakeId_Training==1")
sampleFake.texName         = "Fake"
sampleFake.Name            = "Fake"
sampleFake.style           = styles.lineStyle(ROOT.kGreen)


read_variables = [
'lep_pt/F',
'lep_eta/F',
'lep_phi/F',
'lep_pdgId/F',
'lep_cutBased/F',
'lep_miniPFRelIso_all/F',
'lep_pfRelIso03_all/F',
'lep_sip3d/F',
'lep_lostHits/F',
'lep_convVeto/F',
'lep_dxy/F',
'lep_dz/F',
'lep_charge/F',
'lep_deltaEtaSC/F',
'lep_vidNestedWPBitmap/F',
'lep_dr03EcalRecHitSumEt/F',
'lep_dr03HcalDepth1TowerSumEt/F',
'lep_dr03TkSumPt/F',
'lep_dxyErr/F',
'lep_dzErr/F',
'lep_eCorr/F',
'lep_eInvMinusPInv/F',
'lep_energyErr/F',
'lep_hoe/F',
'lep_ip3d/F',
'lep_jetPtRelv2/F',
'lep_jetRelIso/F',
'lep_miniPFRelIso_chg/F',
'lep_mvaFall17V2noIso/F',
'lep_pfRelIso03_chg/F',
'lep_r9/F',
'lep_sieie/F',
'lep_genPartFlav/F',
'npfCand_charged/I',
'npfCand_neutral/I',
'npfCand_photon/I',
'npfCand_electron/I',
'npfCand_muon/I',
'nSV/I',                
]


stack = Stack([samplePrompt], [sampleNonPrompt], [sampleFake])

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

plots.append(Plot(name      = "lep_cutBased", #
                  texX      = 'cutBased', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_cutBased,
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

plots.append(Plot(name      = "lep_lostHits",
                  texX      = 'lostHits', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_lostHits,
                  binning   = [8,0,8],
                  ))
plots.append(Plot(name      = "lep_convVeto",
                  texX      = 'convVeto', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_convVeto,
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
                  binning   = [100,0,30],
                  ))
plots.append(Plot(name      = "lep_ip3d_zoom",
                  texX      = 'ip3d', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_ip3d,
                  binning   = [100,0,2],
                  ))

plots.append(Plot(name      = "lep_deltaEtaSC",
                  texX      = 'deltaEtaSC', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_deltaEtaSC,
                  binning   = [100,0,5],
                  ))
plots.append(Plot(name      = "lep_vidNestedWPBitmap",
                  texX      = 'vidNestedWPBitmap', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_vidNestedWPBitmap,
                  binning   = [100,200000000,608000000],
                  ))
plots.append(Plot(name      = "lep_dr03EcalRecHitSumEt",
                  texX      = 'dr03EcalRecHitSumEt', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_dr03EcalRecHitSumEt,
                  binning   = [100,0,100],
                  ))
plots.append(Plot(name      = "lep_dr03HcalDepth1TowerSumEt",
                  texX      = 'dr03HcalDepth1TowerSumEt', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_dr03HcalDepth1TowerSumEt,
                  binning   = [100,0,100],
                  ))
plots.append(Plot(name      = "lep_dr03TkSumPt",
                  texX      = 'dr03TkSumPt', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_dr03TkSumPt,
                  binning   = [100,0,100],
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

plots.append(Plot(name      = "lep_mvaFall17V2noIso",
                  texX      = 'mvaFall17V2noIso', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_mvaFall17V2noIso,
                  binning   = [100,0,1],
                  ))

plots.append(Plot(name      = "lep_eCorr",
                  texX      = 'eCorr', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_eCorr,
                  binning   = [100,0,2.5],
                  ))

plots.append(Plot(name      = "lep_eInvMinusPInv",
                  texX      = 'eInvMinusPInv', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_eInvMinusPInv,
                  binning   = [100,-3,3],
                  ))

plots.append(Plot(name      = "lep_energyErr",
                  texX      = 'energyErr', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_energyErr,
                  binning   = [100,0,100],
                  ))

plots.append(Plot(name      = "lep_hoe",
                  texX      = 'hoe', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_hoe,
                  binning   = [100,0,100],
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

plots.append(Plot(name      = "lep_r9",
                  texX      = 'r9', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_r9,
                  binning   = [100,0,30],
                  ))

plots.append(Plot(name      = "lep_sieie",
                  texX      = 'sieie', texY = 'Number of Events ',
                  attribute = lambda event, sample: event.lep_sieie,
                  binning   = [100,0,0.1],
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
                  plot_directory = os.path.join(plot_directory, "2016_ele_Top"),#args.plot_directory),
                  ratio          = None, 
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
