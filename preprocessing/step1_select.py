# Standard imports
import ROOT
import os
import sys
from math import *

# RootTools
from RootTools.core.standard import *

# DeepLepton
from DeepLepton.Tools.user import skim_directory
from DeepLepton.Tools.helpers import getCollection, deltaR, deltaR2

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
    argParser.add_argument('--version',                     action='store',         nargs='?',  type=str,  required = True,        help="Version for output directory")
    argParser.add_argument('--ptSelection',                 action='store',         nargs='?',  type=str,  default='pt_5_-1',      help="pt selection of leptons")
    argParser.add_argument('--muFromTauArePrompt',    action='store_true',        help="Consider muons from tau leptons as prompt")        

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
sample_name = sample.name # 

#file management
len_orig = len(sample.files)
sample = sample.split( n=options.nJobs, nSub=options.job)
logger.info( " Run over %i/%i files for job %i/%i."%(len(sample.files), len_orig, options.job, options.nJobs))
logger.debug( "Files to be run over:\n%s", "\n".join(sample.files) )
if options.small:
    sample.reduceFiles(to=1)
#output directory
output_directory = os.path.join( skim_directory, options.version+('_small' if options.small else ''), 'step1', str(options.year) ) 


if options.muFromTauArePrompt:
    absPdgIds = {'Prompt':[1,15], 'NonPrompt':[4,5], 'Fake':[0,3,22],  'NotPrompt':[0,3,4,5,22]}
else:
    absPdgIds = {'Prompt':[1],    'NonPrompt':[5, 4, 15], 'Fake':[0,3,22],  'NotPrompt':[0,3,4,5,15,22]}

leptonClasses  = {'Prompt'     : {'selector': lambda genPartFlav: abs(genPartFlav) in absPdgIds['Prompt']}, 
                  'NonPrompt'  : {'selector': lambda genPartFlav: abs(genPartFlav) in absPdgIds['NonPrompt']}, 
                  'Fake'       : {'selector': lambda genPartFlav: abs(genPartFlav) not in (absPdgIds['Prompt']+absPdgIds['NonPrompt'])},
                  }

leptonFlavour  =  {'name':'muo', 'pdgId': 13} if options.flavour == 'muo' else  {'name':'ele', 'pdgId': 11}

#pt selection
ptSelectionList = options.ptSelection.split('_')
pt_threshold    = (float(ptSelectionList[1]), float(ptSelectionList[2]))

pf_flavours  = ['charged', 'neutral', 'photon', 'electron', 'muon']

# read variables
from vars import cand_vars_read, cand_vars_train, SV_vars ,ele_vars, muo_vars

read_variables = [
    'nPFCands/I',
    #VectorTreeVariable.fromString("PFCands[%s]"%(",".join(cand_vars + ['ptRel/F', 'dR/F'])), nMax=nPFCandMax),
    VectorTreeVariable.fromString("PFCands[%s]"%(",".join(cand_vars_read)), nMax=nPFCandMax),
    'nSV/I',
    "SV[%s]"%(",".join(SV_vars)),
    ]
read_variables += ["event/l", "luminosityBlock/I", "run/I"]

cand_varnames_read  = map( lambda n:n.split('/')[0], cand_vars_read) 
cand_varnames_write = {pf_flavour: map( lambda n:n.split('/')[0], cand_vars_train[pf_flavour]) for pf_flavour in pf_flavours} 
SV_varnames         = map( lambda n:n.split('/')[0], SV_vars) 

if options.flavour == 'ele':
    lep_vars = ele_vars 
    if not sample.isData:
        lep_vars.extend(['genPartFlav/B'])
    read_variables.extend(['nElectron/I', 'Electron[%s]'%(",".join(lep_vars))])
elif options.flavour == 'muo':
    lep_vars = muo_vars 
    if not sample.isData:
        lep_vars.extend(['genPartFlav/B'])
    read_variables.extend(['nMuon/I', 'Muon[%s]'%(",".join(lep_vars))])

