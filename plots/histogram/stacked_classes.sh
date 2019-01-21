#!/bin/sh

##evaluation test data
#python -i stacked_classes.py --flat --looseId --ptMin 10 --ptMax 0   --trainingClasses fullClasses --flatSample TTs_Muons_biLSTM_2016 --testData 
#python -i stacked_classes.py --flat --looseId --ptMin 10 --ptMax 25  --trainingClasses fullClasses --flatSample TTs_Muons_biLSTM_2016 --testData 
#python -i stacked_classes.py --flat --looseId --ptMin 25 --ptMax 0   --trainingClasses fullClasses --flatSample TTs_Muons_biLSTM_2016 --testData 
#
##evaluation training data
#python -i stacked_classes.py --flat --looseId --ptMin 10 --ptMax 0   --trainingClasses fullClasses --flatSample TTs_Muons_biLSTM_2016
#python -i stacked_classes.py --flat --looseId --ptMin 10 --ptMax 25  --trainingClasses fullClasses --flatSample TTs_Muons_biLSTM_2016
#python -i stacked_classes.py --flat --looseId --ptMin 25 --ptMax 0   --trainingClasses fullClasses --flatSample TTs_Muons_biLSTM_2016

#input training data
#python -i stacked_classes.py --flat --ptMin 5  --ptMax 0   --trainingClasses noTraining --flatSample TTs_Muons_2016_noTraining
python -i stacked_classes.py --flat --flavour ele --ptMin 5  --ptMax 0   --trainingClasses noTraining --flatSample TTJets_Electrons_2016_noTraining
#python -i stacked_classes.py --flat --ptMin 10 --ptMax 0   --trainingClasses noTraining --flatSample TTs_Muons_2016_noTraining
#python -i stacked_classes.py --flat --ptMin 5  --ptMax 25  --trainingClasses noTraining --flatSample TTs_Muons_2016_noTraining
#python -i stacked_classes.py --flat --ptMin 10 --ptMax 25  --trainingClasses noTraining --flatSample TTs_Muons_2016_noTraining
#python -i stacked_classes.py --flat --ptMin 25 --ptMax 0   --trainingClasses noTraining --flatSample TTs_Muons_2016_noTraining

