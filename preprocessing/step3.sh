#!/bin/sh

#PF and SV sorting + isClassId_Training branches
#python -i step3.py --version v4 --year 2016 --flavour muo --ptSelection pt_15_-1 --sampleSelection DYvsQCD --nJobs 100 --job 0
#python -i step3.py --version v4 --year 2016 --flavour muo --ptSelection pt_15_-1 --sampleSelection TTJets  --nJobs 50  --job 0

#python -i step3.py --version v4 --year 2016 --flavour muo --ptSelection pt_15_-1 --sampleSelection DYvsQCD #SPLIT20
#python -i step3.py --version v4 --year 2016 --flavour muo --ptSelection pt_15_-1 --sampleSelection TTJets #SPLIT10

#python -i step3.py --version v5 --year 2016 --flavour muo --ptSelection pt_15_-1 --sampleSelection DYvsQCD #SPLIT20
#python -i step3.py --version v5 --year 2016 --flavour muo --ptSelection pt_5_15  --sampleSelection TTJets  #SPLIT10

python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_5_-1   --sampleSelection TTJets  #SPLIT20
python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_5_15   --sampleSelection TTJets  #SPLIT10
python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_15_25  --sampleSelection TTJets  #SPLIT10
python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_25_-1  --sampleSelection TTJets  #SPLIT10

#python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_5_-1   --sampleSelection TTJets --nJobs 20 --job 0 
#python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_5_15   --sampleSelection TTJets --nJobs 10 --job 0 
#python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_15_25  --sampleSelection TTJets --nJobs 10 --job 0 
#python -i step3.py --version v6 --year 2016 --flavour muo --ptSelection pt_25_-1  --sampleSelection TTJets --nJobs 10 --job 0 