lep_varnames = map( lambda n:n.split('/')[0], lep_vars ) 
new_variables= map( lambda b: "lep_%s"%(b[:-1]+'F'), lep_vars )
new_variables+= ["lep_isPromptId_Training/I", "lep_isNonPromptId_Training/I", "lep_isNotPromptId_Training/I", "lep_isFakeId_Training/I"]

for pf_flavour in pf_flavours:
    # per PFCandidate flavor, add a counter and a vector with all pf candidate variables
    new_variables.append( VectorTreeVariable.fromString( 'pfCand_%s[%s]'%(pf_flavour, ",".join(cand_vars_train[pf_flavour] + ['ptRel/F', 'deltaR/F'])), nMax = 100) ) # here

new_variables.append( VectorTreeVariable.fromString( 'SV[%s]'%( ",".join(SV_vars + ['ptRel/F', 'deltaR/F'])), nMax = 100) )
new_variables += ["event/l", "luminosityBlock/I", "run/I"]  

def fill_vector_collection( event, collection_name, collection_varnames, objects, nMax = 100):
    setattr( event, "n"+collection_name, len(objects) )
    for i_obj, obj in enumerate(objects[:nMax]):
        for var in collection_varnames:
            if var in obj.keys():
                if type(obj[var]) == type("string"):
                    obj[var] = float(ord(obj[var]))
                elif type(obj[var]) == type(True):
                    obj[var] = float(obj[var])
                getattr(event, collection_name+"_"+var)[i_obj] = obj[var]

# Reader 
reader = sample.treeReader( \
    variables = map( lambda v: TreeVariable.fromString(v) if type(v)==type("") else v, read_variables),
    selectionString = "&&".join(skimConds)
    )

for leptonClass_name, leptonClass in leptonClasses.iteritems():

    outfilename =  os.path.join(output_directory, options.flavour, leptonClass_name, options.ptSelection, sample_name, sample.name + '.root')
    logger.debug("Writing to: %s", outfilename)

    if not os.path.exists(os.path.dirname(outfilename)):
        try:
            os.makedirs(os.path.dirname(outfilename))
        except:
            pass

    tmp_directory = ROOT.gDirectory
    outfile = ROOT.TFile.Open(outfilename, 'recreate')
    outfile.cd()
    maker = TreeMaker( sequence  = [ ],
        variables = map( lambda v: TreeVariable.fromString(v) if type(v)==type("") else v, new_variables),
        treeName = 'tree')
    tmp_directory.cd()

    leptonClass['outfile']    = outfile
    leptonClass['outfilename']= outfilename
    #leptonClass['clonedTree'] = reader.cloneTree( [], newTreename = 'tree', rootfile = leptonClass['outfile'] )
    leptonClass['maker']      = maker 
    leptonClass['maker'].start()

# put this function into helpers after it works.
def ptRel(cand, lep):
    a = ROOT.TVector3(cos(lep['phi']),sin(lep['phi']),sinh(lep['eta']))
    o = ROOT.TLorentzVector(cand['pt']*cos(cand['phi']), cand['pt']*sin(cand['phi']),cand['pt']*sinh(cand['eta']),cand['pt']*cosh(cand['eta']),)
    return o.Perp(a)

