#!/bin/bash -x

here=$(dirname $(realpath "$0"))
find /eos/vbc/experiments/cms/store/user/liko/skims/v2 -name *.root -print | xargs -L1 -P20 "$here/get_entries.py" tree root://eos.grid.vbc.ac.at | tee entries.txt


