#!/bin/sh

eval `scramv1 runtime -sh`

python step1_select.py  --version v0 --small --year 2017 --flavour muo --logLevel INFO --ptSelection pt_3.5_-1 --displaced --sample CompSUSY
