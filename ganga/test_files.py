#! /usr/bin/env python

import os
import ROOT

topdir = '/eos/vbc/experiments/cms/store/user/liko/skims'

for  path, dirs, nondirs in os.walk(topdir):
	   for name in nondirs:
			 fname = os.path.join(path,name)
			 print fname, ' : ',
			 tf = ROOT.TFile(fname)
			 tree = tf.Get('tree')
			 print tree.GetEntries()
			 tf.Close()
			

