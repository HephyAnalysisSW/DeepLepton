# Standard imports
import ROOT
import os
import sys

# RootTools
from RootTools.core.standard import *

# DeepLepton
from DeepLepton.Tools.user import skim_directory
from DeepLepton.Tools.helpers import getCollection

# parser
def get_parser():
    ''' Argument parser for post-processing module.
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser for cmgPostProcessing")

    argParser.add_argument('--logLevel',                    action='store',         nargs='?',              choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET', 'SYNC'],     default='INFO',                     help="Log level for logging")
    #argParser.add_argument('--overwrite',                   action='store_true',                                                                                        help="Overwrite existing output files, bool flag set to True  if used")
    argParser.add_argument('--year',                        action='store',                     type=int,   choices=[2016,2017],    required = True,                    help="Which year?")
    argParser.add_argument('--flavour',                      action='store',                     type=str,   choices=['muo', 'ele'], default='muo',                      help="muo or ele?")
    argParser.add_argument('--sample',                      action='store',         nargs='?',  type=str,                           default='WZTo3LNu',                 help="Sample to be post-processed")
    argParser.add_argument('--nJobs',                       action='store',         nargs='?',  type=int,                           default=1,                          help="Maximum number of simultaneous jobs.")
    argParser.add_argument('--job',                         action='store',                     type=int,                           default=0,                          help="Run only job i")
    argParser.add_argument('--small',                       action='store_true',                                                                                        help="Run the file on a small sample (for test purpose), bool flag set to True if used")
    argParser.add_argument('--version',                     action='store',         nargs='?',  type=str,  required = True,         help="Version for output directory")
    argParser.add_argument('--ptSelection',                 action='store',         nargs='?',  type=str,  default='pt_5_-1',      help="pt selection of leptons")

    return argParser

options = get_parser().parse_args()

# Logging
import DeepLepton.Tools.logger as _logger
logger  = _logger.get_logger(options.logLevel, logFile = None)
import RootTools.core.logger as _logger_rt
logger_rt = _logger_rt.get_logger(options.logLevel, logFile = None )

maxN = 2 if options.small else None

# Load samples
if options.year == 2016:
    from DeepLepton.Samples.nanoAOD_PFCands_Summer16 import *
else:
    raise NotImplementedError

# skim conditions. Take all for now.
skimConds = ["(1)"]
# dR thresholds to store cands
dR_PF = 0.5
dR_SV = 0.5
# Max number of PF cands we read
nPFCandMax = 5000

# Load all samples to be post processed
sample = eval( options.sample )
   
#file management
len_orig = len(sample.files)
sample = sample.split( n=options.nJobs, nSub=options.job)
logger.info( " Run over %i/%i files for job %i/%i."%(len(sample.files), len_orig, options.job, options.nJobs))
logger.debug( "Files to be run over:\n%s", "\n".join(sample.files) )

#output directory
output_directory = os.path.join( skim_directory, options.version+('_small' if options.small else ''), 'step1', str(options.year) ) 

leptonClasses  = [{'name':'Prompt',    'selector': lambda l: abs( l['mcMatchId'] ) in [6,23,24,25,37]}, 
                  {'name':'NonPrompt', 'selector': lambda l: not (abs(l['mcMatchId']) in [6,23,24,25,37]) and (abs(l['mcMatchAny']) in [4,5])}, 
                  {'name':'Fake',      'selector': lambda l: not (abs(l['mcMatchId']) in [6,23,24,25,37]) and not (abs(l['mcMatchAny']) in [4,5])}
                 ]
leptonFlavour   =  {'name':'muo', 'pdgId': 13} if options.flavour == 'muo' else  {'name':'ele', 'pdgId': 11}

#pt selection
ptSelectionList = options.ptSelection.split('_')
pt_threshold    = (float(ptSelectionList[1]), float(ptSelectionList[2]))

# read variables
cand_vars = ["d0/F", "d0Err/F", "dz/F", "dzErr/F", "eta/F", "mass/F", "phi/F", "pt/F", "puppiWeight/F", "puppiWeightNoLep/F", "trkChi2/F", "vtxChi2/F", "charge/I", "lostInnerHits/I", "pdgId/I", "pvAssocQuality/I", "trkQuality/I"]
SV_vars   = ['dlen/F', 'dlenSig/F', 'dxy/F', 'dxySig/F', 'pAngle/F', 'chi2/F', 'eta/F', 'mass/F', 'ndof/F', 'phi/F', 'pt/F', 'x/F', 'y/F', 'z/F']
read_variables = [
    'nPFCands/I',
    VectorTreeVariable.fromString("PFCands[%s]"%(",".join(cand_vars)), nMax=nPFCandMax),
    'nSV/I',
    "SV[%s]"%(",".join(SV_vars)),
    ]
cand_varnames = map( lambda n:n.split('/')[0], cand_vars ) 
SV_varnames   = map( lambda n:n.split('/')[0], SV_vars ) 

if options.flavour == 'ele':
    lep_vars = ['pt/F', 'eta/F', 'phi/F', 'pdgId/I', 'cutBased/I', 'miniPFRelIso_all/F', 'pfRelIso03_all/F', 'sip3d/F', 'lostHits/b', 'convVeto/O', 'dxy/F', 'dz/F', 'charge/I', 'deltaEtaSC/F', 'vidNestedWPBitmap/I']
    if not sample.isData:
        lep_vars.extend(['genPartFlav/B', 'genPartIdx/I'])
    read_variables.extend(['nElectron/I', 'Electron[%s]'%(",".join(lep_vars))])
elif options.flavour == 'muo':
    lep_vars = ["pt/F", "eta/F", "phi/F", "pdgId/I", "mediumId/O", "miniPFRelIso_all/F", "pfRelIso03_all/F", "sip3d/F", "dxy/F", "dz/F", "charge/I"]
    if not sample.isData:
        lep_vars.extend(['genPartFlav/B', 'genPartIdx/I'])
    read_variables.extend(['nMuon/I', 'Muon[%s]'%(",".join(lep_vars))])

lep_varnames = map( lambda n:n.split('/')[0], lep_vars ) 
new_variables  = []

def filler( event ):
    r = reader.event
    if options.flavour == 'muo':
        leps = getCollection(r, 'Muon', lep_varnames, 'nMuon')
    elif options.flavour == 'ele':
        leps = getCollection(r, 'Electron', lep_varnames, 'nElectron')

    leps = filter( lambda l: (l['pt']>=pt_threshold[0] or pt_threshold[0]<0) and (l['pt']<pt_threshold[1] or pt_threshold[1]<0), leps )

    # No leptons -> stop.
    if len(leps)==0: return

    PFCands = getCollection(r, 'PFCands', cand_varnames, 'nPFCands', maxN = nPFCandMax)
    SV      = getCollection(r, 'SV', SV_varnames, 'nSV')

    #print len(leps), len(PFCands), len(SV)
    neutral, charged, photon, electron, muon = [[]]*5

    for lep in leps:
        for PFCand in PFCands:
            pdgId = PFCand['pdgId']
            if abs(pdgId)==211:
                charged.append(PFCand)
            elif abs(pdgId)==100:
                neutral.append(PFCand)
            elif abs(pdgId)==21:
                photon.append(PFCand)
            elif abs(pdgId)==13:
                muon.append(PFCand)
            elif abs(pdgId)==11:
                electron.append(PFCand)

#    for lep in lep:


# Create a maker. Maker class will be compiled. This instance will be used as a parent in the loop
treeMaker_parent = TreeMaker(
    sequence  = [ filler ],
    variables = map( lambda v: TreeVariable.fromString(v) if type(v)==type("") else v, new_variables),
    treeName = 'tree',
    )

# Reader.
reader = sample.treeReader( \
    variables = map( lambda v: TreeVariable.fromString(v) if type(v)==type("") else v, read_variables),
    selectionString = "&&".join(skimConds)
    )

# Split input in ranges
outfilename =  os.path.join(output_directory, options.sample, sample.name + '.root')

tmp_directory = ROOT.gDirectory
outfile = ROOT.TFile.Open(outfilename, 'recreate')
tmp_directory.cd()

if not os.path.exists(os.path.dirname(outfilename)):
    try:
        os.makedirs(os.path.dirname(outfilename))
    except:
        pass

clonedTree = reader.cloneTree( [], newTreename = 'tree', rootfile = outfile )

_logger.   add_fileHandler( outfilename.replace('.root', '.log'), options.logLevel )
_logger_rt.add_fileHandler( outfilename.replace('.root', '_rt.log'), options.logLevel )

tree = ROOT.TTree('tree','tree')

maker = treeMaker_parent.cloneWithoutCompile( externalTree = clonedTree )

maker.start()
reader.start()
while reader.run():
    maker.run()

logger.info("Writing tree")
maker.tree.Write()
outputfile.Close()
logger.info( "Written %s", outfilename)

#for leptonClass in leptonClasses:
#    sample_name = sample.name if options.nJobs==1 else '_'.join(sample.name.split('_')[:-1])
#    output_filename = os.path.join( output_directory, 
#                    leptonFlavour['name'], 
#                    leptonClass['name'], 
#                    'pt_%i_%i' % pt_threshold,
#                    sample_name,
#                    'lepton%s.root' % postfix )
#    dirname = os.path.dirname( output_filename )
#    try:
#        os.makedirs(dirname)
#    except OSError as err:
#        pass
#
#    outputFile     = ROOT.TFile(output_filename, 'recreate')
#    outputFileTree = ch.CloneTree(0,"")
#
#    for inputFile in sample.files:
#        readFile     = ROOT.TFile.Open(inputFile, 'read')
#        readFileTree = readFile.Get('tree')
#        readFileTree.CopyAddresses(outputFileTree)
#
#        pdgId     = readFileTree.GetLeaf("lep_pdgId")
#        isClassId = readFileTree.GetLeaf(leptonClass["var"])
#        pt        = readFileTree.GetLeaf("lep_pt")
#
#        for i in xrange(readFileTree.GetEntries()):
#            pdgId.GetBranch().GetEntry(i)
#            isClassId.GetBranch().GetEntry(i)
#            pt.GetBranch().GetEntry(i)
#
#            lep_pdgId     = pdgId.GetValue()
#            lep_isClassId = isClassId.GetValue()
#            lep_pt        = pt.GetValue()
#
#            #print lep_pdgId, lep_isClassId 
#            if abs(lep_pdgId)==leptonFlavour["pdgId"] and lep_isClassId==1 and lep_pt>pt_threshold[0] and ( lep_pt<=pt_threshold[1] or pt_threshold[1]<0):
#                inputEntry = readFileTree.GetEntry(i)
#                readFileTree.CopyAddresses(outputFileTree)
#                outputEntry = outputFileTree.Fill()
#                #if inputEntry!=outputEntry:
#                #    logger.error("error while copying entry")
#                #    break
#        readFile.Close()
#
#    logger.info("%i entries copied to %s" %(outputFileTree.GetEntries(), output_filename))
#    outputFile.Write(output_filename, outputFile.kOverwrite)
#    outputFile.Close()
