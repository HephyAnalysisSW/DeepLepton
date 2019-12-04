

# Standard imports 
import sys
import ROOT
import imp
import pickle
import ctypes
import numpy as np
import itertools
import operator
from shutil import copyfile
from math import sqrt
# turn off graphics
ROOT.gROOT.SetBatch( True )

from RootTools.core.standard import *
from Analysis.Tools.MergingDirDB import MergingDirDB
from multiprocessing import Pool

# Logger
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   'DEBUG', logFile = None)
logger_rt = logger_rt.get_logger('INFO', logFile = None)

from DeepLepton.Tools.user  import plot_directory, cache_directory
from DeepLepton.Tools.cutInterpreter    import cutInterpreter

from regions import regions
 
# Arguments
import argparse

argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--selection',          action='store',     default='lepSel3-onZ-njet3p-nbjet1p-Zpt0', help="Specify cut.")
argParser.add_argument('--small',              action='store_true', default=False, help='Run only on a small subset of the data?')
argParser.add_argument('--region',             action='store',)
argParser.add_argument('--sample',             action='store',      default='DY', choices = ["DY", "TTJets_DiLepton", "WJets", "VV", "TTJets_SingleLepton", "SMS", "Data"])
argParser.add_argument('--year',               action='store',      default=2016)
argParser.add_argument('--lumi',               action='store',      default="35.9")

args = argParser.parse_args()
args.year = int(args.year)
region = regions[int(args.region)]
lumi_scale = args.lumi

if args.year == 2017:
    raise NotImplementedError
elif args.year == 2016:
    data_directory = '/afs/hephy.at/data/cms03/DeepLepton/results/'
    postProcessing_directory = "deepLepton_v5/dilep/"
    from DeepLepton.samples.cmgTuples_Data25ns_80X_07Aug17_postProcessed import *
    from DeepLepton.samples.cmgTuples_deepLepton_Summer16_mAODv2_postProcessed import *
    
    sample_dict = {"DY":DY, "TTJets_DiLepton":TTJets_DiLepton, "WJets":WJets, "VV":VV, "TTJets_SingleLepton":TTJets_SingleLepton, "SMS":SMS_T2tt_lowerpt}    

    if args.sample == "Data":
        MET_data     = vars()['MET_Run2016']
        sample         = MET_data
    else:
        sample = sample_dict[args.sample]


baseDir       = os.path.join( cache_directory, "caches" )
if not os.path.exists( baseDir ): os.makedirs( baseDir )

cacheFileName   = os.path.join( baseDir, "estimates" )
limitCache      = MergingDirDB( cacheFileName )

selectionString      = cutInterpreter.cutString(args.selection)
sample.setSelectionString( selectionString )
sample.setWeightString(lumi_scale)

if args.small:
    sample.normalization=1.
    sample.reduceFiles( factor=10 )
    eventScale = 1./sample.normalization
    sample.addWeightString(eventScale)

sample_rate  = sample.getYieldFromDraw( selectionString=region.cutString(), weightString=None )['val']
limitCache.add(key=(str(args.sample)+'_'+str(region)), data=sample_rate)









