# Standard imports
import ROOT
import os

# RootTools
from RootTools.core.standard import *

########################
### helper functions ###
########################

#Get flat ntuple files + prediction files
def get_flat_files( flat_directory, predict_directory, maxN = -1 ):

    #get predict files
    predict_files = os.listdir(predict_directory)
    #remove DeepJet log file
    if 'tree_association.txt' in predict_files:
        predict_files.remove('tree_association.txt')       

    #get only maxN files
    if len(predict_files)>maxN and maxN>0:
        del predict_files[maxN:]

    #get flat files
    flat_files = predict_files
    flat_files = [file_name.replace('_predict.root', '.root') for file_name in flat_files]

    #append directory to file names
    flat_files    = [file_name.replace(file_name, os.path.join(flat_directory,    file_name)) for file_name in flat_files   ]
    predict_files = [file_name.replace(file_name, os.path.join(predict_directory, file_name)) for file_name in predict_files]

    return flat_files, predict_files

def get_flat_sample( training_name, sample_name, flat_files, predict_files):

    postfix = '_predict'
    flat_sample         = Sample.fromFiles( training_name,         texName = sample_name,            files = flat_files,    treeName='tree' ) 
    flat_sample_predict = Sample.fromFiles( training_name+postfix, texName = sample_name+postfix,    files = predict_files, treeName='tree' ) 
    flat_sample.addFriend( flat_sample_predict, 'tree' )

    return flat_sample

#Get only flat ntuple files (when no training was performed and input training data plots are needed)
def get_flat_files_noTraining( flat_directory, flat_txtfile, maxN = -1 ):

    #get flat files
    with open(flat_txtfile) as f:
        flat_files = f.read().splitlines()

    #get only maxN files
    if len(flat_files)>maxN and maxN>0:
        del flat_files[maxN:]

    #append directory to file names
    flat_files = [file_name.replace(file_name, os.path.join(flat_directory, file_name)) for file_name in flat_files]

    return flat_files

def get_flat_sample_noTraining( sample_name, flat_files ):

    flat_sample = Sample.fromFiles( sample_name+'_sample', texName = sample_name, files = flat_files, treeName='tree' ) 

    return flat_sample

#################
### variables ###
#################

