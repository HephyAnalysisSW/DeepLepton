import os
import shutil

PREDICT = "/mnt/hephy/cms/benjamin.wilhelmy/www/Training_v4/Test_validation_unbalanced_only_dxy_Keras_20eps_0.1dropout/predict_data_plots"
INVESTIGATE = ["/mnt/hephy/cms/benjamin.wilhelmy/www/Training_v4/Test_validation_unbalanced_only_dxy_Keras_20eps_0.1dropout/Plot_Investigate",
               "/mnt/hephy/cms/benjamin.wilhelmy/www/Training_v4/Test_validation_unbalanced_only_dxy_Keras_20eps_0.1dropout/Plot_Investigate_normalized"]

invest_dirs = [os.listdir(INVESTIGATE[0]), os.listdir(INVESTIGATE[1])]

files = []
for f in os.listdir(PREDICT):
    if f.endswith(".png"):
        d = f.split("_predict_data.png")[0]
        if d in invest_dirs[0]:
            files.append([os.path.join(PREDICT,f), os.path.join(INVESTIGATE[0], d, f), os.path.join(PREDICT+"_normalized",f), os.path.join(INVESTIGATE[1], d, f)])

for f in files:
    # print(f)
    shutil.copyfile(f[0], f[1])
    shutil.copyfile(f[2], f[3])
        


