#!/usr/bin/env bash                                                                                                                                    

#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=4G
#SBATCH -J eff_plot
#SBATCH --error=benjamins_eff.err
#SBATCH --output=benjamins_eff.out
#SBATCH --qos=short
#SBATCH --time=00-08:00:00

pre="/scratch-cbe/users/${USER}/DeepLepton/trained"
diction="first_real_training_on_unbalanced_data_only_dxy_weighter_used_0.1_dropout_20epochs/prediction"

prediction="${pre}/${diction}"

python benjamins_eff.py --pathpred ${prediction}