def get_flat_variables(varSelection):

    flat_variables = [
    "run/I",
    "lumi/I",
    "evt/l",
    "lep_trackerHits/I",
    #Training Variables
    "lep_pt/F",
    "lep_eta/F",
    "lep_phi/F",
    "lep_rho/F",
    "lep_innerTrackChi2/F",

    "lep_relIso03/F",
    "lep_relIso04/F",
    "lep_miniRelIso/F",
    "lep_chargedHadRelIso03/F",
    "lep_chargedHadRelIso04/F",
    "lep_miniRelIsoNeutral/F",
    "lep_miniRelIsoCharged/F",

    "lep_lostHits/I", #lost inner hits
    "lep_innerTrackValidHitFraction/F",
    "lep_trackerLayers/I",
    "lep_pixelLayers/I",
    "lep_trackerHits/I",
    "lep_lostOuterHits/I",
    "lep_jetBTagCSV/F",
    "lep_jetBTagDeepCSV/F",
    "lep_jetBTagDeepCSVCvsB/F",
    "lep_jetBTagDeepCSVCvsL/F",

    "lep_jetDR/F",
    "lep_dxy/F",
    "lep_dz/F",
    "lep_edxy/F",
    "lep_edz/F",
    "lep_ip3d/F",
    "lep_sip3d/F",
    "lep_EffectiveArea03/F",
    "lep_jetPtRatiov1/F",
    "lep_jetPtRatiov2/F",
    "lep_jetPtRelv1/F",
    "lep_jetPtRelv2/F",
    "lep_ptErrTk/F",

    "npfCand_neutral/I",
    "npfCand_charged/I",
    "npfCand_photon/I",
    "npfCand_electron/I",
    "npfCand_muon/I",
    "nSV/I",

    "pfCand_neutral[pt_ptRelSorted/F]",
    "pfCand_charged[pt_ptRelSorted/F]",
    "pfCand_photon[pt_ptRelSorted/F]",
    "pfCand_electron[pt_ptRelSorted/F]",
    "pfCand_muon[pt_ptRelSorted/F]",
    "SV[pt_ptSorted/F]",

    #Electron specific
    "lep_etaSc/F",
    "lep_sigmaIEtaIEta/F",
    "lep_full5x5_sigmaIetaIeta/F",
    "lep_dEtaInSeed/F",
    "lep_dPhiScTrkIn/F",
    "lep_dEtaScTrkIn/F",
    "lep_eInvMinusPInv/F",
    "lep_convVeto/I",
    "lep_hadronicOverEm/F",
    "lep_r9/F",
    "lep_mvaIdFall17noIso/F",
    "lep_mvaIdSpring16/F",
    #Muon specific
    "lep_segmentCompatibility/F",
    "lep_muonInnerTrkRelErr/F",
    "lep_isGlobalMuon/I",
    "lep_chi2LocalPosition/F",
    "lep_chi2LocalMomentum/F",
    "lep_globalTrackChi2/F",
    "lep_glbTrackProbability/F",
    "lep_caloCompatibility/F",
    "lep_trkKink/F",
    #other Variables
    "lep_pdgId/I",
    "lep_mcMatchPdgId/I",
    "lep_mcMatchId/I",
    "lep_mcMatchAny/I",
    "lep_mediumMuonId/I",
    "lep_pfMuonId/I",
    "lep_isPromptId_Training/I",
    "lep_isNonPromptId_Training/I",
    "lep_isFakeId_Training/I",
    "lep_mvaTTH/F",
    "lep_mvaTTV/F",
    "nTrueInt/F",
    "lumi_scaleFactor1fb/F",
    ]

    if varSelection=='fullClasses':
        flat_variables.append("prob_lep_isPromptId_Training/F")
        flat_variables.append("prob_lep_isNonPromptId_Training/F")
        flat_variables.append("prob_lep_isFakeId_Training/F")
    if varSelection=='simpleClasses':
        flat_variables.append("prob_lep_isPromptId_Training/F")
        flat_variables.append("prob_lep_isNotPromptId_Training/F")

    return flat_variables

##################
###### 2017 ######
##################

#2017 Muons
TTs_Muons_Tim_2017 = {
'training_name'     : '2017_Muons',
'training_date'     : '20190322',
'sample_name'       : 'TTs_Muons_2017',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/cms03/tbrueckler/DeepLepton/skims/v1/step3/2017/muo/pt_5_-1/TTJets',
'predict_directory'           : '/afs/hephy.at/data/cms03/tbrueckler/trainings/muo_2017_small/TTs_Muon_EvaluationTestData',
'predict_directory_trainData' : '',
}

#2017 Electrons
TTs_Electrons_Tim_2017 = {
'training_name'     : '2017_Electrons',
'training_date'     : '20190325',
'sample_name'       : 'TTs_Electrons_2017',
'train_data'        : 'TTs electrons',
'test_data'         : 'TTs electrons',
'flat_directory'    : '/afs/hephy.at/data/cms03/tbrueckler/DeepLepton/skims/v1/step3/2017/ele/pt_5_-1/TTJets',
'predict_directory'           : '/afs/hephy.at/data/cms03/tbrueckler/trainings/ele_2017_small/TTs_Electrons_EvaluationTestData',
'predict_directory_trainData' : '',
}

#noTraining:
TTs_Muons_2017_noTraining = {
'sample_name'       : 'TTs_Muons_2017',
'training_date'     : 'noTraining',
'flat_directory'    : '/afs/hephy.at/data/cms03/tbrueckler/DeepLepton/skims/v1/step3/2017/muo/pt_5_-1/TTJets',
'flat_txtfile'      : '/afs/hephy.at/data/cms03/tbrueckler/DeepLepton/skims/v1/step3/2017/muo/pt_5_-1/TTJets/train_muo_2017.txt',
}



