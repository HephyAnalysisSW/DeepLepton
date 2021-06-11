#python step2_sample.py --small --version v1 --logLevel INFO --year 2016 --flavour muo --ratio balanced --ptSelectionStep1 pt_3.5_-1 --ptSelection pt_3.5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection DYvsQCD #SPLIT10


#python step2_sample.py --version v_debug --logLevel INFO --year 2016 --flavour muo --ratio balanced --ptSelectionStep1 pt_3.5_-1 --ptSelection pt_3.5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection STopvsTop #SPLIT400

python step2_sample.py --version v3 --logLevel INFO --year 2016 --flavour muo --ratio unbalanced --ptSelectionStep1 pt_3.5_-1 --ptSelection pt_3.5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection STopvsTop #SPLIT400

# python b_step2_mix.py  --version v3 --logLevel INFO --year 2016 --flavour muo --ratio unbalanced --ptSelectionStep1 pt_3.5_-1 --ptSelection pt_3.5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection STopvsTop #SPLIT400

