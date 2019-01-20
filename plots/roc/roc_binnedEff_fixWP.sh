#!/bin/sh

##Gird
#voms-proxy-init -voms cms -out ~/private/.proxy
#export X509_USER_PROXY=~/private/.proxy
#submitBatch.py --dpm launch_deepLepton_plots.sh

#######
#muons#
#######

#python -i roc_binnedEff_fixWP.py --flat --small --testData --flatSample TTs_Muons_biLSTM_split_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned eta

#TESTDATA
python -i roc_binnedEff_fixWP.py --flat --testData --flatSample TTs_Muons_globalVarsOnly_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned high_pt
python -i roc_binnedEff_fixWP.py --flat --testData --flatSample TTs_Muons_globalVarsOnly_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned low_pt
python -i roc_binnedEff_fixWP.py --flat --testData --flatSample TTs_Muons_globalVarsOnly_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned pt

python -i roc_binnedEff_fixWP.py --flat --testData --flatSample TTs_Muons_globalVarsOnly_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned eta
python -i roc_binnedEff_fixWP.py --flat --testData --flatSample TTs_Muons_globalVarsOnly_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned nTrueInt

#TRAINDATA


