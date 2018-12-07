#!/bin/sh


##########
# TTJets #
##########

###full events
#python -i roc.py --ptMin 10  --ptMax 25  --testData --medium
#python -i roc.py --ptMin 25  --ptMax 0   --testData --medium
#python -i roc.py --ptMin 5 --ptMax 0  --testData --testFile --lumi_weight 0

#flat samples

python -i roc.py --flat --ptMin 5  --ptMax 0   --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight 
python -i roc.py --flat --ptMin 25 --ptMax 0   --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight 
python -i roc.py --flat --ptMin 5  --ptMax 25  --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight
python -i roc.py --flat --ptMin 10 --ptMax 25  --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight
python -i roc.py --flat --ptMin 10 --ptMax 0   --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight 
python -i roc.py --flat --ptMin 10 --ptMax 250   --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight 

python -i roc.py --flat --ptMin 5  --ptMax 0   --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight 
python -i roc.py --flat --ptMin 25 --ptMax 0   --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight 
python -i roc.py --flat --ptMin 5  --ptMax 25  --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight
python -i roc.py --flat --ptMin 10 --ptMax 25  --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight
python -i roc.py --flat --ptMin 10 --ptMax 0   --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight 

#python -i roc.py --flat --ptMin 5 --ptMax 0  --testData --flatSample testFile --lumi_weight 0

#testData
#python -i roc.py --flat --ptMin 5  --ptMax 10  --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 10 --ptMax 15  --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 15 --ptMax 20  --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 20 --ptMax 25  --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 5  --ptMax 0   --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 25 --ptMax 0   --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 10 --ptMax 0   --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 10 --ptMax 25  --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 15 --ptMax 25  --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 5  --ptMax 25  --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 5  --ptMax 15  --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016

#python -i roc.py --flat --ptMin 5  --ptMax 10 --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 10 --ptMax 15 --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 15 --ptMax 20 --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 20 --ptMax 25 --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 5  --ptMax 0  --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 25 --ptMax 0  --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 10 --ptMax 0  --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 10 --ptMax 25 --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 15 --ptMax 25 --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 5  --ptMax 25 --flatSample TTs_Muons_balanced_test_pt5toInf_2016
#python -i roc.py --flat --ptMin 5  --ptMax 15 --flatSample TTs_Muons_balanced_test_pt5toInf_2016

##trainData
#python roc.py --flat --ptMin 5  --ptMax 10 --flatSample TTJets_Muons_balanced_pt5toInf_2016
#python roc.py --flat --ptMin 10 --ptMax 15 --flatSample TTJets_Muons_balanced_pt5toInf_2016
#python roc.py --flat --ptMin 15 --ptMax 20 --flatSample TTJets_Muons_balanced_pt5toInf_2016
#python roc.py --flat --ptMin 20 --ptMax 25 --flatSample TTJets_Muons_balanced_pt5toInf_2016
#python roc.py --flat --ptMin 5  --ptMax 0  --flatSample TTJets_Muons_balanced_pt5toInf_2016
#python roc.py --flat --ptMin 25 --ptMax 0  --flatSample TTJets_Muons_balanced_pt5toInf_2016


###########
# DYvsQCD #
###########

#python roc.py --flat --ptMin 15  --ptMax 0   --testData --flatSample DYvsQCD_Muons_balanced_2016
#python roc.py --flat --ptMin 15  --ptMax 0   --testData --flatSample DYvsQCD_Muons_balanced_2016 --lumi_weight 0

