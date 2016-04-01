import argparse 
import threading 
import math 
from math import sqrt
import logging 

#from data_extractor import read_data_files

from data_extractor.data_set import Data_Set

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',datefmt='%m-%d %H:%M:%S',filename='film_recomender.log',filemode='w')

defaultLogger = logging.getLogger('default')


PERSON_MODE = 1 # Tells a function that an identifyer is a person.
FILM_MODE = 0 # Tells a function that an identifyer is a film.

def sim_pearson(prefs,p1,p2):
	#This code taken from page 13 in collective intelligence book

	similarItems={}

	for item in prefs[p1]:
		if item in prefs[p2]:
			similarItems[item] = 1

	# Find the number of elements 
	n = len(similarItems)

	# If they have no items in common return 0
	if n == 0:
		return 0

	# Add up all the preferences 
	sum1 = sum([prefs[p1][it] for it in similarItems])
	sum2 = sum([prefs[p2][it] for it in similarItems])

	# Sum up the squares 
	sum1Sq = sum([math.pow(prefs[p1][it],2) for it in similarItems])
	sum2Sq = sum([math.pow(prefs[p2][it],2) for it in similarItems])

	# Sum up the products 
	pSum = sum([prefs[p1][it] * prefs[p2][it] for it in similarItems])

	# Calculate the pearson score 
	num = pSum - (sum1*sum2/n)

	den = math.sqrt((sum1Sq-pow(sum1,2)/n) * (sum2Sq-pow(sum2,2)/n))
	
	# Check if the denominator is zero
	if den == 0:
		return 0
	
	r = num/den

	return r

# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
  totals={}
  simSums={}
  for other in prefs:
    # don't compare me to myself
    if other==person: continue
    sim=similarity(prefs,person,other)

    # ignore scores of zero or lower
    if sim<=0: continue
    for item in prefs[other]:
	    
      # only score movies I haven't seen yet
      if item not in prefs[person] or prefs[person][item]==0:
        # Similarity * Score
        totals.setdefault(item,0)
        totals[item]+=prefs[other][item]*sim
        # Sum of similarities
        simSums.setdefault(item,0)
        simSums[item]+=sim

  # Create the normalized list
  rankings=[(total/simSums[item],item) for item,total in totals.items()]

  # Return the rankings from highest to lowest
  rankings.sort()
  rankings.reverse()
  #print(rankings)
  return rankings

def transformPrefs(prefs):
  result={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})
      
      # Flip item and person
      result[item][person]=prefs[person][item]
  return result


def calculateSimilarItems(prefs,n=10):
  # Create a dictionary of items showing which other items they
  # are most similar to.
  result={}
  # Invert the preference matrix to be item-centric
  itemPrefs=transformPrefs(prefs)
  c=0
  for item in itemPrefs:
    # Status updates for large datasets
    c+=1
    if c%100==0: print "%d / %d" % (c,len(itemPrefs))
    # Find the most similar items to this one
    scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
    result[item]=scores
  return result

def getRecommendedItems(prefs,itemMatch,user):
  userRatings=prefs[user]
  scores={}
  totalSim={}
  # Loop over items rated by this user
  for (item,rating) in userRatings.items():

    # Loop over items similar to this one
    for (similarity,item2) in itemMatch[item]:

      # Ignore if this user has already rated this item
      if item2 in userRatings: continue
      # Weighted sum of rating times similarity
      scores.setdefault(item2,0)
      scores[item2]+=similarity*rating
      # Sum of all the similarities
      totalSim.setdefault(item2,0)
      totalSim[item2]+=similarity

  # Divide each total score by total weighting to get an average
  rankings=[(score/totalSim[item],item) for item,score in scores.items()]

  # Return the rankings from highest to lowest
  rankings.sort()
  rankings.reverse()

  # Convert tuple to dic

  return rankings

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


def filmRecomendations(ident,result,mode,data,prefList):
	# Get recomendations
	
	if mode == PERSON_MODE:
		defaultLogger.info("Getting Recomendations for person {0}".format(ident))
		
		# Get recomendations for a person
		res = getRecommendations(prefList,ident)
		defaultLogger.info("{0} recomendations found for {1}".format(len(res),ident))
		
		result.append({'mode':PERSON_MODE, 'ident':ident,'top_five_recomendations':res[:5],'bottom_five_recomendations':res[len(res)-5:]})

	elif mode == FILM_MODE:
		# Get recomendations for a film
		moviePrefs = transformPrefs(prefList)

		if type(ident) == str:
			defaultLogger.info("Getting Recomendations for film title {0}".format(ident))

		elif type(ident) == int:
			defaultLogger.info("Getting Recomendations for film id {0}".format(ident))
			res = getRecommendations(moviePrefs,ident)
			result.append({'mode':FILM_MODE, 'ident':ident,'top_five_recomendations':res[:5],'bottom_five_recomendations':res[len(res)-5:]})

		else:
			pass
	else:
		pass

