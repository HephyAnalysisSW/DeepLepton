# Standard imports 
import sys
import ROOT
import imp
import pickle
import ctypes
import numpy as np
import itertools
import operator
import os

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

from DeepLepton.Tools.Cache import Cache
from Analysis.Tools.CardFileWriter  import CardFileWriter
from regions import regions

baseDir       = os.path.join( cache_directory, "caches" )
if not os.path.exists( baseDir ): os.makedirs( baseDir )
estimate_cacheFileName   = os.path.join( baseDir, "estimates" )
estimateCache      = MergingDirDB( estimate_cacheFileName )
cardfileLocation = os.path.join( cache_directory, "cardFiles" )

limitDir       = os.path.join( cache_directory, "limits" )
if not os.path.exists(limitDir): os.makedirs(limitDir)
limit_cacheFileName = os.path.join(limitDir, 'calculatedLimits')
limitCache    = Cache(limit_cacheFileName, verbosity=3)


sample_list = ["DY", "TTJets_DiLepton", "WJets", "VV", "TTJets_SingleLepton", "SMS"]#, "Data"]
bg_list = ["DY", "TTJets_DiLepton", "WJets", "VV", "TTJets_SingleLepton"]


c = CardFileWriter()
c.addUncertainty('JES', 'lnN')
c.addUncertainty('btagging', 'lnN')
c.addUncertainty('mistagging', 'lnN')
c.addUncertainty('muonId', 'lnN')
c.addUncertainty('electronId', 'lnN')

for stopm in [(250+25*i) for i in range(23)]:
    for lspm in [(stopm - delta) for delta in [10,20,30,40,50,60,70,80]]:
        
        observation = []
        for i_region ,region in enumerate(regions):
            nice_name = str(region)
            bin_name = "Region_%i" % i_region
            c.addBin(bin_name, [bg for bg in bg_list], nice_name)
            observation.append(0.)
            nice_name = str(region)
            for bg in bg_list:       
                key=(bg+'_'+str(region))
                estimate = estimateCache.get(key)
                observation[i_region] += estimate
                c.specifyExpectation( bin_name, bg, int(estimate) ) 
                c.specifyUncertainty( 'JES', bin_name, bg, 1.1)
                c.specifyUncertainty( 'btagging', bin_name, bg, 1.1)
                c.specifyUncertainty( 'mistagging', bin_name, bg, 1.1)
                c.specifyUncertainty( 'muonId', bin_name, bg, 1.1)
                c.specifyUncertainty( 'electronId', bin_name, bg, 1.1)
            c.specifyObservation(bin_name, int(observation[i_region]))
            estimate_sig = estimateCache.get("SMS_T2tt_"+str(stopm)+'_'+str(lspm)+'_'+str(region))
            c.specifyExpectation( bin_name, 'signal', int(estimate_sig))
            c.specifyUncertainty( 'JES', bin_name, 'signal', 1.1)
            c.specifyUncertainty( 'btagging', bin_name, 'signal', 1.1)
            c.specifyUncertainty( 'mistagging', bin_name, 'signal', 1.1)
            c.specifyUncertainty( 'muonId', bin_name, 'signal', 1.1)
            c.specifyUncertainty( 'electronId', bin_name, 'signal', 1.1)
            
        cardname = "cardfile_"+str(stopm)+'_'+str(lspm)
        cardFilePath = os.path.join( cardfileLocation, cardname + '.txt' )
        c.writeToFile( cardFilePath )
        print("produced ", cardname)

        limit = c.calcLimit(cardFilePath)
        limitCache.add((stopm,lspm), limit)




