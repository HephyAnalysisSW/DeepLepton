#! /usr/bin/env python

from __future__ import print_function

import csv
import os

from xattr import xattr

icnt = 0
eos_store = '/eos/vbc/experiments/cms/store'
with open('output.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for checksum, size, path in csv_reader:
        print ( ".", end="", flush=True )
        checksum = int(checksum,16)
        size = int(size)
        path = path.strip()
        fullpath = os.path.join(eos_store,path[1:])
        realsize = os.stat(fullpath).st_size
        if realsize != size:
            print ( 'Size mismatch : {}'.format(path) )
        realchecksum = int( xattr( str(fullpath))['eos.checksum'], 16)
        if realchecksum != checksum:
            print ( 'Checksum mismatch : {}'.format(path) )
        icnt += 1

print ( "\nNr of files: {}".format(icnt) )
        
