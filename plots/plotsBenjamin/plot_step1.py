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

# argParser.add_argument('--ncat',
#                         action='store',
#                         required=True,
#                         type = int,
#                         help="how many lepton classes (4 or 5)?")

argParser.add_argument('--special_output_path',
                        action='store',
                        default="",
                        help="path for output if one doesnt want the default one" )

args = argParser.parse_args()



#
# Logger
#
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

logger.info("starting plot_step1.py")

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
directory = args.path

subdirs_susy = ["FromSUSY/", "FromSUSYHF/"]
sample_names_susy = ["Stop250-dm10-006", "Stop250-dm20-006", "Stop600-dm10-006", "Stop600-dm20-006"]

subdirs_ttbar = ["Fake/", "NonPrompt/", "Prompt/"]
sample_names_ttbar = ["TTJets_TuneCP5_13TeV", "TTTo2L2Nu_TuneCP5_13TeV", 
                      "TTToHadronic_TuneCP5_13TeV", "TTToSemiLeptonic_TuneCP5_13TeV",
                      "TT_DiLept_TuneCP5_13TeV"]

# define here the corr colors for the plots:
root_colors = [ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kMagenta]

# directory = [os.path.join(args.path, subdir, "pt_3.5_-1", sample_names) for subdir in subdirs]
# logger.info("Plotting step1 data from paths {}".format(directory))
    
t0 = time.time()
# this list contains the 4 susy samples with diff mass and mass diff. 
# each element is a sample corresponding to a specific susy sample
signal_samples = [Sample.fromDirectory(
        sample_name,
        directory = [os.path.join(args.path, subdir, "pt_3.5_-1", sample_name) for subdir in subdirs_susy],
        # redirector=redirector,
        treeName  = "tree"
        ) for sample_name in sample_names_susy]

bkg_samples = [Sample.fromDirectory(
        sample_name,
        directory = [os.path.join(args.path, subdir, "pt_3.5_-1", sample_name) for subdir in subdirs_ttbar],
        # redirector=redirector,
        treeName  = "tree"
        ) for sample_name in sample_names_ttbar]

logger.info("%i signal files", sum(len(data_sample.files) for data_sample in signal_samples))
logger.info("%i background files", sum(len(data_sample.files) for data_sample in bkg_samples))


small_nfiles = 1
if args.small:
    for data_sample in signal_samples:
        data_sample.reduceFiles( to = small_nfiles )
    for data_sample in bkg_samples:
        data_sample.reduceFiles( to = small_nfiles )


# copy samples:
# list of fake samples corr to 250_10, 250_20, 600_10, 600_20
# fake muons
fake_samples = deepcopy(bkg_samples)
for i, fake_sample in enumerate(fake_samples):
    fake_sample.setSelectionString("lep_isFakeId_Training==1")
    fake_sample.texName = sample_names_ttbar[i]
    fake_sample.Name    = sample_names_ttbar[i]
    fake_sample.style   = styles.lineStyle(root_colors[i])

# susy muons
susy_samples = deepcopy(signal_samples)
for i, susy_sample in enumerate(susy_samples):
    susy_sample.setSelectionString("lep_isFromSUSY_Training==1")
    susy_sample.texName = sample_names_susy[i]
    susy_sample.Name    = sample_names_susy[i]
    susy_sample.style   = styles.lineStyle(root_colors[i])


susy_hf_samples = deepcopy(signal_samples)
for i, susy_hf_sample in enumerate(susy_hf_samples):
    susy_hf_sample.setSelectionString("lep_isFromSUSYHF_Training==1")
    susy_hf_sample.texName = sample_names_susy[i]
    susy_hf_sample.Name    = sample_names_susy[i]
    susy_hf_sample.style   = styles.lineStyle(root_colors[i])

prompt_samples = deepcopy(bkg_samples)
for i, prompt_sample in enumerate(prompt_samples):
    prompt_sample.setSelectionString("lep_isPromptId_Training==1")
    prompt_sample.texName = sample_names_ttbar[i]
    prompt_sample.Name    = sample_names_ttbar[i]
    prompt_sample.style   = styles.lineStyle(root_colors[i])

nonprompt_samples = deepcopy(bkg_samples)
for i, nonprompt_sample in enumerate(nonprompt_samples):
    nonprompt_sample.setSelectionString("lep_isNonPromptId_Training==1")
    nonprompt_sample.texName = sample_names_ttbar[i]
    nonprompt_sample.Name    = sample_names_ttbar[i]
    nonprompt_sample.style   = styles.lineStyle(root_colors[i])

prompt_stack    = Stack(prompt_samples)
nonprompt_stack = Stack(nonprompt_samples)
fake_stack      = Stack(fake_samples)
susy_stack      = Stack(susy_samples)
susy_hf_stack   = Stack(susy_hf_samples)


