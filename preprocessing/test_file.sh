#!/bin/sh

python test_file.py $1
if [ $? -eq 0 ]
then
  echo "OK:    $1"
else
  echo "NOT OK: $1" 
fi
