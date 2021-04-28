#!/bin/sh

rm -f output.txt
rm -f attribute_error.txt
rm -f name_error.txt
rm -f no_output.txt

jobs=$(ls -1 /scratch/liko/gangadir/workspace/liko/LocalXML/ | sort -n)
for j in ${jobs[*]}
do
    for i in {1..150}
    do
        if [ ! -e "/scratch/liko/gangadir/workspace/liko/LocalXML/$j/$i/input" ]; then
            continue
        fi
        stdout="/scratch/liko/gangadir/workspace/liko/LocalXML/$j/$i/output/stdout"
        stderr="/scratch/liko/gangadir/workspace/liko/LocalXML/$j/$i/output/stderr"
        if [ ! -e $stdout ]; then
#            printf "%2.2d:%3.3d: - no output\n" $j $i
            continue
        fi
        grep -q AttributeError $stdout
        if [ $? -eq 0 ]; then
            echo $stdout >> attribute_error.txt
            printf "%2.2d:%3.3d: - Attribute Error\n" $j $i
            continue
        fi
        grep -q NameError $stdout
        if [ $? -eq 0 ]; then
            echo $stdout >> name_error.txt
            printf "%2.2d:%3.3d: - Name Error\n" $j $i
            continue
        fi
        if [ $(grep -c "^adler32" $stderr) -ne 3 ]; then
            echo $stdout >> no_output.txt 
            printf "%2.2d:%3.3d: - Missing output file\n" $j $i
            continue
        fi
        printf "%2.2d:%3.3d: - Ok\n" $j $i
        awk '/^adler32/ { printf "%s , %10d , /user/liko/skims%s\n",$2,$4,substr($3,55) }' $stderr >> output.txt
    done
done
