#! /bin/bash -x 
#
# Run step1_select.py on the grid
#
# Dietrich Liko, March 2021

echo "Setting up CMS environment"
if [ -z "$CMS_PATH" ]; then
    # shellcheck disable=SC1091
    . /cvmfs/cms.cern.ch/cmsset_default.sh
fi

echo "Setting up CMS release $CMSSW_VERSION for $SCRAM_ARCH"
cmsrel "$CMSSW_VERSION"

echo "Extracting userarea"
tar xf userarea.tar -C "$CMSSW_VERSION"

echo "Setting CMS environment"
cd "$CMSSW_VERSION"/src || exit
cmsenv
cd - || exit 

echo "Running step1 select"

python "$CMSSW_VERSION/src/DeepLepton/preprocessing/step1_select.py" "$@"

find . -name "*.root" -exec xrdcp -f -C adler32:print {} "root://eos.grid.vbc.ac.at/$SKIMSDIR/{}" \;
