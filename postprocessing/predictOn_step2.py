# Standard imports
import ROOT
import os
import sys
from math import *
import numpy as np
# RootTools
from RootTools.core.standard import *
from RootTools.core.helpers import shortTypeDict
from copy import deepcopy

# DeepLepton
from DeepLepton.Tools.user import skim_directory
from DeepLepton.Tools.helpers import getCollection, deltaR, deltaR2
from helpers import electronVIDSelector

print('parsing')
# parser
def get_parser():
    ''' Argument parser for post-processing module.
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser for cmgPostProcessing")

    argParser.add_argument('--logLevel',                    action='store',         nargs='?',              choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET', 'SYNC'],     default='INFO',                     help="Log level for logging")
    #argParser.add_argument('--overwrite',                   action='store_true',                                                                                        help="Overwrite existing output files, bool flag set to True  if used")
    argParser.add_argument('--year',                        action='store',                     type=int,   choices=[2016,2017, 2018],    required = True,                    help="Which year?")
    argParser.add_argument('--flavour',                      action='store',                     type=str,   choices=['muo', 'ele'], default='muo',                      help="muo or ele?")
    argParser.add_argument('--sample',                      action='store',         nargs='?',  type=str,                           default='WZTo3LNu',                 help="Sample to be post-processed")
    argParser.add_argument('--nJobs',                       action='store',         nargs='?',  type=int,                           default=1,                          help="Maximum number of simultaneous jobs.")
    argParser.add_argument('--job',                         action='store',                     type=int,                           default=0,                          help="Run only job i")
    argParser.add_argument('--small',                       action='store_true',                                                                                        help="Run the file on a small sample (for test purpose), bool flag set to True if used")
    # argParser.add_argument('--vers',                     action='store',         nargs='?',  type=str,  default='v2',         help="Version for output directory")
    argParser.add_argument('--versionName',                  action='store',                    type=str)
    argParser.add_argument('--ptSelection',                 action='store',         nargs='?',  type=str,  default='pt_5_-1',      help="pt selection of leptons")
    argParser.add_argument('--muFromTauArePrompt',    action='store_true',        help="Consider muons from tau leptons as prompt")        
    argParser.add_argument('--modelPath',                       action='store',       help="Path to Keras model")

    argParser.add_argument('--displaced',           action='store_true',    default=False,                                                          help='Look for displaced leptons from SUSY')

    return argParser

options = get_parser().parse_args()

# Logging
import DeepLepton.Tools.logger as _logger
logger  = _logger.get_logger(options.logLevel, logFile = None)
import RootTools.core.logger as _logger_rt
logger_rt = _logger_rt.get_logger(options.logLevel, logFile = None )


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

# special case, there exists only the sample in roberts directory ....
if options.displaced:
    from RootTools.core.Sample import Sample
     # This line for the old susy data ca. 80'000 muons
     # Compressed SUSY Scenario, this is the old data
    CompSUSY =  Sample.fromDirectory('CompSUSY',
                 '/eos/vbc/user/robert.schoefbeck/DeepLepton/nanoAODUL17_PFCands/signal_stops_compressed',
                 'root://eos.grid.vbc.ac.at') 
    stop250dm10 = Sample.fromDirectory('Stop250-dm10-006',
                  # '/eos/vbc/experiments/cms/store/user/liko/CompStop/SUS-RunIIAutumn18FSPremix-Stop250-dm10-006-nanoAOD/210819_215726/0000',
                  '/eos/vbc/user/benjamin.wilhelmy/DeepLepton/Stop250-dm10-006',
                  'root://eos.grid.vbc.ac.at') 

    stop250dm20 = Sample.fromDirectory('Stop250-dm20-006',
                  # '/eos/vbc/experiments/cms/store/user/liko/CompStop/SUS-RunIIAutumn18FSPremix-Stop250-dm20-006-nanoAOD/210819_215740/0000',
                  '/eos/vbc/user/benjamin.wilhelmy/DeepLepton/Stop250-dm20-006',
                  'root://eos.grid.vbc.ac.at') 

    stop600dm10 = Sample.fromDirectory('Stop600-dm10-006',
                  # '/eos/vbc/experiments/cms/store/user/liko/CompStop/SUS-RunIIAutumn18FSPremix-Stop600-dm10-006-nanoAOD/210819_215757/0000',
                  '/eos/vbc/user/benjamin.wilhelmy/DeepLepton/Stop600-dm10-006',
                  'root://eos.grid.vbc.ac.at') 

    stop600dm20 = Sample.fromDirectory('Stop600-dm20-006',
                  # '/eos/vbc/experiments/cms/store/user/liko/CompStop/SUS-RunIIAutumn18FSPremix-Stop600-dm20-006-nanoAOD/210819_215811/0000',
                  '/eos/vbc/user/benjamin.wilhelmy/DeepLepton/Stop600-dm20-006',
                  'root://eos.grid.vbc.ac.at') 

    step2_v9 = Sample.fromDirectory('step2_v9',
                                    '/scratch-cbe/users/benjamin.wilhelmy/DeepLepton/v9/step2/2018/muo/unbalanced/pt_3.5_-1/STop1vsTTbar',
                                    treeName = "tree")

    STop2vsTTbar = Sample.fromDirectory('STop2vsTTbar',
                                    '/scratch-cbe/users/benjamin.wilhelmy/DeepLepton/v9/step2/2018/muo/unbalanced/pt_3.5_-1/STop2vsTTbar',
                                    treeName = "tree")
    STop3vsTTbar = Sample.fromDirectory('STop3vsTTbar',
                                    '/scratch-cbe/users/benjamin.wilhelmy/DeepLepton/v9/step2/2018/muo/unbalanced/pt_3.5_-1/STop3vsTTbar',
                                    treeName = "tree")
                                    
    STop4vsTTbar = Sample.fromDirectory('STop4vsTTbar',
                                    '/scratch-cbe/users/benjamin.wilhelmy/DeepLepton/v9/step2/2018/muo/unbalanced/pt_3.5_-1/STop4vsTTbar',
                                    treeName = "tree")


else:    
    raise NotImplementedError

# skim conditions. Take all for now.
skimConds = ["(1)"]
# dR thresholds to store cands
dR_PF = 0.5
dR_SV = 0.5
# Max number of PF cands we read
nPFCandMax = 500

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

# find leaf structure
structure = {'': []}

# loop over the sample with the most general list of leaves which should
# be the last element of leptonClasses
for l in sample.chain.GetListOfLeaves():
    # this is an element of a vector branch:
    if l.GetLeafCount():
        counter_var = l.GetLeafCount().GetName()
        vector_name = counter_var[1:]
        vector_branch_declaration = (
            l.GetName()[len(vector_name)+1:], shortTypeDict[l.GetTypeName()])

        if not structure.has_key(vector_name):
            structure[vector_name] = [vector_branch_declaration]
        else:
            structure[vector_name].append(vector_branch_declaration)
    else:
        structure[''].append((l.GetName(), shortTypeDict[l.GetTypeName()]))

# define variables for reading and writing
# they should be the same no?
read_variables = []
write_variables = []
for key, value in structure.iteritems():
    if key == '':
        read_variables.extend(map(lambda v: '/'.join(v), value))
        write_variables.extend(map(lambda v: '/'.join(v), value))
    else:
        read_variables.append(
            key+'[%s]' % (','.join(map(lambda v: '/'.join(v), value))))
        write_variables.append(
            key+'[%s]' % (','.join(map(lambda v: '/'.join(v), value))))
        read_variables.append('n'+key+'/I')

variables = []
for v in read_variables:
    if v.startswith("SV") or v.startswith("pfCand"):
        variables.append(VectorTreeVariable.fromString(v, nMax=nPFCandMax))
    else:
        variables.append(TreeVariable.fromString(v))
read_variables = variables

variables = []
for v in write_variables:
    if v.startswith("SV") or v.startswith("pfCand"):
        variables.append(VectorTreeVariable.fromString(v, nMax=nPFCandMax))
    else:
        variables.append(TreeVariable.fromString(v))
write_variables = variables

write_variables += ["lep_StopsCompressed/I", "lep_precut/F"]

write_variables += ["lep_probPrompt/F", "lep_probNonPrompt/F", "lep_probFake/F", "lep_probNotPrompt/F"]
if options.displaced:
    write_variables += ["prob_lep_isFromSUSYandHF/F",] # prob_isFromSUSY/F, prob_isFromSUSYHF/F



logger.debug("the read_variables are {}".format(read_variables))
reader = sample.treeReader( \
    variables = read_variables, #map( lambda v: TreeVariable.fromString(v) if type(v)==type("") else v, read_variables),
    selectionString = "&&".join(skimConds)
    )


# maybe ad parser argument take from users.py
outfilename =  os.path.join("/scratch-cbe/users/benjamin.wilhelmy/DeepLepton", "predicted_on_sample", options.versionName + ("_small" if options.small else ""), modelPath.split('/')[-2],  str(options.year), options.flavour, options.ptSelection, sample_name, sample.name + '.root')
logger.debug("Writing to: %s", outfilename)

if not os.path.exists(os.path.dirname(outfilename)):
    try:
        os.makedirs(os.path.dirname(outfilename))
    except:
        pass
write_variables = map(lambda v: TreeVariable.fromString(v) if type(v) == type("") else v, write_variables)
logger.debug("write vars are {}".format(write_variables))
def make_maker(n_file):
    tmp_directory = ROOT.gDirectory
    outfile = ROOT.TFile.Open(os.path.join("/scratch-cbe/users/benjamin.wilhelmy/DeepLepton", "predicted_on_sample", options.versionName + ("_small" if options.small else ""), modelPath.split('/')[-2],  str(options.year), options.flavour, options.ptSelection, sample_name, sample.name + "{}.root".format(n_file)), 'recreate')

    outfile.cd()
    maker = TreeMaker(sequence=[],
                      variables=write_variables,
                      treeName='tree')
    tmp_directory.cd()
    maker.outfile = outfile
    return maker


# compare with trainings data class
if options.flavour == 'muo':
    global_branches = [
            #'lep_pt', 'lep_eta',
            'lep_pt', 
            'lep_eta',
            'lep_phi',
            'lep_mediumId',
            'lep_miniPFRelIso_all',
            'lep_sip3d', 
            'lep_dxy', 
            'lep_dz',
            'lep_charge',
            'lep_dxyErr', 
            'lep_dzErr', 
            'lep_ip3d',
            'lep_jetPtRelv2', 
            'lep_jetRelIso',
            'lep_miniPFRelIso_chg', 
            'lep_mvaLowPt', 
            'lep_nStations', 
            'lep_nTrackerLayers', 
            'lep_pfRelIso03_all', 
            'lep_pfRelIso03_chg', 
            'lep_pfRelIso04_all', 
            'lep_ptErr',
            'lep_segmentComp', 
            'lep_tkRelIso', 
            'lep_tunepRelPt',
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

pfCand_neutral_branches  = ['pfCand_neutral_eta', 
                            'pfCand_neutral_phi', 
                            'pfCand_neutral_pt', 
                            'pfCand_neutral_puppiWeight', 
                            'pfCand_neutral_puppiWeightNoLep',
                            'pfCand_neutral_ptRel', 
                            'pfCand_neutral_deltaR',]

pfCand_charged_branches  = ['pfCand_charged_d0', 
                            'pfCand_charged_d0Err', 
                            'pfCand_charged_dz', 
                            'pfCand_charged_dzErr', 
                            'pfCand_charged_eta', 
                            'pfCand_charged_mass',
                            'pfCand_charged_phi', 
                            'pfCand_charged_pt', 
                            'pfCand_charged_puppiWeight', 
                            'pfCand_charged_puppiWeightNoLep', 
                            'pfCand_charged_trkChi2',
                            'pfCand_charged_vtxChi2', 
                            'pfCand_charged_charge', 
                            'pfCand_charged_lostInnerHits', 
                            'pfCand_charged_pvAssocQuality',
                            'pfCand_charged_trkQuality', 
                            'pfCand_charged_ptRel', 
                            'pfCand_charged_deltaR',]

pfCand_photon_branches   = ['pfCand_photon_eta', 
                            'pfCand_photon_phi', 
                            'pfCand_photon_pt', 
                            'pfCand_photon_puppiWeight', 
                            'pfCand_photon_puppiWeightNoLep', 
                            'pfCand_photon_ptRel', 
                            'pfCand_photon_deltaR',]

pfCand_electron_branches = ['pfCand_electron_d0', 
                            'pfCand_electron_d0Err', 
                            'pfCand_electron_dz', 
                            'pfCand_electron_dzErr', 
                            'pfCand_electron_eta', 
                            'pfCand_electron_mass',
                            'pfCand_electron_phi', 
                            'pfCand_electron_pt', 
                            'pfCand_electron_puppiWeight', 
                            'pfCand_electron_puppiWeightNoLep', 
                            'pfCand_electron_trkChi2',
                            'pfCand_electron_vtxChi2', 
                            'pfCand_electron_charge', 
                            'pfCand_electron_lostInnerHits', 
                            'pfCand_electron_pvAssocQuality',
                            'pfCand_electron_trkQuality', 
                            'pfCand_electron_ptRel', 
                            'pfCand_electron_deltaR',]

pfCand_muon_branches     = ['pfCand_muon_d0', 
                            'pfCand_muon_d0Err', 
                            'pfCand_muon_dz', 
                            'pfCand_muon_dzErr', 
                            'pfCand_muon_eta', 
                            'pfCand_muon_mass', 
                            'pfCand_muon_phi',
                            'pfCand_muon_pt', 
                            'pfCand_muon_puppiWeight', 
                            'pfCand_muon_puppiWeightNoLep', 
                            'pfCand_muon_trkChi2', 
                            'pfCand_muon_vtxChi2', 
                            'pfCand_muon_charge',
                            'pfCand_muon_lostInnerHits', 
                            'pfCand_muon_pvAssocQuality', 
                            'pfCand_muon_trkQuality', 
                            'pfCand_muon_ptRel', 
                            'pfCand_muon_deltaR']

SV_branches              = ['SV_dlen', 
                            'SV_dlenSig', 
                            'SV_dxy', 
                            'SV_dxySig', 
                            'SV_pAngle', 
                            'SV_chi2', 
                            'SV_eta', 
                            'SV_mass',
                            'SV_ndof', 
                            'SV_phi', 
                            'SV_pt', 
                            'SV_x', 
                            'SV_y', 
                            'SV_z', 
                            'SV_ptRel', 
                            'SV_deltaR',]


npfCand_neutral  = 10
npfCand_charged  = 80
npfCand_photon   = 50
npfCand_electron = 4
npfCand_muon     = 6
nSV              = 10



# def SVpt(SV):
#     return SV["pt"]

def ptRel(cand, lep):
    a = ROOT.TVector3(cos(lep['phi']),sin(lep['phi']),sinh(lep['eta']))
    o = ROOT.TLorentzVector(cand['pt']*cos(cand['phi']), cand['pt']*sin(cand['phi']),cand['pt']*sinh(cand['eta']),cand['pt']*cosh(cand['eta']),)
    return o.Perp(a)

# there is a problem if the event has for example more npfCand_charged ...
# gives WARNING:tensorflow:Model was constructed with shape (None, 80, 18) for input Tensor("2:0", shape=(None, 80, 18), dtype=float32),but it was called on an input with incompatible shape (None, 101, 18). 
def branches(event, vector_variables, npfC): # n = -2 for pfCand, -1 for SV
    '''vector_variables are the variables for the vector branches as a list
    '''
    # nb will be a list of list with the vector branch values
    # len(nb) = len(vector_variables)
    # len(nb[0]) = npfC
    if vector_variables[0].split('_')[0] == "pfCand":
        name = vector_variables[0].split('_')[0] +"_"+vector_variables[0].split('_')[1]#SV, pfCand
    else: 
        name = vector_variables[0].split('_')[0]
    n_objs = min(npfC, getattr(event, "n"+name))
    nb = []
    # logger.debug("starting branches with name: {}, n_objs: {}".format(name, n_objs))
    if name == 'SV':
        sort_vals = [(getattr(event, "%s_%s" % (name, 'pt'))[
                      i], i) for i in range(n_objs)]
        if 'pt' == 'deltaR':
            sort_vals.sort()
        else:
            sort_vals.sort(key=lambda v: -v[0])
    elif name.startswith('pfCand_'):
        sort_vals = [(getattr(event, "%s_%s" % (name, 'ptRel'))[
                      i], i) for i in range(n_objs)]
        if 'ptRel' == 'deltaR':
            sort_vals.sort()
        else:
            sort_vals.sort(key=lambda v: -v[0])
    else:
        raise RuntimeError("Don't know what to do with %r." % name)
    
    for i in range(n_objs):
        tmp = []
        for j in range(len(vector_variables)):
            # if j==7:
            #     print("{} = {}".format(vector_variables[j], getattr(event, vector_variables[j])[sort_vals[i][1]])) 
            tmp.append(getattr(event, vector_variables[j])[sort_vals[i][1]])
        nb.append(tmp)
    zeros = [0. for i in range(len(vector_variables))]
    for i in range(npfC - n_objs):
        #logger.debug("padding...")
        nb.append(zeros)
    # logger.debug(nb)
    nb = np.asarray([nb]).astype(np.float32, order='C')
    # logger.debug("shape = {}".format(np.shape(nb)))
    return nb

n_maxfileentries = 100000
n_current_entries = 0
n_file = 0

reader.start()
# logger.info("the lep_varnames are {}".format(lep_varnames))
# logger.info("the read vars are    {}".format(read_variables))
while reader.run():
    r = reader.event

    # The first time in while loop make the file
    if n_current_entries == 0 and n_file == 0:
        maker = make_maker(n_file)
        maker.start()
    # if files is large enough save old one and make new file
    if n_current_entries == 0 and n_file > 0:
        logger.info("%i entries copied to %s",
                    maker.tree.GetEntries(), maker.outfile.GetName())
        # logger_string = "Counter: "
        # for leptonClass in leptonClasses:
        #     logger_string += leptonClass['name'] + " {}; ".format(leptonClass['counter'])
        # logger.info(logger_string)
        maker.outfile.Write()
        maker.outfile.Close()
        logger.info("Written %s", maker.outfile.GetName())

        maker = make_maker(n_file)
        maker.start()
    n_current_entries += 1
    # copy
    for name, value in structure.iteritems():
        if name == '':
            for branch_name, _ in value:
                # if some samples have branches other samples doesnt have they will be written but with
                # some default value (for integers its -1).
                # in the susy case we want the value to be 0
                #if branch_name in ['lep_isFromSUSY_Training', 'lep_isFromSUSYHF_Training', 'lep_isFromSUSYandHF_Training'] and \
                #        not "SUSY" in leptonClasses[choice]['name']:
                #    setattr(maker.event, branch_name, 0)

                #else:
                #    setattr(maker.event, branch_name, getattr(r, branch_name))
                setattr(maker.event, branch_name, getattr(r, branch_name))

        else:
            setattr(maker.event, "n"+name, getattr(r, "n"+name))
            # sorting of SV and candidates
            n_objs = min(nPFCandMax, getattr(r, "n"+name))

            # obtain sorting values as list ( [val, i_val], ...) and sort descending wrt. to val (ascending for deltaR).

            if name == 'SV':
                sort_vals = [(getattr(r, "%s_%s" % (name, 'pt'))[
                              i], i) for i in range(n_objs)]
                if 'pt' == 'deltaR':
                    sort_vals.sort()
                else:
                    sort_vals.sort(key=lambda v: -v[0])
            elif name.startswith('pfCand_'):
                sort_vals = [(getattr(r, "%s_%s" % (name, 'ptRel'))[
                              i], i) for i in range(n_objs)]
                if 'ptRel' == 'deltaR':
                    sort_vals.sort()
                else:
                    sort_vals.sort(key=lambda v: -v[0])
            else:
                raise RuntimeError("Don't know what to do with %r." % name)
            # if name == 'pfCand_charged':
            #     for i in range(n_objs):
            #         print(getattr(r, "%s_%s" % (name, 'pt'))[sort_vals[i][1]])

            for val in value:
                for i in range(n_objs):
                    getattr(maker.event, "%s_%s" % (name, val[0]))[i] = getattr(
                        r, "%s_%s" % (name, val[0]))[sort_vals[i][1]]

    # make sure that predicted are in the right Order
    
    # Globals:
    gb = []
    for b in global_branches:
        # gb.append(lep[b.replace("lep_", "")])
        gb.append(getattr(r, b))
    globalB = np.asarray([gb]).astype(np.float32, order='C')
        
    neutralB = branches(r, pfCand_neutral_branches,  npfCand_neutral)
    chargedB = branches(r, pfCand_charged_branches,  npfCand_charged,  )
    photonB  = branches(r, pfCand_photon_branches,   npfCand_photon,   )
    electronB= branches(r, pfCand_electron_branches, npfCand_electron, )
    muonB    = branches(r, pfCand_muon_branches,     npfCand_muon,     )
    svB      = branches(r, SV_branches,              nSV,              )                

    # assert(False)
    #toPredict = np.stack([ gb, neutralB, chargedB, photonB, electronB, muonB, svB ])
    #toPredict = np.concatenate((gb, neutralB, chargedB, photonB, electronB, muonB, svB))
    toPredict = [ globalB, neutralB, chargedB, photonB, electronB, muonB, svB ]
    # prediction = model.predict(toPredict)# [0]
    # print(prediction) -> [[1.28700320e-03 6.61074229e-03 9.91939474e-01 1.62780672e-04]]
    prediction = model.predict(toPredict)[0]

    #print(prediction)
    #print(np.argmax(prediction))
    # print(maker.event.lep_isPromptId_Training, maker.event.lep_isNonPromptId_Training, maker.event.lep_isFakeId_Training)
    
    #if prediction[0] > 0.02:
    #    print('PROMPT!')
    maker.event.lep_probPrompt = prediction[0]
    maker.event.lep_probNonPrompt = prediction[1]
    maker.event.lep_probFake = prediction[2]
    maker.event.lep_probNotPrompt = prediction[1] + prediction[2]
    
    if options.displaced:
        maker.event.prob_lep_isFromSUSYandHF = prediction[3]
        # maker.event.prob_isFromSUSY = prediction[3]
        # maker.event.prob_isFromSUSYHF = prediction [40] -> check if order of these 2 are correct

    # probably used if one removes pt and eta from global features
    # maker.event.lep_pt = lep["pt"]
    # maker.event.lep_eta = lep["eta"]
    
    # maker.event.lep_mvaTTH   = lep["mvaTTH"]
    
    if options.flavour == "muo":
        # maker.event.lep_looseId  = lep["looseId"]
        # maker.event.lep_mediumId = lep["mediumId"]
        # maker.event.lep_tightId  = lep["tightId"]
        # maker.event.lep_pfRelIso03_all = lep["pfRelIso03_all"]
        # lep = {"eta":, "pfRelIso03_all", "pt", "dxy", "dz", "looseId",}
        lep = {}
        lep["eta"]            = getattr(r, "lep_eta")
        lep["pfRelIso03_all"] = getattr(r, "lep_pfRelIso03_all")
        lep["pt"]             = getattr(r, "lep_pt")
        lep["dxy"]            = getattr(r, "lep_dxy")
        lep["dz"]             = getattr(r, "lep_dz")
        lep["looseId"]        = getattr(r, "lep_looseId")
        if lep["pt"] <= 25:
            if abs(lep["eta"]) < 2.4 and lep["pfRelIso03_all"] * lep["pt"] < 5.0 and abs(lep["dxy"]) < 0.02 and abs(lep["dz"]) < 0.1 and lep["looseId"]:
                maker.event.lep_StopsCompressed = 1
            else:
                maker.event.lep_StopsCompressed = 0
        elif lep["pt"] > 25:
            if abs(lep["eta"]) < 2.4 and lep["pfRelIso03_all"] < 0.2 and abs(lep["dxy"]) < 0.02 and abs(lep["dz"]) < 0.1 and lep["looseId"]:
                maker.event.lep_StopsCompressed = 1
            else:
                maker.event.lep_StopsCompressed = 0
    
        if abs(lep["eta"]) < 2.4 and abs(lep["dxy"]) < 0.02 and abs(lep["dz"]) < 0.1 and lep["looseId"]:
            maker.event.lep_precut = 1
        else:
            maker.event.lep_precut = 0
    
    elif options.flavour == "ele":
        maker.event.lep_pfRelIso03_all = lep["pfRelIso03_all"]
        
        if lep["pt"] <= 25:
            if abs(lep["pdgId"]) == 11: 
                absEta = abs(lep["eta"] + lep["deltaEtaSC"])
            else:
                absEta = abs(lep["eta"]) 
            ECALGap = ( absEta > 1.566 or absEta < 1.4442 )
            # StopsCompressed Id
            if abs(lep["dxy"]) < 0.02 and abs(lep["dz"]) < 0.1 and abs(lep["eta"]) < 2.5 and (lep['pfRelIso03_all']*lep['pt']) < 5.0 \
                    and ECALGap and electronVIDSelector( lep, idVal= 1, removedCuts=['pfRelIso03_all'] ):
                maker.event.lep_StopsCompressed = 1
            else:
                maker.event.lep_StopsCompressed = 0
            if abs(lep["dxy"]) < 0.02 and abs(lep["dz"]) < 0.1 and abs(lep["eta"]) < 2.5 \
                    and ECALGap and electronVIDSelector( lep, idVal= 1, removedCuts=['pfRelIso03_all'] ):
                maker.event.lep_precut = 1
            else:
                maker.event.lep_precut = 0
            
        else:
            if abs(lep["pdgId"]) == 11:
                absEta = abs(lep["eta"] + lep["deltaEtaSC"])
            else:
                absEta = abs(lep["eta"]) 
            ECALGap = ( absEta > 1.566 or absEta < 1.4442 )
            # StopsCompressed Id
            if abs(lep["dxy"]) < 0.02 \
                    and abs(lep["dz"]) < 0.1 \
                    and abs(lep["eta"]) < 2.5 \
                    and lep['pfRelIso03_all'] < 0.2 \
                    and ECALGap and electronVIDSelector( lep, idVal= 1, removedCuts=['pfRelIso03_all'] ):
                maker.event.lep_StopsCompressed = 1
            else:
                maker.event.lep_StopsCompressed = 0
            if abs(lep["dxy"]) < 0.02 and abs(lep["dz"]) < 0.1 and abs(lep["eta"]) < 2.5 \
                    and ECALGap and electronVIDSelector( lep, idVal= 1, removedCuts=['pfRelIso03_all'] ):
                maker.event.lep_precut = 1
            else:
                maker.event.lep_precut = 0





    maker.run()

    # check if maximal file entries reached
    if n_current_entries >= n_maxfileentries:
        n_current_entries = 0
        n_file += 1

        
        maker.fill()
        maker.event.init()
        
                
    if n_current_entries%1000 == 0:
        logger.info("n_current_entries = {}".format(n_current_entries))
    # stop early when small.
    if options.small:
        if n_current_entries>=200:
            break

logger.info("Writing trees.")
logger.info("{} entries copied to {}".format(maker.tree.GetEntries(), maker.outfile.GetName()))
#leptonClass['maker'].tree.Write()
maker.outfile.Write()
maker.outfile.Close()
logger.info( "Written %s", outfilename)

