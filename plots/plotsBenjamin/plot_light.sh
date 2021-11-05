training_name="training_on_unbalanced_data_only4lep_classes_dxy_weighted_Keras-loss_20eps_0.1dropout"
in_path="/scratch-cbe/users/benjamin.wilhelmy/DeepLepton/predicted_on_sample/v9/${training_name}/2018/muo/pt_3.5_-1/"

sample1="step2_v9"
sample2="STop2vsTTbar"
sample3="Stop600-dm10-006"
sample4="Stop600-dm20-006"


python plot_light.py --ncat 4 --small --path "${in_path}${sample2}"
