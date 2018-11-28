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

#DYvsQCD
#python -i step2_mix.py --version v5 --year 2016 --flavour muo --ratio balanced --sampleSelection DYvsQCD --ptSelection pt_15_-1 #SPLIT100

##TTJets
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection TTJets  --ptSelection pt_5_-1   #SPLIT100
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection TTJets  --ptSelection pt_5_15   #SPLIT50
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection TTJets  --ptSelection pt_15_25  #SPLIT50
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection TTJets  --ptSelection pt_25_-1  #SPLIT50

#TTs
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection TTs  --ptSelection pt_5_-1   #SPLIT135
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection TTs  --ptSelection pt_10_-1  #SPLIT100

#AllSamples
python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1   #SPLIT250

##restart
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 229
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 230
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 231
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 232
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 233
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 234
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 235
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 236
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 237
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 238
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 239
#
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 240
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 241
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 242
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 243
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 244
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 245
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 246
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 247
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 248
#python -i step2_mix.py --version v6 --year 2016 --flavour muo --ratio balanced --sampleSelection AllSamples  --ptSelection pt_5_-1 --nJobs 250 --job 249
