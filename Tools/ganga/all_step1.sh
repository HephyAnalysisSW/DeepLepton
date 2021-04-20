#! /bin/sh -x

ganga='/cvmfs/ganga.cern.ch/Ganga/install/LATEST/bin/ganga'
for sample in 'QCD' 'DY' 'T'
do
    for flavour in 'ele' 'muo'
    do
       "$ganga" submit_step1 --version v1 --flavour "$flavour" --sample "$sample" "$@"
    done
done
