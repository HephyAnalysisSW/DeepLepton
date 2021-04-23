#!/bin/bash

. /cvmfs/sft.cern.ch/lcg/views/setupViews.sh  LCG_99 x86_64-centos7-gcc10-opt

find $1 -type f -name "*.root" | \
    xargs -P10 -L1 -I{} bash -c "rootls root://eos.grid.vbc.ac.at/{} 2>&1 | grep -q zombie && echo {}"   

