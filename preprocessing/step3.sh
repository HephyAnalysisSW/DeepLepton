#!/bin/sh

#PF and SV sorting + isClassId_Training branches
#python -i step3.py --version v2 --year 2016 --flavour muo --ptSelection pt_15_to_inf --sampleSelection DYvsQCD --nJobs 151 --job 0
#python -i step3.py --version v2 --year 2016 --flavour muo --ptSelection pt_15_to_inf --sampleSelection DYvsQCD #SPLIT151

#python -i step3.py --version v3_small --year 2016 --flavour muo --ptSelection pt_15_to_inf --sampleSelection DYvsQCD #SPLIT1
#python -i step3.py --version v3_small --year 2016 --flavour muo --ptSelection pt_15_to_inf --sampleSelection TTJets #SPLIT1

#python -i step3.py --version v3 --year 2016 --flavour muo --ptSelection pt_15_to_inf --sampleSelection TTJets #SPLIT100
python -i step3.py --version v3 --year 2016 --flavour muo --ptSelection pt_15_to_inf --sampleSelection DYvsQCD #SPLIT100
