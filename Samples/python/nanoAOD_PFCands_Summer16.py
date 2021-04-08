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
if 'CONDOR' in os.environ:
    dbFile = 'DB_Summer16_DeepLepton.sql'
else:
    from Samples.Tools.config import dbDir
    dbFile = dbDir+'/DB_Summer16_DeepLepton.sql'

logger.info("Using db file: %s", dbFile)

#redirector = "/eos/vbc/experiments/cms/"
redirector = "root://eos.grid.vbc.ac.at/"

## DY
#DYJetsToLL_M50_LO = Sample.nanoAODfromDAS("DYJetsToLL_M50_LO",       "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",   dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=False, xSection=2075.14*3)

DYJetsToLL_M50_LO        = Sample.nanoAODfromDAS("DYJetsToLL_M50_LO",       "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",   dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=2075.14*3)
DYJetsToLL_M50_LO_ext2   = Sample.nanoAODfromDAS("DYJetsToLL_M50_LO_ext2",  "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",   dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=2075.14*3)
DYJetsToLL_M50_ext2      = Sample.nanoAODfromDAS("DYJetsToLL_M50_ext2",     "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",  dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=2075.14*3)
DYJetsToLL_M10to50_LO    = Sample.nanoAODfromDAS("DYJetsToLL_M10to50_LO",   "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",   dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=18610)
DYJetsToLL_M10to50       = Sample.nanoAODfromDAS("DYJetsToLL_M10to50",      "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",   dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=18610)

DYJetsToLL_M50_HT70to100      =   Sample.nanoAODfromDAS("DYJetsToLL_M50_HT70to100"    ,     "/DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",         dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=169.9*1.23)
DYJetsToLL_M50_HT100to200_ext =   Sample.nanoAODfromDAS("DYJetsToLL_M50_HT100to200_ext",    "/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",   dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=147.4*1.23)
DYJetsToLL_M50_HT200to400     =   Sample.nanoAODfromDAS("DYJetsToLL_M50_HT200to400",        "/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",        dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=40.99*1.23)
DYJetsToLL_M50_HT200to400_ext =   Sample.nanoAODfromDAS("DYJetsToLL_M50_HT200to400_ext",    "/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",   dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=40.99*1.23)
DYJetsToLL_M50_HT400to600     =   Sample.nanoAODfromDAS("DYJetsToLL_M50_HT400to600",        "/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",        dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=5.678*1.23)
DYJetsToLL_M50_HT400to600_ext =   Sample.nanoAODfromDAS("DYJetsToLL_M50_HT400to600_ext",    "/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",   dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=5.678*1.23)
DYJetsToLL_M50_HT600to800     =   Sample.nanoAODfromDAS("DYJetsToLL_M50_HT600to800"   ,     "/DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",        dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=1.367*1.23 )
DYJetsToLL_M50_HT800to1200    =   Sample.nanoAODfromDAS("DYJetsToLL_M50_HT800to1200"  ,     "/DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",       dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=0.6304*1.23 )
DYJetsToLL_M50_HT1200to2500   =   Sample.nanoAODfromDAS("DYJetsToLL_M50_HT1200to2500" ,     "/DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",      dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=0.1514*1.23 )
DYJetsToLL_M50_HT2500toInf    =   Sample.nanoAODfromDAS("DYJetsToLL_M50_HT2500toInf"  ,     "/DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",       dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=0.003565*1.23 )

DYJetsToLL_M5to50_HT70to100      = Sample.nanoAODfromDAS("DYJetsToLL_M5to50_HT70to100"     , "/DYJetsToLL_M-5to50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",         dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=303.4)
DYJetsToLL_M5to50_HT100to200     = Sample.nanoAODfromDAS("DYJetsToLL_M5to50_HT100to200"    , "/DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",        dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=224.2)
DYJetsToLL_M5to50_HT100to200_ext = Sample.nanoAODfromDAS("DYJetsToLL_M5to50_HT100to200_ext", "/DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",   dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=224.2)
DYJetsToLL_M5to50_HT200to400     = Sample.nanoAODfromDAS("DYJetsToLL_M5to50_HT200to400"    , "/DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",        dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=37.2)
DYJetsToLL_M5to50_HT200to400_ext = Sample.nanoAODfromDAS("DYJetsToLL_M5to50_HT200to400_ext", "/DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",   dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=37.2)
DYJetsToLL_M5to50_HT400to600     = Sample.nanoAODfromDAS("DYJetsToLL_M5to50_HT400to600"    , "/DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",        dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=3.581)
DYJetsToLL_M5to50_HT400to600_ext = Sample.nanoAODfromDAS("DYJetsToLL_M5to50_HT400to600_ext", "/DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",   dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=3.581)
DYJetsToLL_M5to50_HT600toInf     = Sample.nanoAODfromDAS("DYJetsToLL_M5to50_HT600toInf"    , "/DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",        dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=1.124)


