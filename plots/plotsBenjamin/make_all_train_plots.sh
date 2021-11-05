#!/usr/bin/env bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -J submit_all_plots
#SBATCH --error=%x.%j.err
#SBATCH --output=%x.%j.out
#SBATCH --qos=short
#SBATCH --time=00-00:30:00


source config.sh
# sbatch roc_eff.sh
# sbatch discriminator.sh
# sbatch plot.sh
# sbatch plot_investigate.sh
source roc_eff.sh
source discriminator.sh    # discriminator.sh vars:
source plot.sh
source plot_investigate.sh # pre="/scratch-cbe/users/${USER}/DeepLepton/trained"
# 
# diction1="first_real_training_on_balanced_data_no_droppout"
# diction2="first_real_training_on_unbalanced_data_no_removes_0.1_dropout_20epochs"
# diction3="first_real_training_on_unbalanced_data_only_dxy_weighter_used_0.1_dropout_20epochs"
# diction4="first_real_training_on_unbalanced_data_0.1_dropout_30epochs"
# diction5="training_on_unbalanced_data_less_features_0.3_dropout_8epoches_no_removes"
# 
# 
# prediction1="${pre}/${diction1}/prediction"
# prediction2="${pre}/${diction2}/prediction"
# prediction3="${pre}/${diction3}/prediction"
# prediction4="${pre}/${diction4}/prediction"
# prediction5="${pre}/${diction5}/prediction"
# 
# 
# filename1="${prediction1}/outfiles.txt"
# filename2="${prediction2}/outfiles.txt"
# filename3="${prediction3}/outfiles.txt"
# filename4="${prediction4}/outfiles.txt"
# filename5="${prediction5}/outfiles.txt"
# 
# #########################DECLARE-YOUR-CHOICE###################################
# prediction=$prediction1
# filename=$filename1




