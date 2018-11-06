# Standard imports
import ROOT
import os
import sys
import importlib
import random

# RootTools
from RootTools.core.Sample import *

# DeepLepton
from DeepLepton.Tools.user import skim_directory 

DY_2016 = [
'DY1JetsToLL_M50_LO',
'DY2JetsToLL_M50_LO',
'DY3JetsToLL_M50_LO',
'DY4JetsToLL_M50_LO',
]

TTJets_diLepton_2016 = [
'TTJets_DiLepton',
'TTJets_DiLepton_ext',
]

TTJets_singleLepton_2016 = [
'TTJets_SingleLeptonFromTbar',
'TTJets_SingleLeptonFromTbar_ext',
'TTJets_SingleLeptonFromT',
'TTJets_SingleLeptonFromT_ext',
]

TT_Lepton_2016 = ['TTLep_pow',]
TT_semiLepton_2016 = ['TTSemiLep_pow',]

QCD_2016 = [
'QCD_Pt15to20_Mu5',
'QCD_Pt20to30_Mu5',
'QCD_Pt30to50_Mu5',
'QCD_Pt50to80_Mu5',
'QCD_Pt80to120_Mu5',
'QCD_Pt80to120_Mu5_ext',
'QCD_Pt120to170_Mu5',
'QCD_Pt170to300_Mu5',
'QCD_Pt170to300_Mu5_ext',
'QCD_Pt300to470_Mu5',
'QCD_Pt300to470_Mu5_ext',
'QCD_Pt300to470_Mu5_ext2',
'QCD_Pt470to600_Mu5',
'QCD_Pt470to600_Mu5_ext',
'QCD_Pt470to600_Mu5_ext2',
'QCD_Pt600to800_Mu5',
'QCD_Pt600to800_Mu5_ext',
'QCD_Pt800to1000_Mu5',
'QCD_Pt800to1000_Mu5_ext',
'QCD_Pt800to1000_Mu5_ext2',
'QCD_Pt1000toInf_Mu5',
'QCD_Pt1000toInf_Mu5_ext',
]

