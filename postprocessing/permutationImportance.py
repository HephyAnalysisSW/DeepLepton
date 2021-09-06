# Standard imports
import ROOT
import os
import sys
from math import *
import numpy as np
# RootTools
from RootTools.core.standard import *
from helpers import electronVIDSelector

# DeepLepton
from DeepLepton.Tools.user import skim_directory
from DeepLepton.Tools.helpers import getCollection, deltaR, deltaR2

print('parsing')
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
    argParser.add_argument('--vers',                     action='store',         nargs='?',  type=str,  default='v2',         help="Version for output directory")
    argParser.add_argument('--versionName',                  action='store',                    type=str)
    argParser.add_argument('--ptSelection',                 action='store',         nargs='?',  type=str,  default='pt_5_-1',      help="pt selection of leptons")
    argParser.add_argument('--muFromTauArePrompt',    action='store_true',        help="Consider muons from tau leptons as prompt")        
    argParser.add_argument('--modelPath',                       action='store',       help="Path to Keras model")

    return argParser

options = get_parser().parse_args()

# Logging
import DeepLepton.Tools.logger as _logger
logger  = _logger.get_logger(options.logLevel, logFile = None)
import RootTools.core.logger as _logger_rt
logger_rt = _logger_rt.get_logger(options.logLevel, logFile = None )

maxN = 2 if options.small else None

outdir = "/scratch-cbe/users/maximilian.moser/DeepLepton/permutation"

#load keras model
#from keras.models import load_model
logger.info('loading keras model, this may take a minute (or two)')
import tensorflow as tf
modelPath = options.modelPath
if not os.path.exists(modelPath):
    logger.error('modelPath is invalid')
    raise RuntimeError('modelPath is invalid')
model = tf.keras.models.load_model( modelPath )
logger.info('loading Model complete')

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
output_directory = os.path.join( skim_directory, options.vers+('_small' if options.small else ''), 'step1', str(options.year) ) 


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
#read_variables += ["lep_looseId/O"]

cand_varnames_read  = map( lambda n:n.split('/')[0], cand_vars_read) 
cand_varnames_write = {pf_flavour: map( lambda n:n.split('/')[0], cand_vars_train[pf_flavour]) for pf_flavour in pf_flavours} 
SV_varnames         = map( lambda n:n.split('/')[0], SV_vars) 

if options.flavour == 'ele':
    lep_vars = ele_vars 
    if not sample.isData:
        lep_vars.extend(['genPartFlav/b'])
    read_variables.extend(['nElectron/I', 'Electron[%s]'%(",".join(lep_vars))])
elif options.flavour == 'muo':
    lep_vars = muo_vars 
    if not sample.isData:
        lep_vars.extend(['genPartFlav/b'])
    read_variables.extend(['nMuon/I', 'Muon[%s]'%(",".join(lep_vars))])

lep_varnames = map( lambda n:n.split('/')[0], lep_vars ) 
new_variables= map( lambda b: "lep_%s"%(b[:-1]+'F'), lep_vars )
new_variables+= ["lep_isPromptId_Training/I", "lep_isNonPromptId_Training/I", "lep_isNotPromptId_Training/I", "lep_isFakeId_Training/I"]
new_variables+= ["lep_StopsCompressed/I"]#, "lep_looseId/O", "lep_mediumId/O", "lep_tightId/O"]

############### out_variables
#out_variables = ["lep_isPromptId_Training/I", "lep_isNonPromptId_Training/I", "lep_isNotPromptId_Training/I", "lep_isFakeId_Training/I"]
#out_variables += ["lep_pt/F", "lep_eta/F", "lep_probPrompt/F", "lep_probNonPrompt/F", "lep_probFake/F", "lep_probNotPrompt/F"]
#out_variables += ["event/l", "lep_mvaTTH/F"]
#out_variables += ["lep_StopsCompressed/I", "lep_looseId/F", "lep_mediumId/F", "lep_tightId/F"]
#out_variables += ["lep_precut/F", "lep_pfRelIso03_all/F"]
new_variables += ["lep_probPrompt/F", "lep_probNonPrompt/F", "lep_probFake/F", "lep_probNotPrompt/F"]
new_variables += ["event/l", "lep_mvaTTH/F"]
if options.flavour == 'muo':
    new_variables += ["lep_StopsCompressed/I", "lep_looseId/F", "lep_mediumId/F", "lep_tightId/F"]
    new_variables += ["lep_precut/F", "lep_pfRelIso03_all/F"]


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


