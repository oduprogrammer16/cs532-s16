

import credentials.twitter_credentials 
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy


if __name__=='__main__':
	configFileName = 'blankTwitterCredentials.ini'
	credentialSet = credentials.twitter_credentials.TwitterCredentials(configFileName)
	
	print(str(credentialSet))

	# Create an authorization with the twitter credentials.
	auth = credentialSet.create_authorization()
	api = tweepy.API(auth)
	try:
		api.verify_credentials()
		print("Successfully logged in.")
	except: 
		pass

