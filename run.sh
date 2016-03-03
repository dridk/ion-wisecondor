#!/bin/bash


file_path=$1									# BAM file path which you want to test 
dest_path=$2									# Destination folder where results will be stored
plugin_path=$3									# wisecondor parent PATH to run script from anywhere
sample_name=$4                                                                  # Sample name
run_date=$5                                                                     # date of the run sequencing
filename=`basename $file_path`
basename=${filename%.*}


# echo $filename TO $basename.pickle
echo pickle > $2/$sample_name.pickle
samtools view $file_path | python $3/wisecondor/consam.py $2/$sample_name.pickle

# echo $basename.pickle TO $basename.gcc
echo gcc > $2/$sample_name.gcc
python $3/wisecondor/gcc.py  $2/$sample_name.pickle $3/data/hg19.gccount $2/$sample_name.gcc

# echo $basename.gcc TO $basename.tested
echo tested > $2/$sample_name.tested
python $3/wisecondor/test.py $2/$sample_name.gcc $3/data/reftable $2/$sample_name.tested

# echo $basename.tested TO $basename.pdf
echo pdf > $2/$sample_name.pdf
python $3/wisecondor/plot.py $2/$sample_name.tested  $2/$sample_name

#rename output file to add the run date
mv $2/$sample_name.pickle $2/$sample_name"_"$run_date.pickle
mv $2/$sample_name.gcc $2/$sample_name"_"$run_date.gcc
mv $2/$sample_name.tested $2/$sample_name"_"$run_date.tested
mv $2/$sample_name.pdf $2/$sample_name"_"$run_date.pdf