##########################
### training electrons ###
##########################

##bare training samples simon test01
#TTJets_Electrons_2016_noTraining = {
#'sample_name'       : 'TTJets_Electrons_2016',
#'training_date'     : 'noTraining',
#'flat_directory'    : '/afs/hephy.at/work/s/sschneider/DeepLepton/skims/v1_small_simon/step3/2016/ele/pt_5_-1/TTJets/',
#'flat_txtfile'      : '/afs/hephy.at/work/s/sschneider/DeepLepton/skims/v1_small_simon/step3/2016/ele/pt_5_-1/TTJets/train_ele.txt',
#}

#bare training samples simon test02
TTJets_Electrons_2016_noTraining = {
'sample_name'       : 'TTJets_Electrons_2016',
'training_date'     : 'noTraining',
'flat_directory'    : '/afs/hephy.at/data/cms01/DeepLepton/skims/v1/step3/2016/ele/pt_5_-1/TTJets/',
'flat_txtfile'      : '/afs/hephy.at/data/cms01/DeepLepton/skims/v1/step3/2016/ele/pt_5_-1/TTJets/train_ele.txt',
}


#first training TTJets simon
TTJets_Electrons_2016_preliminary = {  # this name to be passed to roc.py
'training_name'     : 'TTJets_Electrons_2016_pt5toInf_preliminary',   #free to choose
'training_date'     : '20190128-01',     #free
'sample_name'       : 'TTJets_Electrons_2016',     #free
'train_data'        : 'TTJets electrons',  #free
'test_data'         : 'TTJets electrons',  #free
'flat_directory'    : '/afs/hephy.at/data/cms01/DeepLepton/skims/v1/step3/2016/ele/pt_5_-1/TTJets/',
'predict_directory'           : '/afs/hephy.at/data/cms01/DeepLepton/results/TTJets_Electron_run03_EvaluationTestData',
#'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181211-01/TTs_Muon_EvaluationTestDataIsTrainData',
}


#first training TTJets simon as above but without mva result as input for training
TTJets_Electrons_2016_preliminary_noMVA = {  # this name to be passed to roc.py
'training_name'     : 'TTJets_Electrons_2016_pt5toInf_preliminary_noMVA',   #free to choose
'training_date'     : '20190129-01',     #free
'sample_name'       : 'TTJets_Electrons_2016',     #free
'train_data'        : 'TTJets electrons',  #free
'test_data'         : 'TTJets electrons',  #free
'flat_directory'    : '/afs/hephy.at/data/cms01/DeepLepton/skims/v1/step3/2016/ele/pt_5_-1/TTJets/',
'predict_directory'           : '/afs/hephy.at/data/cms01/DeepLepton/results/TTJets_Electron_run04_EvaluationTestData',
#'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181211-01/TTs_Muon_EvaluationTestDataIsTrainData',
}


#run with biLSTM configuration
TTJets_Electrons_2016_biLSTM = {  # this name to be passed to roc.py
'training_name'     : 'TTJets_Electrons_2016_pt5toInf_biLSTM',   #free to choose
'training_date'     : '20190211-01',     #free
'sample_name'       : 'TTJets_Electrons_2016',     #free
'train_data'        : 'TTJets electrons',  #free
'test_data'         : 'TTJets electrons',  #free
'flat_directory'    : '/afs/hephy.at/data/cms01/DeepLepton/skims/v1/step3/2016/ele/pt_5_-1/TTJets/',
'predict_directory'           : '/afs/hephy.at/data/cms01/DeepLepton/results/TTJets_Electron_biLSTM_EvaluationTestData',
#'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181211-01/TTs_Muon_EvaluationTestDataIsTrainData',
}


