#!/bin/sh

#Muon ROC plots for DA

###########
#ROC plots#
###########
#python roc_DAgm.py --small --flat --ptMin 25 --ptMax 0   --flatSample TTs_Muons_biLSTM_splitDense_elu_simpleClasses_2016 --lumi_weight --testData

#best
#test data
python roc_DAgm.py --flat --ptMin 5  --ptMax 0   --refTraining initial_deepLepton --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --lumi_weight --testData --name final
python roc_DAgm.py --flat --ptMin 25 --ptMax 0   --refTraining initial_deepLepton --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --lumi_weight --testData --name final
python roc_DAgm.py --flat --ptMin 5  --ptMax 25  --refTraining initial_deepLepton --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --lumi_weight --testData --name final
python roc_DAgm.py --flat --ptMin 10 --ptMax 25  --refTraining initial_deepLepton --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --lumi_weight --testData --name final
python roc_DAgm.py --flat --ptMin 10 --ptMax 0   --refTraining initial_deepLepton --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --lumi_weight --testData --name final
#train data
python roc_DAgm.py --flat --ptMin 5  --ptMax 0   --refTraining initial_deepLepton --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --lumi_weight --name final
python roc_DAgm.py --flat --ptMin 25 --ptMax 0   --refTraining initial_deepLepton --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --lumi_weight --name final
python roc_DAgm.py --flat --ptMin 5  --ptMax 25  --refTraining initial_deepLepton --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --lumi_weight --name final
python roc_DAgm.py --flat --ptMin 10 --ptMax 25  --refTraining initial_deepLepton --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --lumi_weight --name final
python roc_DAgm.py --flat --ptMin 10 --ptMax 0   --refTraining initial_deepLepton --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --lumi_weight --name final
#standard
#test data
python roc_DAgm.py --flat --ptMin 5  --ptMax 0   --flatSample TTs_Muons_2016 --lumi_weight --testData --name initial
python roc_DAgm.py --flat --ptMin 25 --ptMax 0   --flatSample TTs_Muons_2016 --lumi_weight --testData --name initial
python roc_DAgm.py --flat --ptMin 5  --ptMax 25  --flatSample TTs_Muons_2016 --lumi_weight --testData --name initial
python roc_DAgm.py --flat --ptMin 10 --ptMax 25  --flatSample TTs_Muons_2016 --lumi_weight --testData --name initial
python roc_DAgm.py --flat --ptMin 10 --ptMax 0   --flatSample TTs_Muons_2016 --lumi_weight --testData --name initial
#train data
python roc_DAgm.py --flat --ptMin 5  --ptMax 0   --flatSample TTs_Muons_2016 --lumi_weight --name initial
python roc_DAgm.py --flat --ptMin 25 --ptMax 0   --flatSample TTs_Muons_2016 --lumi_weight --name initial
python roc_DAgm.py --flat --ptMin 5  --ptMax 25  --flatSample TTs_Muons_2016 --lumi_weight --name initial
python roc_DAgm.py --flat --ptMin 10 --ptMax 25  --flatSample TTs_Muons_2016 --lumi_weight --name initial
python roc_DAgm.py --flat --ptMin 10 --ptMax 0   --flatSample TTs_Muons_2016 --lumi_weight --name initial

