#! /bin/sh -x
ganga=/'cvmfs/ganga.cern.ch/Ganga/install/LATEST/bin/ganga'
$ganga submit_step2_mix --version v1 --year 2016 --flavour all --sampleSelection Top --small --ratio balanced 