#run with biLSTM_split configuration
TTJets_Electrons_2016_biLSTM_split = {  # this name to be passed to roc.py
'training_name'     : 'TTJets_Electrons_2016_pt5toInf_biLSTM_split',   #free to choose
'training_date'     : '20190211-02',     #free
'sample_name'       : 'TTJets_Electrons_2016',     #free
'train_data'        : 'TTJets electrons',  #free
'test_data'         : 'TTJets electrons',  #free
'flat_directory'    : '/afs/hephy.at/data/cms01/DeepLepton/skims/v1/step3/2016/ele/pt_5_-1/TTJets/',
'predict_directory'           : '/afs/hephy.at/data/cms01/DeepLepton/results/TTJets_Electron_biLSTM_split_EvaluationTestData',
#'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181211-01/TTs_Muon_EvaluationTestDataIsTrainData',
}


#run with pooling configuration
TTJets_Electrons_2016_pooling = {  # this name to be passed to roc.py
'training_name'     : 'TTJets_Electrons_2016_pt5toInf_pooling',   #free to choose
'training_date'     : '20190212-01_pooling',     #free
'sample_name'       : 'TTJets_Electrons_2016',     #free
'train_data'        : 'TTJets electrons',  #free
'test_data'         : 'TTJets electrons',  #free
'flat_directory'    : '/afs/hephy.at/data/cms01/DeepLepton/skims/v1/step3/2016/ele/pt_5_-1/TTJets/',
'predict_directory'           : '/afs/hephy.at/data/cms01/DeepLepton/results/TTJets_Electron_pooling_EvaluationTestData',
#'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181211-01/TTs_Muon_EvaluationTestDataIsTrainData',
}

####################
### flat samples ###
####################

#bare training samples
TTs_Muons_2016_noTraining = {
'sample_name'       : 'TTs_Muons_2016',
'training_date'     : 'noTraining',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
'flat_txtfile'      : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs/50train_muo.txt',
}
DYvsQCD_Muons_2016_noTraining = {
'sample_name'       : 'DYvsQCD_Muons_2016',
'training_date'     : 'noTraining',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/DYvsQCD',
'flat_txtfile'      : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/DYvsQCD/50train_muo.txt',
}

#flat test file
testFile = {
'training_name'     : 'TTs_Muons_balanced_pt5toInf_20181117',
'training_date'     : '20181117',
'sample_name'       : 'testFile',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/testfile/flat/step3',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/testfile/flat/step3/EvaluationTestData_TTJets_on_model_TTs_balanced_pt5toInf_20181117',
'predict_directory_trainData' : '',
}

##############################
### prompt reference class ###
##############################

#unmixed samples
DYvsQCD_Muons_balanced_2016 = {
#'training_name'     : 'DYvsQCD_Muons_balanced_20181108',
#'sample_name'       : 'DYvsQCD_Muons_2016',
#'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/DYvsQCD',
#'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018110801/DYvsQCD_balancedMuonEvaluationTestData',
'training_name'     : 'DYvsQCD_Muons_balanced_20181113',
'training_date'     : '2018111302',
'sample_name'       : 'DYvsQCD_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v5/step3/2016/muo/pt_15_-1/DYvsQCD',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018111302/DYvsQCD_balancedMuonEvaluationTestData',
}

DYvsQCD_Muons_balancedSimple_2016 = {
'training_name'     : 'DYvsQCD_Muons_balancedSimple_20181108',
'sample_name'       : 'DYvsQCD_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/DYvsQCD',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018110802/DYvsQCD_balancedSimpleMuonEvaluationTestData',
}

TTJets_Muons_balanced_2016 = {
#'training_name'     : 'TTJets_Muons_balanced_20181108',
#'sample_name'       : 'TTJets_Muons_2016',
#'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/TTJets',
#'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018110803/TTJets_balancedMuonEvaluationTestData',
'training_name'     : 'TTJets_Muons_balanced_20181112',
'sample_name'       : 'TTJets_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/TTJets',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181112/TTJets_balancedMuonEvaluationTestData',
}

