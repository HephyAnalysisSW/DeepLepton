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

results = []

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
            c.specifyExpectation( bin_name, 'signal', estimate_sig)#int(estimate_sig))
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
        limitCache.add((stopm,stopm), limit)
        results.append(((stopm,stopm), limit))

#limitResultsFilename = os.path.join(baseDir, 'limits', 'SMS_T2tt', 'limitResults.root')

if not os.path.isdir(os.path.join(baseDir, 'limits', 'SMS_T2tt')):
  os.makedirs(os.path.join(baseDir, 'limits', 'SMS_T2tt'))
limitResultsFilename = os.path.join(baseDir, 'limits', 'SMS_T2tt','limitResults.root')

def toGraph2D(name,title,length,x,y,z):
    result = ROOT.TGraph2D(length)
    result.SetName(name)
    result.SetTitle(title)
    for i in range(length):
        result.SetPoint(i,x[i],y[i],z[i])
    h = result.GetHistogram()
    h.SetMinimum(min(z))
    h.SetMaximum(max(z))
    c = ROOT.TCanvas()
    result.Draw()
    del c
    #res = ROOT.TGraphDelaunay(result)
    return result

mStop_list = []
mLSP_list  = []
exp_list   = []
obs_list   = []
exp_up_list   = []
exp_down_list   = []

for r in results:
    s, res = r
    mStop, mNeu = s
    #if mStop%50>0: continue
    #if mNeu%50>0 and not mNeu>(mStop-125): continue
    mStop_list.append(mStop)
    mLSP_list.append(mNeu)
    exp_list.append(res['0.500'])
    exp_up_list.append(res['0.160'])
    exp_down_list.append(res['0.840'])
    obs_list.append(res['-1.000'])

scatter         = ROOT.TGraph(len(mStop_list))
scatter.SetName('scatter')
for i in range(len(mStop_list)):
    scatter.SetPoint(i,mStop_list[i],mLSP_list[i])

exp_graph       = toGraph2D('exp','exp',len(mStop_list),mStop_list,mLSP_list,exp_list)
exp_up_graph    = toGraph2D('exp_up','exp_up',len(mStop_list),mStop_list,mLSP_list,exp_up_list)
exp_down_graph  = toGraph2D('exp_down','exp_down',len(mStop_list),mStop_list,mLSP_list,exp_down_list)
obs_graph       = toGraph2D('obs','obs',len(mStop_list),mStop_list,mLSP_list,obs_list)

outfile = ROOT.TFile(limitResultsFilename, "recreate")
scatter        .Write()
exp_graph      .Write()
exp_down_graph .Write()
exp_up_graph   .Write()
obs_graph      .Write()
outfile.Close()

print limitResultsFilename




#exp      = ROOT.TH2F("exp", "exp", 1600/25, 0, 1600, 1500/25, 0, 1500)
#exp_down = exp.Clone("exp_down")
#exp_up   = exp.Clone("exp_up")
#obs      = exp.Clone("obs")
#
#for r in results:
#    s, res = r
#    mStop, mNeu = s
#    resultList = [(exp, '0.500'), (exp_up, '0.160'), (exp_down, '0.840'), (obs, '-1.000')]
#    for hist, qE in resultList:
#      #print hist, qE, res[qE]
#      if qE=='0.500':
#        print "Masspoint m_gl %5.3f m_neu %5.3f, expected limit %5.3f"%(mStop,mNeu,res[qE])
#      if qE=='-1.000':
#        print "Observed limit %5.3f"%(res[qE])
#      hist.GetXaxis().FindBin(mStop)
#      hist.GetYaxis().FindBin(mNeu)
#      #print hist.GetName(), mStop, mNeu, res[qE]
#      hist.Fill(mStop, mNeu, res[qE]) 
#
#limitResultsFilename = os.path.join(baseDir, 'limits', 'SMS_T2tt', 'limitResults.root')
#if not os.path.exists(os.path.dirname(limitResultsFilename)):
#      os.makedirs(os.path.dirname(limitResultsFilename))
#
#outfile = ROOT.TFile(limitResultsFilename, "recreate")
#exp      .Write()
#exp_down .Write()
#exp_up   .Write()
#obs      .Write()
#outfile.Close()
#print "Written %s"%limitResultsFilename