#parser
def get_parser():
    ''' Argument parser for post-processing module.
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser for cmgPostProcessing")

    argParser.add_argument('--year',                        action='store',                     type=int,   choices=[2016,2017],    required = True,               help="Which year?")
    argParser.add_argument('--logLevel',                    action='store',         nargs='?',              choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET', 'SYNC'],     default='INFO',                     help="Log level for logging")
    argParser.add_argument('--sample',                      action='store',         nargs='?',  type=str,                           default='WZTo3LNu',            help="List of samples to be post-processed, given as CMG component name")
    argParser.add_argument('--nJobs',                       action='store',         nargs='?',  type=int,                           default=1,                     help="Maximum number of simultaneous jobs.")
    argParser.add_argument('--job',                         action='store',                     type=int,                           default=0,                     help="Run only job i")
    argParser.add_argument('--version',                     action='store',         nargs='?',  type=str,  required = True,                                        help="Version for output directory")
    argParser.add_argument('--flavour',                     action='store',                     type=str,   choices=['ele','muo'],    required = True,             help="Which flavour?")
    argParser.add_argument('--sampleSelection',             action='store',                     type=str,   choices=['DY', 'QCD', 'DYvsQCD', 'TTJets', 'TTbar'],  required = True,             help="Which flavour?")
    argParser.add_argument('--small',                       action='store_true',                                                                                        help="Run the file on a small sample (for test purpose), bool flag set to True if used")        
    argParser.add_argument('--ptSelection',                 action='store',                     type=str,   default = "pt_10_-1",                                  help="Which flavour?")

    return argParser

options = get_parser().parse_args()

# Logging
import DeepLepton.Tools.logger as logger
logger  = logger.get_logger(options.logLevel, logFile = None)
import RootTools.core.logger as logger_rt
logger_rt = logger_rt.get_logger(options.logLevel, logFile = None )

selectionString = '(evt%'+str(options.nJobs)+'=='+str(options.job)+'&&abs(lep_pdgId)=='+ ('11' if options.flavour=='ele' else '13')+')'

random.seed(100)

def getInput( sub_directories, class_name):
    inputPath = os.path.join( skim_directory, options.version, "step1", str(options.year), options.flavour, class_name, options.ptSelection)
    inputList = [(os.path.join( inputPath, s )) for s in sub_directories]
    sample = Sample.fromDirectory( class_name, inputList, 'tree', None, selectionString)
    random.shuffle( sample.files )
    return sample

#settings
if options.year == 2016:
    if options.sampleSelection == "DYvsQCD":
        samplePrompt    = getInput( DY_2016, "Prompt")
        sampleNonPrompt = getInput( QCD_2016, "NonPrompt")
        sampleFake      = getInput( QCD_2016, "Fake")
    elif options.sampleSelection == "TTJets":
        samplePrompt    = getInput( TTJets_diLepton_2016+TTJets_singleLepton_2016, "Prompt")
        sampleNonPrompt = getInput( TTJets_diLepton_2016+TTJets_singleLepton_2016, "NonPrompt")
        sampleFake      = getInput( TTJets_diLepton_2016+TTJets_singleLepton_2016, "Fake")

if options.small:
    for s in [ samplePrompt, sampleNonPrompt, sampleFake ]: 
        s.reduceFiles( to = 2 )

prompt    =  {'name':'Prompt',    'sample':samplePrompt,    'TChain':ROOT.TChain('tree'), 'counter':0 }
nonPrompt =  {'name':'NonPrompt', 'sample':sampleNonPrompt, 'TChain':ROOT.TChain('tree'), 'counter':0 }
fake      =  {'name':'Fake',      'sample':sampleFake,      'TChain':ROOT.TChain('tree'), 'counter':0 }

leptonClasses  = [ prompt, nonPrompt, fake ]

postfix = '' if options.nJobs==1 else "_%i" % options.job

#Loop
for leptonClass in leptonClasses:
    logger.info( "Class %s", leptonClass['name'] )

    inputPath = os.path.join( skim_directory, options.version, "step1", str(options.year), options.flavour, leptonClass['name'], options.ptSelection)

    for sampleFile in leptonClass['sample'].files:
            
        leptonClass['TChain'].Add(sampleFile)
    leptonClass['TChain'] = leptonClass['TChain'].CopyTree(selectionString)

    leptonClass['Entries'] = leptonClass['TChain'].GetEntries()
    logger.info( "flavor %s class %s entries %i", options.flavour, leptonClass['name'], leptonClass['Entries'] )

x = [[0,1,2], [leptonClass['Entries'] for leptonClass in leptonClasses]]
y = sum(([t] * w for t, w in zip(*x)), [])

n_maxfileentries = 100000
n_current_entries  = 0
n_file           = 0

outputDir = os.path.join( skim_directory, options.version + ("_small" if options.small else ""), "step2", str(options.year), options.flavour, options.ptSelection, options.sampleSelection)

if not os.path.exists( outputDir ):
    os.makedirs( outputDir )
outputPath = os.path.join( outputDir, 'modulo_'+str(options.job)+'_trainfile_' )

while (prompt['counter']<prompt["Entries"] and nonPrompt['counter']<nonPrompt["Entries"] and fake['counter']<fake["Entries"]):

    #(re)create and save output files
    if n_current_entries==0 and n_file==0:
        outputFile     = ROOT.TFile(str(outputPath)+str(n_file)+'.root', 'recreate')
        outputFileTree = fake['TChain'].CloneTree(0,"")
    if n_current_entries==0 and n_file>0:
        logger.info("%i entries copied to %s", outputFileTree.GetEntries(), outputPath+str(n_file-1)+".root" )
        logger.info("Counter: prompt %i nonprompt %i fake %i", prompt['counter'], nonPrompt['counter'], fake['counter'])
        outputFile.Write(outputPath+str(n_file-1)+".root", outputFile.kOverwrite)
        outputFile.Close()
        outputFile     = ROOT.TFile(outputPath+str(n_file)+".root", 'recreate')
        outputFileTree = fake['TChain'].CloneTree(0,"")

    #write lepton from random class into output file
    choice = random.choice(y)
    inputEntry   = leptonClasses[choice]['TChain'].GetEntry(leptonClasses[choice]['counter'])
    TChainTree   = leptonClasses[choice]['TChain'].GetTree()

    TChainTree.CopyAddresses(outputFileTree)
    outputEntry  = outputFileTree.Fill()
    if inputEntry!=outputEntry: 
        logger.error("error while copying entry")
        break 
   
    #increase counters
    leptonClasses[choice]['counter'] += 1
    n_current_entries += 1

    #check if maximal file entries reached
    if n_current_entries>=n_maxfileentries:
        n_current_entries=0
        n_file += 1

#Save and Close last output File        
logger.info("%i entries copied to %s", outputFileTree.GetEntries(), outputPath+str(n_file)+".root" )
logger.info("Counter: prompt %i nonprompt %i fake %i", prompt['counter'], nonPrompt['counter'], fake['counter'])
outputFile.Write(outputPath+str(n_file)+".root", outputFile.kOverwrite)
outputFile.Close()
