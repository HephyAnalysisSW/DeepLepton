#!/bin/sh

#PF and SV sorting + isClassId_Training branches

##TTJets
#python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_5_-1   --sampleSelection TTJets  #SPLIT20
#python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_5_15   --sampleSelection TTJets  #SPLIT10
#python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_15_25  --sampleSelection TTJets  #SPLIT10
#python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_25_-1  --sampleSelection TTJets  #SPLIT10

#python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_5_-1   --sampleSelection TTJets --nJobs 20 --job 0 
#python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_5_15   --sampleSelection TTJets --nJobs 10 --job 0 
#python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_15_25  --sampleSelection TTJets --nJobs 10 --job 0 
#python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_25_-1  --sampleSelection TTJets --nJobs 10 --job 0 

#TTs
#python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_5_-1   --sampleSelection TTs  #SPLIT54
#python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_5_-1   --sampleSelection TTs_test  #SPLIT32

#test simon
python -i step3.py --version v1_small_simon --year 2016 --flavour ele --ptSelection pt_5_-1   --sampleSelection TTJets  #SPLIT137

##DYvsQCD
#python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_5_-1   --sampleSelection DYvsQCD  #SPLIT137
#
##AllSamples
#python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_5_-1   --sampleSelection all  #SPLIT75


