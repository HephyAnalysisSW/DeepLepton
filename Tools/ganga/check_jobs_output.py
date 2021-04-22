#! /usr/bin/env python

from __future__ import print_function

import csv
import pathlib

from xattr import xattr

eos_store = pathlib.Path('/eos/vbc/experiments/cms/store')
with open('output.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for checksum, size, path in csv_reader:
        checksum = int(checksum,16)
        size = int(size)
        path = path.strip()
        fullpath = eos_store / path[1:]
        realsize = fullpath.stat().st_size
        if realsize != size:
            print ( f'Size mismatch : {path}' )
        realchecksum = int( xattr( str(fullpath))['eos.checksum'], 16)
        if realchecksum != checksum:
            print ( f'Checksum mismatch : {path}' )
        
