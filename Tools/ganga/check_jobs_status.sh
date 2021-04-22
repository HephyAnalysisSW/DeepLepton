#!/bin/sh

rm -f output.txt

for j in {16..21}
do
    for i in {1..150}
    do
        if [ ! -e "/stash/user/liko/gangadir/workspace/liko/LocalXML/$j/$i/input" ]; then
            continue
        fi
        stdout="/stash/user/liko/gangadir/workspace/liko/LocalXML/$j/$i/output/stdout"
        stderr="/stash/user/liko/gangadir/workspace/liko/LocalXML/$j/$i/output/stderr"
        if [ ! -e $stdout ]; then
            printf "%2.2d:%3.3d: - no output\n" $j $i
            continue
        fi
        grep -q AttributeError $stdout
        if [ $? -eq 0 ]; then
            printf "%2.2d:%3.3d: - Attribute Error\n" $j $i
            continue
        fi
        grep -q NameError $stdout
        if [ $? -eq 0 ]; then
            printf "%2.2d:%3.3d: - Name Error\n" $j $i
            continue
        fi
        printf "%2.2d:%3.3d: - Ok\n" $j $i
        echo $stderr
        awk '/^adler32/ { printf "%s , %10d , /user/liko/skims%s\n",$2,$4,substr($3,55) }' $stderr | tee -a output.txt
    done
done
