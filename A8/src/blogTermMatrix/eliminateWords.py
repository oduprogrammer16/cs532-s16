#!/usr/local/bin/python

import sys
import argparse 

sys.path.insert(0, '../libs')

import clusters
import operator

import pprint

def getWordscores(words, data,verbose):

    wordscores = {}

    for i in range(len(words)):
        if verbose:
            sys.stderr.write('examining ' + words[i] + '\n')
    
        for j in range(len(data)):
    
            if words[i] in wordscores:
                wordscores[words[i]] += data[j][i]
            else:
                wordscores[words[i]] = data[j][i]

    return wordscores

def getTopNWords(wordscores, n,verbose):

    topNWords = []

    # thanks Stack Overflow:
    # http://stackoverflow.com/questions/613183/python-sort-a-dictionary-by-value
    reversedWordscores = sorted(
        wordscores.iteritems(), key=operator.itemgetter(1), reverse=True
        )

    for i in range(n):
        if verbose:
            sys.stderr.write(
                "adding " + reversedWordscores[i][0] + " with a score of "
                    + str(reversedWordscores[i][1]) + '\n'
                )
        topNWords.append(reversedWordscores[i][0])

    return topNWords


if __name__ == '__main__':
    fileName = None
    saveFileName = None
    blognames = None 
    words = None 
    data = None 
    clust = None
    n = 500
    verboseMode = False

    # Set up command line argument parser
    parser = argparse.ArgumentParser(description='Eliminates the top n terms from a blog-term-matrix')
    parser.add_argument('-n',action='store',dest='num_terms',nargs=1,help='Number of terms to eliminate.')
    parser.add_argument('-f',action='store',dest='matrixFile',nargs=1,help='Name of the file containing the blog matrix.')
    parser.add_argument('-v',action='store_true',dest='verb',help='Turn on verbose mode.')
    #parser.add_argument('-o',action='store',dest='storeFile',nargs=1,help='Name of the output to store.')

    # Parse the arguments 
    args = parser.parse_args()
    if args.verb:
        verboseMode = True

    if args.matrixFile:
        fileName = args.matrixFile[0]
        sys.stderr.write('Processing {0}...\n'.format(fileName))
        #blognames,words,data = clusters.readfile('../blogdata1V2.txt')
        blognames,words,data = clusters.readfile(fileName)
        sys.stderr.write('...Finished processing {0}\n'.format(fileName))
    #blognames,words,data = clusters.readfile('../q1/test4.txt')
    
    if data is not None:
        if args.num_terms:
            n = int(args.num_terms[0])

        sys.stderr.write('Eliminating {0} terms...\n'.format(n))
        wordscores = getWordscores(words, data,verboseMode) 

        topNWords = getTopNWords(wordscores, n,verboseMode)

        indexlist = []

        for word in topNWords:
            indexlist.append(words.index(word))

        lines = []

        line = []
        line.append('Blog')

        for i in range(len(words)):

            if i in indexlist:
                line.append(words[i])

        lines.append(line)

        for i in range(len(blognames)):
            line = []
            line.append(blognames[i])

            for j in range(len(words)):
                if j in indexlist:
                    line.append(str(int(data[i][j])))

            lines.append(line)

        sys.stderr.write('...Finished eliminating {0} terms\n'.format(n))
        for line in lines:
            print "\t".join(line)
