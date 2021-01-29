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

DY  = { 2016:['DYJetsToLL_M50_LO'], 
        2017:[], 
        2018:[]}
Top = { 2016:[], 
        2017:[], 
        2018:[]}
QCD = { 'muo': {2016: ['QCD_Mu_Pt30to50'], 
                2017: [], 
                2018: []}, 
        'ele': {2016: [], 
                2017: [], 
                2018: []}} 

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
    argParser.add_argument('--sampleSelection',             action='store',                     type=str,   choices=['DYvsQCD', 'Top', 'all'],           required = True,             help="Which flavour?")
    argParser.add_argument('--small',                       action='store_true',                                                                                   help="Run the file on a small sample (for test purpose), bool flag set to True if used")        
    argParser.add_argument('--ptSelectionStep1',            action='store',                     type=str,   default = "pt_5_-1",                                   help="Which ptSelection in step1?")
    argParser.add_argument('--ptSelection',                 action='store',                     type=str,   default = "pt_5_-1",                                   help="Which ptSelection for step2?")
    argParser.add_argument('--ratio',                       action='store',                     type=str,   choices=['balanced', 'unbalanced'], required = True,   help="Which signal to background ratio?")

    return argParser

options = get_parser().parse_args()

# Logging
import DeepLepton.Tools.logger as logger
logger  = logger.get_logger(options.logLevel, logFile = None)
import RootTools.core.logger as logger_rt
logger_rt = logger_rt.get_logger(options.logLevel, logFile = None )

#pt selection option for different pt sub selection of ptSelection in step1
pt_threshold = (int(options.ptSelection.split('_')[1]), int(options.ptSelection.split('_')[2]))
kinematicSelection = 'lep_pt>{pt_min}'.format( pt_min=pt_threshold[0] ) if pt_threshold[1]<0 else 'lep_pt>{pt_min}&&lep_pt<={pt_max}'.format( pt_min=pt_threshold[0], pt_max=pt_threshold[1] )

selectionString = '(event%{nJobs}=={job}&&abs(lep_pdgId)=={flavour}&&{kinematic})'.format( nJobs=options.nJobs, job=options.job, flavour='11' if options.flavour=='ele' else '13', kinematic = kinematicSelection)

random.seed(100) # Otherwise file shuffling not deterministic!
def getInput( sub_directories, class_name):
    assert len(sub_directories)>0, "sub_directories can not be empty!"
    inputPath = os.path.join( skim_directory, options.version, "step1", str(options.year), options.flavour, class_name, options.ptSelectionStep1)
    sample = Sample.fromDirectory( 
        name = class_name, 
        directory = [os.path.join( inputPath, s ) for s in sub_directories], 
        treeName = 'tree', selectionString=selectionString)
    random.shuffle( sample.files )
    return sample

#settings
if options.sampleSelection == "DYvsQCD":
    samplePrompt    = getInput( DY[options.year], "Prompt")
    sampleNonPrompt = getInput( QCD[options.flavour][options.year], "NonPrompt")
    sampleFake      = getInput( QCD[options.flavour][options.year], "Fake")
elif options.sampleSelection == "TT":
    samplePrompt    = getInput( Top[options.year], "Prompt")
    sampleNonPrompt = getInput( Top[options.year], "NonPrompt")
    sampleFake      = getInput( Top[options.year], "Fake")
elif options.sampleSelection == "all":
    samplePrompt    = getInput( Top[options.year]+DY[options.year],  "Prompt")
    sampleNonPrompt = getInput( Top[options.year]+QCD[options.flavour][options.year], "NonPrompt")
    sampleFake      = getInput( Top[options.year]+QCD[options.flavour][options.year], "Fake")

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
    print('leptonClass loop start')
    logger.info( "Class %s", leptonClass['name'] )

    for sampleFile in leptonClass['sample'].files:    
        leptonClass['TChain'].Add(sampleFile)
    
    leptonClass['TChain'] = leptonClass['TChain'].CopyTree(selectionString) # macht aus TChain TTree und filtert mit selection String?
    leptonClass['Entries'] = leptonClass['TChain'].GetEntries()
    logger.info( "flavour %s class %s entries %i", options.flavour, leptonClass['name'], leptonClass['Entries'] )

if options.ratio == 'balanced':
    x = [[0,1,2], [nonPrompt['Entries']+fake['Entries'], nonPrompt['Entries'], fake['Entries']]]
else:
    x = [[0,1,2], [leptonClass['Entries'] for leptonClass in leptonClasses]]

y = sum(([t] * w for t, w in zip(*x)), [])

n_maxfileentries = 100000
n_current_entries  = 0
n_file           = 0

outputDir = os.path.join( skim_directory, options.version + ("_small" if options.small else ""), "step2", str(options.year), options.flavour, options.ptSelection, options.sampleSelection)

try:
    os.makedirs(outputDir)
except OSError as err:
    pass

#if not os.path.exists( outputDir ):
#    os.makedirs( outputDir )
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
logger.info('Successfully Finished')