reader = sample.treeReader( \
    variables = map( lambda v: TreeVariable.fromString(v) if type(v)==type("") else v, read_variables),
    selectionString = "&&".join(skimConds)
    )

####
#outfilename =  os.path.join(output_directory, "predicted", options.flavour, options.ptSelection, sample_name, sample.name + '.root')
outfilename =  os.path.join("/scratch-cbe/users/maximilian.moser/DeepLepton", "predicted", options.versionName, options.flavour, options.ptSelection, sample_name, sample.name + '.root')
logger.debug("Writing to: %s", outfilename)

if not os.path.exists(os.path.dirname(outfilename)):
    try:
        os.makedirs(os.path.dirname(outfilename))
    except:
        pass


tmp_directory = ROOT.gDirectory
outfile = ROOT.TFile.Open(outfilename, 'recreate')
outfile.cd()
#new_maker = TreeMaker( sequence  = [ ],
#    variables = map( lambda v: TreeVariable.fromString(v) if type(v)==type("") else v, new_variables),
#    treeName = 'tree')
tmp_directory.cd()

#new_maker.start()

if options.flavour == 'muo':
    global_branches = [
            #'lep_pt', 'lep_eta',
            'lep_phi',
            'lep_mediumId',
            'lep_miniPFRelIso_all',
            'lep_sip3d', 'lep_dxy', 'lep_dz',
            'lep_charge',
            'lep_dxyErr', 'lep_dzErr', 'lep_ip3d',
            'lep_jetPtRelv2', 'lep_jetRelIso',
            'lep_miniPFRelIso_chg', 'lep_mvaLowPt', 'lep_nStations', 'lep_nTrackerLayers', 'lep_pfRelIso03_all', 'lep_pfRelIso03_chg', 'lep_pfRelIso04_all', 'lep_ptErr',
            'lep_segmentComp', 'lep_tkRelIso', 'lep_tunepRelPt',
            ]

elif options.flavour == 'ele':
    global_branches = ['lep_phi', 'lep_pdgId', 'lep_cutBased',
            'lep_miniPFRelIso_all', 'lep_pfRelIso03_all',
            'lep_sip3d', 'lep_lostHits',
            'lep_convVeto', 'lep_dxy',
            'lep_dz', 'lep_charge',
            'lep_deltaEtaSC', 'lep_vidNestedWPBitmap',
            'lep_dr03EcalRecHitSumEt', 'lep_dr03HcalDepth1TowerSumEt',
            'lep_dr03TkSumPt', 'lep_dxyErr',
            'lep_dzErr', 'lep_eCorr',
            'lep_eInvMinusPInv', 'lep_energyErr',
            'lep_hoe', 'lep_ip3d',
            'lep_jetPtRelv2', 'lep_jetRelIso',
            'lep_miniPFRelIso_chg', 'lep_mvaFall17V2noIso',
            'lep_pfRelIso03_chg', 'lep_r9',
            'lep_sieie',]

pfCand_neutral_branches  = ['pfCand_neutral_eta', 'pfCand_neutral_phi', 'pfCand_neutral_pt', 'pfCand_neutral_puppiWeight', 'pfCand_neutral_puppiWeightNoLep',
                            'pfCand_neutral_ptRel', 'pfCand_neutral_deltaR',]
pfCand_charged_branches  = ['pfCand_chargeid_d0', 'pfCand_charged_d0Err', 'pfCand_charged_dz', 'pfCand_charged_dzErr', 'pfCand_charged_eta', 'pfCand_charged_mass',
                            'pfCand_charged_phi', 'pfCand_charged_pt', 'pfCand_charged_puppiWeight', 'pfCand_charged_puppiWeightNoLep', 'pfCand_charged_trkChi2',
                            'pfCand_charged_vtxChi2', 'pfCand_charged_charge', 'pfCand_charged_lostInnerHits', 'pfCand_charged_pvAssocQuality',
                            'pfCand_charged_trkQuality', 'pfCand_charged_ptRel', 'pfCand_charged_deltaR',]
