import csv 
import json 



if __name__ == '__main__':
	csvFileName = 'kevin_gender_network.csv'
	genderDataFileName = 'backup2.json'

	genderDataFile = open(genderDataFileName,'r')
	genderData = json.loads(genderDataFile.readline())

	edges = []
	
	with open(csvFileName) as f:
		reader = csv.DictReader(f)
		for row in reader:
			edges.append((row['source'],row['target']))

	#for edge in edges:
	#	print(edge)
	#print(genderData)
	maleToMaleEdges = [] 
	femaleToFemaleEdges = []
	crossGenderEdges = [] 

	for edge in edges:
		uName1 = edge[0]
		uName2 = edge[1]
		#print(uName1)
		gender1 = genderData[uName1]['gender']
		gender2 = genderData[uName2]['gender']

		if gender1 == 'male' and gender2 == 'male':
			maleToMaleEdges.append(edge)

		if gender1 == 'female' and gender2 == 'female':
			femaleToFemaleEdges.append(edge)

		if (gender1 == 'male' and gender2 =='female') or (gender1 == 'female' and gender2 =='male' ):
			crossGenderEdges.append(edge)

	print("Number of femaleToFemaleEdges: {0}".format(len(femaleToFemaleEdges)))
	print("Number of maleToMaleEdges: {0}".format(len(maleToMaleEdges)))
	print("Number of crossGenderEdges: {0}".format(len(crossGenderEdges)))
	print("Total number of edges: {0}".format(len(edges)))
	p = float(len(femaleToFemaleEdges))/float(len(edges))
	q = float(len(maleToMaleEdges))/float(len(edges))
	r = float(len(crossGenderEdges))/float(len(edges))
	print('\n')
	print("p: {0}".format(p))
	print("q: {0}".format(q))
	print("r: {0}".format(r))

	gamma = 2*p*q
	print("gamma: {0}".format(gamma))
