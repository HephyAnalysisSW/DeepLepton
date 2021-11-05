#!/usr/bin/env bash                                                                                                                                    

#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --qos=medium
#SBATCH --time=02-00:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=16G
#SBATCH --output=step2.out
#SBATCH --error=step2.err
#SBATCH -J step2


#python step2_sample.py --small --version v1 --logLevel INFO --year 2016 --flavour muo --ratio balanced --ptSelectionStep1 pt_3.5_-1 --ptSelection pt_3.5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection DYvsQCD #SPLIT10


#python step2_sample.py --version v_debug --logLevel INFO --year 2016 --flavour muo --ratio balanced --ptSelectionStep1 pt_3.5_-1 --ptSelection pt_3.5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection STopvsTop #SPLIT400

# python step2_sample.py --version v8 --logLevel INFO --year 2018 --flavour muo --ratio unbalanced --ptSelectionStep1 pt_3.5_-1 --ptSelection pt_3.5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection STopvsTTbar  #SPLIT600
python step2_sample.py --version v9 --logLevel INFO --year 2018 --flavour muo --ratio unbalanced --ptSelectionStep1 pt_3.5_-1 --ptSelection pt_3.5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection STopvsTTbar #SPLIT100
# python step2_sample.py --version v9 --logLevel INFO --year 2018 --flavour muo --ratio unbalanced --ptSelectionStep1 pt_3.5_-1 --ptSelection pt_3.5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection STop4vsTTbar #SPLIT100

# python step2_sample.py --version v8 --logLevel INFO --year 2018 --flavour muo --ratio unbalanced --ptSelectionStep1 pt_3.5_-1 --ptSelection pt_3.5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection STop2vsTTbar #SPLIT600
# python step2_sample.py --version v8 --logLevel INFO --year 2018 --flavour muo --ratio unbalanced --ptSelectionStep1 pt_3.5_-1 --ptSelection pt_3.5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection STop3vsTTbar #SPLIT600
# python step2_sample.py --version v8 --logLevel INFO --year 2018 --flavour muo --ratio unbalanced --ptSelectionStep1 pt_3.5_-1 --ptSelection pt_3.5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection STop4vsTTbar #SPLIT600

# python b_step2_mix.py  --version v3 --logLevel INFO --year 2016 --flavour muo --ratio unbalanced --ptSelectionStep1 pt_3.5_-1 --ptSelection pt_3.5_-1 --SV_sorting pt --pfCand_sorting ptRel --sampleSelection STopvsTop #SPLIT400

