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
#python -i step2_mix.py --version v3_small --year 2016 --flavour muo --sampleSelection TTJets --nJobs 2 --job 0
#python -i step2_mix.py --version v3_small --year 2016 --flavour muo --sampleSelection DYvsQCD --nJobs 2 --job 0
#python -i step2_mix.py --version v3_small --year 2016 --flavour muo --sampleSelection DY --nJobs 2 --job 0
#python -i step2_mix.py --version v3_small --year 2016 --flavour muo --sampleSelection QCD --nJobs 2 --job 0

#full version
#python -i step2_mix.py --version v3 --year 2016 --flavour muo --sampleSelection TTJets #SPLIT200
python -i step2_mix.py --version v3 --year 2016 --flavour muo  --sampleSelection DYvsQCD #SPLIT200
