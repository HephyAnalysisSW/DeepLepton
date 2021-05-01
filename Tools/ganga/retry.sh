#!/bin/bash

max=$1
shift
delay=5
for i in $(seq 0 $max); do
    if [ $i -gt 0 ]; then
        echo "Retry $i/$max in $delay seconds" >&2
        sleep $delay
        delay=$((delay*2))
    fi
    echo "$@"
    "$@" && rc=0 && break
    rc=$?
done

exit $rc
