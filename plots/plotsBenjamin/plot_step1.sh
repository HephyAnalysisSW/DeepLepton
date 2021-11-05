#!/usr/bin/env bash                                                                                                                                    
# for big plots 2days and 40GB mem per cpu

#SBATCH -J plot
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --qos=medium
#SBATCH --time=02-00:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=40G
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err

source config.sh
# python plot.py  --path $prediction --ncat ${ncat} --plot_predictdata # --special_output_path $output_file_name_3_1
python plot_step1.py --small --path $step1 --normalize --logLevel INFO
# python plot_step1.py --path $step1 --normalize


# pre="/scratch-cbe/users/${USER}/DeepLepton/trained"
# 
# diction1="first_real_training_on_balanced_data_no_droppout"
# diction2="first_real_training_on_unbalanced_data_no_removes_0.1_dropout_20epochs"
# diction3="first_real_training_on_unbalanced_data_only_dxy_weighter_used_0.1_dropout_20epochs"
# diction4="first_real_training_on_unbalanced_data_0.1_dropout_30epochs"
# 
# 
# prediction1="${pre}/${diction1}/prediction"
# prediction2="${pre}/${diction2}/prediction"
# prediction3="${pre}/${diction3}/prediction"
# prediction4="${pre}/${diction4}/prediction"


#python plot.py --plot_predictdata --path $prediction2
#python plot.py --plot_predictdata --path $prediction3
#python plot.py --plot_predictdata --path $prediction4



