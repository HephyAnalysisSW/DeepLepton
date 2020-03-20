

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
from DeepLepton.Tools.triggerSelector_deepLepton_analysis import triggerSelector

from regions import regions
 
# Arguments
import argparse

argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--selection',          action='store',     default='', help="Specify cut.")
argParser.add_argument('--small',              action='store_true', default=False, help='Run only on a small subset of the data?')
argParser.add_argument('--region',             action='store',)
argParser.add_argument('--sample',             action='store',      default='DY')#, choices = ["DY", "TTJets_DiLepton", "WJets", "VV", "TTJets_SingleLepton", "SMS", "Data"])
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
    
    sample_dict = {"DY":DY, "TTJets_DiLepton":TTJets_DiLepton, "WJets":WJets, "VV":VV, "TTJets_SingleLepton":TTJets_SingleLepton}#, "SMS":SMS_T2tt_lowerpt}    

    if args.sample == "Data":
        MET_data     = vars()['MET_Run2016']
        sample         = MET_data
    elif "SMS" in args.sample:
        sample = SMS_T2tt_lowerpt
        #sample = SMS_T2tt_SF2
    else:
        sample = sample_dict[args.sample]


baseDir       = os.path.join( cache_directory, "caches" )
if not os.path.exists( baseDir ): os.makedirs( baseDir )

cacheFileName   = os.path.join( baseDir, "estimates" )
limitCache      = MergingDirDB( cacheFileName )

tr = triggerSelector(args.year)
if 'lower_met' in str(region):
    triggerSelection = tr.getSelection("MET")
else:
    triggerSelection = tr.getSelection("MET_high")


selectionString      = cutInterpreter.cutString(args.selection )
print(selectionString)
if sample == SMS_T2tt_lowerpt or sample == SMS_T2tt_SF2 or sample==SMS_T2tt_SF:
    sample.setSelectionString( [selectionString] )
else:
    sample.setSelectionString( [selectionString, triggerSelection] )

#if args.sample == "SMS":
#    sample.setWeightString(str(1234.35))  #TODO: Test!
#else:
sample.setWeightString(lumi_scale)
    
#sample.scale = lumi_scale


weight_ = lambda event, sample: event.weight


sample.read_variables = ["reweightPU36fb/F", "reweightBTagDeepCSV_SF/F"]#, "nlep/I",  "lep[%s]"%(lepton_branches_mc) ]
#sample.weight         = lambda event, sample: event.reweightBTagDeepCSV_SF*event.reweightPU36fb*0.5 # *(1 if args.small else args.reduceMC)
#sample.setWeightString( 'lumiweight1fb*%f/2.5'%(lumi_scale))


if args.small:
    #sample.normalization=1.
    sample.reduceFiles( factor=5 )
    #eventScale = 1./sample.normalization
    #sample.addWeightString(eventScale)



from stops_13TeV import xsecNNLL
from filter_efficiencies import filter_eff

if "SMS" in args.sample:
    WP = args.sample.split('_')[-2:]
    xsec = xsecNNLL[int(WP[0])][0]
    eff = norm[int(WP[0])][int(WP[1])]
    #signal_normalization = 14537894./(float(lumi_scale)*1000.*xsec*10.*eff)
    #signal_normalization = 2.35*1e-5*10000.*xsec * float(lumi_scale)

    #signal_normalization = xsec * float(lumi_scale) * eff
    signal_normalization = xsec * float(lumi_scale) / (109214.) #* eff   

    norm_string = str(signal_normalization)
    print('normalization:', norm_string)
    #sample_rate = sample.getYieldFromDraw( selectionString=region.cutString(), weightString = '%f*weight*reweightBTagDeepCSV_SF*reweightPU36fb'%(signal_normalization) )['val']
    sample_rate = sample.getYieldFromDraw( selectionString=region.cutString(), weightString = '%f*reweightBTagDeepCSV_SF*reweightPU36fb'%(signal_normalization) )['val']
else:
    sample_rate = sample.getYieldFromDraw( selectionString=region.cutString(), weightString = 'weight*reweightBTagDeepCSV_SF*reweightPU36fb' )['val']


limitCache.add(key=(str(args.sample)+'_'+str(region)), data=sample_rate)

print(str(args.sample)+'_'+str(region), sample_rate)






