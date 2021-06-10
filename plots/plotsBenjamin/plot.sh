#!/usr/bin/env bash                                                                                                                                    

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --qos=medium
#SBATCH --time=02-00:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=40G
#SBATCH --output=plot.out
#SBATCH --error=plot.err
#SBATCH -J plot

# Total allocation will be: 4 cores and 4GB of memory on 1 node.
#  cmsenv
python plot.py --normalize

