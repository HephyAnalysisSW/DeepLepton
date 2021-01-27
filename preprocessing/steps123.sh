# Step1
python  step1_select.py  --small --version v1 --year 2016 --flavour ele --logLevel DEBUG --ptSelection pt_5_-1 --sample DYJetsToLL_M50_LO #SPLIT2
python  step1_select.py  --small --version v1 --year 2016 --flavour ele --logLevel DEBUG --ptSelection pt_5_-1 --sample QCD_Mu_Pt30to50 #SPLIT2
python  step1_select.py  --small --version v1 --year 2016 --flavour muo --logLevel DEBUG --ptSelection pt_5_-1 --sample DYJetsToLL_M50_LO  #SPLIT2
python  step1_select.py  --small --version v1 --year 2016 --flavour muo --logLevel DEBUG --ptSelection pt_5_-1 --sample QCD_Mu_Pt30to50 #SPLIT2

# Step2
python  step2_mix.py --version v1_small --year 2016 --flavour ele --ratio balanced --ptSelectionStep1 pt_5_-1 --ptSelection pt_5_-1 --sampleSelection new
python  step2_mix.py --version v1_small --year 2016 --flavour muo --ratio balanced --ptSelectionStep1 pt_5_-1 --ptSelection pt_5_-1 --sampleSelection new

# Step3
python  step3.py --version v1_small  --output_version v1 --year 2016 --flavour ele --ptSelection pt_5_-1 --sampleSelection all
python  step3.py --version v1_small  --output_version v1 --year 2016 --flavour muo --ptSelection pt_5_-1 --sampleSelection all
