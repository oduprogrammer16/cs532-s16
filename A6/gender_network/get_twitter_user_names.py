import credentials.twitter_credentials 
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import signal
import time 
import json

# Finding follower relationships took 4 exactly 4 hours 29 minutes 31.55 seconds

def limit_handled(cursor):
	while True:
		try:
			yield cursor.next()
		except tweepy.RateLimitError:
			print("Rate Limit Exceeded, Sleeping for 15 Minutes\n")
			time.sleep(15 * 60)




def get_names(credentials,screenNames):
	auth = credentials.create_authorization()
	api = tweepy.API(auth)
	userInformation = {}

	# Initialize the dictionary 
	for screenName in screenNames:
		userInformation[screenName] = {'id':None,'screen_name':None,'name':None,'gender':None}
	userInformation['KevinClemmons'] =  {'id':None,'screen_name':None,'name':None,'gender':None}

	counter = 0
	# Get data for each twitter user
	for screenName in userInformation.keys():
		remain = len(userInformation) - counter
		print("Getting username for: {0}, {1} remaining".format(screenName,remain))
		result = None
		try:
			result = api.get_user(screen_name=screenName)
		except tweepy.RateLimitError:
			print("\tRate Limit Exceeded\n")
			# Create a backup file before sleeping for 15 minutes
			print("\tDumping to backup file")
			print("\tSleeping for 15 minutes. ")
			
			with open('data_backup.json','w') as f:
				json.dump(userInformation)
			time.sleep(15 * 60)
			result = api.get_user(screen_name=screenName)

		if result is not None:
			userInformation[screenName]['id'] = result.id
			userInformation[screenName]['screen_name'] = result.screen_name
			userInformation[screenName]['name'] = result.name
			counter += 1 
	
	try:
		result = api.get_user(screen_name='KevinClemmons')
	except tweepy.RateLimitError:
		print("\tRate Limit Exceeded\n")
		# Create a backup file before sleeping for 15 minutes
		print("\tDumping to backup file")
		with open('data_backup.json','w') as f:
			json.dump(userInformation)
		print("\tSleeping for 15 minutes. ")
		time.sleep(15 * 60)
		result = api.get_user(screenName='KevinClemmons')

	if result is not None:
		userInformation['KevinClemmons']['id'] = result.id
		userInformation['KevinClemmons']['screen_name'] = result.screen_name
		userInformation['KevinClemmons']['name'] = result.name

		counter += 1 

	print("Twitter Name Data Retrieved\nDumping data to backup")
	with open('twitter_user_info.json','w') as f:
		json.dump(userInformation,f)
		#print('\n')

	return userInformation




if __name__=='__main__':
	configFileName = 'blankTwitterCredentials.ini'
	credentialSet = credentials.twitter_credentials.TwitterCredentials(configFileName)

	kevinFile = open('kevin_followers.txt','r')

	kevinFollowers = [] 
	for follower in kevinFile:
		kevinFollowers.append(follower.strip('\n'))

	get_names(credentialSet,kevinFollowers)

	