def print_recomendations(recomendation,data,outputfile=None,form='text'):
	if recomendation['mode'] == PERSON_MODE:
		
		# Print the heading
		heading1 = ' Recomendations for user: {0} '.format(recomendation['ident'])
		print('{0:-^68}'.format(heading1))

		print('{0:-^68}'.format(' Top Five Recomendations '))
		for i in range(len(recomendation['top_five_recomendations'])):
			identif = recomendation['top_five_recomendations'][i][1]

			moviesWithId = list(filter(lambda x: x['movie_id'] == identif,data.movie_list))
			title = moviesWithId[0]['movie_title']

			print('{rank}) {movie:.<48}{score:<5}'.format(rank=i+1,movie=title,score=recomendation['top_five_recomendations'][i][0]))

		print('{0:-^68}'.format(' Bottom Five Recomendations '))
		for i in range(len(recomendation['bottom_five_recomendations'])):
			identif = recomendation['bottom_five_recomendations'][i][1]

			moviesWithId = list(filter(lambda x: x['movie_id'] == identif,data.movie_list))
			title = moviesWithId[0]['movie_title']
			print('{rank}) {movie:.<48}{score:<5}'.format(rank=i+1,movie=title,score=recomendation['bottom_five_recomendations'][i][0]))
		print('-'*68)
		print('-'*68)
	elif recomendation['mode'] == FILM_MODE:
		heading1 = ' Recomendations for Film '
		print('{0:-^68}'.format(heading1))

		idente = recomendation['ident']
		identList = list(filter(lambda x: x['movie_id'] == idente,data.movie_list))
		fTit = identList[0]['movie_title']

		print('{0:^68}'.format(fTit))
		print('-'*68)

		for i in range(len(recomendation['top_five_recomendations'])):
			identif = recomendation['top_five_recomendations'][i][1]

			moviesWithId = list(filter(lambda x: x['movie_id'] == identif,data.movie_list))
			title = moviesWithId[0]['movie_title']

			print('{rank}) {movie:.<48}{score:<5}'.format(rank=i+1,movie=title,score=recomendation['top_five_recomendations'][i][0]))

		print('{0:-^68}'.format(' Bottom Five Recomendations '))
		for i in range(len(recomendation['bottom_five_recomendations'])):
			identif = recomendation['bottom_five_recomendations'][i][1]

			moviesWithId = list(filter(lambda x: x['movie_id'] == identif,data.movie_list))
			title = moviesWithId[0]['movie_title']
			print('{rank}) {movie:.<48}{score:<5}'.format(rank=i+1,movie=title,score=recomendation['bottom_five_recomendations'][i][0]))
		print('-'*68)
		print('-'*68)

		#print()
	pass



if __name__ == '__main__':
	# Data needed for the program
	data = Data_Set()

	prefList = get_prefs(data)


	threadList = [] # List of threads so that the program can run concurrent processes

	userIds = [] # ids of the users to get recomendations for.
	films = [] # Film titles or ids to get recomendations for. 

	results = [] # Results from the recomendations. 


	# Command line arguments parsing 
	parser = argparse.ArgumentParser(description='Generates Recomendations for Films')

	# Option to generate recomendations for user ids. 
	parser.add_argument('-u','--user',action='store',nargs='+',dest='user_id',help='Generates recomendations for a user id in a dataset.')

	# Option to generate recomendations based on film titles.
	parser.add_argument('-fT','--film_title',action='store',nargs='+',dest='film_title',help='Generates recomendations based on ratings for a particular title of a film.')
	
	# Options to generate recomendations based on film ids.
	parser.add_argument('-fId','--film_id',action='store',nargs='+',dest='film_id', help='Generates recomendations based on ratings for a particular id of a film.')
	
	# Parser 
	# Parse the arguments 
	args = parser.parse_args()

	

	if args.user_id:
		defaultLogger.info("{0} users to process".format(len(args.user_id)))
		# Convert to list comprehension
		for i in args.user_id:
			#userIds.append(int(i))
			newThread = threading.Thread(target=filmRecomendations,args=(int(i),results,PERSON_MODE,data,prefList))
			threadList.append(newThread)

	if args.film_title:
		#print("Not implemented yet.")
		defaultLogger.info("{0} film titles to process".format(len(args.film_title)))
		for i in args.film_title:
			newThread = threading.Thread(target=filmRecomendations,args=(i,results,FILM_MODE,data,prefList))
			threadList.append(newThread)


	if args.film_id:
		#print("Not implemented yet")
		defaultLogger.info("{0} film ids to process".format(len(args.film_id)))
		for i in args.film_id:
			newThread = threading.Thread(target=filmRecomendations,args=(int(i),results,FILM_MODE,data,prefList))
			threadList.append(newThread)

	# Get recomendations for the users 
	for thread in threadList:
		thread.start()

	# Wait for all the threads to stop
	while True:
		if len(filter(lambda t: t.is_alive(),threadList)) == 0:
			break


	#print(results[0]['top_five_recomendations'])
	for result in results:
		print_recomendations(result,data)
	#print_recomendations(results[0])
	#print(len(results[0]['recomendations']))
	# Get recomendations for the films 
	#for i in films:
	#	filmRecomendations(i,results,FILM_MODE,dataList,userList,itemList,prefList)
