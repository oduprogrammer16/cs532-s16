# -*- code: utf-8 -*-
import xml.etree.ElementTree as ET
import sys 
from xml.dom import minidom
import json

# Extracts a node and all of it's attributes
def extractFriend(friendNode):
	Friend = {}
	elements = friendNode.getElementsByTagName('data')
	
	for element in elements:
		Friend[element.attributes['key'].value] = element.firstChild.data
	return Friend


# Extracts data on all of the friends
def extract_friend_data(inputFileName):
	print("Extracting Information on Friends...")
	friendList = {}
	xmldoc = minidom.parse(inputFileName)
	friendNodes = xmldoc.getElementsByTagName('node')

	for friend in friendNodes:
		friend_data = extractFriend(friend)
		friendList[friend.getAttribute('id')] = friend_data


	return friendList

# Determines which data point belongs to Dr. Nelson
def get_nelson_point(array):
	print("Determining which data point belongs to Dr. Nelson...")
	nelY = 0
	nelX = 0
	for line in array:
		if line[1] == 'Michael Nelson':
			nelY = line[0]
			nelX = line[2]

	nelYS = 'nelsonX <- c(' + str(nelX) + ')\n'
	nelXS = 'nelsonY <- c(' + str(nelY) + ')\n'
	return  nelXS, nelYS

# Creates an r-script to generate a graph and statistics on Dr. Nelson's Information
def create_plot_data(friendData):
	print("Preparing plot data...")
	nelsonX = 0
	nelsonY = 0
	sortedArray = []
	output = []
	output = open('FacebookPlot.r','w')

	counter = 0
	for friendKey in friendData.keys():
		if friendData[friendKey].has_key(u'friend_count'):
			
			sortedArray.append([int(friendData[friendKey][u'friend_count']),str(friendData[friendKey]['name'])])
	sortedArray.append([len(friendData),'Michael Nelson'])

	v = sorted(sortedArray,key=lambda x:x[0])

	# Add ids to each data point
	counter = 1
	for line in v:
		line.append(counter)
		counter += 1

	
	x = []
	y = []


	# Create R Vectors 

	for line in v:
		x.append(line[2])
		y.append(line[0])

	vec_seperator = ','

	x_range = 'x_range <- c(1,' + str(x[len(x)-1]) + ')\n'
	y_range = 'y_range <- c(' + str(y[0]) + ',' +  str(y[len(y)-1]) + ')\n \n'

	xvec_string = []
	yvec_string = []

	for line in y:
		yvec_string.append(str(line))

	for line in x:
		xvec_string.append(str(line))


	# Create x and y vector strings 
	xxC = vec_seperator.join(xvec_string)
	yyC = vec_seperator.join(yvec_string)

	x_ve = 'x <- c(' + xxC + ')\n'
	y_ve = 'y <- c(' + yyC + ')\n'

	
	nelsonX,nelsonY = get_nelson_point(v)

	
	print("Generating R. Script...")
	output.write('pdf(\"NelsonPlot.pdf\")\n')
	output.write(x_range)
	output.write(y_range)
	
	output.write(x_ve)
	output.write(y_ve)

	output.write("plot(x_range,y_range,type=\"n\",xlab=\"Friend Id\", ylab=\"Number of Friends in Log Scale\",log=\"y\")\n\n")
	output.write("points(x,y,col=\'blue\',pch=1,lwd=1)\n")
	output.write(nelsonX)
	output.write(nelsonY)
	
	output.write('\n')
	output.write("points(nelsonX,nelsonY,type=\"b\",lty=5,col=\'red\',pch=16);\n")
	output.write("legend(1,1000,c(\"Number of Dr. Nelson's Friends\"),pch=c(16),cex=.8,col=c(\"Red\"))\n")
	output.write("title(\"Facebook Friends Counts\")\n")
	output.write("dev.off()\n")
	

	output.write("paste(\"Mean:\",mean(y))\n")
	output.write("paste(\"Standard Deviation: \",sd(y))\n")
	output.write("paste(\"Median: \",median(y))\n")
	output.write("paste(\"Number of Friends for Dr. Nelson: \",nelsonY)\n")
	output.write("paste(\"Number of Friends Who have More Friends than Dr. Nelson: \", sum(y > nelsonY[1] ))\n")
	output.write("paste(\"Number of Friends Who have Less Friends than Dr. Nelson: \", sum(y < nelsonY[1]))\n")
	output.close()

	print("R-Script Generated.")
if __name__=='__main__':
	fileName = None
	if len(sys.argv) != 2:
		fileName = 'mln.graphml'
	else:
		fileName = str(sys.argv[1])


	data = extract_friend_data(fileName)
	create_plot_data(data)