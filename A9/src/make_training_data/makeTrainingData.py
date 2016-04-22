import feedparser 
import ConfigParser
import unicodedata
import sys 



def promptForCategory(entry,categoryList,numClassified,size):
	#print()
	num = None
	categoryDisp = list(enumerate(categoryList))
	minimum = categoryDisp[0][0]
	maximum = categoryDisp[len(categoryDisp)-1][0]

	

	while True:
		heading = 'Entry: {0}\n'.format(entry['guid'])
		print('{0:-^72}'.format(heading))
		descript = entry.description
		parsed = unicodedata.normalize('NFKD', descript).encode('ascii','ignore')
		print('| {0}\n'.format(parsed))

		# Compute statistics
		pctg = 0
		if numClassified == 0:
			pctg = 0
		else:
			pctg = (float(numClassified)/float(size)) * 100

		print('{0:-^72}'.format('Stats'))
		print('Classified {0} of {1} entries ({2} % )'.format(numClassified,size,pctg))

		# List categories to classify the topics 
		
		print('{0:-^72}'.format('Categories'))
		for i in enumerate(categoryList):
			line = '({0}) {1}'.format(i[0],i[1])
			print(line)
		print('(-1) Exit')
		print('{0:-^72}'.format('Choose a Category'))
		category = input("> ")
		
		# Calidate input 
		num = int(category)
		if num == -1:
			break
		elif num in range(minimum-1,maximum+1):
			break 
		else:
			print("Error: Please choose a valid number")
	return num


	pass

def createTrainingData(feed,categoryList,trainingDataFileList=None):

	dataFeed = feedparser.parse(feed)
	categorizedEntries = {} # entriesToFeed[id] = {'feed','category'}
	integersToCategories = {} # Maps an integer to a category 
	
	 # Create integers to categories 
	for i in enumerate(categoryList):
		integersToCategories[i[0]] = i[1]
	#print(integersToCategories)
	size = len(dataFeed.entries)
	numClassified = 0
	for e in dataFeed.entries:
		result = promptForCategory(e,categoryList,numClassified,size)
		if result == -1:
			break
		else:
			categorizedEntries[e['guid']] = {'feed':e,'category':integersToCategories[result]}
			numClassified += 1

	print('Name of the file to save categorized data')
	name = raw_input("> ")

	tmp = open(str(name),'w')
	for i in categorizedEntries.keys():
		tmp.write('{0}|{1}\n'.format(i,categorizedEntries[i]['category']))
	tmp.close()

	print('Classified Data saved to: {0}'.format(name))
		#print(e)

if __name__ == '__main__':
	# Read the configueratio settings 
	config = ConfigParser.ConfigParser()
	#config.read(str('../classiferSettings.ini'))
	#feedFileName = str(config.get('feedInformation','file'))
	#fullTrainingDataFileName = str(config.get('training','fullTrainingData'))
	#databaseName = str(config.get('training','database'))
	#categoryListFile = str(config.get('training','categoryList'))

	#databaseName = 
	# Get a list of categories  
	feedFileName = '../newsfeeds/sportsWorldNews/sportsworldnewsfeed.xml'
	categoryListFile = '../config/categoryList.txt'
	categoryList = None
	try:
		categoryFile = open(categoryListFile,'r')
		categoryList = [category.strip('\n') for category in categoryFile.readlines()]
		#categoryList = [str(category.strip('\r')) for category in categoryList]

	except IOError as e:
		sys.stderr.write("Error opening {0}, {1}\n".format(categoryListFile,e[1]))


	createTrainingData(feedFileName,categoryList)