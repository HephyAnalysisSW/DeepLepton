#!/bin/sh

#testData

python -i roc_coloredDiscVal.py --flat --ptMin 10  --ptMax 25  --testData 1 --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --roc deepLepton
python -i roc_coloredDiscVal.py --flat --ptMin 10  --ptMax 25  --testData 1 --flatSample TTs_Muons_biLSTM_splitDense_elu_2016 --roc mvaTTV

python -i roc_coloredDiscVal.py --flat --ptMin 10  --ptMax 25  --testData 1 --flatSample TTs_Muons_biLSTM_splitDense_elu_prompt_2016 --roc deepLepton