pfCand_photon_branches   = ['pfCand_photon_eta', 'pfCand_photon_phi', 'pfCand_photon_pt', 'pfCand_photon_puppiWeight', 'pfCand_photon_puppiWeightNoLep', 'pfCand_photon_ptRel', 'pfCand_photon_deltaR',]
pfCand_electron_branches = ['pfCand_electron_d0', 'pfCand_electron_d0Err', 'pfCand_electron_dz', 'pfCand_electron_dzErr', 'pfCand_electron_eta', 'pfCand_electron_mass',
                            'pfCand_electron_phi', 'pfCand_electron_pt', 'pfCand_electron_puppiWeight', 'pfCand_electron_puppiWeightNoLep', 'pfCand_electron_trkChi2',
                            'pfCand_electron_vtxChi2', 'pfCand_electron_charge', 'pfCand_electron_lostInnerHits', 'pfCand_electron_pvAssocQuality',
                            'pfCand_electron_trkQuality', 'pfCand_electron_ptRel', 'pfCand_electron_deltaR',]
pfCand_muon_branches     = ['pfCand_muon_d0', 'pfCand_muon_d0Err', 'pfCand_muon_dz', 'pfCand_muon_dzErr', 'pfCand_muon_eta', 'pfCand_muon_mass', 'pfCand_muon_phi',
                            'pfCand_muon_pt', 'pfCand_muon_puppiWeight', 'pfCand_muon_puppiWeightNoLep', 'pfCand_muon_trkChi2', 'pfCand_muon_vtxChi2', 'pfCand_muon_charge',
                            'pfCand_muon_lostInnerHits', 'pfCand_muon_pvAssocQuality', 'pfCand_muon_trkQuality', 'pfCand_muon_ptRel', 'pfCand_muon_deltaR']
SV_branches              = ['SV_dlen', 'SV_dlenSig', 'SV_dxy', 'SV_dxySig', 'SV_pAngle', 'SV_chi2', 'SV_eta', 'SV_mass',
                            'SV_ndof', 'SV_phi', 'SV_pt', 'SV_x', 'SV_y', 'SV_z', 'SV_ptRel', 'SV_deltaR',]

npfCand_neutral  = 10
npfCand_charged  = 80
npfCand_photon   = 50
npfCand_electron = 4
npfCand_muon     = 6
nSV              = 10



def SVpt(SV):
    return SV["pt"]

def ptRel(cand, lep):
    a = ROOT.TVector3(cos(lep['phi']),sin(lep['phi']),sinh(lep['eta']))
    o = ROOT.TLorentzVector(cand['pt']*cos(cand['phi']), cand['pt']*sin(cand['phi']),cand['pt']*sinh(cand['eta']),cand['pt']*cosh(cand['eta']),)
    return o.Perp(a)

def branches(pfC,pfC_flav_branches, npfC, n=-2, inlist=True): # n = -2 for pfCand, -1 for SV
    nb = []
    for cand in pfC:
        n = [cand[b.split("_")[-1]] for b in pfC_flav_branches]
        nb.append(n)
    nb.sort(key=lambda n: n[-2])
    zeros = [0. for i in range(len(pfC_flav_branches))]
    for i in range(npfC - len(pfC)):
        nb.append(zeros)
    nb = np.asarray([nb]).astype(np.float32, order='C')
    return nb