TTJets_Muons_balancedSimple_2016 = {
'training_name'     : 'TTJets_Muons_balancedSimple_20181108',
'sample_name'       : 'TTJets_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/TTJets',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018110804/TTJets_balancedSimpleMuonEvaluationTestData',
}

#mixed samples
DYvsQCD_on_TTJets_Muons_balanced_2016 = {
'training_name'     : 'TTJets_Muons_balanced_20181108',
'sample_name'       : 'DYvsQCD_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/DYvsQCD',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/predictions/muons/20181108/EvaluationTestData_DYvsQCD_on_model_TTJets_balanced_20181108',
}

DYvsQCD_on_TTJets_Muons_balancedSimple_2016 = {
'training_name'     : 'TTJets_Muons_balancedSimple_20181108',
'sample_name'       : 'DYvsQCD_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/DYvsQCD',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/predictions/muons/20181108/EvaluationTestData_DYvsQCD_on_model_TTJets_balancedSimple_20181108',
}

TTJets_on_DYvsQCD_Muons_balanced_2016 = {
'training_name'     : 'DYvsQCD_Muons_balanced_20181108',
'sample_name'       : 'TTJets_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/TTJets',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/predictions/muons/20181108/EvaluationTestData_TTJets_on_model_DYvsQCD_balanced_20181108',
}

TTJets_on_DYvsQCD_Muons_balancedSimple_2016 = {
'training_name'     : 'DYvsQCD_Muons_balancedSimple_20181108',
'sample_name'       : 'TTJets_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/TTJets',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/predictions/muons/20181108/EvaluationTestData_TTJets_on_model_DYvsQCD_balancedSimple_20181108',
}

#TTJets pt related trainings
TTJets_Muons_balanced_pt5toInf_2016 = {
'training_name'     : 'TTJets_Muons_balanced_pt5toInf_20181114',
'training_date'     : '20181114-01',
'sample_name'       : 'TTJets_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTJets',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018111401/TTJets_balancedPt5toInfMuonEvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018111401/TTJets_balancedPt5toInfMuonEvaluationTestDataIsTrainData',
#'training_name'     : 'TTJets_Muons_balanced_pt5toInf_20181115',
#'training_date'     : '20181115',
#'sample_name'       : 'TTJets_Muons_2016',
#'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTJets',
#'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181115/TTJets_balancedPt5toInfMuonEvaluationTestData',
#'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181115/TTJets_balancedPt5toInfMuonEvaluationTestDataIsTrainData',
}

TTJets_Muons_balanced_pt5to15_2016 = {
#'training_name'     : 'TTJets_Muons_balanced_pt5to15_20181113',
#'sample_name'       : 'TTJets_Muons_2016',
#'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v5/step3/2016/muo/pt_5_15/TTJets',
#'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181113/TTJets_balancedLowPtMuonEvaluationTestData',
'training_name'     : 'TTJets_Muons_balanced_pt5to15_20181114',
'training_date'     : '20181114-02',
'sample_name'       : 'TTJets_Muons_2016',
'flat_directory'              : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_15/TTJets',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018111402/TTJets_balancedPt5to15MuonEvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018111402/TTJets_balancedPt5to15MuonEvaluationTestDataIsTrainData',
}

TTJets_Muons_balanced_pt15to25_2016 = {
'training_name'     : 'TTJets_Muons_balanced_pt15to25_20181114',
'training_date'     : '20181114-03',
'sample_name'       : 'TTJets_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTJets',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018111403/TTJets_balancedPt15to25MuonEvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018111403/TTJets_balancedPt15to25MuonEvaluationTestDataIsTrainData',
}

TTJets_Muons_balanced_pt25toInf_2016 = {
'training_name'     : 'TTJets_Muons_balanced_pt25toInf_20181114',
'training_date'     : '20181114-04',
'sample_name'       : 'TTJets_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_25_-1/TTJets',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018111404/TTJets_balancedPt25toInfMuonEvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018111404/TTJets_balancedPt25toInfMuonEvaluationTestDataIsTrainData',
}

