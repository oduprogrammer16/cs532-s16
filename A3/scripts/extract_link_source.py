import os 
import sys 
import subprocess 
import json 
def command(link,fileNumber):
	fileName = 'source' + str(fileNumber)
	return "curl " + link + " > " + fileName +".txt"
def extract_link_source(linkList):
	current = 0
	linksToFileNames = {}
	for link in linkList:
		print("Extracting source for ",link)
		v = os.popen(command(link,current))
		theFileName = 'source' + str(current) +'.txt'
		info = {'source_file_name':theFileName}
		linksToFileNames[link] = info

		current = current + 1

	with open('linksToFiles.json','w') as f:
		json.dump(linksToFileNames,f)


if __name__ == '__main__':
	input_file = open('links.txt','r')
	links = input_file.readlines()
	strippedLinks = [] 
	for link in links:
		strippedLinks.append(link.strip('\n'))

	extract_link_source(strippedLinks)
