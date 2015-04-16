#!/bin/bash
file_path=$1
dest_path=$2
plugin_path=$3
filename=`basename $file_path`
basename=${filename%.*}




# echo $filename TO $basename.pickle
echo pickle > $2/$basename.pickle
samtools view $file_path|python $3/wisecondor/consam.py $2/$basename.pickle

# echo $basename.pickle TO $basename.gcc
echo gcc > $2/$basename.gcc
python $3/wisecondor/gcc.py  $2/$basename.pickle $3/data/hg19.gccount $2/$basename.gcc

# echo $basename.gcc TO $basename.tested
echo tested > $2/$basename.tested
python $3/wisecondor/test.py $2/$basename.gcc $3/data/reftable $2/$basename.tested

# echo $basename.tested TO $basename.pdf
echo pdf > $2/$basename.pdf
python $3/wisecondor/plot.py $2/$basename.tested  $2/$basename






