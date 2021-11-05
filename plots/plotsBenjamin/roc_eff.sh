#!/usr/bin/env bash                                                                                                                                    

#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=64G
#SBATCH -J eff_roc_plots
#SBATCH --error=%x.%j.err
#SBATCH --output=%x.%j.out
#SBATCH --qos=short
#SBATCH --time=00-06:00:00

source config.sh

python roc.py --outfilespath ${filename} --ncat ${ncat} # --special_output_path $output_file_name_3_1
python benjamins_eff.py --pathpred ${prediction} --ncat ${ncat} # --special_output_path $output_file_name_3_1

# pre="/scratch-cbe/users/${USER}/DeepLepton/trained"
# 
# diction1="first_real_training_on_balanced_data_no_droppout"
# diction2="first_real_training_on_unbalanced_data_no_removes_0.1_dropout_20epochs"
# diction3="first_real_training_on_unbalanced_data_only_dxy_weighter_used_0.1_dropout_20epochs"
# diction4="first_real_training_on_unbalanced_data_0.1_dropout_30epochs"
# 
# prediction1="${pre}/${diction1}/prediction"
# prediction2="${pre}/${diction2}/prediction"
# prediction3="${pre}/${diction3}/prediction"
# prediction4="${pre}/${diction4}/prediction"
# 
# 
# filename1="${prediction1}/outfiles.txt"
# filename2="${prediction2}/outfiles.txt"
# filename3="${prediction3}/outfiles.txt"
# filename4="${prediction4}/outfiles.txt"
# 
# 
# echo ""
# echo "start pred1"
# echo ""
# 
# python roc.py --outfilespath ${filename1} --ncat 5
# python benjamins_eff.py --pathpred ${prediction1} --ncat 5

# echo ""
# echo "start pred2"
# echo ""
# 
# 
# python roc.py --outfilespath ${filename2} --ncat 5
# python benjamins_eff.py --pathpred ${prediction2} --ncat 5
# 
# echo ""
# echo "start pred3"
# echo ""
# 
# 
# python roc.py --outfilespath ${filename3} --ncat 5
# python benjamins_eff.py --pathpred ${prediction3} --ncat 5
# 
# echo ""
# echo "start pred4"
# echo ""
# 
# 
# python roc.py --outfilespath ${filename4} --ncat 5
# python benjamins_eff.py --pathpred ${prediction4} --ncat 5
# 
# echo ""
# echo "start pred5"
# echo ""
# 
# python roc.py --outfilespath ${filename5} --ncat 5
# python benjamins_eff.py --pathpred ${prediction5} --ncat 5
# 
# echo ""
# echo "start pred6"
# echo ""
# 
# python roc.py --outfilespath ${filename} --ncat $ncat
# python benjamins_eff.py --pathpred ${prediction} --ncat $ncat
# 
