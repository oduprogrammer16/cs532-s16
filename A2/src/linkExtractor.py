#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import simplejson as json
import codecs 
import urllib2
import re 

from timemap import TimeMap
import sys 
from urllib2 import urlopen,URLError, HTTPError

# Extracts a link from a block of text in a tweet  
def extract_single_link(text):
	regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
	match = re.search(regex,text)

	if match:
		return match.group()
	return ''

# Extract links from the tweets
def extract_links(inputFileName):
	print("Processing twitter data...")
	inputfile = open(inputFileName,'r')
	tweets_data = []
	# Read file as json 
	for line in inputfile:
		try:
			tweet = json.loads(line)
			tweets_data.append(tweet)
		except:
			continue
	inputfile.close()


	relaventTweets = filter(lambda tweet: tweet.has_key('text'),tweets_data)

	print("Extracting links...")
	linkList = [] 
	for item in relaventTweets:
		res = extract_single_link(item['text'])

		if res != '':
			linkList.append(res)

	return linkList


def get_redirected_url(url):
	response = None 
	try:
		response = urllib2.urlopen(url).geturl()

	except:
		pass


	return response


def eliminate_duplicate_redirections(linkList,number_of_urls):
	print("Extracting first 1000 uris...\n")
	redirected_links_to_uris = {} # Used to check redirection
	unique_links = {}

	statusExp = re.compile('\/status\/')

	counter = 0 
	for link_index in range(len(linkList)):
		remaining = number_of_urls-counter
		print("{0} links remaining".format(number_of_urls-counter))
		print(linkList[link_index])
		print(" ")
		
		
		url_redirection = get_redirected_url(linkList[link_index])

		
		if url_redirection != None:
			encoded_url = unicode(url_redirection,errors='ignore')
			if encoded_url == url_redirection:
				# Check that it's not a link to a twitter status 
				if not re.search(statusExp,encoded_url):

					# Have we already encountered this url 
					if redirected_links_to_uris.has_key(encoded_url) != True:
						unique_links[linkList[link_index]] = {'shortened_url':linkList[link_index],'redirected_url':encoded_url}
						
						redirected_links_to_uris[encoded_url] = None
						counter = counter + 1 

		if counter > number_of_urls:
			break

	print("Finished Acquiring {0} unique_links".format(number_of_urls))
	print("Saving to json")

	with open('data_set3.json','w') as f:
		json.dump(unique_links,f)

	return unique_links

# Create a request for getting the time map
def create_time_map_request(uri):
	return 'http://mementoproxy.cs.odu.edu/aggr/timemap/link/1/' + uri

def create_time_map_file_name(number):
	return 'mementos/memento_' + str(number) + '.txt'

def requestTimeMap(uriToGet): 
	newTimeMap = None # Stores a new time map object
	
	response = None # Stores response of the request 
	timeMapFile = None # Store the array of content from the memento 
	num_mementos = None # Number of mementos

	# Does a mememento exist
	try:	
		response = urllib2.urlopen(uriToGet)
		timeMapFile = response.readlines()
		response.close()
		#print(timeMapFile)
	except HTTPError as e:
		pass 
	except URLError as e:
		pass
	
	# If response resulted in redirect, get mememnto information
	if response != None:
		
		#print(type(timeMapFile))
		# Create new timeMapObject and extract information
		newTimeMap = TimeMap(data=timeMapFile)

		# How many memento are in the 
		num_mementos = len(newTimeMap.mementos)
 

	return timeMapFile,num_mementos


def retrieve_mementos(dataSet):
	nDataSet = {}

	print("Retrieving time_maps")
	counter = 0
	current = 0
	size = len(dataSet)
	for link in dataSet.keys():
		print("{0} remaining".format((size-current)))
		#print(dataSet[link].keys())
		link_inform = {'shortened_url':dataSet[link]['shortened_url'],'redirected_url':dataSet[link]['redirected_url']}
		

		# Create time_map request 
		print("Requesting time map")
		request = requestTimeMap(create_time_map_request(dataSet[link]['redirected_url']))
		tMapInfo = {'time_map_file_name':None,'number_of_mementos':None,'time_map_found':None}
		if request[0] != None:
			print("Timemap found")
			tMapInfo = {'time_map_file_name': create_time_map_file_name(counter),'number_of_mementos':str(request[1]),'time_map_found':'true'}

			print("Writing time map to file")
			output = open(create_time_map_file_name(counter),'w')
			for line in request[0]:
				toPrint = line
				output.write(toPrint)
			output.close()
			counter = counter + 1

		tmp = {'link_info':link_inform,'time_map_info':tMapInfo}
		nDataSet[link] = tmp
		current = current + 1

	with open('data_set3.json','w') as f:
		json.dump(nDataSet,f)



def mementoData(fileName):
	fileN = open(fileName,'r')

	data_set = json.loads(fileN.read())
	fileN.close()

	memementoCountFile = open('mementoCount.txt','w')
	counter = 0 
	memementoCountFile.write("URI Memento\n")
	for link in data_set.keys():
		if data_set[link]['time_map_info']['time_map_file_name'] != None:
			memementoCountFile.write('{0},{1}\n'.format(data_set[link]['link_info']['redirected_url'],data_set[link]['time_map_info']['number_of_mementos']))
		else:
			memementoCountFile.write('{0},\n'.format(data_set[link]['link_info']['redirected_url']))

	fileN.close()

def generate_dataset(input_file,numberOf_Unique_URIs=1000):
	#links_from_tweets = extract_links(input_file)
	#for link in links_from_tweets:
	#	print(link)
	#data_set = eliminate_duplicate_redirections(links_from_tweets,numberOf_Unique_URIs)

	#fileN = open('data_set2.json','r')

	#data_set = json.loads(fileN.read())

	#data_set = retrieve_mementos(data_set)
	mementoData('data_set3.json')


if __name__ == '__main__':
	#i
	twitter_data = 'twitter_data.txt'
	generate_dataset(twitter_data)
	




	

