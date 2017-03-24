#!/usr/bin/env python
from ion.plugin import * 
import os
import sys
import json 
import subprocess 
import glob 
import pickle
from django.template import Context, Template
from django.conf import settings

class IonWisecondor_v2(IonPlugin):
	""" IonWisecondor_v2"""
	version = "2.0"
	allow_autorun = False
	author = "sacha@labsquare.org"
	envDict = dict(os.environ)
	
	def launch(self, data=None):
		print("Launch started...")
		
		# ================ GET GLOBAL PATH
		self.outputDir 		= os.environ["RESULTS_DIR"];  # The wisecondor results directory
		self.analysisDir 	= os.environ["ANALYSIS_DIR"];
		self.pluginDir		= os.environ["PLUGIN_PATH"];
		self.urlRoot 		= os.environ["URL_ROOT"]   # /output/Home/X/
		self.urlPlugin 		= os.environ["TSP_URLPATH_PLUGIN_DIR"] # /output/Home/X/plugin_out/IonWisecondor
		self.date               = os.environ["TSP_ANALYSIS_DATE"]
		
		# ================ GET INSTANCE PARAMETERS AND STORE THEM IN A LIST 
		fileCount = int(os.environ["PLUGINCONFIG__COUNT"])
		files = []
		for i in range(fileCount):
			item       	= {}
			key        	= "PLUGINCONFIG__ITEMS__"+str(i)
			barcode    	= os.environ[key+"__BARCODE"]
			sample	   	= os.environ[key+"__SAMPLE"]
			input 		= self.analysisDir +"/" + barcode + "_rawlib.bam"
			
			sample = sample.replace(' ', '_')
			
			item["sample"] 	= sample
			item["barcode"] = barcode
			item["input"] 	= input
			item["pickle"] 	= self.urlPlugin + "/" + sample + "_" + self.date +".pickle" 
			item["gcc"] 	= self.urlPlugin + "/" + sample + "_" + self.date +".gcc" 
			item["tested"] 	= self.urlPlugin + "/" + sample + "_" + self.date +".tested" 
			item["pdf"] 	= self.urlPlugin + "/" + sample + "_" + self.date +".pdf"
			
			files.append(item)
			
		# ================ LOOP ON EACH FILES AND START COMPUTATION 
		for item in files:

			# dereplication 
			cmd_dereplication = "{pluginDir}/sambamba markdup -r -t 10 {bam} {sample}.derep.bam".format(bam=item["input"], pluginDir = self.pluginDir,sample = item["sample"])
			self.jobLauncher(cmd_dereplication)
			

			# pickle
			cmd_pickle = "samtools view {sample}.derep.bam -q 1 | python {pluginDir}/wisecondor/consam.py -outfile {outputDir}/{sample}_{date}.pickle".format(bam=item["input"], pluginDir = self.pluginDir, outputDir = self.outputDir, sample = item["sample"], date= self.date)
			self.jobLauncher(cmd_pickle)
			
			# gcc
			cmd_gcc = "python {pluginDir}/wisecondor/gcc.py  {outputDir}/{sample}_{date}.pickle {pluginDir}/data/hg19.gccount {outputDir}/{sample}_{date}.gcc".format(pluginDir = self.pluginDir, outputDir = self.outputDir, sample = item["sample"], date= self.date)
			self.jobLauncher(cmd_gcc)
			
			# tested
			cmd_tested = "python {pluginDir}/wisecondor/test.py {outputDir}/{sample}_{date}.gcc {pluginDir}/data/reftable {outputDir}/{sample}_{date}.tested".format(pluginDir = self.pluginDir, outputDir = self.outputDir, sample = item["sample"], date= self.date)
			self.jobLauncher(cmd_tested)
			
			# pdf
			cmd_pdf = "python {pluginDir}/wisecondor/plot.py {outputDir}/{sample}_{date}.tested  {outputDir}/{sample}_{date}".format(pluginDir = self.pluginDir, outputDir = self.outputDir, sample = item["sample"], date= self.date)	
			self.jobLauncher(cmd_pdf)
			
			# get score
			filePath = os.environ["RESULTS_DIR"] + "/" + item["sample"] + "_" + self.date + ".tested"
			item["s21"] = self.scoreOf(filePath, "21")
			item["s18"] = self.scoreOf(filePath, "18")
			item["s13"] = self.scoreOf(filePath, "13")
		
		# ================ GENERATE RESULTS HTML FROM DJANGO TEMPLATE SYSTEM
		settings.configure()
		source = open(os.environ["RUNINFO__PLUGIN__PATH"] + "/block_template.html", "r").read()
		t = Template(source)
		# Pass files arguments to the template 
		c = Context({'files': files})
		html = t.render(c)
		# Output html render 
		f = open(self.outputDir+"/resultat_block.html","w")
		f.write(html)
		f.close()

	def scoreOf(self, testedFile, chrom):
		with open(testedFile) as file:
			data 	= pickle.loads(file.read())
			zScores = data["zSmoothDict"][chrom]
			score   = -1
			try:
				score = sum(zScores) / len(zScores)
			except :
				score = -1
		return round(score,2)
	
	def jobLauncher(self, cmd):
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		stdout, stderr = p.communicate()
		if p.returncode == 0:
			print(stdout)
		else:
			raise Exception(stderr)

if __name__ == "__main__":
  PluginCLI()
