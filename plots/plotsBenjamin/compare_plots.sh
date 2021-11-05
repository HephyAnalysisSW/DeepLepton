# training_name="training_on_balanced_data_only4lep_classes_dxy_weighted_KerasLoss_50eps_0.1dropout"
training_name="training_on_unbalanced_data_only4lep_classes_dxy_weighted_Keras-loss_20eps_0.1dropout"
in_path="/scratch-cbe/users/benjamin.wilhelmy/DeepLepton/predicted_on_sample/v9/${training_name}/2018/muo/pt_3.5_-1/"

sample1="STop1vsTTbar"
sample2="STop2vsTTbar"
sample3="STop3vsTTbar"
sample4="STop4vsTTbar"
# --logLevel DEBUG 
# python compare_plots.py --outfilespath "Training_v6/${training_name}/vsStopsCompressed/${sample1}" --input_dir "${in_path}${sample1}" --ncat 4
sample=$sample4
python compare_plots.py --outfilespath "Training_v4/${training_name}/vsStopsCompressed/${sample}" --input_dir "${in_path}${sample}" --ncat 4 
syncWWW

# python compare_plots.py --outfilespath "Training_v6/${training_name}/vsStopsCompressed/${sample2}" --input_dir "${in_path}${sample2}" --ncat 4 
# python compare_plots.py --outfilespath "Training_v6/${training_name}/vsStopsCompressed/${sample3}" --input_dir "${in_path}${sample3}" --ncat 4 
# python compare_plots.py --outfilespath "Training_v6/${training_name}/vsStopsCompressed/${sample4}" --input_dir "${in_path}${sample4}" --ncat 4 

# index="/mnt/hephy/cms/benjamin.wilhelmy/www/index.php"
# plotdir="/mnt/hephy/cms/benjamin.wilhelmy/www/Training_v4/${training_name}/vsStopsCompressed"
# cp -v -n "${index}" "${plotdir}"
# cp -v -n "${index}" "${plotdir}/${sample1}"
# cp -v -n "${index}" "${plotdir}/${sample1}/lep_pt"
# cp -v -n "${index}" "${plotdir}/${sample1}/lep_dxy"

# cp -v -n "${index}" "${plotdir}/${sample2}"
# cp -v -n "${index}" "${plotdir}/${sample2}/lep_pt"
# cp -v -n "${index}" "${plotdir}/${sample2}/lep_dxy"
# 
# cp -v -n "${index}" "${plotdir}/${sample3}"
# cp -v -n "${index}" "${plotdir}/${sample3}/lep_pt"
# cp -v -n "${index}" "${plotdir}/${sample3}/lep_dxy"
# 
# cp -v -n "${index}" "${plotdir}/${sample4}"
# cp -v -n "${index}" "${plotdir}/${sample4}/lep_pt"
# cp -v -n "${index}" "${plotdir}/${sample4}/lep_dxy"
# 
