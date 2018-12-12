#!/bin/sh

#testData
#python -i roc_coloredDiscVal.py --small --flat --ptMin 5  --ptMax 25  --testData 1 --flatSample TTs_Muons_2016

python -i roc_coloredDiscVal.py --small --flat --ptMin 5  --ptMax 25  --testData 1 --flatSample TTs_Muons_2016
python -i roc_coloredDiscVal.py --small --flat --ptMin 5  --ptMax 25  --testData 1 --flatSample TTs_Muons_splitDense_2016
python -i roc_coloredDiscVal.py --small --flat --ptMin 5  --ptMax 25  --testData 1 --flatSample TTs_Muons_simpleClasses_2016
python -i roc_coloredDiscVal.py --small --flat --ptMin 5  --ptMax 25  --testData 1 --flatSample TTs_Muons_globalVarsOnly_2016


