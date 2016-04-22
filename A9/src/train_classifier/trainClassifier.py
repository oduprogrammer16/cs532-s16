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


def extractFeedInformation(settings,categorizedDat=None):
	# Get data from feeds
	data = feedparser.parse(settings['rssfeedfile'])
	for entry in data.entries:
		guid = entry.link
		categorizedDat[guid]['title'] = entry.title #unicodedata.normalize('NFKD', entry.title).encode('ascii','ignore')
		#categorizedDat[guid]['description'] = entry.description#unicodedata.normalize('NFKD',entry.description).encode('ascii','ignore')
		categorizedDat[guid]['description'] = unicodedata.normalize('NFKD',entry.description).encode('ascii','ignore')


def loadFeedInformationToDatabase(settings,allCats):
	# Put feed information in database

	database = FeedDatabase(settings['database'])
	counter = 0
	size = len(allCats)

	for elem in allCats.keys():
		sys.stderr.write('...Uploading... ({0}/{1})\n'.format(counter,size))
		title = allCats[elem]['title']
		guid = elem
		description = allCats[elem]['description']
		categry = allCats[elem]['category']

		database.add_feed_element(title,guid,description,categry)
		counter +=1 
	sys.stderr.write('...Finished Uploading Information to Database\n')
	database.close_database()

def train_classifier(settings,trainingData):
	
	counter = 0
	size = len(trainingData)
	database = FeedDatabase(settings['database'])

	for key in trainingData.keys():
		database.change_classified(key,classified=True)
	database.close_database()


	classifier = fisherclassifier(getwords)
	classifier.setdb(settings['database'])
	for key in trainingData.keys():
		sys.stderr.write('...Training ({0}/{1})...\n'.format(counter,size))
		classifier.train(trainingData[key]['description'],trainingData[key]['category'])
		counter +=1
	sys.stderr.write('...Finished Training Classifier\n')

if __name__ == '__main__':
	settings = getSettings()

	trainingDataFile = 'partialTrainingData.txt'
	allCategories = 'CompleteTrainingData.txt'

	# Put all the feeds and their categories in the database 
	allCats = readCategorizedData(allCategories)
	trainingDat = readCategorizedData(trainingDataFile)

	extractFeedInformation(settings,categorizedDat=allCats)
	for key in trainingDat:
		trainingDat[key]['description'] = allCats[key]['description']
	#extractFeedInformation(settings,categorizedDat=trainingDat)

	sys.stderr.write('Uploading Entries to database...\n')

	loadFeedInformationToDatabase(settings,allCats)

	sys.stderr.write('Training Classifier...\n')
	train_classifier(settings,trainingDat)
