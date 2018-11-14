#!/bin/sh

#testData
python -i stacked_classes.py --flat --ptMin 5  --ptMax 0   --testData 1 --flatSample TTJets_Muons_balanced_pt5toInf_2016

python -i stacked_classes.py --flat --ptMin 5  --ptMax 15  --testData 1 --flatSample TTJets_Muons_balanced_pt5toInf_2016
python -i stacked_classes.py --flat --ptMin 5  --ptMax 15  --testData 1 --flatSample TTJets_Muons_balanced_pt5to15_2016

python -i stacked_classes.py --flat --ptMin 15 --ptMax 25  --testData 1 --flatSample TTJets_Muons_balanced_pt5toInf_2016
python -i stacked_classes.py --flat --ptMin 15 --ptMax 25  --testData 1 --flatSample TTJets_Muons_balanced_pt15to25_2016

python -i stacked_classes.py --flat --ptMin 25 --ptMax 0   --testData 1 --flatSample TTJets_Muons_balanced_pt5toInf_2016
python -i stacked_classes.py --flat --ptMin 25 --ptMax 0   --testData 1 --flatSample TTJets_Muons_balanced_pt25toInf_2016

#trainData
python -i stacked_classes.py --flat --ptMin 5  --ptMax 0   --testData 0 --flatSample TTJets_Muons_balanced_pt5toInf_2016

python -i stacked_classes.py --flat --ptMin 5  --ptMax 15  --testData 0 --flatSample TTJets_Muons_balanced_pt5toInf_2016
python -i stacked_classes.py --flat --ptMin 5  --ptMax 15  --testData 0 --flatSample TTJets_Muons_balanced_pt5to15_2016

python -i stacked_classes.py --flat --ptMin 15 --ptMax 25  --testData 0 --flatSample TTJets_Muons_balanced_pt5toInf_2016
python -i stacked_classes.py --flat --ptMin 15 --ptMax 25  --testData 0 --flatSample TTJets_Muons_balanced_pt15to25_2016

python -i stacked_classes.py --flat --ptMin 25 --ptMax 0   --testData 0 --flatSample TTJets_Muons_balanced_pt5toInf_2016
python -i stacked_classes.py --flat --ptMin 25 --ptMax 0   --testData 0 --flatSample TTJets_Muons_balanced_pt25toInf_2016



