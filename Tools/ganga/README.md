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
## 2. Preparations on the CMSCONNECT login node

Define __ganga__ command in your `.bashrc` and add a fix
for an incompatibility between cmsconnect and ganga
```bash
alias ganga='/cvmfs/ganga.cern.ch/Ganga/install/LATEST/bin/ganga'
export SAVEPYTHONPATH=$PYTHONPATH
unset PYTHONPATH
export PATH="~/.local/bin:$PATH"
```

And put a shim into `~/.local/bin`

```
mkdir -p ~/.local/bin
cd .local/bin
curl -sLO https://raw.githubusercontent.com/HephyAnalysisSW/DeepLepton/newgrid/Tools/ganga/condor_submit
chmod +x ~/.local/bin/condor_submit
cd -
```

Create `.gangarc`
```bash
ganga -g
```
and set 
```bash
gangadir = /stash/user/<name>/gangadir
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

Copy your samples DB from `cbe.vbc.ac.at` to `login-el7.uscms.org`
```
scp "~/caches/Samples/DB_Summer16_DeepLepton.sql::memory:?cache=share" login-el7.uscms.org:DB_Summer16_DeepLepton.sql
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

Use ganga interactively to verify the job status. Some useful commands

* `ganga` - Start ganga interactive
* `jobs` - list the status of all jobs
* `jobs(1).subjobs` - list the status of all subjobs generated
* `j=jobs("1.0")` - variable `j` references subjob 0 of job 0
* `ls $j.outputdir` - job output
* `less $j.outputdir/stdout` - view the stdout of the job (after the job has finished)

```bash

jobs
jobs(3).subjobs
```

The job log files are stored in the Ganga workspace

The skim files can be found on EOS

```bash
ls /eos/vbc/experiments/user/<nickname>/skims
```

***
## 4. Submitting jobs with SLURM on CLIP

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