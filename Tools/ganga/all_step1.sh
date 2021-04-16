#! /bin/sh -x

/cvmfs/ganga.cern.ch/Ganga/install/LATEST/bin/ganga \
	submit_step1 --version v1 --year 2016 --flavour all --sample ALL "$@"
