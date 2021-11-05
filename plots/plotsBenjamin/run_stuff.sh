python benjamins_eff.py --pathpred ${prediction} --ncat $ncat
python roc.py --outfilespath ${filename} --ncat $ncat
python discriminator.py --pathpred $prediction --ncat $ncat
python plot.py --plot_predictdata --path $prediction --ncat $ncat



