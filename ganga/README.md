# Running DeepLepton Jobs using ganga

Ganga is a modular too for Job Management on the Grid and Local Batch System

https://ganga.readthedocs.io/en/latest/

Two modes have been implemented, both running jobs at CLIP. 

* Using the local batch system Slurm
* Using the Grid using CMSCONNECT and Condor 

## Using Slurm

Prepare the environment  by adding following alias to `.bashrc`

```bash
alias ganga='/cvmfs/ganga.cern.ch/Ganga/install/LATEST/bin/ganga'
```

Download and install the software
```bash
cmsrel CMSSW_10_2_18
cd CMSSW_10_2_18/src
cmsenv
git clone https://github.com/HephyAnalysisSW/DeepLepton -b grid
git clone https://github.com/HephyAnalysisSW/Samples
git clone https://github.com/HephyAnalysisSW/RootTools
git clone https://github.com/HephyAnalysisSW/Analysis
scram b -j9 
```

Create the VOMS proxy and save it securely on the shared file system
```bash
voms-proxy-init -voms cms -valid 192:0 -out ~/private/proxy
export X509_USER_PROXY=$HOME/private/proxy
```

Run the jobs
```bash
ganga submit_step1_select --version=v1 --year=2016 --small --sample ALL
```

The output can be found at
```
/eos/vbs/experiments/cms/store/user/<nickname>/skims
```

## Using CMSCONNECT

You gave to regsiter yourself following the instructions on https://connect.uscms.org/signup
I used my CERN login to register und choose the same username as on lxplus.

After follow thew Quick Start https://ci-connect.atlassian.net/wiki/spaces/CMS/overview
and copy the certificates

```bash
copy_certificates
```

Prepare the environment on `login-el7.uscms.org` by adding following to `.bash_profile`

```bash
alias ganga='/usr/bin/env -u PYTHONPATH /cvmfs/ganga.cern.ch/Ganga/install/LATEST/bin/ganga'
export PATH=/home/<user>/bin:$PATH
export SAVEPYTHONPATH=$PYTHONPATH
```

Create `$HOME/bin` and add the file 
```bash
curl https://raw.githubusercontent.com/HephyAnalysisSW/DeepLepton/grid/ganga/condor_submit -o $HOME/bin/condor_submit
chmod +x $HOME/bin/condor_submit
```

Create ganga config and 
```bash
ganga -g
```

Add add following additions to `.gangarc`

```bash
SCRIPTS_PATH = Ganga/scripts:/home/<user>/CMSSW_10_2_18/src/DeepLepton/ganga

gangadir = /scratch/<user>/gangadir
```

Copy the samples DB to from CLIP to `login-el7.uscms.org`. This has to be initiated from the login node of CLIP
due to connectivity issue.
```bash
scp ~/caches/Samples/DB_Summer16_DeepLepton.sql::memory:?cache=shared <user>@login-el7.uscms.org:
```

Download and install the software

```bash
cmsrel CMSSW_10_2_18
cd CMSSW_10_2_18/src
cmsenv
git clone https://github.com/HephyAnalysisSW/DeepLepton -b grid
git clone https://github.com/HephyAnalysisSW/Samples
git clone https://github.com/HephyAnalysisSW/RootTools
git clone https://github.com/HephyAnalysisSW/Analysis
scram b -j9 
```

Create the VOMS proxy
```bash
voms-proxy-init -voms cms -valid 192:0
```

Finally submit jobs

```bash
ganga submit_step1_select --version=v1 --year=2016 --samples ALL --condor
```    