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


#TTJets
#python -i step2_mix.py --version v1_small_simon --year 2016 --flavour ele --ratio balanced --sampleSelection TTJets  --ptSelection pt_5_-1   #SPLIT100

#python -i step2_mix.py --version v1 --year 2016 --flavour ele --ratio balanced --sampleSelection TTJets  --ptSelection pt_5_-1 #SPLIT100


#full version

#DYvsQCD
python -i step2_mix.py --version v4 --year 2016 --flavour muo --ratio balanced --ptSelectionStep1 pt_15_-1 --sampleSelection DYvsQCD --ptSelection pt_15_-1 #SPLIT100

##TTs
#python -i step2_mix.py --version v1 --year 2016 --flavour muo --ratio balanced --ptSelectionStep1 pt_15_-1 --sampleSelection TTs  --ptSelection pt_15_-1   #SPLIT100

#all
python -i step2_mix.py --version v1 --year 2016 --flavour muo --ratio balanced --ptSelectionStep1 pt_15_-1 --sampleSelection all  --ptSelection pt_15_-1   #SPLIT200

