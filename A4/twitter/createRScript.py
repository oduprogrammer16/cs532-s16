# -*- coding: utf-8 -*-

import json 

# Get the data point for a specific person, i.e. me
def get_kevin_point(array):
	kCountX = 0
	kCountY = 0

	for line in array:
		if line[0] == u'KevinClemmons':
			kCountX = line[2]
			kCountY = line[1]
	kX = str(kCountX)
	kY = str(kCountY)

	xx = 'kevinX <- c(' + kX + ')\n'
	yy = 'kevinY <- c(' + kY + ')\n'

	return xx,yy

def generate_r_script(data,outputFileName):
	
	dataArray = []

	# Parse through the json
	for key in data.keys():
		dataArray.append([key,data[key]['follower_count']])
	dataArray.append(['KevinClemmons',len(dataArray)])

	sortedData = sorted(dataArray,key=lambda x: x[1])
	
	

	# Add ids to the data 
	counter = 1
	for line in sortedData:
		line.append(counter)
		counter += 1

	# Extract only the ids and counts	
	x = []
	y = []
	for line in sortedData:
		x.append(line[1])
		y.append(line[2])

	xStrings = []
	yStrings = []

	# Convert numerical data into strings
	for line in sortedData:
		xStrings.append(str(line[2]))

	for line in sortedData:
		yStrings.append(str(line[1]))

	
	#print(x)
	# Create R. Vectors

	# Range for plot 
	x_range = 'x_range <- c(1' + ',' + xStrings[len(xStrings)-1] + ')\n'
	y_range = 'y_range <- c(' + yStrings[0] + ',' + yStrings[len(yStrings)-1] + ')\n\n'

	# Create the vectors
	vec_seperator = ','
	xxC = vec_seperator.join(xStrings)
	yyC = vec_seperator.join(yStrings)

	# H Vectors with data
	x_ve = 'x <- c(' + xxC + ')\n'
	y_ve = 'y <- c(' + yyC + ')\n\n'

	kevinX, kevinY = get_kevin_point(sortedData)

	output = open(outputFileName,'w')
	output.write('pdf(\"KevinTwitterPlot.pdf\")\n')
	output.write(x_range)
	output.write(y_range)

	output.write(x_ve)
	output.write(y_ve)
	output.write("plot(x_range,y_range,type=\"n\",xlab=\"Follower Id\", ylab=\"Number of Followers in Log Scale\",log=\"y\")\n\n")
	output.write("points(x,y,col=\'blue\',pch=1,lwd=1)\n")
	output.write(kevinX)
	output.write(kevinY)

	output.write('\n')
	output.write("points(kevinX,kevinY,type=\"b\",lty=5,col=\'red\',pch=16);\n")

	output.write("legend(1,35000,c(\"Number of Followers for KevinClemmons\"),pch=c(16),cex=.8,col=c(\"Red\"))\n")
	output.write("title(\"Twitter Follower Counts\")\n")
	output.write("dev.off()\n\n")

	# R-Code to display statistics 
	output.write("paste(\"Mean:\",mean(y))\n")
	output.write("paste(\"Standard Deviation: \",sd(y))\n")
	output.write("paste(\"Median: \",median(y))\n")
	output.write("paste(\"Number of Followers for KevinClemmons: \",kevinY)\n")
	output.write("paste(\"Number of Followers Who have More Followers than KevinClemmons: \", sum(y > kevinY[1] ))\n")
	output.write("paste(\"Number of Followers Who have Less Followers than KevinClemmons: \", sum(y < kevinY[1]))\n")
	output.close()


if __name__ == '__main__':
	import sys 
	if len(sys.argv) >= 3:
		dataFile = sys.argv[1]
		dataToProcess = json.loads(open(dataFile,'r').read())
		outputFile = sys.argv[2]

		generate_r_script(dataToProcess,outputFile)
	else:
		dataFile = 'twitter_follower_counts_test3.json'
		dataToProcess = json.loads(open(dataFile,'r').read())
		#outputFile = sys.argv[2]
		outputFile = 'twitterData.r'
		generate_r_script(dataToProcess,outputFile)