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

def classifyEntries(settings):
	database = FeedDatabase(settings['database'])
	unclassifiedEntries = database.get_unpredicted_entries()
	#for i in unclassifiedEntries:
	#	print(i)
	#print(len(unclassifiedEntries))
	database.close_database()

	classifier = fisherclassifier(getwords)
	classifier.setdb(settings['database'])
	counter = 0
	size = len(unclassifiedEntries)
	results = []
	for entr in unclassifiedEntries:
		a = open('resul2.txt','w+')
		for i in results:
			a.write('{0}|{1}\n'.format(i['guid'],i['category']))
		a.close()
		category = classifier.classify(entr['description'])
		#print('{0}|{1}'.format(entr['guid'],category))
		results.append({'guid':entr['guid'],'category':category})

		counter += 1 
		sys.stderr.write('...Classified {0} of {1} entries\n'.format(counter,size))



if __name__ == '__main__':
	settings = getSettings()
	classifyEntries(settings)