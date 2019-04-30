#!/bin/sh

#PF and SV sorting + isClassId_Training branches

##TTJets
#python -i step3.py --version v6 --output_version v2 --year 2016 --flavour muo --ptSelection pt_5_-1   --sampleSelection TTJets  #SPLIT20
#python -i step3.py --version v6 --output_version v2 --year 2016 --flavour muo --ptSelection pt_5_15   --sampleSelection TTJets  #SPLIT10
#python -i step3.py --version v6 --output_version v2 --year 2016 --flavour muo --ptSelection pt_15_25  --sampleSelection TTJets  #SPLIT10
#python -i step3.py --version v6 --output_version v2 --year 2016 --flavour muo --ptSelection pt_25_-1  --sampleSelection TTJets  #SPLIT10

#python -i step3.py --version v6 --output_version v2 --year 2016 --flavour muo --ptSelection pt_5_-1   --sampleSelection TTJets --nJobs 20 --job 0 
#python -i step3.py --version v6 --output_version v2 --year 2016 --flavour muo --ptSelection pt_5_15   --sampleSelection TTJets --nJobs 10 --job 0 
#python -i step3.py --version v6 --output_version v2 --year 2016 --flavour muo --ptSelection pt_15_25  --sampleSelection TTJets --nJobs 10 --job 0 
#python -i step3.py --version v6 --output_version v2 --year 2016 --flavour muo --ptSelection pt_25_-1  --sampleSelection TTJets --nJobs 10 --job 0 

#TTs
#python -i step3.py --version v6 --output_version v2 --year 2016 --flavour muo --ptSelection pt_5_-1   --sampleSelection TTs  #SPLIT54
#python -i step3.py --version v6 --output_version v2 --year 2016 --flavour muo --ptSelection pt_5_-1   --sampleSelection TTs_test  #SPLIT32

#test01 simon
#python -i step3.py --version v1_--output_version v2 small_simon --year 2016 --flavour ele --ptSelection pt_5_-1   --sampleSelection TTJets  #SPLIT137

#test02 simon
#python -i step3.py --version v1 --output_version v2 --year 2016 --flavour ele --ptSelection pt_5_-1   --sampleSelection TTJets  #SPLIT137

##DYvsQCD
#python -i step3.py --version v6 --output_version v2 --year 2016 --flavour muo --ptSelection pt_5_-1   --sampleSelection DYvsQCD  #SPLIT137
#
##AllSamples
#python -i step3.py --version v6 --output_version v2 --year 2016 --flavour muo --ptSelection pt_5_-1   --sampleSelection all  #SPLIT75

#2017
#python -i step3.py --version v1 --output_version v4 --year 2017 --flavour muo --ptSelection pt_5_-1   --sampleSelection TTJets  #SPLIT360
python -i step3.py --version v1  --output_version v4 --year 2017 --flavour ele --ptSelection pt_5_-1 --sampleSelection TTJets  #SPLIT1895

#Test
#python -i step3.py --version v1 --output_version v2 --year 2017 --flavour ele --ptSelection pt_5_-1   --sampleSelection TTs_test  #SPLIT1
