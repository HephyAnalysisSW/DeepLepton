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
dbFile = dbDir+'/DB_Summer16_DeepLepton.sql'

logger.info("Using db file: %s", dbFile)

redirector = "/eos/vbc/experiments/cms/"

## DY
DYJetsToLL_M50_LO = Sample.nanoAODfromDAS("DYJetsToLL_M50_LO",       "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",   dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=False, xSection=2075.14*3)

DY = [ DYJetsToLL_M50_LO ]

QCD_Mu_Pt30to50   = Sample.nanoAODfromDAS("DYJetsToLL_M10to50_LO",   "/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/mmoser-crab_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_v6_PFCands-91e8898dad3723f03bca2e9d2835912d/USER",   dbFile=dbFile, instance = "phys03", redirector=redirector, overwrite=ov, xSection=18610)
QCD = [ QCD_Mu_Pt30to50 ]


allSamples = DY + QCD


for s in allSamples:
    s.isData = False

from Samples.Tools.AutoClass import AutoClass
samples = AutoClass( allSamples )
