from random import random,randint
import math

def readfile(filename):
  #lines=[line for line in file(filename)]
  lines=[]
  for line in open(filename):
    lines.append(line)
	
  # First line is the column titles
  colnames=lines[0].strip().split('\t')[1:]
  rownames=[]
  data=[]
  for line in lines[1:]:
    p=line.strip().split('\t')
    # First column in each row is the rowname
    rownames.append(p[0])
    # The data for this row is the remainder of the row
    data.append([float(x) for x in p[1:]])
  return rownames,colnames,data
  
def Cosine(v1,v2):
	sumxx, sumxy, sumyy = 0, 0, 0
	for i in range(len(v1)):
		x = v1[i]; y = v2[i]
		sumxx += x*x
		sumyy += y*y
		sumxy += x*y
	return 1-(sumxy/math.sqrt(sumxx*sumyy))
  
def getdistances(data,vec1):
	distancelist=[]
	for i in range(len(data)):
		vec2=data[i]
		distancelist.append((Cosine(vec1,vec2),i))
	distancelist.sort( )
	return distancelist 

def knnestimate(data,vec1,k=3):
	# Get sorted distances
	dlist=getdistances(data,vec1)
	avg=0.0
	# Take the average of the top k results
	for i in range(k):
		idx=dlist[i][1]
		avg+= idx
		#avg+=data[idx]
	avg=avg/k
	return avg
	
blognames,words,data=readfile(r'myblogtermmatrix.txt')
#print(blognames[50])
#print(blognames[44])
print("F-Measure:")
print("\tk={0}: {1}".format(1,knnestimate(data,data[7],k=1)))
print("\tk={0}: {1}".format(2,knnestimate(data,data[7],k=2)))
print("\tk={0}: {1}".format(5,knnestimate(data,data[7],k=5)))
print("\tk={0}: {1}".format(10,knnestimate(data,data[7],k=10)))
print("\tk={0}: {1}\n".format(20,knnestimate(data,data[7],k=20)))

print("Web Science and Digital Libraries:")
print("\tk={0}: {1}".format(1,knnestimate(data,data[90],k=1)))
print("\tk={0}: {1}".format(2,knnestimate(data,data[90],k=2)))
print("\tk={0}: {1}".format(5,knnestimate(data,data[90],k=5)))
print("\tk={0}: {1}".format(10,knnestimate(data,data[90],k=10)))
print("\tk={0}: {1}".format(20,knnestimate(data,data[90],k=20)))