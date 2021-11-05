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

argParser.add_argument('--plot_predictdata', action='store_true', default=False,
                        help="reduces the plot variables to 2")

argParser.add_argument('--path', action='store', required=True, help="Path to root files to plot")

argParser.add_argument('--ncat',
                        action='store',
                        required=True,
                        type = int,
                        help="how many lepton classes (4 or 5)?")

argParser.add_argument('--special_output_path',
                        action='store',
                        default="",
                        help="path for output if one doesnt want the default one" )

argParser.add_argument('--step1',
                        action = 'store',
                        choices = ["Top", "DY", "FromSUSY"],
                        default = "",
                        help = "Do you want to plot step1 data?\
                                Then path is to the Fake, Prompt, ... Dirs.")

argParser.add_argument('--predictOnSample',
                        action = 'store',
                        default = "",
                        type = str,
                        help = "Do you want to plot predictOnSample data?\
                                If yes, give sample name and give the path up to \
                                the sample directory (same name as the sample)")


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

# dietrich_step1_files = "/eos/vbc/user/dietrich.liko/DeepLepton/v0/step1/2017/muo/"
# directory = [os.path.join(dietrich_step1_files, subdir, "pt_3.5_-1/CompSUSY/") for subdir in subdirs]
# directory = [
        # "/eos/vbc/user/benjamin.wilhelmy/DeepLepton/v1/step2/2016/muo/pt_3.5_-1/DYvsQCD/",
        # "/eos/vbc/user/benjamin.wilhelmy/DeepLepton/v1_compr_stop/step1/2017/muo/NonPrompt/pt_3_-1/stopCompr/Sample_0/",
        # "/eos/vbc/user/benjamin.wilhelmy/DeepLepton/v1_compr_stop/step1/2017/muo/Prompt/pt_3_-1/stopCompr/Sample_0/",
        # "/eos/vbc/user/benjamin.wilhelmy/DeepLepton/v1_compr_stop/step1/2017/muo/Fake/pt_3_-1/stopCompr/Sample_0/"
        #"/eos/vbc/user/dietrich.liko/DeepLepton/v0/step1/2017/muo/FromSUSYHF/pt_3.5_-1/CompSUSY/
#        ]
DY = ["DYJetsToLL_M10to50_LO",
      "DYJetsToLL_M50_LO          ",
      "DYJetsToLL_M4to50_HT100to200_LO    ",
      "DYJetsToLL_M50_NLO         ",
      "DYJetsToLL_M4to50_HT200to400_LO    ",
      "DYJetsToLL_M4to50_HT400to600_LO    ",
      "DYJetsToLL_M4to50_HT600toInf_LO",
      "DYJetsToLL_M4to50_HT70to100_LO     ",
      "DYJetsToLL_M50_HT100to200_LO  ",
      "DYJetsToLL_M50_HT1200to2500_LO     ",
      "DYJetsToLL_M50_HT200to400_LO ",
      "DYJetsToLL_M50_HT2500toInf_LO      ",
      "DYJetsToLL_M50_HT400to600_LO     ",
      "DYJetsToLL_M50_HT400to600_LO_ext2",
      "DYJetsToLL_M50_HT600to800_LO       ",
      "DYJetsToLL_M50_HT70to100_LO        ",
      "DYJetsToLL_M50_HT800to1200_LO"]
    
