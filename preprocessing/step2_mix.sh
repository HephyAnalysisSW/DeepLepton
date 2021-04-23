#!/bin/sh

#python step2_mix.py --small --logLevel DEBUG --version v2 --year 2016 --flavour ele --ratio balanced --ptSelectionStep1 pt_5_-1 --ptSelection pt_5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection DYvsQCD #SPLIT400
#python step2_mix.py --version v2 --year 2016 --flavour ele --ratio balanced --ptSelectionStep1 pt_5_-1 --ptSelection pt_5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection DYvsQCD #SPLIT200
##python step2_mix.py --version v2 --year 2016 --flavour muo --ratio balanced --ptSelectionStep1 pt_3.5_-1 --ptSelection pt_3.5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection DYvsQCD #SPLIT200
python step2_mix.py --version v2 --logLevel INFO --year 2016 --flavour muo --ratio balanced --ptSelectionStep1 pt_3.5_-1 --ptSelection pt_3.5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection Top #SPLIT400

#python step2_mix.py --version v1 --year 2016 --flavour ele --ratio balanced --ptSelectionStep1 pt_5_-1 --ptSelection pt_5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection all #SPLIT100
#python step2_mix.py  --version v1 --year 2016 --flavour muo --ratio balanced --ptSelectionStep1 pt_3.5_-1 --ptSelection pt_3.5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection all #SPLIT200



#python step2_mix.py --version v2 --logLevel INFO --year 2016 --flavour muo --ratio balanced --ptSelectionStep1 pt_3.5_-1 --ptSelection pt_3.5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection Top --job 0 --nJobs 1000 
