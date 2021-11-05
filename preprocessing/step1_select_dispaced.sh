#!/usr/bin/env bash                                                                                                                                    

#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --qos=medium
#SBATCH --time=02-00:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=8G
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err

# other options: CompSUSY (2017), stop250dm10 (2018), stop250dm20 (2018), stop600dm10 (2018), stop600dm20 (2018), 
python step1_select.py --version v10 --year 2018 --flavour muo --logLevel INFO --ptSelection pt_3.5_-1 --displaced --sample TTToHadronic_TuneCP5_13TeV #SPLIT300
 
python step1_select.py --version v10 --year 2018 --flavour muo --logLevel INFO --ptSelection pt_3.5_-1 --displaced --sample TTJets_TuneCP5_13TeV #SPLIT30 
python step1_select.py --version v10 --year 2018 --flavour muo --logLevel INFO --ptSelection pt_3.5_-1 --displaced --sample TTTo2L2Nu_TuneCP5_13TeV #SPLIT100

python step1_select.py --version v10 --year 2018 --flavour muo --logLevel INFO --ptSelection pt_3.5_-1 --displaced --sample TTToSemiLeptonic_TuneCP5_13TeV #SPLIT120

python step1_select.py --version v10 --year 2018 --flavour muo --logLevel INFO --ptSelection pt_3.5_-1 --displaced --sample TT_DiLept_TuneCP5_13TeV #SPLIT10



python step1_select.py --version v10 --year 2018 --flavour muo --logLevel INFO --ptSelection pt_3.5_-1 --displaced --sample stop250dm20 #SPLIT5
python step1_select.py --version v10 --year 2018 --flavour muo --logLevel INFO --ptSelection pt_3.5_-1 --displaced --sample stop600dm10 #SPLIT5
python step1_select.py --version v10 --year 2018 --flavour muo --logLevel INFO --ptSelection pt_3.5_-1 --displaced --sample stop600dm20 #SPLIT5
python step1_select.py --version v10 --year 2018 --flavour muo --logLevel INFO --ptSelection pt_3.5_-1 --displaced --sample stop250dm10 #SPLIT5 