Top =  [# 'ST_schannel_4f_NLO',
              # 'ST_schannel_4f_NLO_PS',
              # 'ST_tchannel_antitop_4f_incl_pow',
              # 'ST_tchannel_antitop_5f_pow_PS',
              # 'ST_tchannel_antitop_5f_pow_PS_old_pmx',
              # 'ST_tchannel_top_4f_incl_pow',
              # 'ST_tchannel_top_5f_pow',
              # 'ST_tchannel_top_5f_pow_old_pmx',
              # 'ST_tW_antitop_incl_5f_pow',
              # 'ST_tW_antitop_incl_5f_pow_PS',
              # 'ST_tW_antitop_NoFullyHad_5f_pow_PS',
              # 'ST_tW_top_incl_5f_pow',
              # 'ST_tW_top_incl_5f_pow_PS',
              # 'ST_tW_top_NoFullyHad_5f_pow',
              # 'ST_tW_top_NoFullyHad_5f_pow_PS',
              # 'ST_tWll_5f_LO',
              # 'ST_tWnunu_5f_LO',
              # 'TTHH_LO',
              # 'TTJets_dilep_genMET150_LO',
              # 'TTJets_dilep_LO',
              # 'TTJets_HT1200to2500_LO',
              # 'TTJets_HT2500toInf_LO',
              # 'TTJets_HT600to800_LO',
              # 'TTJets_HT800to1200_LO',
              # 'TTJets_LO',
              # 'TTJets_NLO',
              # 'TTJets_semilepFromT_genMET150_LO',
              # 'TTJets_semilepFromT_LO',
              # 'TTJets_semilepFromTbar_genMET150_LO',
              # 'TTJets_semilepFromTbar_LO',
              # 'TTTo2L2Nu_pow',
              # 'TTTo2L2Nu_pow_PS',
              # 'TTToSemiLeptonic_pow',
              # 'TTToSemiLeptonic_pow_PS',
              # 'TTWH_LO',
              # 'TTWW_LO',
              # 'TTWZ_LO',
              # 'TTZH_LO',
              # 'TTZZ_LO', 
              'ST_schannel_LO',
              'ST_tW_antitop_pow',
              'ST_tW_top_pow',
              'ST_tWll_LO',
              'ST_tWnunu_LO',
              'ST_tchannel_antitop_4f_pow',
              'ST_tchannel_top_4f_pow',
              'TGJets_lep_NLO',
              'TTTo2L2Nu_pow',
              'TTZJets_LO',
              'TT_LO',
              'TT_dilep_NLO',
              ]

FromSUSY = ["Stop600-dm20-006", "Stop600-dm10-006", "Stop250-dm20-006", "Stop250-dm10-006"]
# if one wants to plot step1 data...
if args.step1 != "":
    sample_list = eval(args.step1)
# /eos/vbc/experiments/cms/store/user/liko/skims/v3/step1/2018/muo/Prompt/pt_3.5_-1

    # dirs = os.listdir(args.path)
    # directories = []
    # for directory in dirs:
    #     if os.path.isdir(directory):
    #         directories.append(directory)
    subdirs = ["Fake/", "NonPrompt/", "Prompt/"]
    if args.step1 == "FromSUSY":
        subdirs.extend(["FromSUSY/", "FromSUSYHF/"])
        logger.info("Searching in subdirs {}".format(subdirs))
    # subdirs = ["Fake/", "FromSUSY/", "FromSUSYHF/", "NonPrompt/", "Prompt/"]
    # sample_name = "Stop600-dm20-006" #Stop250-dm20-006  Stop600-dm10-006  Stop600-dm20-006
    directory = []
    for sample_name in sample_list:
        directory.extend([os.path.join(args.path, subdir, "pt_3.5_-1", sample_name) for subdir in subdirs])
    logger.info("Plotting step1 data from paths {}".format(directory))
    sample_name = args.step1
    
elif args.predictOnSample != "":
    sample_name = args.predictOnSample
    directory = os.path.join(args.path, sample_name)
    logger.info("Plotting predictOnSample data from path {}".format(directory))


else:
    directory = args.path
    sample_name = "data"