#various tests
python roc_DAgm.py --flat --ptMin 25 --ptMax 0   --refTraining initial_deepLepton --flatSample TTs_Muons_biLSTM_2016 --lumi_weight --testData --name biLSTM
python roc_DAgm.py --flat --ptMin 10 --ptMax 25  --refTraining initial_deepLepton --flatSample TTs_Muons_biLSTM_2016 --lumi_weight --testData --name biLSTM
python roc_DAgm.py --flat --ptMin 25 --ptMax 0   --refTraining initial_deepLepton --flatSample TTs_Muons_splitDense_2016 --lumi_weight --testData --name split
python roc_DAgm.py --flat --ptMin 10 --ptMax 25  --refTraining initial_deepLepton --flatSample TTs_Muons_splitDense_2016 --lumi_weight --testData --name split
python roc_DAgm.py --flat --ptMin 25 --ptMax 0   --refTraining initial_deepLepton --flatSample TTs_Muons_noCNN_2016 --lumi_weight --testData --name noCNN
python roc_DAgm.py --flat --ptMin 10 --ptMax 25  --refTraining initial_deepLepton --flatSample TTs_Muons_noCNN_2016 --lumi_weight --testData --name noCNN
python roc_DAgm.py --flat --ptMin 25 --ptMax 0   --refTraining initial_deepLepton --flatSample TTs_Muons_pooling_2016 --lumi_weight --testData --name pooling
python roc_DAgm.py --flat --ptMin 10 --ptMax 25  --refTraining initial_deepLepton --flatSample TTs_Muons_pooling_2016 --lumi_weight --testData --name pooling
python roc_DAgm.py --flat --ptMin 25 --ptMax 0   --refTraining initial_deepLepton --flatSample TTs_Muons_globalVarsOnly_2016 --lumi_weight --testData --name LEPvars
python roc_DAgm.py --flat --ptMin 10 --ptMax 25  --refTraining initial_deepLepton --flatSample TTs_Muons_globalVarsOnly_2016 --lumi_weight --testData --name LEPvars
python roc_DAgm.py --flat --ptMin 25 --ptMax 0   --refTraining initial_deepLepton --flatSample TTs_Muons_TTVonly_2016 --lumi_weight --testData --name TTVvars
python roc_DAgm.py --flat --ptMin 10 --ptMax 25  --refTraining initial_deepLepton --flatSample TTs_Muons_TTVonly_2016 --lumi_weight --testData --name TTVvars

python roc_DAgm.py --flat --ptMin 25 --ptMax 0   --refTraining final_deepLepton   --flatSample TTs_Muons_biLSTM_splitDense_elu_prompt_2016 --lumi_weight --testData --name prompt
python roc_DAgm.py --flat --ptMin 10 --ptMax 25  --refTraining final_deepLepton   --flatSample TTs_Muons_biLSTM_splitDense_elu_prompt_2016 --lumi_weight --testData --name prompt
python roc_DAgm.py --flat --ptMin 25 --ptMax 0   --refTraining final_deepLepton   --flatSample TTs_Muons_biLSTM_splitDense_elu_simpleClasses_2016 --lumi_weight --testData --name 2output
python roc_DAgm.py --flat --ptMin 10 --ptMax 25  --refTraining final_deepLepton   --flatSample TTs_Muons_biLSTM_splitDense_elu_simpleClasses_2016 --lumi_weight --testData --name 2output
python roc_DAgm.py --flat --ptMin 25 --ptMax 0   --refTraining final_deepLepton   --flatSample TTs_Muons_biLSTM_splitDense_2016 --lumi_weight --testData --name RELU
python roc_DAgm.py --flat --ptMin 10 --ptMax 25  --refTraining final_deepLepton   --flatSample TTs_Muons_biLSTM_splitDense_2016 --lumi_weight --testData --name RELU
python roc_DAgm.py --flat --ptMin 25 --ptMax 0   --refTraining final_deepLepton   --flatSample TTs_Muons_biLSTM_splitDense_selu_2016 --lumi_weight --testData --name SELU
python roc_DAgm.py --flat --ptMin 10 --ptMax 25  --refTraining final_deepLepton   --flatSample TTs_Muons_biLSTM_splitDense_selu_2016 --lumi_weight --testData --name SELU


#####################
#binned efficiencies#
#####################

##TESTDATA
##small
##python roc_binnedEff_DAgm.py --flat --small --testData --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned low_pt
##best
#python roc_binnedEff_DAgm.py --flat --testData --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned high_pt
#python roc_binnedEff_DAgm.py --flat --testData --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned low_pt
#python roc_binnedEff_DAgm.py --flat --testData --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned pt
#python roc_binnedEff_DAgm.py --flat --testData --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned eta
#python roc_binnedEff_DAgm.py --flat --testData --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned nTrueInt
##standard
#python roc_binnedEff_DAgm.py --flat --testData --flatSample TTs_Muons_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned high_pt
#python roc_binnedEff_DAgm.py --flat --testData --flatSample TTs_Muons_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned low_pt
#python roc_binnedEff_DAgm.py --flat --testData --flatSample TTs_Muons_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned pt
#python roc_binnedEff_DAgm.py --flat --testData --flatSample TTs_Muons_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned eta
#python roc_binnedEff_DAgm.py --flat --testData --flatSample TTs_Muons_2016 --lumi_weight --eS_TTV 90 --eS_DL 90 --binned nTrueInt


