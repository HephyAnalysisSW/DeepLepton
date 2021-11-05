#!/usr/bin/env bash                                                                                                                                    
# for big plots 2days and 40GB mem per cpu

#SBATCH -J plot_investigate
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --qos=short
#SBATCH --time=00-08:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=40G
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err

source config.sh
python plot_investigate.py  --path $prediction --ncat ${ncat} --normalize # --special_output_path $output_file_name_3_1

python plot_investigate.py  --path $prediction --ncat ${ncat}