DY = [  DYJetsToLL_M50_LO,
        DYJetsToLL_M50_LO_ext2,
        DYJetsToLL_M50_ext2,
        DYJetsToLL_M10to50_LO,
        DYJetsToLL_M10to50,
        DYJetsToLL_M50_HT70to100,
        DYJetsToLL_M50_HT100to200_ext, 
        DYJetsToLL_M50_HT200to400,
        DYJetsToLL_M50_HT200to400_ext,
        DYJetsToLL_M50_HT400to600,
        DYJetsToLL_M50_HT400to600_ext,
        DYJetsToLL_M50_HT600to800,
        DYJetsToLL_M50_HT800to1200,
        DYJetsToLL_M50_HT1200to2500,
        DYJetsToLL_M50_HT2500toInf,
        DYJetsToLL_M5to50_HT70to100,
        DYJetsToLL_M5to50_HT100to200,
        DYJetsToLL_M5to50_HT100to200_ext,
        DYJetsToLL_M5to50_HT200to400,
        DYJetsToLL_M5to50_HT200to400_ext,
        DYJetsToLL_M5to50_HT400to600,
        DYJetsToLL_M5to50_HT400to600_ext,
        DYJetsToLL_M5to50_HT600toInf,
        ]


QCD_Mu_pt15to20         = Sample.nanoAODfromDAS("QCD_Mu_pt15to20",   "/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",     dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_Mu_pt20to30         = Sample.nanoAODfromDAS("QCD_Mu_pt20to30",   "/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",     dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=558528000*0.0053)
QCD_Mu_pt30to50         = Sample.nanoAODfromDAS("QCD_Mu_pt30to50",   "/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",     dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=139803000*0.01182)
QCD_Mu_pt50to80         = Sample.nanoAODfromDAS("QCD_Mu_pt50to80",   "/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",     dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=19222500*0.02276)
QCD_Mu_pt80to120        = Sample.nanoAODfromDAS("QCD_Mu_pt80to120",   "/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",     dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=2758420*0.03844)
QCD_Mu_pt80to120_ext1   = Sample.nanoAODfromDAS("QCD_Mu_pt80to120_ext1",   "/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",     dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=2758420*0.03844)
QCD_Mu_pt120to170       = Sample.nanoAODfromDAS("QCD_Mu_pt120to170",   "/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",     dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=469797*0.05362)
QCD_Mu_pt170to300       = Sample.nanoAODfromDAS("QCD_Mu_pt170to300",   "/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",     dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=117989*0.07335)
QCD_Mu_pt170to300_ext1  = Sample.nanoAODfromDAS("QCD_Mu_pt170to300_ext1",   "/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",     dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=117989*0.07335)
QCD_Mu_pt300to470       = Sample.nanoAODfromDAS("QCD_Mu_pt300to470",   "/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",     dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=7820.25*0.10196)
QCD_Mu_pt300to470_ext1  = Sample.nanoAODfromDAS("QCD_Mu_pt300to470_ext1",   "/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",     dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=7820.25*0.10196)
QCD_Mu_pt470to600       = Sample.nanoAODfromDAS("QCD_Mu_pt470to600",   "/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",     dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=645.528*0.12242)
QCD_Mu_pt470to600_ext1  = Sample.nanoAODfromDAS("QCD_Mu_pt470to600_ext1",   "/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",     dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=645.528*0.12242)
QCD_Mu_pt600to800       = Sample.nanoAODfromDAS("QCD_Mu_pt600to800",   "/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",     dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=187.109*0.13412)
QCD_Mu_pt600to800_ext1  = Sample.nanoAODfromDAS("QCD_Mu_pt600to800_ext1",   "/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",     dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=187.109*0.13412)
QCD_Mu_pt800to1000      = Sample.nanoAODfromDAS("QCD_Mu_pt800to1000",   "/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",     dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=32.3486*0.14552)
QCD_Mu_pt800to1000_ext1 = Sample.nanoAODfromDAS("QCD_Mu_pt800to1000_ext1",   "/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",     dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=32.3486*0.14552)
QCD_Mu_pt1000toInf      = Sample.nanoAODfromDAS("QCD_Mu_pt1000toInf",   "/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",     dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=10.4305*0.15544)
QCD_Mu_pt1000toInf_ext1 = Sample.nanoAODfromDAS("QCD_Mu_pt1000toInf_ext1",   "/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",     dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=10.4305*0.15544)


QCD_EMEnriched_pt20to30        = Sample.nanoAODfromDAS("QCD_EMEnriched_pt20to30",  "/QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_EMEnriched_pt30to50        = Sample.nanoAODfromDAS("QCD_EMEnriched_pt30to50",  "/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",  dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_EMEnriched_pt30to50_ext1   = Sample.nanoAODfromDAS("QCD_EMEnriched_pt30to50_ext1",  "/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",  dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_EMEnriched_pt50to80        = Sample.nanoAODfromDAS("QCD_EMEnriched_pt50to80",  "/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",  dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_EMEnriched_pt50to80_ext1   = Sample.nanoAODfromDAS("QCD_EMEnriched_pt50to80_ext1",  "/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",  dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_EMEnriched_pt80to120       = Sample.nanoAODfromDAS("QCD_EMEnriched_pt80to120",  "/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",  dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_EMEnriched_pt80to120_ext1  = Sample.nanoAODfromDAS("QCD_EMEnriched_pt80to120_ext1",  "/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",  dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_EMEnriched_pt120to170      = Sample.nanoAODfromDAS("QCD_EMEnriched_pt120to170",  "/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",  dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_EMEnriched_pt120to170_ext1 = Sample.nanoAODfromDAS("QCD_EMEnriched_pt120to170_ext1",  "/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",  dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_EMEnriched_pt170to300      = Sample.nanoAODfromDAS("QCD_EMEnriched_pt170to300",  "/QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",  dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_EMEnriched_pt300toInf      = Sample.nanoAODfromDAS("QCD_EMEnriched_pt300toInf",  "/QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",  dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)

QCD_bcToE_pt15to20  = Sample.nanoAODfromDAS("QCD_bcToE_pt15to20"   ,  "/QCD_Pt_15to20_bcToE_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER" , dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_bcToE_pt20to30  = Sample.nanoAODfromDAS("QCD_bcToE_pt20to30"   ,  "/QCD_Pt_20to30_bcToE_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER"  , dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_bcToE_pt30to80  = Sample.nanoAODfromDAS("QCD_bcToE_pt30to80"   ,  "/QCD_Pt_30to80_bcToE_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER"  , dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_bcToE_pt80to170 = Sample.nanoAODfromDAS("QCD_bcToE_pt80to170"  ,  "/QCD_Pt_80to170_bcToE_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_backup_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER" , dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
QCD_bcToE_pt170to250 = Sample.nanoAODfromDAS("QCD_bcToE_pt170to250" ,  "/QCD_Pt_170to250_bcToE_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection =-1)
QCD_bcToE_pt250toInf = Sample.nanoAODfromDAS("QCD_bcToE_pt250toInf" ,  "/QCD_Pt_250toInf_bcToE_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)


QCD = [ QCD_Mu_pt15to20,
        QCD_Mu_pt20to30,
        QCD_Mu_pt30to50,
        QCD_Mu_pt50to80,
        QCD_Mu_pt80to120,
        QCD_Mu_pt80to120_ext1,
        QCD_Mu_pt120to170,
        QCD_Mu_pt170to300,
        QCD_Mu_pt170to300_ext1,
        QCD_Mu_pt300to470,
        QCD_Mu_pt300to470_ext1,
        QCD_Mu_pt470to600,
        QCD_Mu_pt470to600_ext1,
        QCD_Mu_pt600to800,
        QCD_Mu_pt600to800_ext1,
        QCD_Mu_pt800to1000,
        QCD_Mu_pt800to1000_ext1,
        QCD_Mu_pt1000toInf,
        QCD_Mu_pt1000toInf_ext1,

        QCD_EMEnriched_pt20to30,
        QCD_EMEnriched_pt30to50, 
        QCD_EMEnriched_pt30to50_ext1,
        QCD_EMEnriched_pt50to80,
        QCD_EMEnriched_pt50to80_ext1,
        QCD_EMEnriched_pt80to120,
        QCD_EMEnriched_pt80to120_ext1,
        QCD_EMEnriched_pt120to170,
        QCD_EMEnriched_pt120to170_ext1,
        QCD_EMEnriched_pt170to300,
        QCD_EMEnriched_pt300toInf,

        QCD_bcToE_pt15to20,
        QCD_bcToE_pt20to30,
        QCD_bcToE_pt30to80,
        QCD_bcToE_pt80to170,
        QCD_bcToE_pt170to250,
        QCD_bcToE_pt250toInf,
]


TTTo2L2Nu_noSC_pow  = Sample.nanoAODfromDAS("TTTo2L2Nu_noSC_pow", "/TTTo2L2Nu_noSC_TuneCUETP8M2T4_13TeV-powheg-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",  dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTTo2L2Nu_pow_CP5   = Sample.nanoAODfromDAS("TTTo2L2Nu_pow_CP5",  "/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTTo2L2Nu_pow       = Sample.nanoAODfromDAS("TTTo2L2Nu_pow",  "/TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTToSemilepton_pow  = Sample.nanoAODfromDAS("TTToSemilepton_pow",  "/TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTToSemilepton_pow_CP5 = Sample.nanoAODfromDAS("TTToSemilepton_pow_CP5",  "/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TT_pow              = Sample.nanoAODfromDAS("TT_pow",  "/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)


ST_schannel_4f_NLO                 = Sample.nanoAODfromDAS("ST_schannel_4f_NLO",  "/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_schannel_4f_CP5                 = Sample.nanoAODfromDAS("ST_schannel_4f_CP5",  "/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tchannel_antitop_4f_pow         = Sample.nanoAODfromDAS("ST_tchannel_antitop_4f_pow",  "/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tchannel_antitop_4f_pow_CP5     = Sample.nanoAODfromDAS("ST_tchannel_antitop_4f_pow_CP5",  "/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tchannel_top_4f_pow             = Sample.nanoAODfromDAS("ST_tchannel_top_4f_pow",  "/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tchannel_top_4f_pow_CP5         = Sample.nanoAODfromDAS("ST_tchannel_top_4f_pow_CP5",  "/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)

ST_tW_antitop_NoFullyHad_5f_pow    = Sample.nanoAODfromDAS("ST_tW_antitop_NoFullyHad_5f_pow",  "/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tW_antitop_5f_pow_ext1          = Sample.nanoAODfromDAS("ST_tW_antitop_5f_pow_ext1",  "/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tW_antitop_5f_pow               = Sample.nanoAODfromDAS("ST_tW_antitop_5f_pow",  "/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tW_antitop_5f_pow_CP5           = Sample.nanoAODfromDAS("ST_tW_antitop_5f_pow_CP5",  "/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tW_top_NoFullyHad_5f_pow        = Sample.nanoAODfromDAS("ST_tW_top_NoFullyHad_5f_pow",  "/ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tW_top_NoFullyHad_5f_pow_ext    = Sample.nanoAODfromDAS("ST_tW_top_NoFullyHad_5f_pow_ext",  "/ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tW_top_5f_pow_ext1              = Sample.nanoAODfromDAS("ST_tW_top_5f_pow_ext1",  "/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tW_top_5f_pow                   = Sample.nanoAODfromDAS("ST_tW_top_5f_pow",  "/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tW_top_5f_pow_CP5               = Sample.nanoAODfromDAS("ST_tW_top_5f_pow_CP5",  "/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER"    , dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tWll_5f_LO                      = Sample.nanoAODfromDAS("ST_tWll_5f_LO",  "/ST_tWll_5f_LO_13TeV-MadGraph-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
ST_tWnunu_5f_LO                    = Sample.nanoAODfromDAS("ST_tWnunu_5f_LO",  "/ST_tWnunu_5f_LO_13TeV-MadGraph-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)


THQ_LO                  = Sample.nanoAODfromDAS("THQ_LO",  "/THQ_Hincl_13TeV-madgraph-pythia8_TuneCUETP8M1/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
THW_LO                  = Sample.nanoAODfromDAS("THW_LO",  "/THW_Hincl_13TeV-madgraph-pythia8_TuneCUETP8M1/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TZq_ll_NLO              = Sample.nanoAODfromDAS("TZq_ll_NLO",  "/tZq_ll_4f_13TeV-amcatnlo-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TZq_nunu_NLO            = Sample.nanoAODfromDAS("TZq_nunu_NLO",  "/tZq_nunu_4f_13TeV-amcatnlo-pythia8_TuneCUETP8M1/mmoser-crab_RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)

TTTT_NLO                = Sample.nanoAODfromDAS("TTTT_NLO",  "/TTTT_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTWW_NLO                = Sample.nanoAODfromDAS("TTWW_NLO",  "/TTWW_TuneCUETP8M2T4_13TeV-madgraph-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTWZ_NLO                = Sample.nanoAODfromDAS("TTWZ_NLO",  "/TTWZ_TuneCUETP8M2T4_13TeV-madgraph-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTZZ_NLO                = Sample.nanoAODfromDAS("TTZZ_NLO",  "/TTZZ_TuneCUETP8M2T4_13TeV-madgraph-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)

TTW_LO                  = Sample.nanoAODfromDAS("TTW_LO",  "/ttWJets_13TeV_madgraphMLM/mmoser-crab_RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTWJetsToLNu_NLO        = Sample.nanoAODfromDAS("TTWJetsToLNu_NLO",  "/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTWJetsToQQ_NLO         = Sample.nanoAODfromDAS("TTWJetsToQQ_NLO",  "/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTZToLLNuNu_NLO_ext2    = Sample.nanoAODfromDAS("TTZToLLNuNu_NLO_ext2",  "/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTZToLLNuNu_NLO_ext3    = Sample.nanoAODfromDAS("TTZToLLNuNu_NLO_ext3",  "/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTZToLL_M1to10_LO       = Sample.nanoAODfromDAS("TTZToLL_M1to10_LO",  "/TTZToLL_M-1to10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TTZToQQ_NLO             = Sample.nanoAODfromDAS("TTZToQQ_NLO",  "/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TtZJets_LO              = Sample.nanoAODfromDAS("TtZJets_LO",  "/ttZJets_13TeV_madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TtHToNonbb_pow          = Sample.nanoAODfromDAS("TtHToNonbb_pow",  "/ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TtHTobb_pow             = Sample.nanoAODfromDAS("TtHTobb_pow",  "/ttHTobb_M125_13TeV_powheg_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)
TGG                     = Sample.nanoAODfromDAS("TGG",  "/TGGJets_leptonDecays_13TeV_MadGraph_madspin_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER", dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=-1)

T = [
      TTTo2L2Nu_noSC_pow,
      TTTo2L2Nu_pow_CP5,
      TTTo2L2Nu_pow,
      TTToSemilepton_pow,
      TTToSemilepton_pow_CP5,
      TT_pow,

      ST_schannel_4f_NLO,
      ST_schannel_4f_CP5,
      ST_tchannel_antitop_4f_pow,
      ST_tchannel_antitop_4f_pow_CP5,
      ST_tchannel_top_4f_pow,
      ST_tchannel_top_4f_pow_CP5,

      ST_tW_antitop_NoFullyHad_5f_pow,
      ST_tW_antitop_5f_pow_ext1,
      ST_tW_antitop_5f_pow,
      ST_tW_antitop_5f_pow_CP5,
      ST_tW_top_NoFullyHad_5f_pow,
      ST_tW_top_NoFullyHad_5f_pow_ext,
      ST_tW_top_5f_pow_ext1,
      ST_tW_top_5f_pow,
      ST_tW_top_5f_pow_CP5,
      ST_tWll_5f_LO,
      ST_tWnunu_5f_LO,

      THQ_LO,
      THW_LO,
      TZq_ll_NLO,
      TZq_nunu_NLO,

      TTTT_NLO,
      TTWW_NLO,
      TTWZ_NLO,
      TTZZ_NLO,

      TTW_LO,
      TTWJetsToLNu_NLO,
      TTWJetsToQQ_NLO,
      TTZToLLNuNu_NLO_ext2,
      TTZToLLNuNu_NLO_ext3,
      TTZToLL_M1to10_LO,
      TTZToQQ_NLO,
      TtZJets_LO,
      TtHToNonbb_pow,
      TtHTobb_pow,
      TGG,
      ]


allSamples = DY + QCD + T


for s in allSamples:
    s.isData = False

from Samples.Tools.AutoClass import AutoClass
samples = AutoClass( allSamples )
