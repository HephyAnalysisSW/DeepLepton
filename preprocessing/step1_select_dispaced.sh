#!/bin/sh

eval `scramv1 runtime -sh`

python step1_select.py  --version v3d --year 2017 --flavour muo --logLevel INFO --ptSelection pt_3.5_-1 --displaced --sample CompSUSY
python step1_select.py  --version v3d --year 2017 --flavour ele --logLevel INFO --ptSelection pt_3.5_-1 --displaced --sample CompSUSY
