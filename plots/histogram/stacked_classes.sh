#!/bin/sh

#testData
python -i stacked_classes.py --flat --looseId --ptMin 10 --ptMax 0   --varSelection fullClasses --flatSample TTs_Muons_onTTs_2016 --testData 
python -i stacked_classes.py --flat --looseId --ptMin 10 --ptMax 25  --varSelection fullClasses --flatSample TTs_Muons_onTTs_2016 --testData 
python -i stacked_classes.py --flat --looseId --ptMin 25 --ptMax 0   --varSelection fullClasses --flatSample TTs_Muons_onTTs_2016 --testData 

#trainData
python -i stacked_classes.py --flat --looseId --ptMin 10 --ptMax 0   --varSelection fullClasses --flatSample TTs_Muons_onTTs_2016
python -i stacked_classes.py --flat --looseId --ptMin 10 --ptMax 25  --varSelection fullClasses --flatSample TTs_Muons_onTTs_2016
python -i stacked_classes.py --flat --looseId --ptMin 25 --ptMax 0   --varSelection fullClasses --flatSample TTs_Muons_onTTs_2016

python -i stacked_classes.py --flat --ptMin 5  --ptMax 0   --flatSample TTs_Muons_onTTs_2016
python -i stacked_classes.py --flat --ptMin 10 --ptMax 0   --flatSample TTs_Muons_onTTs_2016
python -i stacked_classes.py --flat --ptMin 10 --ptMax 25  --flatSample TTs_Muons_onTTs_2016
python -i stacked_classes.py --flat --ptMin 25 --ptMax 0   --flatSample TTs_Muons_onTTs_2016

#testData
python -i stacked_classes.py --flat --looseId --ptMin 10 --ptMax 0   --varSelection fullClasses --flatSample DYvsQCD_Muons_onDYvsQCD_2016 --testData 
python -i stacked_classes.py --flat --looseId --ptMin 10 --ptMax 25  --varSelection fullClasses --flatSample DYvsQCD_Muons_onDYvsQCD_2016 --testData 
python -i stacked_classes.py --flat --looseId --ptMin 25 --ptMax 0   --varSelection fullClasses --flatSample DYvsQCD_Muons_onDYvsQCD_2016 --testData 

#trainData
python -i stacked_classes.py --flat --looseId --ptMin 10 --ptMax 0   --varSelection fullClasses --flatSample DYvsQCD_Muons_onDYvsQCD_2016
python -i stacked_classes.py --flat --looseId --ptMin 10 --ptMax 25  --varSelection fullClasses --flatSample DYvsQCD_Muons_onDYvsQCD_2016
python -i stacked_classes.py --flat --looseId --ptMin 25 --ptMax 0   --varSelection fullClasses --flatSample DYvsQCD_Muons_onDYvsQCD_2016

python -i stacked_classes.py --flat --ptMin 5  --ptMax 0   --flatSample DYvsQCD_Muons_onDYvsQCD_2016
python -i stacked_classes.py --flat --ptMin 10 --ptMax 0   --flatSample DYvsQCD_Muons_onDYvsQCD_2016
python -i stacked_classes.py --flat --ptMin 10 --ptMax 25  --flatSample DYvsQCD_Muons_onDYvsQCD_2016
python -i stacked_classes.py --flat --ptMin 25 --ptMax 0   --flatSample DYvsQCD_Muons_onDYvsQCD_2016

