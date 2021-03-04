#! /bin/sh -x 
#
# Run step2_mix.py on the grid
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

pwd
echo "Running step1 select"
python $CMSSW_VERSION/src/DeepLepton/preprocessing/step1_select.py "$@"

for path in $(find . -name "*.root")
do
    xrdcp -f $path $SKIMSDIR/$path
done
