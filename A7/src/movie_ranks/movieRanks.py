import argparse 
import threading 
import math 
from math import sqrt
import logging 
import time
import urllib2
import operator
from bs4 import BeautifulSoup
#from data_extractor import read_data_files

from data_extractor.data_set import Data_Set
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',datefmt='%m-%d %H:%M:%S',filename='movie_ranking.log',filemode='w+')


defaultLogger = logging.getLogger('default')

def get_prefs(data):
	'''Create a dictionary of people and the movies that they have rated. 
	'''
	# This code taken from page 26 in collective intelligence book
	prefs = {} # A dictionary containing user_ids, 
	movies = {} # A dictionary of movie ids to movie titles

	for movie in data.movie_list:
		movie_id = int(movie['movie_id'])
		movie_title = movie['movie_title']
		movies[movie_id] = movie_title

	

	for dataPoint in data.rating_list:
		user_id = int(dataPoint['user_id'])
		prefs.setdefault(user_id,{})

		movieId = int(dataPoint['item_id'])
		rating = dataPoint['rating']
		
		prefs[user_id][movieId] = float(rating)
	return prefs

def transformPrefs(prefs):
  result={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})
      
      # Flip item and person
      result[item][person]=prefs[person][item]
  return result


# Get rating from url on imdb database
def get_rating(uri):
	numPeople = None 
	rating = None
	resul = None
	request = urllib2.Request(uri)
	response = None
	#print(uri)
	try:
		request.add_header('User-agent','Mozilla 5.10')
		response = urllib2.urlopen(request)
	except urllib2.URLError as e:
		defaultLogger.error("Error retrieving url: {0}, {1}".format(uri,e))
		pass 
	except urllib2.HTTPError as e:
		defaultLogger.error("Error retrieving url: {0}, {1}".format(uri,e))

	if response is not None:
		soup = BeautifulSoup(response,'html.parser')

		# Rating information located in section as below
		# <div class="ratingValue">
		# <strong title="6.9 based on 213,373 user ratings"><span itemprop="ratingValue">6.9</span></strong><span class="grey">/</span><span class="grey" itemprop="bestRating">10</span> </div>
		
		divSec = soup.find_all('div',class_='ratingValue')
		#print(uri)
		strr = None

		try:
			strr = str(divSec[0].strong['title'])
		except: 
			defaultLogger.error("Unable to retrieve rating for {0}".format(uri))
		if strr is not None:
			v = strr.split()
		#print(v)
			rating = float(v[0])
			numPeople = int(v[3].replace(',',''))
		
	return rating,numPeople

def get_ratings(data,backupFileName='imdb_ratings.txt',noRatingsFile='noRatings.txt'):
	defaultLogger.info("Retrieving ratings for {0} urls".format(len(data.movie_list)))
	fileToPrint = open(backupFileName,'w')
	noRatingsFile = open(noRatingsFile,'w')

	rating_list = []
	no_ratings = []
	size = len(data.movie_list)
	counter = 0
	for movie in data.movie_list:
		movie_id = movie['movie_id']
		#print(movie['IMDb_URL'])
		#defaultLogger.info('Gettign rating for: {0}'.format(movie['IMDb_URL']))
		counter += 1
		if movie['IMDb_URL'] != '':
			defaultLogger.info('Gettign rating for: {0}'.format(movie['IMDb_URL']))
			movie_rating, numPeople = get_rating(movie['IMDb_URL'])
			
			
			if movie_rating is not None:
				fileToPrint.write('{movieID}|{rating}|{peopleCount}\n'.format(movieID=movie_id,rating=movie_rating,peopleCount=numPeople))
				rating_list.append({'movie_id':movie_id,'rating':movie_rating,'numPeople':numPeople})
			else:
				no_ratings.append(movie_id)
				noRatingsFile.write('{0}\n'.format(movie_id))
			print('{0} films remaining'.format(len(data.movie_list) - counter))
		else:
			defaultLogger.error("Invalid url for movie {0}".format(movie_id))
			no_ratings.append(movie_id)
		defaultLogger.info('{0} films remaining'.format(len(data.movie_list) - counter))
		defaultLogger.info('{0} Successful Retrieved Ratings'.format(len(rating_list)))
		defaultLogger.info('{0} Failed Retrievals\n'.format(len(no_ratings)))
	fileToPrint.close()
	noRatingsFile.close()
		#counter += 1
		#print('{0} films remaining'.format(len(data.movie_list) - counter))
		#time.sleep(1)

	defaultLogger.info("Finished retrieving ratings")
	defaultLogger.info('{0} Successful Retrieved Ratings'.format(len(rating_list)))
	defaultLogger.info('{0} Failed Retrievals\n'.format(len(no_ratings)))
	
	return rating_list, no_ratings

if __name__ == '__main__':
	data = Data_Set()
	#get_ratings(data)
	#parser = argparse.
	inputFile = open('imdb_ratings.txt','r')
	ratingsSet = []
	for line in inputFile.readlines():
		res = line.strip('\n')
		tmp = line.split('|')
		ratingsSet.append({'movie_id':int(tmp[0]),'rating':float(tmp[1]),'numPeople':int(tmp[2].strip('\n'))})
	#print(ratingsSet)

	prefs = transformPrefs(get_prefs(data))

	#for line in prefs.keys():
	#	print(prefs[line])

	lensMovieRankings = []
	for line in prefs.keys():
		rankingSum = 0 
		for val in prefs[line].keys():
			rankingSum += prefs[line][val]
		avg = float(rankingSum)/float(len(prefs[line].keys()))
		lensMovieRankings.append({'movie_id':line,'avg':avg,'numPeople':len(prefs[line].keys())})


	lensMovieRankings.sort(key=operator.itemgetter('avg','numPeople'))
	#lensMovieRankings.reverse()

	ratingsSet.sort(key=operator.itemgetter('rating','numPeople'))
	#ratingsSet.reverse()
	for line in ratingsSet:
		print(line)

	fileOut = open('vectors.txt','w')
	v1 = '('
	v2 = '('
	deletedMovies = []
	a = open('noRatings.txt','r')
	for line in a.readlines():
		deletedMovies.append(int(line.strip('\n')))

	a.close()
	for ranking in lensMovieRankings:
		if len(list(filter(lambda x: x['movie_id'] == ranking['movie_id'],ratingsSet))) != 0:
			v1 = v1 + str(ranking['avg']) + ','

	for ranking in ratingsSet:
		v2 = v2 + str(ranking['rating']) + ','
	v1 = v1 + ')'
	v2 = v2 + ')'
	fileOut.write(v1)
	fileOut.write('\n')
	fileOut.write(v2)
	fileOut.write('\n')
