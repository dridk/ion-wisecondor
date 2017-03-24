#!/usr/bin/python

import numpy
import os
import sys
import json 
import subprocess 
from multiprocessing.pool import Pool
import glob 
import pickle
from django.template import Context, Template
from django.conf import settings

#print 'Hello World'
#print ("Sys Arg", sys.argv[1])
filePath = sys.argv[1]
#filePath = "/media/raid/DATA/Lagarde_Arnaud/DPNI/IonWisecondor_v2/output/IonXpress_026_2017-03-16.tested"

print "sum Zscore / length Zscore = Mean Zscore"

def scoreOf(testedFile, chrom):
	with open(testedFile) as file:
		data 	= pickle.loads(file.read())
#		print(data)
		zScores = data["zSmoothDict"][chrom]
#		print("Zscore ",zScores,"\n")
		score   = -1
		try:
			score = sum(zScores) / len(zScores)
		except :
			score = -1
			
		print "Chromosome",chrom,":",sum(zScores)," / ", len(zScores), " = ", score
#		print("Len Zscore ",len(zScores))
		
	return round(score,2)

item = {}
scoreOf(filePath, "13")
scoreOf(filePath, "18")
scoreOf(filePath, "21")


























