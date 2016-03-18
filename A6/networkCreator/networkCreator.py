import credentials.twitter_credentials 
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import signal
import time 

# Finding follower relationships took 4 exactly 4 hours 29 minutes 31.55 seconds
edgeList = []

unknownEdges = []
def limit_handled(cursor):
	while True:
		try:
			yield cursor.next()
		except tweepy.RateLimitError:
			print("Rate Limit Exceeded, Sleeping for 15 Minutes\n")
			time.sleep(15 * 60)




	#for personFollowing in followerList:



def printEdgeList(edList,edgeListFile):
	edgeFile = open(edgeListFile,'w')

	for edge in edList:
		toPrint = edge[0] + "," + edge[1] + ',1.1\n'
		edgeFile.write(toPrint)

	print("Edge list written to: {0}".format(edgeListFile))

# Create a list of tuples in the format 
# (personFollowing,personBeingFollowed)
def createGraph(credentials,followerList):
	auth = credentials.create_authorization()
	api = tweepy.API(auth)
	#for follower in followerList:
	#	getEdgesForFollower(credentials,follower,followerList)
	numFollowers = len(followerList)
	processedUsers = 0
	for user in followerList:

		print("Getting Edges for user: {0}".format(user))
		current2 = 0
		for follower in followerList:
			

			if follower != user:
				current2 += 1 
				remain = numFollowers - current2
				print("\tProcessing: {0}, {1} followers remaining".format(follower,remain ))
				result = None
				try:
					result = api.show_friendship(source_screen_name=user,target_screen_name=follower)
				except tweepy.RateLimitError:
					printEdgeList(edgeList,'kevin_network.csv')
					printEdgeList(unknownEdges,'unknownEdges.csv')
					print("\t\tRate Limit Error Exceeded: sleeping for 15 minutes")
					time.sleep(15 * 60)
					result = api.show_friendship(source_screen_name=user,target_screen_name=follower)
				except tweepy.TweepError as e:
					#print(e.response.status)
					pass

				if result is not None:
					if result[1].following:
						edgeList.append((follower,user))
				else:
					unknownEdges.append((follower,user))
		processedUsers +=1
		ress = numFollowers - processedUsers
		printEdgeList(edgeList,'kevin_network.csv')
		printEdgeList(unknownEdges,'unknownEdges.csv')

		print("Finished processing {0}, {1} remaining followers".format(user,ress))
# Username: The username to retrieve a list of followers
def retrieveFollowers(credentials,userName=None):
	# Create an authorization with the twitter credentials.
	auth = credentials.create_authorization()
	api = tweepy.API(auth)
	followerList = []
	verificationValue = None
	
	usr = userName
	if usr == None:
		usr = credentials.user_name
		
	print("Creating List of Followers for: {0}".format(usr))
	#
	for follower in limit_handled(tweepy.Cursor(api.followers,screen_name=usr).items()):
		print("\tAdding: {0}".format(follower.screen_name))
		followerList.append(follower.screen_name)
	return followerList

def printFollowerList(followerList,fileName):
	out = open(fileName,'w')
	for follower in followerList:
		toPrint = follower +'\n'
		out.write(toPrint)
	out.close()

if __name__=='__main__':
	configFileName = 'blankTwitterCredentials.ini'
	credentialSet = credentials.twitter_credentials.TwitterCredentials(configFileName)

	followers = retrieveFollowers(credentialSet)
	#print("Printing followers list")
	#printFollowerList(followers,'nelson_followers.txt')

	kevinFile = open('kevin_followers.txt','r')
	#kevinFile = open('nelson_followers.txt','r')
	kevinFollowers = [] 
	for follower in kevinFile:
		kevinFollowers.append(follower.strip('\n'))
		#print(follower)

	createGraph(credentialSet,kevinFollowers)

	

