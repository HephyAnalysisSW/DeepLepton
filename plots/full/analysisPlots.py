#!/usr/bin/env python
''' Analysis script for standard plots
'''
#
# Standard imports and batch mode
#
import ROOT, os
ROOT.gROOT.SetBatch(True)
import itertools

from math                         import sqrt, cos, sin, pi
from RootTools.core.standard      import *
from DeepLepton.Tools.user            import plot_directory
from DeepLepton.Tools.helpers         import deltaR, deltaPhi, getObjDict, getVarValue
from DeepLepton.Tools.objectSelection import getFilterCut, isAnalysisJet, isBJet
from DeepLepton.Tools.cutInterpreter  import cutInterpreter

#
# Arguments
# 
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',      default='INFO',          nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--noData',             action='store_true', default=False,           help='also plot data?')
argParser.add_argument('--year',               action='store',      default=2016,            choices = [2016, 2017], type=int, help='2016 or 2017?',)
argParser.add_argument('--small',                                   action='store_true',     help='Run only on a small subset of the data?', )
argParser.add_argument('--plot_directory',     action='store',      default='DeepLepton')
argParser.add_argument('--selection',          action='store',      default='njet1p-btag1p')
args = argParser.parse_args()

#
# Logger
#
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

if args.small:                        args.plot_directory += "_small"
if args.year == 2017:                 args.plot_directory += "_Run2017"
if args.noData:                       args.plot_directory += "_noData"
#
# Make samples, will be searched for in the postProcessing directory
#

if args.year == 2017:
    postProcessing_directory = "TopEFT_PP_2017_v14/dilep"
    data_directory           = "/afs/hephy.at/data/dspitzbart02/cmgTuples"  
    from DeepLepton.samples.cmgTuples_Data25ns_92X_Run2017_postProcessed import *
    from DeepLepton.samples.cmgTuples_Summer17_92X_mAODv2_postProcessed import *

    #SingleElectron_data = SingleElectron_Run2017
    #SingleMuon_data     = SingleMuon_Run2017
    #SingleEleMu_data    = SingleEleMu_Run2017

else:
    data_directory           = "/afs/hephy.at/data/rschoefbeck02/cmgTuples/"  
    postProcessing_directory = "deepLepton_v4/singlelep"
    from DeepLepton.samples.cmgTuples_Data25ns_80X_07Aug17_postProcessed import *
    data_directory           = "/afs/hephy.at/data/gmoertl01/cmgTuples/"
    postProcessing_directory = "deepLepton_v4/singlelep"
    from DeepLepton.samples.cmgTuples_deepLepton_Summer16_mAODv2_postProcessed import *

    DoubleMuon_data     = DoubleMuon_Run2016
    data_sample         = DoubleMuon_data
# backgrounds / mc
if args.year == 2017:
    mc             = [ ]
else:
    mc             = [ TTJets_DiLepton ]

for sample in mc: sample.style = styles.fillStyle(sample.color)

# Read variables and sequences
#
read_variables =    ["weight/F",
                    "jet[pt/F,eta/F,phi/F,btagCSV/F,id/I,btagDeepCSV/F]", "njet/I", 'nJetSelected/I',
                    "lep[pt/F,eta/F,phi/F,pdgId/I]", "nlep/I",
                    "met_pt/F", "met_phi/F", "metSig/F", "ht/F", "nBTag/I", 
                    ]

sequence = []

def getJets( event, sample ):
    jetVars              = ['eta','pt','phi','btagCSV','id', 'btagDeepCSV']
    event.jets           = filter( lambda j:j['pt']>30 and j['id'], [getObjDict(event, 'jet_', jetVars, i) for i in range(int(getVarValue(event, 'njet')))] )

    event.jets   = filter( isAnalysisJet, event.jets )
    event.b_jets = filter( lambda j: isAnalysisJet(j) and isBJet(j), event.jets )

sequence.append( getJets )

def getLeptons( event, sample ):
    leptonVars              = [ 'eta', 'pt', 'phi']
    #event.leptons           = filter( lambda j:j['pt']>30 and j['id'], [getObjDict(event, 'lepton_', leptonVars, i) for i in range(int(getVarValue(event, 'nlepton')))] )
    #event.leptons   = filter( isAnalysisLepton, event.leptons )
    #event.b_leptons = filter( lambda j: isAnalysisLepton(j) and isBLepton(j), event.leptons )

sequence.append( getLeptons )


sequence.append( makeMyObservables )

# Text on the plots
#
def drawObjects( plotData, dataMCScale, lumi_scale ):
    tex = ROOT.TLatex()
    tex.SetNDC()
    tex.SetTextSize(0.04)
    tex.SetTextAlign(11) # align right
    lines = [
      (0.15, 0.95, 'CMS Preliminary' if plotData else 'CMS Simulation'), 
      (0.45, 0.95, 'L=%3.1f fb{}^{-1} (13 TeV) Scale %3.2f'% ( lumi_scale, dataMCScale ) ) if plotData else (0.45, 0.95, 'L=%3.1f fb{}^{-1} (13 TeV)' % lumi_scale)
    ]
    return [tex.DrawLatex(*l) for l in lines] 

