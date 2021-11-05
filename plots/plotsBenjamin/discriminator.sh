#!/usr/bin/env bash

#SBATCH -N 1
#SBATCH -n 2
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH -J discriminator_plots
#SBATCH --error=%x.%j.err
#SBATCH --output=%x.%j.out
#SBATCH --qos=short
#SBATCH --time=00-08:00:00

source config.sh
python discriminator.py --pathpred $prediction --ncat ${ncat} # --special_output_path $output_file_name_3_1

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

# echo "finished first"
# python discriminator.py --pathpred $prediction4
# echo "finished second"
# python discriminator.py --pathpred $prediction3
# echo "finished third"
# python discriminator.py --pathpred $prediction2
