#!/bin/sh

###################
### full events ###
###################
#python -i roc.py --ptMin 10  --ptMax 25  --testData --medium
#python -i roc.py --ptMin 25  --ptMax 0   --testData --medium
#python -i roc.py --ptMin 5 --ptMax 0  --testData --testFile --lumi_weight 0

####################
### flat samples ###
####################

python -i roc.py --flat --ptMin 5  --ptMax 0   --testData --flatSample TTs_Muons_globalVarsOnly_2016 --lumi_weight 
python -i roc.py --flat --ptMin 25 --ptMax 0   --testData --flatSample TTs_Muons_globalVarsOnly_2016 --lumi_weight 
python -i roc.py --flat --ptMin 5  --ptMax 25  --testData --flatSample TTs_Muons_globalVarsOnly_2016 --lumi_weight
python -i roc.py --flat --ptMin 10 --ptMax 25  --testData --flatSample TTs_Muons_globalVarsOnly_2016 --lumi_weight
python -i roc.py --flat --ptMin 10 --ptMax 0   --testData --flatSample TTs_Muons_globalVarsOnly_2016 --lumi_weight 
python -i roc.py --flat --ptMin 10 --ptMax 250 --testData --flatSample TTs_Muons_globalVarsOnly_2016 --lumi_weight 

python -i roc.py --flat --ptMin 5  --ptMax 0   --flatSample TTs_Muons_globalVarsOnly_2016 --lumi_weight 
python -i roc.py --flat --ptMin 25 --ptMax 0   --flatSample TTs_Muons_globalVarsOnly_2016 --lumi_weight 
python -i roc.py --flat --ptMin 5  --ptMax 25  --flatSample TTs_Muons_globalVarsOnly_2016 --lumi_weight
python -i roc.py --flat --ptMin 10 --ptMax 25  --flatSample TTs_Muons_globalVarsOnly_2016 --lumi_weight
python -i roc.py --flat --ptMin 10 --ptMax 0   --flatSample TTs_Muons_globalVarsOnly_2016 --lumi_weight 




#python -i roc.py --flat --ptMin 5 --ptMax 0  --testData --flatSample testFile --lumi_weight 0