Xlist = []
Ylist = []


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
    #counter+=1

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
        #maker = new_maker # only use this one maker
        if type(lep['genPartFlav']) == int:
            genPartFlav = lep['genPartFlav']
        else:
            genPartFlav = ord(lep['genPartFlav'])
        if int(genPartFlav) == 15:
            continue        
        
        #for leptonClass in leptonClasses.values():
        #    if leptonClass['selector'](genPartFlav):
        #        maker = leptonClass['maker']
        #        break
        #if maker is None:
        #    raise RuntimeError("Unclassified lepton: genPartFlav: %i " % reader.event.lep_genPartFlav)
        #maker.event.event           = r.event
        #maker.event.luminosityBlock = r.luminosityBlock
        #maker.event.run             = r.run
        # write the lepton
        #for b in lep_varnames:
        #    if type(lep[b])==type(""):
        #        setattr(maker.event, "lep_"+b, float(ord(lep[b])))
        #    else:
        #        setattr(maker.event, "lep_"+b, float(lep[b]))

        lep_isPromptId_Training     = leptonClasses['Prompt']['selector'](genPartFlav)
        if lep_isPromptId_Training == 0:
            continue
            #pass
        
        #maker.event.lep_isNonPromptId_Training  = leptonClasses['NonPrompt']['selector'](genPartFlav)
        #maker.event.lep_isFakeId_Training       = leptonClasses['Fake']['selector'](genPartFlav)
        #maker.event.lep_isNotPromptId_Training  = (maker.event.lep_isNonPromptId_Training or maker.event.lep_isFakeId_Training)

        # write vector with PF candidates
        
        pfCands = {}
        for pf_flavour in pf_flavours:
            cands = filter( lambda c: deltaR2(c, lep) < dR_PF**2, sorted_cands[pf_flavour] )
            if pf_flavour == 'muon' and options.flavour=='muo': 
                cands = filter( lambda c: deltaR2(c, lep) > 0.000225*dR_PF**2, cands ) # 0.000225 = 0.015**2
            elif pf_flavour == 'electron' and options.flavour=='ele':
                cands = filter( lambda c: deltaR2(c, lep) > 0.000225*dR_PF**2, cands )
            for cand in cands:
                cand["ptRel"]  = ptRel  (cand, lep)
                cand["deltaR"] = deltaR2(cand, lep)
            pfCands[pf_flavour] = cands   
            #fill_vector_collection( maker.event, 'pfCand_%s'%pf_flavour, cand_varnames_write[pf_flavour] + ['ptRel', 'deltaR'], cands, nMax = 100 )
        # write nearby SVs
        SV = filter( lambda c: deltaR2(c, lep) < dR_PF**2, SVs )
        for sv in SV:
            sv["ptRel"]  = ptRel  (sv, lep)
            sv["deltaR"] = deltaR2(sv, lep)
            
        #fill_vector_collection( maker.event, 'SV', SV_varnames + ['ptRel', 'deltaR'], SV, nMax = 100 )
        # make sure that predicted are in the right Order
       
        if options.flavour == "muo":
            if abs(lep["eta"]) < 2.4 and abs(lep["dxy"]) < 0.02 and abs(lep["dz"]) < 0.1 and lep["looseId"]:
                pass
            else:
                continue
        else:
            if abs(lep["pdgId"]) == 11:
                absEta = abs(lep["eta"] + lep["deltaEtaSC"])
            else:
                absEta = abs(lep["eta"])
            ECALGap = ( absEta > 1.566 or absEta < 1.4442 )
            if abs(lep["dxy"]) < 0.02 and abs(lep["dz"]) < 0.1 and abs(lep["eta"]) < 2.5 \
                        and ECALGap and electronVIDSelector( lep, idVal= 1, removedCuts=['pfRelIso03_all'] ):
                pass
            else:
                continue

 
        # Globals:
        gb = []
        for b in global_branches:
            gb.append(lep[b.replace("lep_", "")])
        globalB = np.asarray([gb]).astype(np.float32, order='C')
            
        neutralB = branches(pfCands["neutral"],  pfCand_neutral_branches,  npfCand_neutral,  n=-2)
        chargedB = branches(pfCands["charged"],  pfCand_charged_branches,  npfCand_charged,  n=-2)
        photonB  = branches(pfCands["photon"],   pfCand_photon_branches,   npfCand_photon,   n=-2)
        electronB= branches(pfCands["electron"], pfCand_electron_branches, npfCand_electron, n=-2)
        muonB    = branches(pfCands["muon"],     pfCand_muon_branches,     npfCand_muon,     n=-2)
        svB      = branches(SV,                  SV_branches,              nSV,              n=-1)                

        #toPredict = np.stack([ gb, neutralB, chargedB, photonB, electronB, muonB, svB ])
        #toPredict = np.concatenate((gb, neutralB, chargedB, photonB, electronB, muonB, svB))
        
        #if options.flavour == "muo":
        #    if abs(lep["eta"]) < 2.4 and abs(lep["dxy"]) < 0.02 and abs(lep["dz"]) < 0.1 and lep["looseId"]:
        #        pass
        #    else:
        #        continue 






        # TO Predict is the relevant thing
        toPredict = [ globalB, neutralB, chargedB, photonB, electronB, muonB, svB ]
        labels = [ int(leptonClasses['Prompt']['selector'](genPartFlav)), int(leptonClasses['NonPrompt']['selector'](genPartFlav)), int(leptonClasses['Fake']['selector'](genPartFlav)) ]
        Xlist.append(toPredict)
        Ylist.append(labels)
        prediction = model.predict(toPredict)[0]
        counter+=1
        
        #print(prediction)
        #print(np.argmax(prediction))
        #print(maker.event.lep_isPromptId_Training, maker.event.lep_isNonPromptId_Training, maker.event.lep_isFakeId_Training)
        
        #if prediction[0] > 0.02:
        #    print('PROMPT!')
        #maker.event.lep_probPrompt = prediction[0]
        #maker.event.lep_probNonPrompt = prediction[1]
        #maker.event.lep_probFake = prediction[2]
        #maker.event.lep_probNotPrompt = prediction[1] + prediction[2]
        
        #maker.event.lep_pt = lep["pt"]
        #maker.event.lep_eta = lep["eta"]
        
        #maker.event.lep_mvaTTH   = lep["mvaTTH"]
        
        #if options.flavour == "muo":
        #    maker.event.lep_looseId  = lep["looseId"]
        #    maker.event.lep_mediumId = lep["mediumId"]
        #    maker.event.lep_tightId  = lep["tightId"]
        #    maker.event.lep_pfRelIso03_all = lep["pfRelIso03_all"]

        #    if lep["pt"] <= 25:
        #        if abs(lep["eta"]) < 2.4 and lep["pfRelIso03_all"] * lep["pt"] < 5.0 and abs(lep["dxy"]) < 0.02 and abs(lep["dz"]) < 0.1 and lep["looseId"]:
        #            maker.event.lep_StopsCompressed = 1
        #        else:
        #            maker.event.lep_StopsCompressed = 0
        #    elif lep["pt"] > 25:
        #        if abs(lep["eta"]) < 2.4 and lep["pfRelIso03_all"] < 0.2 and abs(lep["dxy"]) < 0.02 and abs(lep["dz"]) < 0.1 and lep["looseId"]:
        #            maker.event.lep_StopsCompressed = 1
        #        else:
        #            maker.event.lep_StopsCompressed = 0
        
        #    if abs(lep["eta"]) < 2.4 and abs(lep["dxy"]) < 0.02 and abs(lep["dz"]) < 0.1 and lep["looseId"]:
        #        maker.event.lep_precut = 1
        #    else:
        #        maker.event.lep_precut = 0
        #maker.fill()
        #maker.event.init()
        
                
        
    # stop early when small.
    if options.small:
        if counter>=500:
            break
    else:
        if counter >= 10000:
            break

