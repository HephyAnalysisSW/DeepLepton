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
# path="/eos/vbc/experiments/cms/store/user/liko/skims/v3/step1/2018/muo"

# path="/eos/vbc/user/benjamin.wilhelmy/DeepLepton/v6/step1/2018/muo"
# path="/scratch-cbe/users/benjamin.wilhelmy/DeepLepton/v6_new/step1/2018/muo"
# python plot.py --path ${path} --ncat 4 --step1 FromSUSY --normalize

# for plot_predictdata the read types are different (important)
python plot.py --path ${step2} --ncat ${ncat}
# python plot.py --path ${step2} --ncat ${ncat} --normalize

# python plot.py --special_output_path $special_output1 --predictOnSample $sample1 --ncat ${ncat} --path $datapath
# python plot.py --special_output_path $special_output2 --predictOnSample $sample2 --ncat ${ncat} --path $datapath
# python plot.py --special_output_path $special_output3 --predictOnSample $sample3 --ncat ${ncat} --path $datapath
# python plot.py --special_output_path $special_output4 --predictOnSample $sample4 --ncat ${ncat} --path $datapath



# python plot.py  --path $prediction --ncat ${ncat} --plot_predictdata # --special_output_path $output_file_name_3_1
# python plot.py  --path $prediction --ncat ${ncat} --plot_predictdata --normalize 
# # python plot.py --path $step2 --ncat ${ncat} --normalize


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



