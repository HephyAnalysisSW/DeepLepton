#!/bin/sh

###################
### full events ###
###################
#python -i roc.py --ptMin 10  --ptMax 25  --testData --medium
#python -i roc.py --ptMin 25  --ptMax 0   --testData --medium
#python -i roc.py --ptMin 5 --ptMax 0  --testData --testFile --lumi_weight 0

####################
### flat samples ###
####################

#python -i roc.py --flat --ptMin 5  --ptMax 0   --flatSample TTs_Muons_noCNN_2016 --lumi_weight --testData 
#python -i roc.py --flat --ptMin 25 --ptMax 0   --flatSample TTs_Muons_noCNN_2016 --lumi_weight --testData 
#python -i roc.py --flat --ptMin 5  --ptMax 25  --flatSample TTs_Muons_noCNN_2016 --lumi_weight --testData 
#python -i roc.py --flat --ptMin 10 --ptMax 25  --flatSample TTs_Muons_noCNN_2016 --lumi_weight --testData 
#python -i roc.py --flat --ptMin 10 --ptMax 0   --flatSample TTs_Muons_noCNN_2016 --lumi_weight --testData 
#python -i roc.py --flat --ptMin 10 --ptMax 250 --flatSample TTs_Muons_noCNN_2016 --lumi_weight --testData 
#
#python -i roc.py --flat --ptMin 5  --ptMax 0   --flatSample TTs_Muons_noCNN_2016 --lumi_weight 
#python -i roc.py --flat --ptMin 25 --ptMax 0   --flatSample TTs_Muons_noCNN_2016 --lumi_weight 
#python -i roc.py --flat --ptMin 5  --ptMax 25  --flatSample TTs_Muons_noCNN_2016 --lumi_weight
#python -i roc.py --flat --ptMin 10 --ptMax 25  --flatSample TTs_Muons_noCNN_2016 --lumi_weight
#python -i roc.py --flat --ptMin 10 --ptMax 0   --flatSample TTs_Muons_noCNN_2016 --lumi_weight 


#python -i roc.py --flat --small --ptMin 25 --ptMax 0   --flatSample uons_biLSTM_split_2016 --lumi_weight --testData 


#python -i roc.py --flat --ptMin 5 --ptMax 0  --testData --flatSample testFile --lumi_weight 0


#################
### electrons ###
#################

python -i roc.py --flat --ptMin 7  --ptMax 0   --flatSample TTJets_Electrons_2016_biLSTM_split --flavour ele  --lumi_weight --testData

python -i roc.py --flat --ptMin 7  --ptMax 25   --flatSample TTJets_Electrons_2016_biLSTM_split --flavour ele  --lumi_weight --testData

python -i roc.py --flat --ptMin 25  --ptMax 0   --flatSample TTJets_Electrons_2016_biLSTM_split --flavour ele  --lumi_weight --testData

python -i roc.py --flat --ptMin 12  --ptMax 25   --flatSample TTJets_Electrons_2016_biLSTM_split --flavour ele  --lumi_weight --testData
