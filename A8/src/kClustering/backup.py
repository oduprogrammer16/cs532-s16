#!/usr/local/bin/python

# all code here stolen shamelessly from 
# "Programming Collective Intelligence, Chapter 3"

import sys
import argparse 

sys.path.insert(0, '../libs')

import clusters

if __name__ == '__main__':

	textFileName = None 
	blognames = None 
	words = None 
	data = None

	parser = parser = argparse.ArgumentParser(description='Makes a dendrogram in either ascii or jpeg format.')
	parser = argparse.ArgumentParser(description='Get file name and extension')
	parser.add_argument('-f',action='store',dest='text_file',nargs=1,help='Blog data text file')
	parser.add_argument('-k',action='store',dest='number_of_clusters',nargs='+',help='Number of Clusters')

	args = parser.parse_args()

	if args.text_file:
		textFileName = args.text_file[0]
		blognames,words,data=clusters.readfile(textFileName)

	if args.number_of_clusters:
		if data:
			for k in args.number_of_clusters:
				print("For k= {0}".format(k))
				kclust = clusters.kcluster(data,k=int(k))
				for j in range(int(k)):
					print('*' * 41)
					print [blognames[r] for r in kclust[j]]




