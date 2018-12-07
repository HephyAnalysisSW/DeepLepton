#!/bin/sh

##Gird
#voms-proxy-init -voms cms -out ~/private/.proxy
#export X509_USER_PROXY=~/private/.proxy
#submitBatch.py --dpm launch_deepLepton_plots.sh

#######
#muons#
#######

#TESTDATA

#python roc_binnedEff_fixWP.py --small --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS_TTV 90 --eS_DL 95 --binned pt
#python roc_binnedEff_fixWP.py --small --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned eta
#python roc_binnedEff_fixWP.py --small --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned nTrueInt

#python roc_binnedEff_fixWP.py --small --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned low_pt
#python roc_binnedEff_fixWP.py --small --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned high_pt

python -i roc_binnedEff_fixWP.py --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS_TTV 95 --eS_DL 95 --binned high_pt
python -i roc_binnedEff_fixWP.py --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned high_pt
python -i roc_binnedEff_fixWP.py --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS_TTV 85 --eS_DL 85 --binned high_pt
python -i roc_binnedEff_fixWP.py --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS_TTV 80 --eS_DL 80 --binned high_pt

python -i roc_binnedEff_fixWP.py --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS_TTV 95 --eS_DL 95 --binned low_pt
python -i roc_binnedEff_fixWP.py --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned low_pt
python -i roc_binnedEff_fixWP.py --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS_TTV 85 --eS_DL 85 --binned low_pt
python -i roc_binnedEff_fixWP.py --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS_TTV 80 --eS_DL 80 --binned low_pt

#python -i roc_binnedEff_fixWP.py --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS_TTV 90 --eS_DL 85 --binned pt
#python -i roc_binnedEff_fixWP.py --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS_TTV 90 --eS_DL 80 --binned pt
#python -i roc_binnedEff_fixWP.py --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS_TTV 90 --eS_DL 75 --binned pt
#python -i roc_binnedEff_fixWP.py --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS_TTV 90 --eS_DL 70 --binned pt

#python -i roc_binnedEff_fixWP.py --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned eta
#python -i roc_binnedEff_fixWP.py --flat --ptMin 10 --ptMax 0 --testData --flatSample TTs_Muons_balanced_test_pt5toInf_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned nTrueInt

#TRAINDATA