#TTs pt related trainings
TTs_Muons_prompt_2016 = {
#'training_name'     : 'TTs_Muons_balanced_pt5toInf_20181117',
#'training_date'     : '20181117',
#'sample_name'       : 'TTs_Muons_2016',
#'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
#'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181117/TTs_balanced_pt5toInf_MuonEvaluationTestData',
#'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181117/TTs_balanced_pt5toInf_MuonEvaluationTestDataIsTrainData',
#'training_name'     : 'TTs_Muons_balanced_pt5toInf_20181127',
#'training_date'     : '20181127',
#'sample_name'       : 'TTs_Muons_2016',
#'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
#'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181127/TTs_balanced_pt5toInf_MuonEvaluationTestData',
#'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181127/TTs_balanced_pt5toInf_MuonEvaluationTestDataIsTrainData',
'training_name'     : 'prompt muons as reference class',
'training_date'     : '20181202',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181202/TTs_balanced_pt5toInf_MuonEvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181202/TTs_balanced_pt5toInf_MuonEvaluationTestDataIsTrainData',
}

TTs_Muons_prompt_test_2016 = {
'training_name'     : 'prompt muons as reference class, test',
'training_date'     : '20181205-03',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181205-03/TTs_balanced_pt5toInf_MuonEvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181205-03/TTs_balanced_pt5toInf_MuonEvaluationTestDataIsTrainData',
}

#################################
### nonPrompt reference class ###
#################################

#Standard Training
TTs_Muons_2016 = {
'training_name'     : 'standard',
'training_date'     : '20181211-01',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181211-01/TTs_Muon_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181211-01/TTs_Muon_EvaluationTestDataIsTrainData',
}

#Test Architectures
TTs_Muons_splitDense_2016 = {
'training_name'     : 'split dense layers',
'training_date'     : '20181211-02',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181211-02/TTs_Muon_splitDense_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181211-02/TTs_Muon_splitDense_EvaluationTestDataIsTrainData',
}

TTs_Muons_simpleClasses_2016 = {
'training_name'     : 'simple classes',
'training_date'     : '20181211-03',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181211-03/TTs_Muon_simpleClasses_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181211-03/TTs_Muon_simpleClasses_EvaluationTestDataIsTrainData',
}

TTs_Muons_globalVarsOnly_2016 = {
'training_name'     : 'no PF and SV',
'training_date'     : '20181211-04',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181211-04/TTs_Muon_globalVarsOnly_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181211-04/TTs_Muon_globalVarsOnly_EvaluationTestDataIsTrainData',
}

TTs_Muons_pooling_2016 = {
'training_name'     : 'pooling layers',
'training_date'     : '20181212-01',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181212-01/TTs_Muon_pooling_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181212-01/TTs_Muon_pooling_EvaluationTestDataIsTrainData',
}

TTs_Muons_TTVonly_2016 = {
'training_name'     : 'TTV lepton varibles, no PF and SV',
'training_date'     : '20181212-03',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181212-03/TTs_Muon_TTVonly_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181212-03/TTs_Muon_TTVonly_EvaluationTestDataIsTrainData',
}

TTs_Muons_TTV_2016 = {
'training_name'     : 'TTV lepton variables',
'training_date'     : '20181212-04',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181212-04/TTs_Muon_TTV_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181212-04/TTs_Muon_TTV_EvaluationTestDataIsTrainData',
}

TTs_Muons_noCNN_2016 = {
'training_name'     : 'no CNN',
'training_date'     : '20181212-05',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181212-05/TTs_Muon_noCNN_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181212-05/TTs_Muon_noCNN_EvaluationTestDataIsTrainData',
}

TTs_Muons_biLSTM_simpleClasses_2016 = {
'training_name'     : 'biLSTM, simple classes',
'training_date'     : '20181228-01',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181228-01/TTs_Muon_biLSTM_simpleClasses_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181228-01/TTs_Muon_biLSTM_simpleClasses_EvaluationTestDataIsTrainData',
}

