#!/bin/sh

#evaluation test data

#best
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 10 --ptMax 0   --trainingClasses fullClasses --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --testData 
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 10 --ptMax 25  --trainingClasses fullClasses --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --testData 
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 25 --ptMax 0   --trainingClasses fullClasses --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --testData 
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 10 --ptMax 0   --trainingClasses fullClasses --flatSample TTs_Muons_biLSTM_splitDense_elu_2016
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 10 --ptMax 25  --trainingClasses fullClasses --flatSample TTs_Muons_biLSTM_splitDense_elu_2016
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 25 --ptMax 0   --trainingClasses fullClasses --flatSample TTs_Muons_biLSTM_splitDense_elu_2016
#standard
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 10 --ptMax 0   --trainingClasses fullClasses --flatSample TTs_Muons_2016 --testData 
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 10 --ptMax 25  --trainingClasses fullClasses --flatSample TTs_Muons_2016 --testData 
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 25 --ptMax 0   --trainingClasses fullClasses --flatSample TTs_Muons_2016 --testData 
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 10 --ptMax 0   --trainingClasses fullClasses --flatSample TTs_Muons_2016
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 10 --ptMax 25  --trainingClasses fullClasses --flatSample TTs_Muons_2016
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 25 --ptMax 0   --trainingClasses fullClasses --flatSample TTs_Muons_2016
#simpleClasses
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 10 --ptMax 0   --trainingClasses simpleClasses --flatSample TTs_Muons_biLSTM_splitDense_elu_simpleClasses_2016 --testData 
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 10 --ptMax 25  --trainingClasses simpleClasses --flatSample TTs_Muons_biLSTM_splitDense_elu_simpleClasses_2016 --testData 
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 25 --ptMax 0   --trainingClasses simpleClasses --flatSample TTs_Muons_biLSTM_splitDense_elu_simpleClasses_2016 --testData 
#prompt
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 10 --ptMax 0   --trainingClasses fullClasses --flatSample TTs_Muons_biLSTM_splitDense_elu_prompt_2016 --testData 
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 10 --ptMax 25  --trainingClasses fullClasses --flatSample TTs_Muons_biLSTM_splitDense_elu_prompt_2016 --testData 
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 25 --ptMax 0   --trainingClasses fullClasses --flatSample TTs_Muons_biLSTM_splitDense_elu_prompt_2016 --testData 
#no CNN
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 10 --ptMax 0   --trainingClasses fullClasses --flatSample TTs_Muons_noCNN_2016 --testData 
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 10 --ptMax 25  --trainingClasses fullClasses --flatSample TTs_Muons_noCNN_2016 --testData 
python -i stacked_classes_DAgm.py --flat --looseId --ptMin 25 --ptMax 0   --trainingClasses fullClasses --flatSample TTs_Muons_noCNN_2016 --testData 


#input training data
#python -i stacked_classes_DAgm.py --small --flat --ptMin 5  --ptMax 0   --trainingClasses noTraining --flatSample TTs_Muons_2016_noTraining
python -i stacked_classes_DAgm.py --flat --ptMin 5   --ptMax 0   --trainingClasses noTraining --flatSample TTs_Muons_2016_noTraining
python -i stacked_classes_DAgm.py --flat --ptMin 15  --ptMax 0   --trainingClasses noTraining --flatSample DYvsQCD_Muons_2016_noTraining
python -i stacked_classes_DAgm.py --flat --ptMin 15  --ptMax 0   --trainingClasses noTraining --flatSample TTs_Muons_2016_noTraining