#results = model.predict(Xlist)

print("start permutation")
from copy import deepcopy
import random
from sklearn.metrics import log_loss

Ys = [np.argmax(y) for y in Ylist]

def get_column(Xlist, i):
    return [x[0][0][i] for x in Xlist]
def set_column(Xlist, column, i):
    xlist = deepcopy(Xlist)
    for x, c in zip(xlist, column):
        x[0][0][i] = c
    return xlist


from copy import deepcopy
def shuffle(Xlist, i):
    Xlistcp = deepcopy(Xlist)
    column = get_column(Xlistcp, i)
    #print(column)
    random.shuffle(column)
    #print(column)
    newXlist = set_column(Xlistcp, column, i)
    return newXlist


def get_log_acc(Xlist, Ylist, Ys):
    loglist = []
    acclist = []
    reslist = []
    for X, Y, YY in zip(Xlist, Ylist, Ys):
        res = model.predict(X)[0].tolist()
        # print(res, Y)
        loss = 0
        for y, p in zip(Y, res):
            loss -= y * np.log(p)
        loglist.append(loss)
        reslist.append(res)
        if np.argmax(Y) == np.argmax(res):
            acclist.append(1)
        else:
            acclist.append(0)
    return np.mean(loglist), np.mean(acclist), 0#log_loss(Ys, reslist)


outfilename = os.path.join(outdir, "permutation_{}_{}_{}".format(options.year, options.flavour, str(options.job)+".txt"))
f = open(outfilename, "w")


print(len(Xlist), len(Ylist), len(Ys))
baseloss, baseacc, baseloss2 = get_log_acc(Xlist, Ylist, Ys)
print(baseloss, baseacc, baseloss2)
losslist = []
acclist = []
for j in range(len(global_branches)):
    print(j, " of ", len(global_branches))
    for iii in range(2):
        Xlistcp = deepcopy(Xlist)
        newXlist = shuffle(Xlistcp, j)
        #print(newXlist)
        l, a,  l2 = get_log_acc(newXlist, Ylist, Ys)
        losslist.append(l)
        acclist.append(a)
        print("variable {}: loss {}, lossdiff {}, acc {}, accdiff {}".format(global_branches[j], l, l-baseloss, a, a-baseacc))
        f.write("variable {}: loss {}, lossdiff {}, acc {}, accdiff {}\n".format(global_branches[j], l, l-baseloss, a, a-baseacc))

f.close()





