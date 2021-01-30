# Standard imports
import ROOT
import os
import sys
import importlib
import random
import numpy as np
from array import array

# RootTools
from RootTools.core.Sample import *

# DeepLepton 
from DeepLepton.Tools.user import skim_directory 

#parser
def get_parser():
    ''' Argument parser for sorter.
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser for cmgPostProcessing")

    argParser.add_argument('--logLevel',        action='store',  nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET', 'SYNC'], default='INFO', help="Log level for logging")
    argParser.add_argument('--version',         action='store',             type=str, required = True, help="Version for input directory")
    argParser.add_argument('--output_version',  action='store',             type=str, required = True, help="Version for output directory")
    argParser.add_argument('--year',            action='store',             type=int, choices=[2016,2017],                      required = True, help="Which year?")
    argParser.add_argument('--flavour',         action='store',             type=str, choices=['ele','muo'],                    required = True, help="Which Flavour?")
    argParser.add_argument('--ptSelection',     action='store',             type=str,  default = "pt_15_-1", help="Which pt selection?")
    argParser.add_argument('--sampleSelection', action='store',             type=str, choices=['DYvsQCD', 'TTJets', 'TTs', 'TTs_test','all'],   required = True, help="Which sample selection?")
    argParser.add_argument('--small',           action='store_true',        help="Run the file on a small sample (for test purpose), bool flag set to True if used")        
    argParser.add_argument('--nJobs',           action='store', nargs='?',  type=int, default=1, help="Maximum number of simultaneous jobs.")
    argParser.add_argument('--job',             action='store',             type=int, default=0, help="Run only job i")
    argParser.add_argument('--muFromTauArePrompt',    action='store_true',        help="Consider muons from tau leptons as prompt")        

    return argParser

options = get_parser().parse_args()

# Logging
import DeepLepton.Tools.logger as logger
logger  = logger.get_logger(options.logLevel, logFile = None)
import RootTools.core.logger as logger_rt
logger_rt = logger_rt.get_logger(options.logLevel, logFile = None )

#some helper functions
def printData(data):
    for row in data:
        print row

def getKey(item):
    return float(item[2])

def varList(pfCandId):

    if pfCandId=='SV':
        pfCandVarList = [
        'SV_pt',
        'SV_eta',
        'SV_phi',
        'SV_mass',
        #'SV_charge',
        #'SV_ntracks',
        'SV_chi2',
        'SV_ndof',
        'SV_dxy',
        'SV_dlen',
        'SV_dlenSig',
        'SV_dxySig',
        'SV_pAngle',
        'SV_x',
        'SV_y',
        'SV_z',
        ]

    else:
        #define related variables of PF candidates
        pfCandVarList = [
        'pfCand_'+pfCandId+'_pdgId',
        'pfCand_'+pfCandId+'_pt',
        'pfCand_'+pfCandId+'_eta',
        'pfCand_'+pfCandId+'_phi',
        'pfCand_'+pfCandId+'_mass',
        'pfCand_'+pfCandId+'_puppiWeight',
        'pfCand_'+pfCandId+'_deltaR',
        'pfCand_'+pfCandId+'_ptRel',
        'pfCand_'+pfCandId+'_d0',
        'pfCand_'+pfCandId+'_d0Err',
        'pfCand_'+pfCandId+'_dz',
        'pfCand_'+pfCandId+'_dzErr',
        'pfCand_'+pfCandId+'_puppiWeightNoLep',
        'pfCand_'+pfCandId+'_trkChi2',
        'pfCand_'+pfCandId+'_vtxChi2',
        'pfCand_'+pfCandId+'_charge',
        'pfCand_'+pfCandId+'_lostInnerHits',
        'pfCand_'+pfCandId+'_pdgId',
        'pfCand_'+pfCandId+'_pvAssocQuality',
        'pfCand_'+pfCandId+'_trkQuality',
        ]

    return pfCandVarList

#define PF candidates for loop
pfCandIdList = [
                'neutral',
                'charged',
                'photon',
                'electron',
                'muon',
                'SV',
               ]

#vetoNanSelection = "&&".join(["(!TMath::IsNaN(%s))"%var for var in varList('SV')])

#class list
classList = ['Prompt', 'NonPrompt', 'Fake', 'NotPrompt']
#Ele: Flavour of genParticle for MC matching to status==1 electrons or photons: 1 = prompt electron (including gamma*->mu mu), 15 = electron from prompt tau, 22 = prompt photon (likely conversion), 5 = electron from b, 4 = electron from c, 3 = electron from light or unknown, 0 = unmatched
#Mu:  Flavour of genParticle for MC matching to status==1 muons: 1 = prompt muon (including gamma*->mu mu), 15 = muon from prompt tau, 5 = muon from b, 4 = muon from c, 3 = muon from light or unknown, 0 = unmatched

if options.muFromTauArePrompt:
    absPdgIds = {'Prompt':[1,15], 'NonPrompt':[5, 4,], 'Fake':[0,3,22],  'NotPrompt':[0,3,4,5,22]}
else:
    absPdgIds = {'Prompt':[1], 'NonPrompt':[5, 4, 15], 'Fake':[0,3,22],  'NotPrompt':[0,3,4,5,15,22]}

#define paths
inputPath    = os.path.join( skim_directory, options.version + ("_small" if options.small else ""), "step2", str(options.year), options.flavour, options.ptSelection, options.sampleSelection)
#outputPath   = os.path.join( skim_directory, options.version+'_'+options.output_version + ("_small" if options.small else ""), "step3", str(options.year), options.flavour, options.ptSelection, options.sampleSelection)
outputPath   = os.path.join( skim_directory, options.version + ("_small" if options.small else ""), "step3", str(options.year), options.flavour, options.ptSelection, options.sampleSelection)

print(inputPath, outputPath)

try:
    os.makedirs(outputPath)
except OSError as err:
    pass

#get file list
sample = Sample.fromDirectory( "sample", inputPath, treeName = "tree" )
sample = sample.split( n=options.nJobs, nSub=options.job )
if len(sample.files)==0:
    logger.info('No files found. Exiting.')
    sys.exit(0)

inputFileList = sample.files
if options.small:
   inputFileList = sample.files[:1]

logger.info( "Processing %i files", len( inputFileList ) )
#Loop over input files
for inputFile in inputFileList:
    iFile     = ROOT.TFile.Open(os.path.join(inputPath,inputFile), 'read')
    logger.info( "Input file %s", iFile.GetName() )
    iFileTree = iFile.Get('tree')
    nEntries  = iFileTree.GetEntries()

    #clone tree
    oFile     = ROOT.TFile.Open(os.path.join(outputPath,os.path.basename(inputFile)), 'recreate')
    logger.info( "Output file %s", oFile.GetName() )
    oFileTree = iFileTree.CloneTree() # in the parenthesis was 0 before

    #add class branches
    for leptonClass in classList:
        name = 'lep_is'+leptonClass+'Id'+'_Training'
        varName = name+'/I'
        vars()[name] = array( 'i', [ 0 ] )
        oFileTree.Branch(name , vars()[name], varName )

    #Loop over PF candidate ID
    for pfCandId in pfCandIdList:
        pfCandVarList = varList(pfCandId)

        #add PF and SV branches
        for pfCandVar in pfCandVarList:
            name = pfCandVar+('_ptSorted' if pfCandId=='SV' else '_ptRelSorted')
            varName = name+('[nSV' if pfCandId=='SV' else '[npfCand_'+pfCandId)+']/F'
            vars()[name] = array('f', np.tile(0.0, 100)) #important: maximum length of pf cands per pf cand flavour per lepton
            oFileTree.Branch(name , vars()[name], varName )
            if pfCandVar in ['SV_maxD3dTracks', 'SV_secD3dTracks']:  # used to produce NaN-free data
                name = pfCandVar+'_ptSorted_patch'
                varName = name+'[nSV]/F'
                vars()[name] = array('f', np.tile(0.0, 100))
                oFileTree.Branch(name , vars()[name], varName )
            if pfCandVar in ['pfCand_charged_dzAssociatedPV', 'pfCand_charged_dz_pf']:  # used to produce Inf-free data
                name = pfCandVar+'_ptRelSorted_patch'
                varName = name+'[nSV]/F'
                vars()[name] = array('f', np.tile(0.0, 100))
                oFileTree.Branch(name , vars()[name], varName )
                       
    #iFileTree.Draw(">>eList", vetoNanSelection)
    #eList = ROOT.gDirectory.Get("eList")
    #nGoodEntries = eList.GetN()
    #if nGoodEntries!=nEntries:
    #    logger.warning( "Removing events with Nans: Reduce from %i to %i", nEntries, nGoodEntries )

    #loop over all entries
    #for i in xrange(200):
     
    for i in xrange(nEntries):
        iFileTree.GetEntry(i) # What does this do?
 
        for pfCandId in pfCandIdList:
            pfCandVarList = varList(pfCandId)
            npfCand = 'nSV' if pfCandId=='SV' else 'npfCand_'+pfCandId

            #check if number of leaves matches number of PF candidates    
            ptRel = oFileTree.GetLeaf('SV_pt' if pfCandId=='SV' else 'pfCand_'+pfCandId+'_ptRel')
            npf   = oFileTree.GetLeaf(npfCand).GetValue()
            
            if ptRel.GetLen() != npf:
                logger.warning( 'Wrong number of PF candidates!' )

            #collect ptRel  + indices (entry, leaf, ptRel)
            ptRelData = []
            for j in xrange(ptRel.GetLen()):
                ptRelData.append([i, j, ptRel.GetValue(j)])
           
            #reorder leaf indices by ptRel, entry indices remain the same
            ptRelData=sorted(ptRelData, key=getKey, reverse=True)


            for pfCandVar in pfCandVarList:
                name = pfCandVar+('_ptSorted' if pfCandId=='SV' else '_ptRelSorted')
                pfVar = oFileTree.GetLeaf(pfCandVar)
                k=0
                for instance in ptRelData:
                    
                    value = pfVar.GetValue(instance[1])

                    if pfCandVar in ['SV_maxD3dTracks', 'SV_secD3dTracks']:    #remove NaNs by substituting with -1
                        if ROOT.TMath.IsNaN(value): vars()[name+'_patch'][k] = -1
                        else:                       vars()[name+'_patch'][k] = value
                    if pfCandVar in ['pfCand_dzAssociatedPV', 'pfCand_dz_pf']:    #remove Infs by substituting with -1
                        if isinf(value): vars()[name+'_patch'][k] = -1
                        else:            vars()[name+'_patch'][k] = value
                          
                    vars()[name][k]=value
                    k +=1

            #for pfCandVar in pfCandVarList:
            #    name = pfCandVar+('_ptSorted' if pfCandId=='SV' else '_ptRelSorted')
            #    pfVar = oFileTree.GetLeaf(pfCandVar)

            #    #fill pTRel sorted vars()[name] in branches
            #    k=0
            #    for instance in ptRelData:
            #        value = pfVar.GetValue(instance[1])
            #        vars()[name][k]=value
            #        k +=1
            #    #print vars()[name]

            #for pfCandVar in ['SV_maxD3dTracks', 'SV_secD3dTracks']:
            #    name = pfCandVar+'_ptSorted_patch'
            #    pfVar = oFileTree.GetLeaf(pfCandVar)

            #    #fill pTRel sorted vars()[name] in branches
            #    k=0
            #    for instance in ptRelData:
            #        value = pfVar.GetValue(instance[1])
            #        if ROOT.TMath.IsNaN(value): #print "Found Nan", value, pfCandVar
            #            vars()[name][k]=-1
            #            k +=1
            #        else: 
            #            vars()[name][k]=value
            #            k +=1


        #fill training lepton classes 

        genPartFlav = oFileTree.GetLeaf('lep_genPartFlav').GetValue()
        for leptonClass in classList:
            vars()['lep_is'+leptonClass+'Id_Training'][0] = (genPartFlav in absPdgIds[leptonClass]) 

        #fill tree    
        iFileTree.CopyAddresses(oFileTree)
        oFileTree.Fill() 

    logger.info( '%i of %i Entries processed for %s', i+1, nEntries, inputFile)

    #save and close files
    iFile.Close()
    oFile.Write(os.path.join(outputPath,os.path.basename(inputFile)),oFile.kOverwrite)
    logger.info( "Written %s", os.path.join(outputPath,os.path.basename(inputFile)) )
    oFile.Close()
