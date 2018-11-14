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
python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_5_-1   --sampleSelection TTs  #SPLIT20
python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_5_15   --sampleSelection TTs  #SPLIT10
python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_15_25  --sampleSelection TTs  #SPLIT10
python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_25_-1  --sampleSelection TTs  #SPLIT10

