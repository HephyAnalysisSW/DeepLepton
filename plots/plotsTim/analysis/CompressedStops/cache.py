''' Plot script WC parameter LogLikelihood
'''

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

# RootTools
from RootTools.core.standard import *

from Analysis.Tools.MergingDirDB                import MergingDirDB

from multiprocessing import Pool

# Logger
#import TTXPheno.Tools.logger as logger
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   'DEBUG', logFile = None)
logger_rt = logger_rt.get_logger('INFO', logFile = None)

# TTXPheno
#from TTXPheno.samples.benchmarks        import *   
from DeepLepton.Tools.user  import plot_directory, cache_directory
from DeepLepton.Tools.cutInterpreter    import cutInterpreter

ROOT.gStyle.SetNumberContours(255)

# Arguments
import argparse

argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--version',            action='store',     default='v2', help='Appendix to plot directory')
#argParser.add_argument('--bestFit',            action='store_true', help='Run combine with bestFit scenario (wide r ranges)')
#argParser.add_argument('--removeCardFiles',    action='store_true', help='remove cardfiles after calculation?')
argParser.add_argument('--selection',          action='store',     default='lepSel3-onZ-njet3p-nbjet1p-Zpt0', help="Specify cut.")
argParser.add_argument('--small',              action='store_true', default=False, help='Run only on a small subset of the data?')
#argParser.add_argument('--contours',           action='store_true', help='draw 1sigma and 2sigma contour line?')
#argParser.add_argument('--binning',            action='store',     default = [10, 0.0, 0.003], type=float, nargs=3, help = "argument parameters")
#argParser.add_argument('--yRange',             action='store',     default = [0, 6], type=float, nargs=2, help = "argument parameters")
argParser.add_argument('--cores',              action='store',     default=1, type=int, help='number of cpu cores for multicore processing')
argParser.add_argument('--overwrite',          action='store_true', help='overwrite datafile?')
#argParser.add_argument('--fitOnly',            action='store_true', help='plot only?')
argParser.add_argument('--sample',             action='store',      default='ttZ', choices = ["tt", "ttZ"])
argParser.add_argument('--year',               action='store',      default=2016, choices = [2016, 2017])
argParser.add_argument('--signal',             action='store',      default='SMS', choices = ["SMS"])
#argParser.add_argument('--pdf',                action='store',      default='1d0')

args = argParser.parse_args()

args.selection = "lep_SR_all-jet_SR-med_met-filters"


lumi_scale = 35.9
nloXSec   = 831.76 #inclusive NLO xsec
#nloXSec   = 0.0915/(0.10099) if args.sample == "ttZ" else 831.76 #inclusive NLO xsec

from regions import regions
#if args.binning[0] > 1:
#    xRange = np.linspace( args.binning[1], args.binning[2], int(args.binning[0]), endpoint=False)
#else:
#    xRange = [ 0.5 * ( args.binning[2] - args.binning[1] ) ]


if args.year == 2017:
    raise NotImplementedError
elif args.year == 2016:
    data_directory = '/afs/hephy.at/data/cms03/DeepLepton/results/'
    postProcessing_directory = "deepLepton_v5/dilep/" 
    from DeepLepton.samples.cmgTuples_Data25ns_80X_07Aug17_postProcessed import *
    data_directory = '/afs/hephy.at/data/cms03/DeepLepton/results/'
    postProcessing_directory = "deepLepton_v5/dilep/" 
    from DeepLepton.samples.cmgTuples_deepLepton_Summer16_mAODv2_postProcessed import *    
     
    MET_data     = vars()['MET_Run2016']
    data_sample         = MET_data

if args.year == 2017:
    raise NotImplementedError 
    mc             = [ ]
elif args.year == 2016:
    mc             = [ DY, TTJets_DiLepton, VV,]
for sample in mc: sample.style = styles.fillStyle(sample.color)


if args.signal == "SMS":
    data_directory = '/afs/hephy.at/data/cms03/DeepLepton/results/'
    postProcessing_directory = "deepLepton_v5/dilep/" 
    from DeepLepton.samples.cmgTuples_deepLepton_Summer16_mAODv2_postProcessed import *
    SMS_T2tt                 = SMS_T2tt_lowerpt
    SMS_T2tt.style           = styles.lineStyle( ROOT.kRed, width=3 )
    signal = [ SMS_T2tt,]
