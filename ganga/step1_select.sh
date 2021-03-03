#! /bin/sh -x 
#
<<<<<<< HEAD
# Run step2_mix.py on the grid
=======
# Run step1_select.py on the grid
>>>>>>> Worls with SLURM
#
# Dietrich Liko, March 2021

echo "Setting up CMS environment"
source /cvmfs/cms.cern.ch/cmsset_default.sh

echo "Setting up CMS release $CMSSW_VERSION for $SCRAM_ARCH"
cmsrel $CMSSW_VERSION

echo "Extracting userarea"
tar xf userarea.tar -C $CMSSW_VERSION

echo "Setting CMS environment"
pushd $CMSSW_VERSION/src > /dev/null
cmsenv
popd > /dev/null

<<<<<<< HEAD
echo "Running step2 select"
=======
pwd
echo "Running step1 select"
>>>>>>> Worls with SLURM
python $CMSSW_VERSION/src/DeepLepton/preprocessing/step1_select.py "$@"

for path in $(find . -name "*.root")
do
<<<<<<< HEAD
    xrdcp -f -C adler32 $path $SKIMSDIR/$path
=======
    xrdcp -f $path $SKIMSDIR/$path
>>>>>>> Worls with SLURM
done
