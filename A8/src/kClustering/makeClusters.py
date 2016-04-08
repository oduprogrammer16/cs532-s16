#!/usr/local/bin/python

# all code here stolen shamelessly from 
# "Programming Collective Intelligence, Chapter 3"

import sys
import argparse 

sys.path.insert(0, '../libs')

import clusters

i = 0
text_file = ''
number_of_clusters = 0
a = 0

parser = argparse.ArgumentParser(description='Get file name and extension')
parser.add_argument('-f',action='store',dest='text_file',nargs=1,help='Blog data text file')
parser.add_argument('-k',action='store',dest='number_of_clusters',nargs='+',help='Number of Clusters')

a = len(sys.argv) - 4

print a

while i < a:
	args = parser.parse_args()
	if args.text_file:
		text_file = (args.text_file[0])
	if args.text_file:
		number_of_clusters = int(args.number_of_clusters[i])

	blognames,words,data=clusters.readfile(text_file)



#######################################Test Input

#######################################User Defined Intput
	print "For k= " + str(args.number_of_clusters[i])
	kclust=clusters.kcluster(data, k= number_of_clusters)
	print
	print "Clusters"
	for j in range(number_of_clusters):
		print '-----------------------------------------'
		print [blognames[r] for r in kclust[j]]
	i= i + 1