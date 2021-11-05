# All the vars needed for plotting

step="/scratch-cbe/users/benjamin.wilhelmy/DeepLepton/v9/step2/2018/muo/"
unbalanced="unbalanced/pt_3.5_-1/STopvsTTbar"
balanced="balanced/pt_3.5_-1/STopvsTTbar"
step2="${step}${unbalanced}"
# step1="/eos/vbc/user/benjamin.wilhelmy/DeepLepton/v6/step1/2018/muo/"
step1="/scratch-cbe/users/benjamin.wilhelmy/DeepLepton/v9/step1/2018/muo"


# If one wants to plot traindata:
pre="/scratch-cbe/users/${USER}/DeepLepton/trained_v6"

diction1="first_real_training_on_balanced_data_no_droppout"
diction2="first_real_training_on_unbalanced_data_no_removes_0.1_dropout_20epochs"
diction3="first_real_training_on_unbalanced_data_only_dxy_weighter_used_0.1_dropout_20epochs"
diction4="first_real_training_on_unbalanced_data_0.1_dropout_30epochs"
diction5="training_on_unbalanced_data_less_features_0.3_dropout_8epoches_no_removes"
diction6="training_on_unbalanced_data_only4lep_classes_3eps_0.1dropout_no_removes"
diction7="training_on_unbalanced_data_only4lep_classes_5eps_0.1dropout_no_removes_weighted_loss"
#V4 From Here:
diction8="training_on_unbalanced_data_only4lep_classes_dxy_weighted_customLossFn_20eps_0.1dropout"
diction9="training_on_unbalanced_data_only4lep_classes_dxy_weighted_Keras-loss_100eps_0.5dropout"
diction10="training_on_unbalanced_data_only4lep_classes_dxy_weighted_Keras-loss_20eps_0.1dropout"
diction11="training_on_unbalanced_data_only4lep_classes_dxy_weighted_Keras-loss_50eps_0.1dropout"
diction12="training_on_unbalanced_data_only4lep_classes_dxy_weighted_customLossFn_50eps_0.1dropout"
diction13="training_on_unbalanced_data_only4lep_classes_dxy_weighted_customloss_100eps_0.5dropout"
diction14="training_on_unbalanced_data_only4lep_classes_dxy_weighted_customloss_1_1_10_200_weights_45eps_0.6dropout_batch_size_5000"
diction15="training_on_unbalanced_data_only4lep_classes_dxy_weighted_customloss_1_1_10_200_weights_500eps_0.6dropout_batch_size_5000"
diction16="training_on_unbalanced_data_only4lep_classes_dxy_weighted_customloss_all_balanced_weights_25eps_0.3dropout_batch_size_5000"
diction17="training_on_unbalanced_data_only4lep_classes_dxy_weighted_customloss_unity_weights_20eps_0.1dropout"
#V6 From Here:
diction18="training_on_balanced_data_only4lep_classes_dxy_weighted_KerasLoss_50eps_0.1dropout"
diction19="training_on_balanced_data_only4lep_classes_dxy_weighted_KerasLoss_20eps_0.1dropout"
diction20="training_on_unbalanced_data_only4lep_classes_dxy_weighted_KerasLoss_20eps_0.1dropout"
diction21="training_on_balanced_data_only4lep_classes_dxy_weighted_KerasLoss_50eps_0.5dropout"


prediction1="${pre}/${diction1}/prediction"
prediction2="${pre}/${diction2}/prediction"
prediction3="${pre}/${diction3}/prediction"
prediction3_1="${pre}/${diction3}/prediction_more_features"
prediction4="${pre}/${diction4}/prediction"
prediction5="${pre}/${diction5}/prediction"
prediction6="${pre}/${diction6}/prediction"
prediction7="${pre}/${diction7}/prediction_2nd_epoch"
#V4 From here:
prediction8="${pre}/${diction8}/prediction"
prediction9="${pre}/${diction9}/prediction"
prediction10="${pre}/${diction10}/prediction"
prediction11="${pre}/${diction11}/prediction"
prediction12="${pre}/${diction12}/prediction"
prediction13="${pre}/${diction13}/prediction"
prediction14="${pre}/${diction14}/prediction"
prediction15="${pre}/${diction15}/prediction"
prediction16="${pre}/${diction16}/prediction"
prediction17="${pre}/${diction17}/prediction"
#V6 From here:
prediction18="${pre}/${diction18}/prediction"
prediction19="${pre}/${diction19}/prediction"
prediction20="${pre}/${diction20}/prediction"
prediction21="${pre}/${diction21}/prediction"


filename1="${prediction1}/outfiles.txt"
filename2="${prediction2}/outfiles.txt"
filename3="${prediction3}/outfiles.txt"
filename3_1="${prediction3_1}/outfiles.txt"
filename4="${prediction4}/outfiles.txt"
filename5="${prediction5}/outfiles.txt"
filename6="${prediction6}/outfiles.txt"
filename7="${prediction7}/outfiles.txt"
#V4 From here:
filename8="${prediction8}/outfiles.txt"
filename9="${prediction9}/outfiles.txt"
filename10="${prediction10}/outfiles.txt"
filename11="${prediction11}/outfiles.txt"
filename12="${prediction12}/outfiles.txt"
filename13="${prediction13}/outfiles.txt"
filename14="${prediction14}/outfiles.txt"
filename15="${prediction15}/outfiles.txt"
filename16="${prediction16}/outfiles.txt"
filename17="${prediction17}/outfiles.txt"
#V6 From here:
filename18="${prediction18}/outfiles.txt"
filename19="${prediction19}/outfiles.txt"
filename20="${prediction20}/outfiles.txt"
filename21="${prediction21}/outfiles.txt"



# special output-filename:
output_file_name_3_1="first_real_training_on_unbalanced_data_only_dxy_weighter_used_0.1_dropout_20epochs_more_features"





# For plots of predictOnSample:
datamodel="training_on_balanced_data_only4lep_classes_dxy_weighted_KerasLoss_50eps_0.5dropout"
datapath="/scratch-cbe/users/benjamin.wilhelmy/DeepLepton/predicted_on_sample/${datamodel}/v6/2018/muo/pt_3.5_-1"

special_output1="/mnt/hephy/cms/benjamin.wilhelmy/www/Training_v6/FeaturesPlots_predictOnSample/Stop250-dm10-006"
special_output2="/mnt/hephy/cms/benjamin.wilhelmy/www/Training_v6/FeaturesPlots_predictOnSample/Stop250-dm20-006"
special_output3="/mnt/hephy/cms/benjamin.wilhelmy/www/Training_v6/FeaturesPlots_predictOnSample/Stop600-dm10-006"
special_output4="/mnt/hephy/cms/benjamin.wilhelmy/www/Training_v6/FeaturesPlots_predictOnSample/Stop600-dm20-006"



#samples: Stop250-dm10-006  Stop250-dm20-006  Stop600-dm10-006  Stop600-dm20-006
sample1="Stop250-dm10-006"
sample2="Stop250-dm20-006"
sample3="Stop600-dm10-006"
sample4="Stop600-dm20-006"




#########################DECLARE-YOUR-CHOICE###################################
prediction=$prediction21
filename=$filename21
ncat="4"

