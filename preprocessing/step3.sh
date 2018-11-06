#!/bin/sh

#PF and SV sorting + isClassId_Training branches
#python -i step3.py --version v2 --year 2016 --flavour muo --ptSelection pt_10_-1 --sampleSelection DYvsQCD --nJobs 151 --job 0
#python -i step3.py --version v2 --year 2016 --flavour muo --ptSelection pt_10_-1 --sampleSelection DYvsQCD #SPLIT151

#python -i step3.py --version v3_small --year 2016 --flavour muo --ptSelection pt_10_-1 --sampleSelection DYvsQCD #SPLIT1
#python -i step3.py --version v3_small --year 2016 --flavour muo --ptSelection pt_10_-1 --sampleSelection TTJets #SPLIT1

#python -i step3.py --version v3 --year 2016 --flavour muo --ptSelection pt_10_-1 --sampleSelection TTJets #SPLIT100
python -i step3.py --version v3 --year 2016 --flavour muo --ptSelection pt_10_-1 --sampleSelection DYvsQCD #SPLIT100
