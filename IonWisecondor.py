#!/usr/bin/python
from ion.plugin import * 
import os
import sys
import json 
from subprocess import *
from django.conf import settings
from django import template

class IonWisecondor(IonPlugin):
	version = "1.0"
	allow_autorun = False
	envDict = dict(os.environ)
	

	def launch(self, data=None):
		file = open("/tmp/mywisecondor","w")
		file.write("launched...")
		file.write("sacha")
		file.write(json.dumps(data))
 
		self.outputDir = os.environ["RESULTS_DIR"];

		
		try:
			with open('startplugin.json', 'r') as fh:
				self.json_data = json.load(fh)
				print(self.json_data["pluginconfig"])
		except:
			print 'Error reading plugin json.'


		
		if not os.path.isdir(self.outputDir):
			print("le dossier n'existe pas...")
			file.write("le dossier n'existe pas")
			os.makedirs(self.outputDir)

		
		#load results page 
		settings.configure()
		t = template.Template('My name is {{ name }}.')
		c = template.Context({'name': 'Adrian'})
		print t.render(c)
	
		htmlFile = self.outputDir+"/resultat.html"
		f = open(htmlFile,"w");
		f.write(t.render(c))
		f.close()


		#load block page 
		t = template.Template("This is a block {{name}}")
		c = template.Context({'name': 'Adrian'})
		f = open(self.outputDir+"/resultat_block.html","w")
		f.write(t.render(c))
		f.close()






		file.close()


if __name__ == "__main__":
  PluginCLI(IonWisecondor())
  print(os.environ)

