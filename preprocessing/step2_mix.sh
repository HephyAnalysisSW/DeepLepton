#####################
# trainings samples #
#####################

#before submitting get grid certificate:
#voms-proxy-init -voms cms -out ~/private/.proxy
#export X509_USER_PROXY=~/private/.proxy

#submit jobs to batch:
#submitBatch.py --dpm step2_mix.sh

#job status:
#squeue|grep gmoertl

#single jobs

#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection TTJets  --ptSelection pt_5_-1  --nJobs 100 --job 0 
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection TTJets  --ptSelection pt_5_15  --nJobs 50 --job 0 
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection TTJets  --ptSelection pt_15_25 --nJobs 50 --job 0 
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection TTJets  --ptSelection pt_25_-1 --nJobs 50 --job 0 


#full version

#QCD
#python -i step2_mix.py --version v5 --year 2016 --flavour muo --ratio balanced --sampleSelection DYvsQCD --ptSelection pt_15_-1 #SPLIT100

##TTJets
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection TTJets  --ptSelection pt_5_-1   #SPLIT100
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection TTJets  --ptSelection pt_5_15   #SPLIT50
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection TTJets  --ptSelection pt_15_25  #SPLIT50
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection TTJets  --ptSelection pt_25_-1  #SPLIT50

#TTs
python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection TTs  --ptSelection pt_5_-1   #SPLIT200
python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection TTs  --ptSelection pt_5_15   #SPLIT100
python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection TTs  --ptSelection pt_15_25  #SPLIT100
python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection TTs  --ptSelection pt_25_-1  #SPLIT100