logger.info("copied samples successfully")

read_variables = [
                  "lep_pt/F",
		          "lep_eta/F",
                  "lep_phi/F",
                  "lep_pdgId/F",
                  "lep_mediumId/F",
                  "lep_miniPFRelIso_all/F",
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
                  "lep_isFromSUSYandHF_Training/I",
                  "lep_isPromptId_Training/I",
                  "lep_isNonPromptId_Training/I",
                  "lep_isFakeId_Training/I",
                  "lep_isFromSUSY_Training/I",
                  "lep_isFromSUSYHF_Training/I"
                 ]

# lep_cat is fake, susy, ... to change the plot name accordingly
def fill_list_with_plots(plots, stack, lep_cat):
    '''
    plots is the list to be filled
    stack is the stack to be used -> chooses the samples
    # Plot is from Plot.setDefaults(stack = stack)
    '''

    plots.append(Plot(name      = "{}_lep_pt".format(lep_cat),
                      stack     = stack,
                      texX      = 'p_{T}(l)', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_pt,
                      binning   = [100,0,210],                  
                      ))
    
    plots.append(Plot(name      = "{}_lep_eta".format(lep_cat),
                      stack     = stack,
                      texX      = 'eta', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_eta,
                      binning   = [100,0,3],
                      ))
    
    plots.append(Plot(name      = "{}_lep_phi".format(lep_cat),
                      stack     = stack,
                      texX      = 'phi', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_phi,
                      binning   = [100,0,4],
                      ))
    
    plots.append(Plot(name      = "{}_lep_pdgId".format(lep_cat),
                      stack     = stack,
                      texX      = 'pdgId', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_pdgId,
                      binning   = [100,0,20],
                      ))
    
    plots.append(Plot(name      = "{}_lep_mediumId".format(lep_cat),
                      stack     = stack,   
                      texX      = 'mediumId', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_mediumId,
                      binning   = [100,0,5],
                      ))
    
    plots.append(Plot(name      = "{}_lep_miniPFRelIso_all".format(lep_cat),
                      stack     = stack,
                      texX      = 'miniPFRelIso_all', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_miniPFRelIso_all,
                      binning   = [100,0,1],
                      ))
    
    plots.append(Plot(name   = "{}_lep_sip3d".format(lep_cat),
                      stack     = stack,
                      texX      = 'sip3d', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_sip3d,
                      binning   = [100,0,5000],
                      ))
    
    plots.append(Plot(name      = "{}_lep_dxy".format(lep_cat),
                      stack     = stack,
                      texX      = 'dxy', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_dxy,
                      binning   = [100,-5,5],# -0.05,0.05
                      ))
    
    plots.append(Plot(name      = "{}_lep_dxy_zoom".format(lep_cat),
                      stack     = stack,
                      texX      = 'dxy', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_dxy,
                      binning   = [100,-0.05,0.05],# -5,5
                      ))
    
    plots.append(Plot(name      = "{}_lep_dz".format(lep_cat),
                      stack     = stack,
                      texX      = 'dz', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_dz,
                      binning   = [100,-50,50], # -0.1,0.1
                      ))
    
    plots.append(Plot(name      = "{}_lep_dz_zoom".format(lep_cat),
                      stack     = stack,
                      texX      = 'dz', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_dz,
                      binning   = [100,-1,1], # -0.1,0.1
                      ))
    
    plots.append(Plot(name      = "{}_lep_charge".format(lep_cat),
                      stack     = stack,
                      texX      = 'charge', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_charge,
                      binning   = [100,-2,2],
                      ))
    
    plots.append(Plot(name      = "{}_lep_dxyErr".format(lep_cat),
                      stack     = stack,
                      texX      = 'dxyErr', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_dxyErr,
                      binning   = [100,0,1],
                      ))
    
    plots.append(Plot(name      = "{}_lep_dzErr".format(lep_cat),
                      stack     = stack,
                      texX      = 'dzErr', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_dzErr,
                      binning   = [100,0,15],
                      ))
    
    plots.append(Plot(name      = "{}_lep_ip3d".format(lep_cat),
                      stack     = stack,
                      texX      = 'ip3d', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_ip3d,
                      binning   = [100,-1,30],
                      ))
    
    plots.append(Plot(name      = "{}_lep_jetPtRelv2".format(lep_cat),
                      stack     = stack,
                      texX      = 'jetPtRelv2', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_jetPtRelv2,
                      binning   = [100,-10,300],
                      ))
    
    plots.append(Plot(name      = "{}_lep_jetRelIso".format(lep_cat),
                      stack     = stack,
                      texX      = 'jetRelIso', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_jetRelIso,
                      binning   = [100,0,1],
                      ))
    
    plots.append(Plot(name      = "{}_lep_miniPFRelIso_chg".format(lep_cat),
                      stack     = stack,
                      texX      = 'miniPFRelIso_chg', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_miniPFRelIso_chg,
                      binning   = [100,0,1],
                      ))
    
    plots.append(Plot(name      = "{}_lep_mvaLowPt".format(lep_cat),
                      stack     = stack,
                      texX      = 'mvaLowPt', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_mvaLowPt,
                      binning   = [100,0,1],
                      ))
    
    plots.append(Plot(name      = "{}_lep_nStations".format(lep_cat),
                      stack     = stack,
                      texX      = 'nStations', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_nStations,
                      binning   = [100,0,10],
                      ))
    
    plots.append(Plot(name      = "{}_lep_nTrackerLayers".format(lep_cat),
                      stack     = stack,
                      texX      = 'nTrackerLayers', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_nTrackerLayers,
                      binning   = [20,0,20],
                      ))
    
    plots.append(Plot(name      = "{}_lep_pfRelIso03_all".format(lep_cat),
                      stack     = stack,
                      texX      = 'pfRelIso03_all', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_pfRelIso03_all,
                      binning   = [100,0,1],
                      ))
    
    plots.append(Plot(name      = "{}_lep_pfRelIso03_chg".format(lep_cat),
                      stack     = stack,
                      texX      = 'pfRelIso03_chg', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_pfRelIso03_chg,
                      binning   = [100,0,1],
                      ))
    
    plots.append(Plot(name      = "{}_lep_pfRelIso04_all".format(lep_cat),
                      stack     = stack,
                      texX      = 'pfRelIso04_all', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_pfRelIso04_all,
                      binning   = [100,0,1],
                      ))
    
    plots.append(Plot(name      = "{}_lep_ptErr".format(lep_cat),
                      stack     = stack,
                      texX      = 'ptErr', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_ptErr,
                      binning   = [100,0,40],
                      ))
    
    plots.append(Plot(name      = "{}_lep_segmentComp".format(lep_cat),
                      stack     = stack,
                      texX      = 'segmentComp', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_segmentComp,
                      binning   = [50,0,1],
                      ))
    
    plots.append(Plot(name      = "{}_lep_tkRelIso".format(lep_cat),
                      stack     = stack,
                      texX      = 'tkRelIso', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_tkRelIso,
                      binning   = [100,0,1],
                      ))
    
    plots.append(Plot(name      = "{}_lep_tunepRelPt".format(lep_cat),
                      stack     = stack,
                      texX      = 'tunepRelPt', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_tunepRelPt,
                      binning   = [100,0,50],
                      ))
    
    plots.append(Plot(name      = "{}_lep_genPartFlav".format(lep_cat),
                       stack     = stack, 
                      texX      = 'genPartFlav', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_genPartFlav,
                      binning   = [100,0,150],
                      ))
    
    plots.append(Plot(name      = "{}_npfCand_charged".format(lep_cat),
                      stack     = stack,
                      texX      = 'npfCand_charged', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.npfCand_charged,
                      binning   = [80,0,80],
                      ))
    
    plots.append(Plot(name      = "{}_npfCand_neutral".format(lep_cat),
                      stack     = stack,
                      texX      = 'npfCand_neutral', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.npfCand_neutral,
                      binning   = [20,0,20],
                      ))
    
    plots.append(Plot(name      = "{}_npfCand_photon".format(lep_cat), 
                      stack     = stack,
                      texX      = 'npfCand_photon', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.npfCand_photon,     
                      binning   = [40,0,40],
                      ))
    
    plots.append(Plot(name      = "{}_npfCand_electron".format(lep_cat),
                       stack     = stack,
                      texX      = 'npfCand_electron', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.npfCand_electron,      
                      binning   = [10,0,10],
                      ))
    
    plots.append(Plot(name      = "{}_npfCand_muon".format(lep_cat),
                      stack     = stack,
                      texX      = 'npfCand_muon', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.npfCand_muon,   
                      binning   = [10,0,10],
                      ))
    
    plots.append(Plot(name      = "{}_nSV".format(lep_cat),
                      stack     = stack,
                      texX      = 'nSV', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.nSV,
                      binning   = [10,0,20],
                      ))

    plots.append(Plot(name      = "{}_lep_isFromSUSYandHF_Training".format(lep_cat),
                      stack     = stack,
                      texX      = 'lep_isFromSUSYandHF_Training', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_isFromSUSYandHF_Training,
                      binning   = [100,-0.1,1.1],
                      ))

    plots.append(Plot(name      = "{}_lep_isPromptId_Training".format(lep_cat),
                      stack     = stack,
                      texX      = 'lep_isPromptId_Training', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_isPromptId_Training,
                      binning   = [100,-0.1,1.1],
                      ))

    plots.append(Plot(name      = "{}_lep_isNonPromptId_Training".format(lep_cat),
                      stack     = stack,
                      texX      = 'lep_isNonPromptId_Training', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_isNonPromptId_Training,
                      binning   = [100,-0.1,1.1],
                      ))

    plots.append(Plot(name      = "{}_lep_isFakeId_Training".format(lep_cat),
                      stack     = stack,
                      texX      = 'lep_isFakeId_Training', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_isFakeId_Training,
                      binning   = [100,-0.1,1.1],
                      ))

    plots.append(Plot(name      = "{}_lep_isFromSUSY_Training".format(lep_cat),
                      stack     = stack,
                      texX      = 'lep_isFromSUSY_Training', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_isFromSUSY_Training,
                      binning   = [100,-0.1,1.1],
                      ))

    plots.append(Plot(name      = "{}_lep_isFromSUSYHF_Training".format(lep_cat),
                      stack     = stack,
                      texX      = 'lep_isFromSUSYHF_Training', texY = 'Number of Events ',
                      attribute = lambda event, sample: event.lep_isFromSUSYHF_Training,
                      binning   = [100,-0.1,1.1],
                      ))



