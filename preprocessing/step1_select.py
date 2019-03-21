# Standard imports
import ROOT
import os
import sys
from fnmatch import fnmatch
import importlib

# RootTools
from RootTools.core.Sample import *

# DeepLepton
from DeepLepton.Tools.user import skim_directory

# parser
def get_parser():
    ''' Argument parser for post-processing module.
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser for cmgPostProcessing")

    argParser.add_argument('--logLevel',                    action='store',         nargs='?',              choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET', 'SYNC'],     default='INFO',                     help="Log level for logging")
    #argParser.add_argument('--overwrite',                   action='store_true',                                                                                        help="Overwrite existing output files, bool flag set to True  if used")
    argParser.add_argument('--year',                        action='store',                     type=int,   choices=[2016,2017],    required = True,                    help="Which year?")
    argParser.add_argument('--flavor',                      action='store',                     type=str,   choices=['muo', 'ele'], default='muo',                      help="muo or ele?")
    argParser.add_argument('--sample',                      action='store',         nargs='?',  type=str,                           default='WZTo3LNu',                 help="List of samples to be post-processed, given as CMG component name")
    argParser.add_argument('--nJobs',                       action='store',         nargs='?',  type=int,                           default=1,                          help="Maximum number of simultaneous jobs.")
    argParser.add_argument('--job',                         action='store',                     type=int,                           default=0,                          help="Run only job i")
    argParser.add_argument('--small',                       action='store_true',                                                                                        help="Run the file on a small sample (for test purpose), bool flag set to True if used")
    argParser.add_argument('--forceProxy',                  action='store_true',                                                                                        help="Don't check certificate")
    argParser.add_argument('--version',                     action='store',         nargs='?',  type=str,  required = True,         help="Version for output directory")
    argParser.add_argument('--ptSelection',                 action='store',         nargs='?',  type=str,  default='pt_5_-1',      help="List of samples to be post-processed, given as CMG component name")

    return argParser

options = get_parser().parse_args()

# Logging
import DeepLepton.Tools.logger as logger
logger  = logger.get_logger(options.logLevel, logFile = None)
import RootTools.core.logger as logger_rt
logger_rt = logger_rt.get_logger(options.logLevel, logFile = None )

maxN = 2 if options.small else None

if options.year == 2016:
    module_ = 'CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2'
    MCgeneration = "Summer16"
    from DeepLepton.samples.heppy_dpm_samples import lepton_2016_heppy_mapper as lepton_heppy_mapper
elif options.year == 2017:
    module_ = 'CMGTools.RootTools.samples.samples_13TeV_RunIIFall17MiniAOD' 
    MCgeneration = "Fall17"
    from DeepLepton.samples.heppy_dpm_samples import lepton_2017_heppy_mapper as lepton_heppy_mapper
else:
    raise NotImplementedError

try:
    heppy_sample = getattr(importlib.import_module( module_ ), options.sample)
except:
    raise ValueError( "Could not load sample '%s' from %s "%( options.sample, module_ ) )

sample = lepton_heppy_mapper.from_heppy_samplename(heppy_sample.name, maxN = maxN)
    
if sample is None or len(sample.files)==0:
    logger.info( "Sample %r is empty. Exiting" % sample )
    sys.exit(-1)
else:
    logger.info( "Sample %s has %i files", sample.name, len(sample.files))

# lumi scale factor
targetLumi      = 1000 #pb-1 Which lumi to normalize to
xSection        = sample.heppy.xSection
normalization   = float(sample.normalization)
lumiScaleFactor = xSection*targetLumi/normalization

#file management
len_orig = len(sample.files)
sample = sample.split( n=options.nJobs, nSub=options.job)
logger.info( " Run over %i/%i files for job %i/%i."%(len(sample.files), len_orig, options.job, options.nJobs))
logger.debug( "Files to be run over:\n%s", "\n".join(sample.files) )

#output directory

output_directory = os.path.join( skim_directory, options.version+('_small' if options.small else ''), 'step1', str(options.year) ) 

leptonClasses  = [{'name':'Prompt', 'var': 'lep_isPromptId'}, {'name':'NonPrompt', 'var': 'lep_isNonPromptId'}, {'name':'Fake', 'var': 'lep_isFakeId'}]
leptonFlavor   =  {'name':'muo', 'pdgId': 13} if options.flavor == 'muo' else  {'name':'ele', 'pdgId': 11}
               

#pt selection
ptSelectionList = options.ptSelection.split('_')
pt_threshold = (int(ptSelectionList[1]), int(ptSelectionList[2]))

#make FileList
pattern  = 'tree.root'

#helper TChain for CloneTree
ch = ROOT.TChain('tree')
ch.Add(sample.files[0])
#inputFileList = TestFileList

postfix = '' if options.nJobs==1 else "_%i" % options.job

for leptonClass in leptonClasses:
    sample_name = sample.name if options.nJobs==1 else '_'.join(sample.name.split('_')[:-1])
    output_filename = os.path.join( output_directory, 
                    leptonFlavor['name'], 
                    leptonClass['name'], 
                    'pt_%i_%i' % pt_threshold,
                    sample_name,
                    'lepton%s.root' % postfix )
    dirname = os.path.dirname( output_filename )
    try:
        os.makedirs(dirname)
    except OSError as err:
        pass

    outputFile     = ROOT.TFile(output_filename, 'recreate')
    outputFileTree = ch.CloneTree(0,"")

    #add branches for lumi scale factor
    name = 'lumi_scaleFactor1fb'
    varName = name+'/F'
    vars()[name] = array( 'f', [ 0 ] )
    vars()[name][0] = lumiScaleFactor
    outputFileTree.Branch(name , vars()[name], varName )

    name = 'xSection_heppy'
    varName = name+'/F'
    vars()[name] = array( 'f', [ 0 ] )
    vars()[name][0] = xSection
    outputFileTree.Branch(name , vars()[name], varName )

    name = 'normalization_nEvents'
    varName = name+'/F'
    vars()[name] = array( 'f', [ 0 ] )
    vars()[name][0] = normalization
    outputFileTree.Branch(name , vars()[name], varName )

    for inputFile in sample.files:
        readFile     = ROOT.TFile.Open(inputFile, 'read')
        readFileTree = readFile.Get('tree')
        readFileTree.CopyAddresses(outputFileTree)

        pdgId     = readFileTree.GetLeaf("lep_pdgId")
        isClassId = readFileTree.GetLeaf(leptonClass["var"])
        pt        = readFileTree.GetLeaf("lep_pt")

        for i in xrange(readFileTree.GetEntries()):
            pdgId.GetBranch().GetEntry(i)
            isClassId.GetBranch().GetEntry(i)
            pt.GetBranch().GetEntry(i)

            lep_pdgId     = pdgId.GetValue()
            lep_isClassId = isClassId.GetValue()
            lep_pt        = pt.GetValue()

            #print lep_pdgId, lep_isClassId 
            if abs(lep_pdgId)==leptonFlavor["pdgId"] and lep_isClassId==1 and lep_pt>pt_threshold[0] and ( lep_pt<=pt_threshold[1] or pt_threshold[1]<0):
                inputEntry = readFileTree.GetEntry(i)
                readFileTree.CopyAddresses(outputFileTree)
                outputEntry = outputFileTree.Fill()
                #if inputEntry!=outputEntry:
                #    logger.error("error while copying entry")
                #    break
        readFile.Close()

    logger.info("%i entries copied to %s" %(outputFileTree.GetEntries(), output_filename))
    outputFile.Write(output_filename, outputFile.kOverwrite)
    outputFile.Close()
