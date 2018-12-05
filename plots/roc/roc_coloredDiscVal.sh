#!/bin/sh


##########
# TTJets #
##########

#testData
#python -i roc_coloredDiscVal.py --small --flat --ptMin 5  --ptMax 10  --testData 1 --flatSample TTs_Muons_balanced_test_pt5toInf_2016
python -i roc_coloredDiscVal.py --small --flat --ptMin 5  --ptMax 25  --testData 1 --flatSample TTs_Muons_balanced_test_pt5toInf_2016

##trainData
#python -i roc_coloredDiscVal.py --flat --ptMin 5  --ptMax 25  --testData 0 --flatSample TTJets_Muons_balanced_pt5toInf_2016


###########
# DYvsQCD #
###########

#python roc_coloredDiscVal.py --flat --ptMin 15  --ptMax 0   --testData 1 --flatSample DYvsQCD_Muons_balanced_2016
#python roc_coloredDiscVal.py --flat --ptMin 15  --ptMax 0   --testData 1 --flatSample DYvsQCD_Muons_balanced_2016 --lumi_weight 0

