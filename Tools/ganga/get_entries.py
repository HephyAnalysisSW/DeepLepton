#!/usr/bin/env python

from __future__ import print_function

import sys

import ROOT

chain = ROOT.TChain(sys.argv[1])
chain.Add(f'{sys.argv[2]}//{sys.argv[3]}')

try:
    entries = chain.GetEntries()
    print ( f'{sys.argv[3]} has {entries} entries.' )
except:
    print ( f'{sys.argv[3]} is bad' )