def drawPlots(plots, dataMCScale):
  for log in [False, True]:
    plot_directory_ = os.path.join(plot_directory, 'analysisPlots', args.plot_directory, ("log" if log else "lin"), args.selection)
    for plot in plots:
      if not max(l[0].GetMaximum() for l in plot.histos): 
        logger.warning( "Empty plot! Do nothing" )
        continue # Empty plot
        
      plotting.draw(plot,
	    plot_directory = plot_directory_,
	    ratio = {'yRange':(0.1,1.9)} if not args.noData else None,
	    logX = False, logY = log, sorting = True,
	    yRange = (0.03, "auto") if log else (0.001, "auto"),
	    scaling = {},
	    legend = [ (0.15,0.9-0.03*sum(map(len, plot.histos)),0.9,0.9), 2],
	    drawObjects = drawObjects( not args.noData, dataMCScale , lumi_scale ),
        copyIndexPHP = True
      )

#
# Loop over channels
#
yields     = {}
allPlots   = {}

data_sample.setSelectionString([getFilterCut(isData=True, year=args.year)])
data_sample.name           = "data"
data_sample.read_variables = ["evt/I","run/I"]
data_sample.style          = styles.errorStyle(ROOT.kBlack)
lumi_scale                 = data_sample.lumi/1000

if args.noData: lumi_scale = 35.9
weight_ = lambda event, sample: event.weight

for sample in mc:
  sample.scale          = lumi_scale
  #sample.read_variables = ['reweightTopPt/F','reweightDilepTriggerBackup/F','reweightLeptonSF/F','reweightBTag_SF/F','reweightPU36fb/F', 'nTrueInt/F', 'reweightLeptonTrackingSF/F']
  #sample.weight         = lambda event, sample: event.reweightTopPt*event.reweightBTag_SF*event.reweightLeptonSF*event.reweightDilepTriggerBackup*event.reweightPU36fb*event.reweightLeptonTrackingSF
  sample.setSelectionString([getFilterCut(isData=False, year=args.year)])

if not args.noData:
  stack = Stack(mc, data_sample)
else:
  stack = Stack(mc)

if args.small:
    for sample in stack.samples:
        sample.reduceFiles( to = 1 )

# Use some defaults
Plot.setDefaults(stack = stack, weight = staticmethod( weight_ ), selectionString = cutInterpreter.cutString(args.selection), addOverFlowBin='upper')

plots = []

plots.append(Plot(
  name = 'nVtxs', texX = 'vertex multiplicity', texY = 'Number of Events',
  attribute = TreeVariable.fromString( "nVert/I" ),
  binning=[50,0,50],
))

plots.append(Plot(
    texX = 'E_{T}^{miss} (GeV)', texY = 'Number of Events / 20 GeV',
    attribute = TreeVariable.fromString( "met_pt/F" ),
    binning=[400/20,0,400],
))

plots.append(Plot(
    texX = '#phi(E_{T}^{miss})', texY = 'Number of Events / 20 GeV',
    attribute = TreeVariable.fromString( "met_phi/F" ),
    binning=[10,-pi,pi],
))

plots.append(Plot(
  texX = 'N_{jets}', texY = 'Number of Events',
  attribute = TreeVariable.fromString( "nJetSelected/I" ),
  binning=[5,2.5,7.5],
))

plots.append(Plot(
  texX = 'p_{T}(leading jet) (GeV)', texY = 'Number of Events / 30 GeV',
  name = 'jet1_pt', attribute = lambda event, sample: event.jets[0]['pt'] if len(event.jets)>0 else float('nan'),
  binning=[600/30,0,600],
))

plots.append(Plot(
  texX = 'p_{T}(2nd leading jet) (GeV)', texY = 'Number of Events / 30 GeV',
  name = 'jet2_pt', attribute = lambda event, sample: event.jets[1]['pt'] if len(event.jets)>1 else float('nan'),
  binning=[600/30,0,600],
))

# Lepton plots

#plots.append(Plot(
#  texX = '|#eta|(leading non-b jet)', texY = 'Number of Events / 30 GeV',
#  name = 'jetLeadNonB_absEta', attribute = lambda event, sample: abs(event.leading_untagged_jet['eta']) if event.leading_untagged_jet is not None else float('nan'),
#  binning=[26,0,5.2],
#))

plotting.fill(plots, read_variables = read_variables, sequence = sequence, max_events = 20000 if args.small else -1)

dataMCScale = -1
drawPlots(plots, dataMCScale)

logger.info( "Done with prefix %s and selectionString %s", args.selection, cutInterpreter.cutString(args.selection) )

