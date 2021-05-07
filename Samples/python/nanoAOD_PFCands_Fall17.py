import copy, os, sys
from RootTools.core.Sample import Sample

def get_parser():
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser for samples file")
    argParser.add_argument('--overwrite',          action='store_true',    help="Overwrite current entry in db?")
    argParser.add_argument('--update',             action='store_true',    help="Update current entry in db?")
    argParser.add_argument('--check_completeness', action='store_true',    help="Check competeness?")
    return argParser

# Logging
if __name__=="__main__":
    import Samples.Tools.logger as logger
    logger = logger.get_logger("INFO", logFile = None )
    import RootTools.core.logger as logger_rt
    logger_rt = logger_rt.get_logger("INFO", logFile = None )
    options = get_parser().parse_args()
    ov = options.overwrite
    if options.update:
        ov = 'update'
else:
    import logging
    logger = logging.getLogger(__name__)
    ov = False

# DB
from Samples.Tools.config import dbDir
dbFile = dbDir+'/DB_Fall17_DeepLepton.sql'

logger.info("Using db file: %s", dbFile)

#redirector = "/eos/vbc/experiments/cms/"
redirector = "root://eos.grid.vbc.ac.at/"

## SUSY sample

Signal_CompressedStops                 = Sample.fromDirectory("Signal_CompressedStops", "/eos/vbc/user/robert.schoefbeck/DeepLepton/nanoAODUL17_PFCands/signal_stops_compressed/")

## DY

