#!/bin/bash

file_path=$1					# BAM file path which you want to test 
dest_path=$2					# Destination folder where results will be stored
plugin_path=$3					# wisecondor parent PATH to run script from anywhere
sample_name=$4                                  # Sample name
run_date=$5                                     # date of the run sequencing
filename=`basename $file_path`
basename=${filename%.*}



#dedup
echo $3 $file_path
$3/sambamba markdup -t 28 -r $file_path $sample_name.dedup.bam # change threads

touch $2/$sample_name.pickle
samtools view $sample_name.dedup.bam -q 1 | python $3/wisecondor/consam.py -outfile $2/$sample_name.pickle

touch $2/$sample_name.gcc
python $3/wisecondor/gcc.py  $2/$sample_name.pickle $3/data/hg19.gccount $2/$sample_name.gcc

touch $2/$sample_name.tested
python $3/wisecondor/test.py $2/$sample_name.gcc $3/data/reftable $2/$sample_name.tested

touch $2/$sample_name.pdf
python $3/wisecondor/plot.py $2/$sample_name.tested  $2/$sample_name

echo "Mean zScore calculation"
python $3/getScore.py $2/$sample_name.tested

#rename output file to add the run date
mv $2/$sample_name.pickle $2/$sample_name"_"$run_date.pickle
mv $2/$sample_name.gcc $2/$sample_name"_"$run_date.gcc
mv $2/$sample_name.tested $2/$sample_name"_"$run_date.tested
mv $2/$sample_name.pdf $2/$sample_name"_"$run_date.pdf
