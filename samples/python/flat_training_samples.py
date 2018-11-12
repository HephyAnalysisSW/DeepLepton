# Standard imports
import ROOT
import os

# RootTools
from RootTools.core.standard import *

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

#flat samples

DYvsQCD_Muons_on_TTJets_2016 = {
'training_name'     : 'DYvsQCD_Muons_20181026',
'sample_name'       : 'TTJets_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainfiles/v3/2016/muo/pt_15_to_inf/TTJets_sorted',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/predictions/muons/EvaluationTestData_TTJets_sorted_on_model_20181026',
}

#unmixed samples
DYvsQCD_Muons_balanced_2016 = {
'training_name'     : 'DYvsQCD_Muons_balanced_20181108',
'sample_name'       : 'DYvsQCD_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/DYvsQCD',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018110801/DYvsQCD_balancedMuonEvaluationTestData',
}

DYvsQCD_Muons_balancedSimple_2016 = {
'training_name'     : 'DYvsQCD_Muons_balancedSimple_20181108',
'sample_name'       : 'DYvsQCD_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/DYvsQCD',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018110802/DYvsQCD_balancedSimpleMuonEvaluationTestData',
}

TTJets_Muons_balanced_2016 = {
'training_name'     : 'TTJets_Muons_balanced_20181108',
'sample_name'       : 'TTJets_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/TTJets',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018110803/TTJets_balancedMuonEvaluationTestData',
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


flat_sample = DYvsQCD_Muons_balanced_2016
#flat_sample = DYvsQCD_Muons_balancedSimple_2016
#flat_sample = TTJets_Muons_balanced_2016
#flat_sample = TTJets_Muons_balancedSimple_2016
#flat_sample = DYvsQCD_on_TTJets_Muons_balanced_2016
#flat_sample = DYvsQCD_on_TTJets_Muons_balancedSimple_2016
#flat_sample = TTJets_on_DYvsQCD_Muons_balanced_2016
#flat_sample = TTJets_on_DYvsQCD_Muons_balancedSimple_2016

flat_files, predict_files = get_flat_files( flat_sample['flat_directory'], flat_sample['predict_directory'])
flat_sample = get_flat_sample( flat_sample['training_name'], flat_sample['sample_name'], flat_files, predict_files )


