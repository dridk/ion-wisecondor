#!/usr/bin/python
from ion.plugin import * 
import os
import sys
import json 
from subprocess import *
from multiprocessing.pool import Pool
from django.conf import settings
from django import template
import glob 

class IonWisecondor(IonPlugin):
	version = "1.0"
	allow_autorun = False
	envDict = dict(os.environ)
		
	


	def launch(self, data=None):
		print("bein alors ???")

		#For debugging... 
		if "RESULTS_DIR" not in os.environ:
			self.outputDir = "/home/ionadmin/result_dir"
			self.rootDir="/home/ionadmin/root_dir"
		else:
			self.outputDir = os.environ["RESULTS_DIR"];
			self.rootDir = os.environ["REPORT_ROOT_DIR"];
			self.analysisName = os.environ["TSP_ANALYSIS_NAME"];
	# Retrive instance parameter sended 		
		try:
			with open('startplugin.json', 'r') as fh:
				self.json_data = json.load(fh)
				self.filenames = self.json_data["pluginconfig"]["items"]
				#self.filenames = [self.rootDir+"/"+name+"_rawlib.bam" for name in self.filenames]	
				print(self.filenames)
		except:
			print 'Error reading plugin json.'


	#Create html report 
		
		if not os.path.isdir(self.outputDir):
			print("le dossier n'existe pas...")
			os.makedirs(self.outputDir)
		
#		settings.configure()
#	
#		#load result page
#		t = template.Template('My name is {{ name }}.')
#		c = template.Context({'name': 'Adrian'})
#		print t.render(c)
#		htmlFile = self.outputDir+"/resultat.html"
#		f = open(htmlFile,"w");
#		f.write(t.render(c))
#		f.close()
#

		html = "<html><body>"
		for file in glob.glob("/results/analysis/output/Home/wisecondor/*.pdf"):
			basename = os.path.basename(file)
			if self.analysisName in basename:
				for barcode in self.filenames:
					if barcode in basename:
						html+= "<img src='/site_media/img/gnome-pdf.png'/><a href='/output/Home/wisecondor/"+ basename +"' target='_blank'>"+basename+"</a><br/>"
		

		html += "</body></html>"
		print(html)
		#load block page 
		f = open(self.outputDir+"/resultat_block.html","w")
		f.write(html)
		f.close()








if __name__ == "__main__":
  PluginCLI(IonWisecondor())

