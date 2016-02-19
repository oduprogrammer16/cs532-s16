# -*- coding: utf-8 -*-
import os 
import sys 
import subprocess 
import json 

def command(fileName):
	m_fileName = fileName.strip('.txt')
	return "lynx -dump -force_html " + fileName + " > " + m_fileName +".processed.txt"

def strip_html_from_sources(input_file_name):
	input_file = open('linksToFiles.json','r')
	linksToFiles = json.loads(input_file.read())
	#strip_html_from_sources(linksToFiles)

	n_link_files = {}
	for link in linksToFiles.keys():
		print("Stripping html from: {0}".format(linksToFiles[link]['source_file_name']))
		v = os.popen(command(linksToFiles[link]['source_file_name']))
		m_fileName = linksToFiles[link]['source_file_name'].strip('.txt')
		m_fileName = m_fileName +".processed.txt"
		info = {'source_file_name':linksToFiles[link]['source_file_name'], 'stripped_source_file_name': m_fileName }
		n_link_files[link] = info

	with open('linksToFiles2.json','w')as f:
		json.dump(n_link_files,f)

	a = open('linksToFiles2Readable.json','w')
	a.write(json.dumps(n_link_files,indent=4))




if __name__ == '__main__':
	fName = 'linksToFiles.json'
	strip_html_from_sources(fName)