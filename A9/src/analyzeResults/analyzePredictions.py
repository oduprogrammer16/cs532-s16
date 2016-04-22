# -*- coding: UTF-8 -*-
import sys
sys.path.insert(0,'../lib')
sys.path.insert(0,'../databases/sportsworldnews')
import unicodedata 
import ConfigParser
import feedparser 
import sqlite3

from docclass import fisherclassifier
from docclass import getwords 
from feedfilter import entryfeatures

from feedDatabase import FeedDatabase

def parseResults(resultFileName):
	results = None
	try:
		f = open(resultFileName,'r')
		#results = [{'ident':line.split('|')[0],'category':line.split('|')[1].strip('\n')} for line in f.readlines()]
		results = []
		for i in f.readlines():
			ii = i.replace('\r','')
			ii = ii.strip('\n')
			tmp = ii.split('|')
			iden = tmp[0]
			#cat = tmp[1].replace(' ','')
			cat = tmp[1].strip('\n')
			#cat2 = cat.strip('\n')
			results.append({'ident':iden,'category':cat})
		f.close()
	except IOError as e:
		sys.stderr.write('Error opening result file : {0}, {1}\n'.format(resultFileName,e[1]))

	return results 

def getSettings(sectionName='sportsWorldNews',configFileName='../config/predictorConfig.ini'):
	# Get settings from config file
	conf = ConfigParser.ConfigParser()
	files = None
	try:
		files = {}
		v = open(configFileName)
		v.close()
		cnf = ConfigParser.ConfigParser()
		cnf.read(configFileName)
		options = cnf.options(sectionName)
		for option in options:
			files[option] = str(cnf.get(sectionName,option))

	except IOError as e:
		sys.stderr.write('Error opening config file {0}, {1}\n'.format(configFileName,e[1]))

	return files

def readCategorizedData(fileName):
	# Read feed file with guid and categories
	categorizedFeeds = None

	try:
		f = open(fileName,'r')
		categorizedFeeds = {}
		for line in f.readlines():
			line = line.replace('\r','')
			line = line.strip('\n')
			tmp = line.split('|')
			iden = tmp[0]
			cat = tmp[1]
			categorizedFeeds[iden] = {'category':cat,'title':None,'description':None,'guid':iden}
	except IOError as e:
		sys.stderr.write('Error opening categorized file {0}, {1}\n'.format(fileName,e[1]))

	return categorizedFeeds

def analyzeResults(settings,resuls):
	#database = FeedDatabase(settings['database'])
	classifier = fisherclassifier(getwords)
	classifier.setdb(settings['database'])
	counter = 0
	size = len(resuls.keys())
	for resul in resuls.keys():
		#sys.stderr.write()
		# Get the actual category and description of the blog entry 
		query = "SELECT actualcategory,description,title FROM feeds WHERE guid='{0}'".format(resuls[resul]['guid'])
		query = classifier.con.execute(query).fetchone()
		actCatgory = query[0]
		descrip = query[1]

		#print(query)
		#print(qResult[0])
		cProb = -1
		fProb = -1
		#print(descrip)
		#print(cprob)
		fProb = classifier.fisherprob(descrip,actCatgory)

		guid = resuls[resul]['guid']
		predictedCategory = resuls[resul]['category']
		tit = unicodedata.normalize('NFKD', query[2]).encode('ascii','ignore')
		tit = tit.replace('&','\&')
		#print('{0}|{1}|{2}|{3}'.format(guid,predictedCategory,actCatgory,fProb))
		print('{0} & {1} & {2} & {3} \\\\\\hline'.format(tit,predictedCategory,actCatgory,fProb))
		#classifier.con.execute('''INSERT INTO predictedEntries VALUES (?,?,?,?)''',(guid,predictedCategory,fProb,cprob))
		#classifier.con.commit()

		#print(len(qResult))
	qry = ""
	report = [{''}]




if __name__ == '__main__':
	settings = getSettings()
	catgorizedResulFile = '../classify_feed/resul2.txt'
	resul = readCategorizedData(catgorizedResulFile)
	analyzeResults(settings,resul)