# plots = []
fake_plots =      []
susy_plots =      []
susy_hf_plots =   []
prompt_plots =    []
nonprompt_plots = []

all_plots = {'fake':fake_plots,
             'susy':susy_plots,
             'susy_hf': susy_hf_plots,
             'prompt': prompt_plots,
             'nonprompt': nonprompt_plots}
# Shockingly this doesnt work in py27!!!
# logger.info("should be: fake susy, susyhf, promp, nonpromt")
# for i in range(5):
#     logger.info("{}, {}".format(i , list(all_plots.keys())[i]))
fill_list_with_plots(fake_plots, fake_stack, "fake")
fill_list_with_plots(susy_plots, susy_stack, "susy")
fill_list_with_plots(susy_hf_plots, susy_hf_stack, "susy_hf")
fill_list_with_plots(prompt_plots, prompt_stack, "prompt")
fill_list_with_plots(nonprompt_plots, nonprompt_stack, "nonprompt")





# plotting.fill(plots, read_variables = read_variables)
logger.info("starting filling with fakes")
plotting.fill(fake_plots, read_variables = read_variables)
logger.info("done filling fakes")

logger.info("starting filling with susy")
plotting.fill(susy_plots, read_variables = read_variables)
logger.info("done filling with susy")

logger.info("starting filling susy hf")
plotting.fill(susy_hf_plots, read_variables = read_variables)
logger.info("done filling with susy hf")

