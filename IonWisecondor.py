#!/usr/bin/python
from ion.plugin import * 
import os
import sys
import json 
import subprocess 
from multiprocessing.pool import Pool
import glob 

from django.template import Context, Template
from django.conf import settings
settings.configure()


class IonWisecondor(IonPlugin):
	version = "1.0"
	allow_autorun = False
	author = "sacha@labsquare.org"
	envDict = dict(os.environ)
		
	


	def launch(self, data=None):
		print("Launch started...")

		#For debugging... 
		if "RESULTS_DIR" not in os.environ:
			self.outputDir = "/home/ionadmin/result_dir"
			self.rootDir="/home/ionadmin/root_dir"
		else:
			self.outputDir = os.environ["RESULTS_DIR"];  # The wisecondor results directory
			self.analysisDir = os.environ["ANALYSIS_DIR"];
			self.pluginDir = os.environ["PLUGIN_PATH"];
			self.urlRoot = os.environ["URL_ROOT"]   # /output/Home/X/
			self.urlPlugin = os.environ["TSP_URLPATH_PLUGIN_DIR"] # /output/Home/X/plugin_out/IonWisecondor



			print(os.environ["PLUGINCONFIG__COUNT"])

			

		#=================Set files dictionnary to send to html report template 
		fileCount = int(os.environ["PLUGINCONFIG__COUNT"])
		files = []
		for i in range(fileCount):
			item       	= {}
			key        	= "PLUGINCONFIG__ITEMS__"+str(i)
			barcode    	= os.environ[key+"__BARCODE"]
			sample	   	= os.environ[key+"__SAMPLE"]
			path 		= self.analysisDir +"/" + barcode + "_rawlib.bam"

			item["sample"] 	= sample
			item["barcode"] = barcode
 			item["key"]  	= key
			item["path"] 	= path 
			# item["name"] = os.path.splitext(os.path.basename(path))[0]
			item["pickle"] 	= self.urlPlugin + "/" + barcode +"_rawlib.pickle" 
			item["gcc"] 	= self.urlPlugin + "/" + barcode +"_rawlib.gcc" 
			item["tested"] 	= self.urlPlugin + "/" + barcode +"_rawlib.tested" 
			item["pdf"] 	= self.urlPlugin + "/" + barcode +"_rawlib.pdf" 

 			files.append(item)

		# ====================Start Computation 

		for item in files:
			cmd = self.pluginDir+"/run.sh %s %s %s" % (item["path"], self.outputDir, self.pluginDir)
			print(cmd)
			p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			stdout, stderr = p1.communicate()

			if p1.returncode == 0:
				print(stdout)
			else:
				raise Exception(stderr)

		# ====================Generate HTML

		source = open(os.environ["RUNINFO__PLUGIN__PATH"] + "/block_template.html", "r").read()
		t = Template(source)
		c = Context({'files': files})
		html = t.render(c)

		f = open(self.outputDir+"/resultat_block.html","w")
		f.write(html)
		f.close()





if __name__ == "__main__":
  PluginCLI(IonWisecondor())