TTs_Muons_biLSTM_2016 = {
'training_date'     : '20181212-02',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181212-02/TTs_Muon_biLSTM_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181212-02/TTs_Muon_biLSTM_EvaluationTestDataIsTrainData',
'training_name'     : 'biLSTM',
#'training_date'     : '20181228-02',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
#'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181228-02/TTs_Muon_biLSTM_EvaluationTestData',
#'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181228-02/TTs_Muon_biLSTM_EvaluationTestDataIsTrainData',
}

TTs_Muons_biLSTM_split_2016 = {
'training_name'     : 'biLSTM, split dense layers',
'training_date'     : '20181228-03',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181228-03/TTs_Muon_biLSTM_split_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181228-03/TTs_Muon_biLSTM_split_EvaluationTestDataIsTrainData',
}

TTs_Muons_biLSTM_split_simpleClasses_2016 = {
'training_name'     : 'biLSTM, split dense layers, simple classes',
'training_date'     : '20181228-04',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181228-04/TTs_Muon_biLSTM_split_simpleClasses_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181228-04/TTs_Muon_biLSTM_split_simpleClasses_EvaluationTestDataIsTrainData',
}

TTs_Muons_selu_2016 = {
'training_name'     : 'selu',
'training_date'     : '20190115',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190115/TTs_Muon_selu_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190115/TTs_Muon_selu_EvaluationTestDataIsTrainData',
}
TTs_Muons_biLSTM_splitDense_2016 = {
'training_name'     : 'biLSTM, split dense layers',
#'training_date'     : '20190129-02',
'training_date'     : '20190222-01',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
#'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190129-02/TTs_Muon_biLSTM_splitDense_EvaluationTestData',
#'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190129-02/TTs_Muon_biLSTM_splitDense_EvaluationTestDataIsTrainData',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190222-01/TTs_Muon_biLSTM_splitDense_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190222-01/TTs_Muon_biLSTM_splitDense_EvaluationTestDataIsTrainData',
}
TTs_Muons_biLSTM_splitDense_selu_2016 = {
'training_name'     : 'biLSTM, split dense layers, selu', 
'training_date'     : '20190129-03',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190129-03/TTs_Muon_biLSTM_splitDense_selu_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190129-03/TTs_Muon_biLSTM_splitDense_selu_EvaluationTestDataIsTrainData',
}
TTs_Muons_endVar_2016 = {
'training_name'     : 'standard',
'training_date'     : '20190129-01',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190129-01/TTs_Muon_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190129-01/TTs_Muon_EvaluationTestDataIsTrainData',
}
TTs_Muons_biLSTM_splitDense_elu_2016 = {
'training_name'     : 'biLSTM, split dense layers, elu', 
'training_date'     : '20190222-02',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190222-02/TTs_Muon_biLSTM_splitDense_elu_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190222-02/TTs_Muon_biLSTM_splitDense_elu_EvaluationTestDataIsTrainData',
}



#Cross Evaluation
DYvsQCD_Muons_onDYvsQCD_2016 = {
'training_name'     : 'standard',
'training_date'     : '20190211-01',
'sample_name'       : 'DYvsQCD_Muons_2016',
'train_data'        : 'DYvsQCD muons',
'test_data'         : 'DYvsQCD muons',
'flat_directory'    : '/afs/hephy.at/data/cms02/DeepLepton/skims/v1/step3/2016/muo/pt_15_-1/DYvsQCD',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190211-01/DYvsQCD_Muon_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190211-01/DYvsQCD_Muon_EvaluationTestDataIsTrainData',
}
DYvsQCD_Muons_onTTs_2016 = {
'training_name'     : 'standard',
'training_date'     : '20190211-01',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'DYvsQCD muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/cms02/DeepLepton/skims/v1/step3/2016/muo/pt_15_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190211-01/DYvsQCD_Muon_CrossEvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190211-01/DYvsQCD_Muon_EvaluationTestDataIsTrainData',
}
DYvsQCD_Muons_onAll_2016 = {
'training_name'     : 'standard',
'training_date'     : '20190211-01',
'sample_name'       : 'all_Muons_2016',
'train_data'        : 'DYvsQCD muons',
'test_data'         : 'DYvsQCD+TTs muons',
'flat_directory'    : '/afs/hephy.at/data/cms02/DeepLepton/skims/v1/step3/2016/muo/pt_15_-1/all',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190211-01/DYvsQCD_Muon_CrossAllEvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190211-01/DYvsQCD_Muon_EvaluationTestDataIsTrainData',
}