t0 = time.time()
data_sample = Sample.fromDirectory(
        sample_name,
        directory = directory,
        # redirector=redirector,
        treeName  = "tree"
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
sampleFake.style           = styles.lineStyle(ROOT.kGreen + 1)

if args.ncat == 5: 
    sampleSUSY                 = deepcopy(data_sample)
    sampleSUSY.setSelectionString("lep_isFromSUSY_Training==1") #lep_isFromSUSY_Training/I
    sampleSUSY.texName         = "FromSUSY"
    sampleSUSY.Name            = "FromSUSY"
    sampleSUSY.style           = styles.lineStyle(ROOT.kRed)
    
    sampleSUSYHF                 = deepcopy(data_sample)
    sampleSUSYHF.setSelectionString("lep_isFromSUSYHF_Training==1")
    sampleSUSYHF.texName         = "FromSUSYHF"
    sampleSUSYHF.Name            = "FromSUSYHF"
    sampleSUSYHF.style           = styles.lineStyle(ROOT.kMagenta)

    if args.predictOnSample != "":
        raise NotImplemented()

    stack = Stack([samplePrompt], [sampleNonPrompt], [sampleFake], [sampleSUSY], [sampleSUSYHF])

elif args.ncat == 4: 
    sampleSUSY                 = deepcopy(data_sample)
    sampleSUSY.setSelectionString("lep_isFromSUSYandHF_Training==1") #lep_isFromSUSY_Training/I
    sampleSUSY.texName         = "FromSUSY"
    sampleSUSY.Name            = "FromSUSY"
    sampleSUSY.style           = styles.lineStyle(ROOT.kRed)

    if args.predictOnSample != "":
        print("we are plotting predictOnSample data")
        # TODO: when changed in predictOnSample change lep_precut/I!
        read_variables += ["lep_StopsCompressed/I", "lep_precut/F", "lep_probPrompt/F",
                            "lep_probNonPrompt/F", "lep_probFake/F", "prob_lep_isFromSUSYandHF/F"]

        sampleStopsCompressed = deepcopy(data_sample)
        sampleStopsCompressed.setSelectionString("lep_StopsCompressed==1")
        sampleStopsCompressed.texName         = "isStopsCompressed"
        sampleStopsCompressed.Name            = "isStopsCompressed"
        sampleStopsCompressed.style           = styles.lineStyle(ROOT.kMagenta)

        stack = Stack([samplePrompt], 
                        [sampleNonPrompt], 
                        [sampleFake], 
                        [sampleSUSY], 
                        [sampleStopsCompressed])

    else:
        stack = Stack([samplePrompt], 
                        [sampleNonPrompt], 
                        [sampleFake], 
                        [sampleSUSY])
else:
    stack = Stack([samplePrompt], [sampleNonPrompt], [sampleFake])

logger.info("copied samples successfully")


if args.plot_predictdata:
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
# This is a static memberfunc
Plot.setDefaults(stack = stack)

plots = []

if not args.plot_predictdata:
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
    
#     plots.append(Plot(name      = "lep_isFromSUSYandHF_Training",
#                       texX      = 'lep_isFromSUSYandHF_Training', texY = 'Number of Events ',
#                       attribute = lambda event, sample: event.lep_isFromSUSYandHF_Training,
#                       binning   = [100,0,1.5],
#                       ))
################################
    if args.predictOnSample != "":
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






else:
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
    
    plots.append(Plot(name      = "lep_dxy_big_range",
                      texX      = 'dxy', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_dxy,
                      binning   = [100,-250,250],# -5, 5
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
                      binning   = [100,0,1],
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

if args.predictOnSample != "":
    logger.info("making special output name for predict on sample")
    subdir = directory.split('/')[-6]
    output_path = os.path.join(plot_directory,
                          'Training_v6', # the old ones: Training, Training_v4
                          subdir,
                          "predict_data_plots",
                          args.predictOnSample + ("_small" if args.small else "") + \
                          ("_normalized" if args.normalize else ""))

elif args.step1 != "":
    output_path = os.path.join(plot_directory,
                          "{}_v6_step1".format(args.step1), 
                          "lep" + ("{}_small".format(small_nfiles) if args.small else "") + \
                          ("_normalized" if args.normalize else ""))



elif args.special_output_path:
    output_path = args.special_output_path
    logger.info("found special output_path will use {} as outputpath".format(output_path))


elif args.plot_predictdata:
    subdir = directory.split('/')[-2]
    output_path = os.path.join(plot_directory,
                          'Training_v6', # the old ones: Training, Training_v4
                          subdir,
                          "predict_data_plots" + ("_small" if args.small else "") + \
                          ("_normalized" if args.normalize else ""))


else:
    output_path = os.path.join(plot_directory, 
                            "TTbar",
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