DYJetsToLL_M10to50_LO                  = Sample.nanoAODfromDAS("DYJetsToLL_M10to50_LO", "/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M4to50_HT100to200_LO        = Sample.nanoAODfromDAS("DYJetsToLL_M4to50_HT100to200_LO", "/DYJetsToLL_M-4to50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1) 
DYJetsToLL_M4to50_HT100to200_LO_ext1   = Sample.nanoAODfromDAS("DYJetsToLL_M4to50_HT100to200_LO_ext1", "/DYJetsToLL_M-4to50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1) 
DYJetsToLL_M4to50_HT200to400_LO        = Sample.nanoAODfromDAS("DYJetsToLL_M4to50_HT200to400_new_pmx_LO", "/DYJetsToLL_M-4to50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M4to50_HT200to400_old_pmx_LO=Sample.nanoAODfromDAS("DYJetsToLL_M4to50_HT200to400_LO", "/DYJetsToLL_M-4to50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M4to50_HT200to400_LO_ext1   = Sample.nanoAODfromDAS("DYJetsToLL_M4to50_HT200to400_LO_ext1", "/DYJetsToLL_M-4to50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M4to50_HT400to600_LO        = Sample.nanoAODfromDAS("DYJetsToLL_M4to50_HT400to600_LO", "/DYJetsToLL_M-4to50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M4to50_HT400to600_LO_ext1   = Sample.nanoAODfromDAS("DYJetsToLL_M4to50_HT400to600_LO_ext1", "/DYJetsToLL_M-4to50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M4to50_HT600toInf_LO        = Sample.nanoAODfromDAS("DYJetsToLL_M4to50_HT600toInf_LO", "/DYJetsToLL_M-4to50_HT-600toInf_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M4to50_HT600toInf_LO_ext1   = Sample.nanoAODfromDAS("DYJetsToLL_M4to50_HT600toInf_LO_ext1", "/DYJetsToLL_M-4to50_HT-600toInf_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M50_NLO                     = Sample.nanoAODfromDAS("DYJetsToLL_M50_NLO", "/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_ext1-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M50_LO                      = Sample.nanoAODfromDAS("DYJetsToLL_M50_LO", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M50_LO_ext1                 = Sample.nanoAODfromDAS("DYJetsToLL_M50_LO_ext1", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14_ext1-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M50_HT70to100_LO            = Sample.nanoAODfromDAS("DYJetsToLL_M50_HT70to100_LO", "/DYJetsToLL_M-50_HT-70to100_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M50_HT100to200_LO           = Sample.nanoAODfromDAS("DYJetsToLL_M50_HT100to200_LO", "/DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M50_HT100to200_LO_ext1      = Sample.nanoAODfromDAS("DYJetsToLL_M50_HT100to200_LO_ext1", "/DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M50_HT200to400_LO           = Sample.nanoAODfromDAS("DYJetsToLL_M50_HT200to400_LO", "/DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M50_HT200to400_LO_ext1      = Sample.nanoAODfromDAS("DYJetsToLL_M50_HT200to400_LO_ext1", "/DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M50_HT400to600_LO           = Sample.nanoAODfromDAS("DYJetsToLL_M50_HT400to600_LO", "/DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M50_HT400to600_LO_ext1      = Sample.nanoAODfromDAS("DYJetsToLL_M50_HT400to600_LO_ext1", "/DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M50_HT600to800_LO           = Sample.nanoAODfromDAS("DYJetsToLL_M50_HT600to800_LO", "/DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M50_HT800to1200_LO          = Sample.nanoAODfromDAS("DYJetsToLL_M50_HT800to1200_LO", "/DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M50_HT1200to2500_LO         = Sample.nanoAODfromDAS("DYJetsToLL_M50_HT1200to2500_LO", "/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
DYJetsToLL_M50_HT2500toInf_LO          = Sample.nanoAODfromDAS("DYJetsToLL_M50_HT2500toInf_LO", "/DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)



DY = [DYJetsToLL_M10to50_LO,
      DYJetsToLL_M4to50_HT100to200_LO,
      DYJetsToLL_M4to50_HT100to200_LO_ext1,
      DYJetsToLL_M4to50_HT200to400_LO,
      DYJetsToLL_M4to50_HT200to400_old_pmx_LO,
      DYJetsToLL_M4to50_HT200to400_LO_ext1,
      DYJetsToLL_M4to50_HT400to600_LO,
      DYJetsToLL_M4to50_HT400to600_LO_ext1,
      DYJetsToLL_M4to50_HT600toInf_LO,
      DYJetsToLL_M4to50_HT600toInf_LO_ext1,
      DYJetsToLL_M50_NLO,
      DYJetsToLL_M50_LO,
      DYJetsToLL_M50_LO_ext1,
      DYJetsToLL_M50_HT70to100_LO,
      DYJetsToLL_M50_HT100to200_LO,
      DYJetsToLL_M50_HT100to200_LO_ext1,
      DYJetsToLL_M50_HT200to400_LO,
      DYJetsToLL_M50_HT200to400_LO_ext1,
      DYJetsToLL_M50_HT400to600_LO,
      DYJetsToLL_M50_HT400to600_LO_ext1,
      DYJetsToLL_M50_HT600to800_LO,
      DYJetsToLL_M50_HT800to1200_LO,
      DYJetsToLL_M50_HT1200to2500_LO,
      DYJetsToLL_M50_HT2500toInf_LO,
        ]

#QCD
QCD_Mu_pt15to20         = Sample.nanoAODfromDAS("QCD_Mu_pt15to20", "/QCD_Pt-15to20_MuEnrichedPt5_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_Mu_pt20to30         = Sample.nanoAODfromDAS("QCD_Mu_pt20to30", "/QCD_Pt-20to30_MuEnrichedPt5_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_Mu_pt30to50         = Sample.nanoAODfromDAS("QCD_Mu_pt30to50", "/QCD_Pt-30to50_MuEnrichedPt5_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_Mu_pt50to80         = Sample.nanoAODfromDAS("QCD_Mu_pt50to80", "/QCD_Pt-50to80_MuEnrichedPt5_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_Mu_pt80to120        = Sample.nanoAODfromDAS("QCD_Mu_pt80to120", "/QCD_Pt-80to120_MuEnrichedPt5_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_Mu_pt120to170       = Sample.nanoAODfromDAS("QCD_Mu_pt120to170", "/QCD_Pt-120to170_MuEnrichedPt5_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_Mu_pt170to300       = Sample.nanoAODfromDAS("QCD_Mu_pt170to300", "/QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_Mu_pt300to470       = Sample.nanoAODfromDAS("QCD_Mu_pt300to470", "/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_Mu_pt470to600       = Sample.nanoAODfromDAS("QCD_Mu_pt470to600", "/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_Mu_pt600to800       = Sample.nanoAODfromDAS("QCD_Mu_pt600to800", "/QCD_Pt-600to800_MuEnrichedPt5_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_Mu_pt800to1000      = Sample.nanoAODfromDAS("QCD_Mu_pt800to1000", "/QCD_Pt-800to1000_MuEnrichedPt5_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_Mu_pt1000toInf      = Sample.nanoAODfromDAS("QCD_Mu_pt1000toInf", "/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)

QCD_EMEnriched_pt20to30        = Sample.nanoAODfromDAS("QCD_EMEnriched_pt20to30", "/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_EMEnriched_pt30to50        = Sample.nanoAODfromDAS("QCD_EMEnriched_pt30to50", "/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_EMEnriched_pt50to80        = Sample.nanoAODfromDAS("QCD_EMEnriched_pt50to80", "/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_EMEnriched_pt80to120       = Sample.nanoAODfromDAS("QCD_EMEnriched_pt80to120", "/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_EMEnriched_pt120to170      = Sample.nanoAODfromDAS("QCD_EMEnriched_pt120to170", "/QCD_Pt-120to170_MuEnrichedPt5_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_EMEnriched_pt170to300      = Sample.nanoAODfromDAS("QCD_EMEnriched_pt170to300", "/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_EMEnriched_pt300toInf      = Sample.nanoAODfromDAS("QCD_EMEnriched_pt300toInf", "/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)

QCD_bcToE_pt20to30_new_pmx  = Sample.nanoAODfromDAS("QCD_bcToE_pt20to30_new_pmx", "/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_bcToE_pt20to30          = Sample.nanoAODfromDAS("QCD_bcToE_pt20to30", "/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_bcToE_pt30to80          = Sample.nanoAODfromDAS("QCD_bcToE_pt30to80", "/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_bcToE_pt80to170         = Sample.nanoAODfromDAS("QCD_bcToE_pt80to170", "/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_bcToE_pt170to250        = Sample.nanoAODfromDAS("QCD_bcToE_pt170to250", "/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_bcToE_pt250toInf        = Sample.nanoAODfromDAS("QCD_bcToE_pt250toInf", "/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)

QCD = [QCD_Mu_pt15to20,
       QCD_Mu_pt20to30,
       QCD_Mu_pt30to50,
       QCD_Mu_pt50to80,
       QCD_Mu_pt80to120,
       QCD_Mu_pt120to170,
       QCD_Mu_pt170to300,
       QCD_Mu_pt300to470,
       QCD_Mu_pt470to600,
       QCD_Mu_pt600to800,
       QCD_Mu_pt800to1000,
       QCD_Mu_pt1000toInf,

       QCD_EMEnriched_pt20to30,
       QCD_EMEnriched_pt30to50,
       QCD_EMEnriched_pt50to80,
       QCD_EMEnriched_pt80to120,
       QCD_EMEnriched_pt120to170,
       QCD_EMEnriched_pt170to300,
       QCD_EMEnriched_pt300toInf,

       QCD_bcToE_pt20to30_new_pmx,
       QCD_bcToE_pt20to30,
       QCD_bcToE_pt30to80,
       QCD_bcToE_pt80to170,
       QCD_bcToE_pt170to250,
       QCD_bcToE_pt250toInf,]

# T

ST_schannel_4f_NLO                      = Sample.nanoAODfromDAS("ST_schannel_4f_NLO", "/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_schannel_4f_NLO_PS                   = Sample.nanoAODfromDAS("ST_schannel_4f_NLO_PS", "/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tchannel_antitop_4f_incl_pow         = Sample.nanoAODfromDAS("ST_tchannel_antitop_4f_incl_pow", "/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tchannel_top_4f_incl_pow             = Sample.nanoAODfromDAS("ST_tchannel_top_4f_incl_pow", "/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)

ST_tchannel_antitop_5f_pow_PS           = Sample.nanoAODfromDAS("ST_tchannel_antitop_5f_pow_PS", "/ST_t-channel_antitop_5f_TuneCP5_PSweights_13TeV-powheg-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tchannel_antitop_5f_pow_PS_old_pmx   = Sample.nanoAODfromDAS("ST_tchannel_antitop_5f_pow_PS_old_pmx", "/ST_t-channel_antitop_5f_TuneCP5_PSweights_13TeV-powheg-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tchannel_top_5f_pow_old_pmx          = Sample.nanoAODfromDAS("ST_tchannel_top_5f_pow_old_pmx", "/ST_t-channel_top_5f_TuneCP5_13TeV-powheg-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tchannel_top_5f_pow                  = Sample.nanoAODfromDAS("ST_tchannel_top_5f_pow", "/ST_t-channel_top_5f_TuneCP5_13TeV-powheg-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tW_antitop_NoFullyHad_5f_pow_PS      = Sample.nanoAODfromDAS("ST_tW_antitop_NoFullyHad_5f_pow_PS", "/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tW_antitop_incl_5f_pow               = Sample.nanoAODfromDAS("ST_tW_antitop_incl_5f_pow", "/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tW_antitop_incl_5f_pow_PS            = Sample.nanoAODfromDAS("ST_tW_antitop_incl_5f_pow_PS", "/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tW_top_NoFullyHad_5f_pow             = Sample.nanoAODfromDAS("ST_tW_top_NoFullyHad_5f_pow", "/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tW_top_NoFullyHad_5f_pow_PS          = Sample.nanoAODfromDAS("ST_tW_top_NoFullyHad_5f_pow_PS", "/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tW_top_incl_5f_pow                   = Sample.nanoAODfromDAS("ST_tW_top_incl_5f_pow", "/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tW_top_incl_5f_pow_PS                = Sample.nanoAODfromDAS("ST_tW_top_incl_5f_pow_PS", "/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)

ST_tWll_5f_LO                           = Sample.nanoAODfromDAS("ST_tWll_5f_LO", "/ST_tWll_5f_LO_TuneCP5_PSweights_13TeV-madgraph-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tWnunu_5f_LO                         = Sample.nanoAODfromDAS("ST_tWnunu_5f_LO", "/ST_tWnunu_5f_LO_TuneCP5_PSweights_13TeV-madgraph-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v3_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)

TTJets_NLO                              = Sample.nanoAODfromDAS("TTJets_NLO", "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTJets_LO                               = Sample.nanoAODfromDAS("TTJets_LO", "/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTJets_semilepFromT_LO                  = Sample.nanoAODfromDAS("TTJets_semilepFromT_LO", "/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTJets_semilepFromTbar_LO               = Sample.nanoAODfromDAS("TTJets_semilepFromTbar_LO", "/TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTJets_dilep_LO                         = Sample.nanoAODfromDAS("TTJets_dilep_LO", "/TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTJets_semilepFromT_genMET150_LO        = Sample.nanoAODfromDAS("TTJets_semilepFromT_genMET150_LO", "/TTJets_SingleLeptFromT_genMET-150_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTJets_semilepFromTbar_genMET150_LO     = Sample.nanoAODfromDAS("TTJets_semilepFromTbar_genMET150_LO", "/TTJets_SingleLeptFromTbar_genMET-150_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTJets_dilep_genMET150_LO               = Sample.nanoAODfromDAS("TTJets_dilep_genMET150_LO", "/TTJets_DiLept_genMET-150_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)

TTTo2L2Nu_pow                           = Sample.nanoAODfromDAS("TTTo2L2Nu_pow", "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTTo2L2Nu_pow_PS                        = Sample.nanoAODfromDAS("TTTo2L2Nu_pow_PS", "/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTToSemiLeptonic_pow                    = Sample.nanoAODfromDAS("TTToSemiLeptonic_pow", "/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTToSemiLeptonic_pow_PS                 = Sample.nanoAODfromDAS("TTToSemiLeptonic_pow_PS", "/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)

TTHH_LO                                    = Sample.nanoAODfromDAS("TTHH_LO", "/TTHH_TuneCP5_13TeV-madgraph-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTZH_LO                                    = Sample.nanoAODfromDAS("TTZH_LO", "/TTZH_TuneCP5_13TeV-madgraph-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTWH_LO                                    = Sample.nanoAODfromDAS("TTWH_LO", "/TTWH_TuneCP5_13TeV-madgraph-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTWW_LO                                    = Sample.nanoAODfromDAS("TTWW_LO", "/TTWW_TuneCP5_13TeV-madgraph-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_ext1-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTWZ_LO                                    = Sample.nanoAODfromDAS("TTWZ_LO", "/TTWZ_TuneCP5_13TeV-madgraph-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTZZ_LO                                    = Sample.nanoAODfromDAS("TTZZ_LO", "/TTZZ_TuneCP5_13TeV-madgraph-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)

TTJets_HT600to800_LO                       = Sample.nanoAODfromDAS("TTJets_HT600to800_LO", "/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTJets_HT800to1200_LO                      = Sample.nanoAODfromDAS("TTJets_HT800to1200_LO", "/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTJets_HT1200to2500_LO                     = Sample.nanoAODfromDAS("TTJets_HT1200to2500_LO", "/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTJets_HT2500toInf_LO                      = Sample.nanoAODfromDAS("TTJets_HT2500toInf_LO", "/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3_v6_PFCands-6ed54b6dbec6325fc1ce711bde233f01/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)

T = [
     ST_schannel_4f_NLO,
     ST_schannel_4f_NLO_PS,
     ST_tchannel_antitop_4f_incl_pow,
     ST_tchannel_top_4f_incl_pow,

     ST_tchannel_antitop_5f_pow_PS,
     ST_tchannel_antitop_5f_pow_PS_old_pmx,
     ST_tchannel_top_5f_pow_old_pmx,
     ST_tchannel_top_5f_pow,
     ST_tW_antitop_NoFullyHad_5f_pow_PS,
     ST_tW_antitop_incl_5f_pow,
     ST_tW_antitop_incl_5f_pow_PS,
     ST_tW_top_NoFullyHad_5f_pow,
     ST_tW_top_NoFullyHad_5f_pow_PS,
     ST_tW_top_incl_5f_pow,
     ST_tW_top_incl_5f_pow_PS,

     ST_tWll_5f_LO,
     ST_tWnunu_5f_LO,

     TTJets_NLO,
     TTJets_LO,
     TTJets_semilepFromT_LO,
     TTJets_semilepFromTbar_LO,
     TTJets_dilep_LO,
     TTJets_semilepFromT_genMET150_LO,
     TTJets_semilepFromTbar_genMET150_LO,
     TTJets_dilep_genMET150_LO,

     TTTo2L2Nu_pow,
     TTTo2L2Nu_pow_PS,
     TTToSemiLeptonic_pow,
     TTToSemiLeptonic_pow_PS,

     TTHH_LO,
     TTZH_LO,
     TTWH_LO,
     TTWW_LO,
     TTWZ_LO,
     TTZZ_LO,

     TTJets_HT600to800_LO,
     TTJets_HT800to1200_LO,
     TTJets_HT1200to2500_LO,
     TTJets_HT2500toInf_LO,]


allSamples = DY + QCD + T


for s in allSamples:
    s.isData = False

from Samples.Tools.AutoClass import AutoClass
samples = AutoClass( allSamples )
