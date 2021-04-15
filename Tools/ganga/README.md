# Running DeepLepton Jobs with CMSCONNET

[CMSCONNECT](https://connect.uscms.org) provides access to the HTCondor based grid infrastucture
of CMS, which is usually hidden from the user by CRAB.

[Ganga](https://ganga.readthedocs.io/en/latest/) is a modular tool for Job Management on the Grid and Local Batch System

Two modes have been implemented, both running jobs at CLIP. 

* Submit jobs to the grid using CMSCONNECT 
* Using the local batch system SLURM (for testing)

***
## 1. Preparations for CMSCONNECT

Singup at https://connect.uscms.org and wait that your request will
be processed. You will have to provide a ssh-key to give you
access to the login node (for me only a rsa key worked).

Login to 

```bash
ssh -l <username> login-el7.uscms.org
```

To allow ganga to submit jobs, you have to upload your grid certificate,
as described in documentation.

There is also [much more information](https://ci-connect.atlassian.net/wiki/spaces/CMS/overview) 
on the service available. 

***
## 2. Preparations on the login node

Define __ganga__ command in your `.bashrc`
```bash
alias ganga='/cvmfs/ganga.cern.ch/Ganga/install/LATEST/bin/ganga'
export PATH="~/.local/bin:$PATH"
```

To avoid a conflict between ganga and the HTCondor installation
```
mkdir -p ~/.local/bin
curl -sL -o ~/.local/bin/condor_submit 

```

***
## 3. Submitting the job with HTCondor to CLIP

Install the software
```bash
cmsrel CMSSW_10_2_18
cd CMSSW_10_2_18/src
cmsenv
git clone https://github.com/HephyAnalysisSW/DeepLepton
git clone https://github.com/HephyAnalysisSW/Samples
git clone https://github.com/HephyAnalysisSW/RootTools
git clone https://github.com/HephyAnalysisSW/Analysis
scram b -j9 
```

Create the proxy
```bash
voms-proxy-init -voms cms -rfc -valid 192:0
```

Submit a test job
```bash
cd DeepLepton/Tools/ganga

ganga submit_step1 --version v1 --year 2016 --flavour all --sample TGG --small
```

Use ganga interactively to verify the job status.

```bash
ganga
jobs
jobs(3).subjobs
```

The job log files are stored in the Ganga workspace

The skim files can be found on EOS

```bash
ls /eos/vbc/experiments/user/<nickname>/skims
```

***
## 3. Submitting jobs with SLURM on CLIP

Similar preparations on CLIP.

```bash
alias ganga='/cvmfs/ganga.cern.ch/Ganga/install/LATEST/bin/ganga'
```

Create the VOMS proxy and save it securely on the shared file system
```bash
mkdir ~/private
chmod 700 ~/private
voms-proxy-init -voms cms -valid 192:0 -out ~/private/proxy
export X509_USER_PROXY=$HOME/private/proxy
```

Run the jobs
```bash
cd DeepLepton/Tools/ganga
ganga submit_step1 --version v1 --year 2016 --flavour all --sample TGG --small
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