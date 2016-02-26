# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import time
import json
import sys 

def limit_handled(cursor):
	while True:
		try: 
			yield cursor.next()
		except tweepy.RateLimitError:
			print("We got a timeout...sleeping for 15 minutes")
			time.sleep(15 * 60)

def get_followers_from_twitter(twitter_credentials,verbose=True):
	auth = tweepy.OAuthHandler(twitter_credentials[u'consumer_key'],twitter_credentials[u'consumer_secret'])
	auth.set_access_token(twitter_credentials[u'access_token'],twitter_credentials[u'access_token_secret'])
	api = tweepy.API(auth)

	
	#user = tweepy.Cursor(api.followers,screen_name=user_name).items()

	if(api.verify_credentials):
		follower_list = []
		if verbose:
			print("Successfully Logged in")
			print("Getting twitter follower list")

		for user in limit_handled(tweepy.Cursor(api.followers,screen_name=str(twitter_credentials['user_name'])).items()):
			usr = user
			follower_list.append(usr.screen_name)
			
		
		return follower_list 
	else:
		if verbose:
			print("Invalid Credentials")
		return []

def get_count_of_followers(twitter_credentials,data=[],verbose=True):
	auth = tweepy.OAuthHandler(twitter_credentials[u'consumer_key'],twitter_credentials[u'consumer_secret'])
	auth.set_access_token(twitter_credentials[u'access_token'],twitter_credentials[u'access_token_secret'])
	api = tweepy.API(auth)
	if(api.verify_credentials):
		follower_data = {}
		if verbose:
			print("Successfully Logged in")
			print("Getting number of followers for each follower")
		if type(data) == list:
			for follower in data:
				try:
					usr = api.get_user(follower)
					follower_data[follower] = {'follower_count':usr.followers_count}
				except:
					if verbose:
						print("We got a timeout...sleeping for 15 minutes\nWARNING: IF YOU TERMINATE THE PROGRAM, FOLLOWER LIST WILL BE LOST\n")
						time.sleep(15*60)
						usr = api.get_user(key)
						follower_data[follower] = {'follower_count':usr.followers_count}
		return follower_data
	else:
		print("Invalid Credentials")
		return {}


if __name__ == '__main__':
	config_file = open('twitter_config.json','r')
	twitter_credent_config = json.loads(config_file.readline())
	#print(twitter_credent_config)
	config_file.close()

	follower_List = get_followers_from_twitter(twitter_credent_config,verbose=True)
	follower_counts = get_count_of_followers(twitter_credent_config,data=follower_List,verbose=True)
	
	with open('twitterFollowerCounts.json','w')as f:
		json.dump(follower_counts,f)