else:
    signal = []

# Samples
from DeepLepton.samples.cmgTuples_Data25ns_80X_07Aug17_postProcessed import *
from DeepLepton.samples.cmgTuples_deepLepton_Summer16_mAODv2_postProcessed import *
#from TTXPheno.samples.hepmc_samples_11_06  import *
#hepSample = ttbarZ if args.sample == "ttZ" else ttbar
#hepSample.root_samples_dict = { name:sample for name, sample in hepSample.root_samples_dict.iteritems() if name.startswith(args.pdf+"_") or name == "PP"}

baseDir       = os.path.join( cache_directory, "hepmc", "limits" )
if not os.path.exists( baseDir ): os.makedirs( baseDir )

cacheFileName   = os.path.join( baseDir, "calculatedLimits" )
limitCache      = MergingDirDB( cacheFileName )

#sample_directory = hepSample.name
#if args.small:     sample_directory += "_small"

addon = []


# set selection string
selectionString      = cutInterpreter.cutString(args.selection)

# configure samples
for sample in signal:
    sample.setWeightString( 'lumiweight1fb*%f/2.5'%(lumi_scale))#, fancyScale ) ) #correct plots by hand (sorry)
    sample.setSelectionString( selectionString )
    print sample.weightString, sample.name
#for sample in bg:
for sample in mc:
    sample.setWeightString( 'lumiweight1fb*%f/2.5'%(lumi_scale))#, 2. if sample.name == tWSample.name else .1 if sample.name == WJetsSample.name else 1.) )
    sample.setSelectionString( selectionString )
    print sample.weightString, sample.name
     if sample.name == WJetsSample.name: sample.addWeightString(".1")
     if sample.name == tWSample.name: sample.addWeightString("2.") #xsec correction t and tbar
# somehow has to be separate from the next loop
if args.small:
    for sample in signal + bg:
        sample.normalization=1.
        sample.reduceFiles( factor=10 )
        eventScale = 1./sample.normalization
        sample.addWeightString(eventScale)

observation                    = {}

signal_btagging_uncertainty    = {}
signal_mistagging_uncertainty  = {}
signal_jes_uncertainty         = {}
signal_electronId_uncertainty  = {}
signal_muonId_uncertainty      = {}


signal_SM_rate                  = {}
signal_coeffList                = {}

background_rate                   = {}
background_btagging_uncertainty   = {}
background_mistagging_uncertainty = {}
background_jes_uncertainty        = {}
background_electronId_uncertainty = {}
background_muonId_uncertainty     = {}

inonPromptObservation              = {}

#SMsigmaC = getHiggsWeight( 0 )

for i_region, region in enumerate(regions):
    # compute signal yield for this region (this is the final code)

    logger.info( "At region %s", region )

    # signal SM
    if  not limitCache.contains("signal_"+str(region)): 
        signal_SM_rate[region]    = signal[0].getYieldFromDraw( selectionString=region.cutString(), weightString="%f"%(nloXSec) )['val']
        limitCache.add(key="signal_"+str(region), signal_SM_rate[region])
    
    background_rate[region]                   = {}
    background_btagging_uncertainty[region]   = {}
    background_mistagging_uncertainty[region] = {}
    background_muonId_uncertainty[region]     = {}
    background_electronId_uncertainty[region] = {}
    background_jes_uncertainty[region]        = {}

    for i_background, background in enumerate(mc):
        # compute bg yield for this region (this is the final code)

        if  not limitCache.contains(str(background)+'_'+str(region)): 
            background_rate                   [region][background.name] = background.getYieldFromDraw( selectionString=region.cutString() )['val']
            limitCache.add(key=str(background.name)'_'+str(region), signal_SM_rate[region])

        background_btagging_uncertainty   [region][background.name] = 1.1
        background_mistagging_uncertainty [region][background.name] = 1.1
        background_muonId_uncertainty     [region][background.name] = 1.1
        background_electronId_uncertainty [region][background.name] = 1.1
        background_jes_uncertainty        [region][background.name] = 1.1

    #observation[region] = int( sum( background_rate[region].values() + [signal_SM_rate[region]] ) )


