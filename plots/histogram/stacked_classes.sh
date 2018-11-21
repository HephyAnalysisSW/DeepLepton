#!/bin/sh

#testData
#python -i stacked_classes.py --flat --ptMin 5  --ptMax 0   --testData 1 --flatSample TTs_Muons_balanced_pt5toInf_2016
#python -i stacked_classes.py --flat --ptMin 5  --ptMax 15  --testData 1 --flatSample TTs_Muons_balanced_pt5toInf_2016
#python -i stacked_classes.py --flat --ptMin 15 --ptMax 25  --testData 1 --flatSample TTs_Muons_balanced_pt5toInf_2016
#python -i stacked_classes.py --flat --ptMin 25 --ptMax 0   --testData 1 --flatSample TTs_Muons_balanced_pt5toInf_2016
#python -i stacked_classes.py --flat --ptMin 10 --ptMax 0   --testData 1 --flatSample TTs_Muons_balanced_pt5toInf_2016
#python -i stacked_classes.py --flat --ptMin 10 --ptMax 15  --testData 1 --flatSample TTs_Muons_balanced_pt5toInf_2016
python -i stacked_classes.py --flat --ptMin 10 --ptMax 25  --testData 1 --flatSample TTs_Muons_balanced_pt5toInf_2016
python -i stacked_classes.py --flat --ptMin 15 --ptMax 25  --testData 1 --flatSample TTs_Muons_balanced_pt5toInf_2016
python -i stacked_classes.py --flat --ptMin 5  --ptMax 25  --testData 1 --flatSample TTs_Muons_balanced_pt5toInf_2016

#trainData
#python -i stacked_classes.py --flat --ptMin 5  --ptMax 0   --testData 0 --flatSample TTs_Muons_balanced_pt5toInf_2016
#python -i stacked_classes.py --flat --ptMin 5  --ptMax 15  --testData 0 --flatSample TTs_Muons_balanced_pt5toInf_2016
#python -i stacked_classes.py --flat --ptMin 15 --ptMax 25  --testData 0 --flatSample TTs_Muons_balanced_pt5toInf_2016
#python -i stacked_classes.py --flat --ptMin 25 --ptMax 0   --testData 0 --flatSample TTs_Muons_balanced_pt5toInf_2016
#python -i stacked_classes.py --flat --ptMin 10 --ptMax 0   --testData 0 --flatSample TTs_Muons_balanced_pt5toInf_2016
#python -i stacked_classes.py --flat --ptMin 10 --ptMax 15  --testData 0 --flatSample TTs_Muons_balanced_pt5toInf_2016
python -i stacked_classes.py --flat --ptMin 10 --ptMax 25  --testData 0 --flatSample TTs_Muons_balanced_pt5toInf_2016
python -i stacked_classes.py --flat --ptMin 15 --ptMax 25  --testData 0 --flatSample TTs_Muons_balanced_pt5toInf_2016
python -i stacked_classes.py --flat --ptMin 5  --ptMax 25  --testData 0 --flatSample TTs_Muons_balanced_pt5toInf_2016



#python stacked_classes.py --flat --ptMin 15 --ptMax 0    --testData 1 --flatSample DYvsQCD_Muons_balanced_2016
#python stacked_classes.py --flat --ptMin 15 --ptMax 25   --testData 1 --flatSample DYvsQCD_Muons_balanced_2016
#python stacked_classes.py --flat --ptMin 25 --ptMax 0    --testData 1 --flatSample DYvsQCD_Muons_balanced_2016


