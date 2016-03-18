# -*- coding: utf-8 -*-
import signal
import time 
import json
from gender_detector import GenderDetector
import csv











def determineGenders(twitterUserData):
	detector = GenderDetector('us')
	for screenName in twitterUserData.keys():
		print("Getting gender for: {0} ".format(screenName))
		nam = twitterUserData[screenName]['name']
		#print(nam)
		toCheck = None
		if nam != '.':
			if " " in nam:
				toCheck = nam.split(" ")[0]

			if toCheck is not None:
				twitterUserData[screenName]['gender'] = detector.guess(toCheck)
			else:
				print(nam)
				twitterUserData[screenName]['gender'] = detector.guess(nam)


	print("Creating backup file:")
	with open('backup2.json','w') as f:
		json.dump(twitterUserData,f)
		#print(twitterUserData)

	print("Results")
	for result in twitterUserData.keys():
		print(result)
		print("\tid: {0}".format(result))
		print("\tscreenName: {0}".format(twitterUserData[result]['screen_name']))
		print("\tgender: {0}".format(twitterUserData[result]['gender']))
	return twitterUserData

# Determine which users don't have an assigned gender
def usersWithNoGender(twitterData):
	screenNamesToEliminate = []
	for sName in twitterData.keys():
		if twitterData[sName]['gender'] == 'unknown':
			print("{0}: {1}".format(sName,twitterData[sName]['gender']))
			screenNamesToEliminate.append(sName)
	return screenNamesToEliminate

# Check to see  if the name needs to be eliminated.

def eliminateName(userName,twitData):
	if twitData[userName]['gender'] == 'unknown' or twitData[userName]['gender'] is None:
		return True  
	else:
		return False 

def reviseCSV(csvFileName,twitterUsrData,newCSVFileName):
	oldCSVResults = []
	newCsvResilts = []

	with open(csvFileName) as csvFile:
		reader = csv.DictReader(csvFile)
		for row in reader:
			#print(row['source'],row['target'])
			# If both nodes are not in the list of users to eliminate, then add the edge to the new set of csv results
			#print(eliminateName(row['source'],nodesToEliminate))
			if eliminateName(row['source'],twitterUsrData) is False and eliminateName(row['target'],twitterUsrData) is False:
				newCsvResilts.append((row['source'],row['target']))

	newOut = open(newCSVFileName,'w')
	headings = 'source,target,value\n'
	newOut.write(headings)
	for item in newCsvResilts:
		tmp = item[0] + ',' + item[1] + ',1.0\n'
		newOut.write(tmp)
	newOut.close()

	# Create a table of users and their genders 
	#v = open('gender_user_table.txt','w')
	#t = open('no_gender_table.txt','w')
	for sName in twitterUsrData.keys():
		if eliminateName(sName,twitterUsrData) is not True:
			tmp = twitterUsrData[sName]['screen_name'] + u" & " + twitterUsrData[sName]['name'] + u" & " + twitterUsrData[sName]['gender'] + u' \ \ \hline '
			print(tmp)
			#v.write(tmp)
		else:
			tmp = twitterUsrData[sName]['screen_name'] + " & " + twitterUsrData[sName]['name'] + u"\ \ \hline "
			#print(tmp)
			#t.write(tmp)
	#v.close()
	#t.close() 


if __name__=='__main__':
	global twitter_user_data
	
	kevinFollowers = [] 

	dataFileName = 'twitter_user_info.json'

	twitter_data_file = open(dataFileName,'r')
	twitter_user_data = json.loads(twitter_data_file.readline())
	
	#print(twitter_user_data)
	twitter_data_file.close()

	oldCsvFile = 'kevin_network.csv'
	newCsv = 'kevin_gender_network.csv'

	twitterData = determineGenders(twitter_user_data)

	reviseCSV(oldCsvFile,twitterData,newCsv)