reader.start()
counter=0
while reader.run():
    r = reader.event
    if options.flavour == 'muo':
        leps = getCollection(r, 'Muon', lep_varnames, 'nMuon')
    elif options.flavour == 'ele':
        leps = getCollection(r, 'Electron', lep_varnames, 'nElectron')

    # write leptons to event
    leps = filter( lambda l: (l['pt']>=pt_threshold[0] or pt_threshold[0]<0) and (l['pt']<pt_threshold[1] or pt_threshold[1]<0), leps )

    # No leptons -> don't consider this event.
    if len(leps)==0: 
        continue
    counter+=1

    # get the candidates
    PFCands = getCollection(r, 'PFCands', cand_varnames_read, 'nPFCands', maxN = nPFCandMax)
    SVs     = getCollection(r, 'SV', SV_varnames, 'nSV')
    #print len(leps), len(PFCands), len(SVs)
    sorted_cands = {pf_flavour:[] for pf_flavour in pf_flavours}
    for PFCand in PFCands:
        pdgId = PFCand['pdgId']
        if abs(pdgId)==211:
            sorted_cands['charged'].append(PFCand)
        elif abs(pdgId)==130:
            sorted_cands['neutral'].append(PFCand)
        elif abs(pdgId)==22:
            sorted_cands['photon'].append(PFCand)
        elif abs(pdgId)==13:
            sorted_cands['muon'].append(PFCand)
        elif abs(pdgId)==11:
            sorted_cands['electron'].append(PFCand)

    for lep in leps:
        #now decide which maker to use
        maker = None
    
        genPartFlav = ord(lep['genPartFlav'])
        for leptonClass in leptonClasses.values():
            if leptonClass['selector'](genPartFlav):
                maker = leptonClass['maker']
                break
        if maker is None:
            raise RuntimeError("Unclassified lepton: genPartFlav: %i " % reader.event.lep_genPartFlav)
        maker.event.event           = r.event
        maker.event.luminosityBlock = r.luminosityBlock
        maker.event.run             = r.run
        # write the lepton
        for b in lep_varnames:
            if type(lep[b])==type(""):
                setattr(maker.event, "lep_"+b, float(ord(lep[b])))
            else:
                setattr(maker.event, "lep_"+b, float(lep[b]))

        maker.event.lep_isPromptId_Training     = leptonClasses['Prompt']['selector'](genPartFlav)
        maker.event.lep_isNonPromptId_Training  = leptonClasses['NonPrompt']['selector'](genPartFlav)
        maker.event.lep_isFakeId_Training       = leptonClasses['Fake']['selector'](genPartFlav)
        maker.event.lep_isNotPromptId_Training  = (maker.event.lep_isNonPromptId_Training or maker.event.lep_isFakeId_Training)

        # write vector with PF candidates
        for pf_flavour in pf_flavours:
            if pf_flavour == 'muon' and args.flavor=='muo': 
                cands = filter( lambda c: deltaR2(c, lep) > 0.000225 dR_PF**2, sorted_cands[pf_flavour] ) #cands )
            if pf_flavour == 'electron' and args.flavor=='ele':
                cands = filter( lambda c: deltaR2(c, lep) > 0.000225 dR_PF**2, sorted_cands[pf_flavour] ) #cands )
            #cands = filter( lambda c: deltaR2(c, lep) < dR_PF**2, sorted_cands[pf_flavour] )
            for cand in cands:
                cand["ptRel"]  = ptRel  (cand, lep)
                cand["deltaR"] = deltaR2(cand, lep)
            
            fill_vector_collection( maker.event, 'pfCand_%s'%pf_flavour, cand_varnames_write[pf_flavour] + ['ptRel', 'deltaR'], cands, nMax = 100 )
        # write nearby SVs
        SV = filter( lambda c: deltaR2(c, lep) < dR_PF**2, SVs )
        for sv in SV:
            sv["ptRel"]  = ptRel  (sv, lep)
            sv["deltaR"] = deltaR2(sv, lep)
            
        fill_vector_collection( maker.event, 'SV', SV_varnames + ['ptRel', 'deltaR'], SV, nMax = 100 )

        maker.fill()
        maker.event.init()
                
    # stop early when small.
    if options.small:
        if counter==200:
            break

logger.info("Writing trees.")
for leptonClass in leptonClasses.values():
    #leptonClass['maker'].tree.Write()
    leptonClass['outfile'].Write()
    leptonClass['outfile'].Close()
    logger.info( "Written %s", leptonClass['outfilename'])
