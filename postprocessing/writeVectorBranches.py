# Standard imports
import ROOT
import os
import sys
import importlib
import numpy as np
from array import array

#parser
def get_parser():
    ''' Argument parser for sorter.
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser for cmgPostProcessing")

    argParser.add_argument('--iFile',    action='store',     type=str,   required = True,    help="Which input file?")
    argParser.add_argument('--oFile',    action='store',     type=str,   required = True,    help="Which output file?")
    argParser.add_argument('--logLevel', action='store',     nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET', 'SYNC'], default='INFO', help="Log level for logging")

    return argParser
options = get_parser().parse_args()

# Logging
import DeepLepton.Tools.logger as logger
logger  = logger.get_logger(options.logLevel, logFile = None)
import RootTools.core.logger as logger_rt
logger_rt = logger_rt.get_logger(options.logLevel, logFile = None )

##################################################################
### read input file and write vector branch to new output file ###
##################################################################

#define paths
iFilePath = options.iFile
iTreeName = 'tree'
oFilePath = options.oFile
oTreeName = iTreeName

#read input file
iFile     = ROOT.TFile.Open(iFilePath, 'read')
logger.info( "Input file %s", iFile.GetName() )
iFileTree = iFile.Get(iTreeName)
nEntries  = iFileTree.GetEntries()

#clone tree
oFile     = ROOT.TFile.Open(oFilePath, 'recreate')
logger.info( "Output file %s", oFile.GetName() )
oFileTree = ROOT.TTree(oTreeName,'friendTree')

#add branch with multiplicity
branchName   = 'mult'
varName      = '{name}/I'.format(name = branchName)
mult         = array( 'i', [0] )
oFileTree.Branch(branchName , mult, varName )

#add new vector branch with variable length
branchName           = 'newVectorBranch'
varName              = '{name}[mult]/F'.format(name = branchName)
max_length           = 100
branchValues         = array( 'f', np.tile(0.0, max_length) )
oFileTree.Branch(branchName , branchValues, varName )

branchWithLengthInfo = 'npfCand_neutral'
branchWithValues     = 'pfCand_neutral_pt'

#loop over all entries
for i in xrange(nEntries):
    #Get Entries
    iFileTree.GetEntry(i)
    #Get Leaves per Entry
    mult[0] = int(iFileTree.GetLeaf(branchWithLengthInfo).GetValue())
    #Set Values in new branch
    for j in xrange(mult[0]):
        branchValues[j] = iFileTree.GetLeaf(branchWithValues).GetValue(j)
    #Fill tree
    oFileTree.Fill()

#save and close files
#oFileTree.Print()
#oFileTree.Write()    
logger.info( '%i of %i Entries processed for %s', i+1, nEntries, iFilePath)

logger.info( "Written %s", oFilePath)
oFile.Write()
oFile.Close()
iFile.Close()