TTs_Muons_onTTs_2016 = {
'training_name'     : 'standard',
'training_date'     : '20190211-02',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/cms02/DeepLepton/skims/v1/step3/2016/muo/pt_15_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190211-02/TTs_Muon_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190211-02/TTs_Muon_EvaluationTestDataIsTrainData',
}
TTs_Muons_onDYvsQCD_2016 = {
'training_name'     : 'standard',
'training_date'     : '20190211-02',
'sample_name'       : 'DYvsQCD_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'DYvsQCD muons',
'flat_directory'    : '/afs/hephy.at/data/cms02/DeepLepton/skims/v1/step3/2016/muo/pt_15_-1/DYvsQCD',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190211-02/TTs_Muon_CrossEvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190211-02/TTs_Muon_EvaluationTestDataIsTrainData',
}
TTs_Muons_onAll_2016 = {
'training_name'     : 'standard',
'training_date'     : '20190211-02',
'sample_name'       : 'all_Muons_2016',
'train_data'        : 'TTs muons',
'test_data'         : 'DYvsQCD+TTs muons',
'flat_directory'    : '/afs/hephy.at/data/cms02/DeepLepton/skims/v1/step3/2016/muo/pt_15_-1/all',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190211-02/TTs_Muon_CrossAllEvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190211-02/TTs_Muon_EvaluationTestDataIsTrainData',
}

all_Muons_2016 = {
'training_name'     : 'standard',
'training_date'     : '20190211-03',
'sample_name'       : 'all_Muons_2016',
'train_data'        : 'DYvsQCD+TTs muons',
'test_data'         : 'DYvsQCD+TTs muons',
'flat_directory'    : '/afs/hephy.at/data/cms02/DeepLepton/skims/v1/step3/2016/muo/pt_15_-1/all',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190211-03/all_Muon_EvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190211-03/all_Muon_EvaluationTestDataIsTrainData',
}
all_Muons_onDYvsQCD_2016 = {
'training_name'     : 'standard',
'training_date'     : '20190211-03',
'sample_name'       : 'DYvsQCD_Muons_2016',
'train_data'        : 'DYvsQCD+TTs muons',
'test_data'         : 'DYvsQCD muons',
'flat_directory'    : '/afs/hephy.at/data/cms02/DeepLepton/skims/v1/step3/2016/muo/pt_15_-1/DYvsQCD',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190211-03/all_Muon_CrossDYvsQCDEvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190211-03/all_Muon_EvaluationTestDataIsTrainData',
}
all_Muons_onTTs_2016 = {
'training_name'     : 'standard',
'training_date'     : '20190211-03',
'sample_name'       : 'TTs_Muons_2016',
'train_data'        : 'DYvsQCD+TTs muons',
'test_data'         : 'TTs muons',
'flat_directory'    : '/afs/hephy.at/data/cms02/DeepLepton/skims/v1/step3/2016/muo/pt_15_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190211-03/all_Muon_CrossTTsEvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20190211-03/all_Muon_EvaluationTestDataIsTrainData',
}


#usage
#flat_sample = TTJets_Muons_balanced_pt25toInf_2016
#flat_files, predict_files = get_flat_files( flat_sample['flat_directory'], flat_sample['predict_directory'])
#flat_sample = get_flat_sample( flat_sample['training_name'], flat_sample['sample_name'], flat_files, predict_files )


