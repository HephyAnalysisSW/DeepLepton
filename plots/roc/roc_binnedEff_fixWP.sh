#!/bin/sh

##Gird
#voms-proxy-init -voms cms -out ~/private/.proxy
#export X509_USER_PROXY=~/private/.proxy
#submitBatch.py --dpm launch_deepLepton_plots.sh

#######
#muons#
#######

#TESTDATA

#python -i roc_binnedEff_fixWP.py --small --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS 90 --binned pt

python -i roc_binnedEff_fixWP.py --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS 50 --binned pt
python -i roc_binnedEff_fixWP.py --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS 50 --binned eta
python -i roc_binnedEff_fixWP.py --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS 50 --binned nTrueInt

#TRAINDATA


