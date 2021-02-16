
# DeepLepton ntuple production

## Installation of release dependent code (CMSSW_10_2_18) 
```
cmsrel CMSSW_10_2_18
cd CMSSW_10_2_18/src
git clone https://github.com/HephyAnalysisSW/DeepLepton
git clone https://github.com/HephyAnalysisSW/DeepJet
git clone https://github.com/HephyAnalysisSW/Samples
git clone https://github.com/HephyAnalysisSW/RootTools
git clone https://github.com/HephyAnalysisSW/Analysis
scram b -j9
```
## Installation of DeepJet and DeepJetCore for training i.e. outside a release
on CBE
```
singularity run /cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/liko/centos7-djc:latest /bin/bash
git clone https://github.com/HephyAnalysisSW/DeepJet
git clone https://github.com/HephyAnalysisSW/DeepJetCore
```
## Preparing the training data
The nanoAOD samples with the ParticleFlow Candidate collection are produced with the Samples/cfg/*PFCands*.py cfg. 
The only difference to central nanoAOD is a producer that stores PFCandidates in a vector.
We collect the resulting samples in Samples/python/nanoAOD_PFCands_Summer16.py etc.
Fill the sample cache by running
```
python DeepLepton/Samples/python/nanoAOD_PFCands_Summer16.py
```
## Preprocessing
The two preprocessing steps are CMSSW scripts that run on CBE by submitting, e.g.
```
DeepLepton/preprocessing/step1_select.sh
DeepLepton/preprocessing/step2_select.sh
``` 
step1 selectes the events and the leptons in the events and writes a TTree 'tree' with one entry per lepton. 
Truth information is added and dR and ptRel of the SV and PFCandidates are computed. step2 mixes the data randomly and takes care of
the sorting of SV and PFCand.  
## 

# DeepLepton training framework: Repository for training and evaluation of DNN for lepton ID 

This package depends on DeepJetCore (https://github.com/DL4Jets/DeepJetCore) and the HEPHY fork of DeepJet (https://github.com/HephyAnalysisSW/DeepJet).
DeepJet and DeepJetCore must be installed on a CentOS 7 machine (HEPHY: hepgpu01, CERN: lxplus7) but NOT in a release area!

## Setup

The DeepJet package and DeepJetCore have to share the same parent directory. After following the installation recipe of DeepJetCore, clone the HEPHY fork of DeepJet:
```
git clone https://github.com/HephyAnalysisSW/DeepJet
```

## Usage

After logging in, please source the right environment (please cd to the directory first!):
```
cd <your working dir>/DeepJet
source lxplus_env.sh / gpu_env.sh
```


The preparation for the training consists of the following steps

- define the data structure for the training (example in modules/datastructures/TrainData_template.py)
  for simplicity, copy the file to TrainData_template.py and adjust it. 
  Define a new class name (e.g. TrainData_template), leave the inheritance untouched
  
- convert the root file to the data strucure for training using DeepJetCore tools:
  ```
  convertFromRoot.py -i /path/to/the/root/ntuple/list_of_root_files.txt -o /output/path/that/needs/some/disk/space -c TrainData_myclass
  ```
  
  This step can take a while.


- prepare the training file and the model. Please refer to DeepJet/Train/XXX_template.reference.py
  


## Training

Since the training can take a while, it is advised to open a screen session, such that it does not die at logout.
```
ssh lxplus.cern.ch
<note the machine you are on, e.g. lxplus058>
screen
ssh lxplus7
```
Then source the environment, and proceed with the training. Detach the screen session with ctr+a d.
You can go back to the session by logging in to the machine the session is running on (e.g. lxplus58):

```
ssh lxplus.cern.ch
ssh lxplus058
screen -r
``` 

Please close the session when the training is finished

the training is launched in the following way:
```
python train_template.py /path/to/the/output/of/convert/dataCollection.dc <output dir of your choice>
```


## Evaluation

After the training has finished, the performance can be evaluated.
The evaluation consists of a few steps:

1) converting the test data
```
convertFromRoot.py --testdatafor <output dir of training>/trainsamples.dc -i /path/to/the/root/ntuple/list_of_test_root_files.txt -o /output/path/for/test/data
```

2) applying the trained model to the test data
```
predict.py <output dir of training>/KERAS_model.h5  /output/path/for/test/data/dataCollection.dc <output directory>
```
This creates output trees. and a tree_association.txt file that is input to the plotting tools

There is a set of plotting tools with examples in 
DeepJet/Train/Plotting
