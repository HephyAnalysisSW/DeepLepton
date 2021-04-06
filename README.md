This repository holds the release dependent code for DeepLepton, i.e., to prepare the training data and evaluate the training output.
The training is done with a container and the release independent code is in [DeepLepton-Training](https://github.com/HephyAnalysisSW/DeepLepton-Training).
The latter builds on [DeepjetCore](https://github.com/DL4Jets/DeepJetCore). Starters should go through the training example there.

# DeepLepton ntuple production

## Installation of release dependent code (CMSSW_10_2_18) 
```
cmsrel CMSSW_10_2_18
cd CMSSW_10_2_18/src
git clone https://github.com/HephyAnalysisSW/DeepLepton
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

## Installation of release independent training framework
on CBE checkout the training repository:
```
git clone https://github.com/HephyAnalysisSW/DeepLepton-Training
```
##  select node, container, and environment (container)

```
srun --partition=g --gres=gpu:V100 --reservation=interactive --qos=medium --time 12:00:00 --mem=32G --pty bash # for GPU
srun --reservation=interactive --qos=medium --time 08:00:00 --mem=64G --cpus-per-task=10 --pty bash # for CPU

cd DeepLepton-Training
singularity run /scratch-cbe/users/dietrich.liko/deepjetcore3-latest.sif /bin/bash #for CPU
singularity run --nv /scratch-cbe/users/dietrich.liko/deepjetcore3-latest.sif /bin/bash #for GPU
source ./env.sh 
```

## prepare the root input files (container)
Equip the output directories of step2 with .txt files that contain the filenames. Then run from within the container
```
convertFromSource.py -i <input>/<filename>.txt -o output_directory -c TrainDataDeepLepton
```
``input`` is the path to the folder with input root files, i.e. the output from step2 above, and ``<filename>.txt`` is a txt file that contains the filenames of the input training files including ``.root`` and excluding the path.

Alternatively convertjob.sh can be used to submit the conversion to the batch system with ``sbatch convertjob.sh`` 

# DeepLepton training 
```
python3 Train/deepLepton_Muons_biLSTM_splitDense_elu_reference.py <input>/dataCollection.djcdc <output>/<training>
```

Again, trainjob.sh can be used to run the training on the batch system. This is recommended for long trainings.
