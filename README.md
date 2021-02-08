This repository holds the release dependent code for DeepLepton, i.e., to prepare the training data and evaluate the training output.
The training is done with a container and the release independent code is in [https://github.com/HephyAnalysisSW/DeepLepton-Training](DeepLepton-Training).
The latter builds on [https://github.com/DL4Jets/DeepJetCore](DeepJetCore). Starters should go through the training example there.

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
## Preparing the training data (release)
NanoAOD that include also the PFCandidates is produced with cfg's stored in [Samples](https://github.com/HephyAnalysisSW/Samples), e.g. [here](https://github.com/HephyAnalysisSW/Samples/blob/master/cfg/nano_v6_mc_10218_Summer16_NANO_PFCands.py).
The privately produced & published nanoAOD samples are collected in Samples/python/nanoAOD_PFCands_Summer16.py
Filenames and normalizations are cached. the cache can be filled in advance by 
```
python DeepLepton/Samples/python/nanoAOD_PFCands_Summer16.py
```
The data are preprocessed (e.g. to write a tree with one lepton per 'Event') by executing step1 and step2 of [https://github.com/HephyAnalysisSW/DeepLepton/tree/2.0/preprocessing](DeepLepton/preprocessing). This is release dependent code.

## Installation of release independent training framework
on CBE checkout the training repository:
```
git clone https://github.com/HephyAnalysisSW/DeepLepton-Training
```
##  select node, container, and environment (container)

```
srun --partition=g --reservation=interactive --qos=medium --time 08:00:00 --pty bash # for GPU
srun --reservation=interactive --qos=medium --time 08:00:00 --pty bash # for CPU

cd DeepLepton-Training
singularity run /scratch-cbe/users/dietrich.liko/deepjetcore3-latest.sif /bin/bash
source ./env.sh 
```

## prepare the root input files (container)
Equip the output directories of step2 with .txt files that contain the filenames. Then run from within the container
```
convertFromSource.py -i <input>/<filename>.txt -o output_directory -c TrainDataDeepLepton
```
``input`` is the path to the folder with input root files, i.e. the output from step2 above, and ``<filename>.txt`` is a txt file that contains the filenames of the input training files including ``.root`` and excluding the path.

# DeepLepton training 
```
python3 Train/deepLepton_Muons_biLSTM_splitDense_elu_reference.py <input>/dataCollection.djcdc <output>/<training>
```