logger.info("starting filling prompt")
plotting.fill(prompt_plots, read_variables = read_variables)
logger.info("done filling with prompt")

logger.info("starting filling nonprompt")
plotting.fill(nonprompt_plots, read_variables = read_variables)
logger.info("done filling with nonprompt")





# if args.normalize:
#     scaling = {0:3, 1:3, 2:3}
# else:
#     scaling = {}
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


def remove_lep_class_from_string(mystring):
    to_remove = ["fake_", "susy_hf_", "susy_", "prompt_", "nonprompt_"]
    for cat in to_remove:
        if mystring.startswith(cat):
            mystring = mystring.split(cat)[-1]
    return mystring

def draw_the_plots(plots, scaling):
    for plot in plots: #plots:
        plotting.draw(plot, 
                      plot_directory = os.path.join(plot_directory, 
                                                    "CompSUSY_v9_step1" + \
                                                    ("_normalized" if args.normalize else ""),
                                                    "v9_susy_{}".format(remove_lep_class_from_string(plot.name))+\
                                                    ("_args_small_nfiles_{} ".format(small_nfiles) if args.small else "")+\
                                                    ("_"+year[0] if useyear else "")+\
                                                    ("_small" if "small" in directory else "")) #args.plot_directory),
    , 
                      ratio          = None, 
                      scaling        = scaling,  
                      logX           = False, 
                      logY           = True,
                      sorting        = True, 
                      yRange         = (1.0, "auto"),
                      #legend         = "auto"
                      #drawObjects    = drawObjects( )
                      copyIndexPHP   = True,
                      extensions     = ["png", "pdf"] #, "root"]
                                                  )
for key, plots in all_plots.iteritems():
    if key in ["fake", "prompt", "nonprompt"]:
        scaling = {1:0, 2:0, 3:0, 4:0}
    else:
        scaling = {0:1, 1:2, 2:3}
    logger.info("******-plotting-{}-*******".format(key))
    draw_the_plots(plots, scaling)
# logger.info("%f s per file, %f total", (time.time()-t0)/len(data_samples[0].files), time.time()-t0)
