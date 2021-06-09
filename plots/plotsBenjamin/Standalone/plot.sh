#!/usr/bin/env bash


#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --time=0-05:10:00
#SBATCH --output=plot.out
#SBATCH --output=plot.stdout
#SBATCH --error=plot.err

# Total allocation will be: 4 cores and 4GB of memory on 1 node.
source env.sh
python plot.py
# IMPORTANT ONE NEEDS A VALID KERBEROS TOKEN -> RUN KINIT!
source pushplots.sh
