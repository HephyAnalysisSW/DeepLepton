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



#TTJets prediction on 20181026 DYvsQCD training
flat_directory    = '/afs/hephy.at/data/gmoertl01/DeepLepton/trainfiles/v3/2016/muo/pt_15_to_inf/TTJets_sorted'
predict_directory = '/afs/hephy.at/data/gmoertl01/DeepLepton/predictions/muons/EvaluationTestData_TTJets_sorted_on_model_20181026'

flat_files, predict_files = get_flat_files( flat_directory, predict_directory )

training_20181026         = Sample.fromFiles( 'TTJets_muo',         texName = 'TTJets muons',            files = flat_files,    treeName='tree' )
training_20181026_predict = Sample.fromFiles( 'TTJets_muo_predict', texName = 'TTJets muons prediction', files = predict_files, treeName='tree' ) 
training_20181026.addFriend( training_20181026_predict, 'tree' ) 

#usage
# from DeepLepton.samples.flat_training_samples import training_20181026




