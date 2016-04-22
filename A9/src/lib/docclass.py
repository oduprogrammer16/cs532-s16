# Revised to work with sqlite3
# Table names also revised 
# Author Kevin Clemmons
# Revised on 4/14/15
import sqlite3

import re
import math
import sys
import unicodedata

def getwords(doc):
  splitter=re.compile('\\W*')
  #print doc

  words=[s.lower() for s in splitter.split(doc) 
          if len(s)>2 and len(s)<20]
  # Return the unique set of words only
  return dict([(w,1) for w in words])

class classifier:
  def __init__(self,getfeatures,filename=None):
    # Counts of feature/category combinations
    self.feature_category_combinations={}
    
    # Counts of documents in each category
    self.category_counts={}
    self.getfeatures=getfeatures
    
  def setdb(self,dbfile):
    self.con=sqlite3.connect(dbfile)
    self.con.execute('CREATE TABLE IF NOT EXISTS feature_category_combinations(feature,category,count)')
    self.con.execute('CREATE TABLE IF NOT EXISTS category_counts(category,count)')

  def incf(self,f,cat):
    count=self.fcount(f,cat)
    if count==0:
      self.con.execute("INSERT INTO feature_category_combinations VALUES ('{feature}','{ccat}',1)".format(feature=f,ccat=cat))
    else:
      self.con.execute("UPDATE feature_category_combinations SET count={ccount} WHERE feature='{feat}' AND category='{ccat}'".format(ccount=count+1,feat=f,ccat=cat)) 
  
  # Problem is this function 
  def fcount(self,f,cat):
    res=self.con.execute('SELECT count FROM feature_category_combinations WHERE feature="{0}" AND category="{1}"'.format(f,cat)).fetchone()
    #ss = f.replace("\'",'')
    #ss = f.replace('\"','')
    #query = 'SELECT count FROM feature_category_combinations WHERE feature="{0}" AND category="{1}"'.format(f,cat)
    #print(query)
    #res = self.con.execute(query).fetchone()
    if res==None: return 0
    else: return float(res[0])

  def incc(self,cat):
    count=self.catcount(cat)
    if count==0:
      self.con.execute("INSERT INTO category_counts VALUES ('{ccat}',1)".format(ccat=cat))
    else:
      self.con.execute("UPDATE category_counts SET count={ccount} WHERE category='{ccat}'".format(ccount=count+1,ccat=cat))

  def catcount(self,cat):
    res=self.con.execute('SELECT count FROM category_counts WHERE category="{ccat}"'.format(ccat=cat)).fetchone()
    
    if res==None: return 0
    else: return float(res[0])

  def categories(self):
    cur=self.con.execute('SELECT category FROM category_counts');
    return [d[0] for d in cur]

  def totalcount(self):
    res=self.con.execute('SELECT SUM(count) from category_counts').fetchone();

    if res==None: return 0
    return res[0]

  def train(self,item,cat):
    features=self.getfeatures(item)
    # Increment the count for every feature with this category
    for f in features:
      self.incf(f,cat)

    # Increment the count for this category
    self.incc(cat)
    self.con.commit()

  def fprob(self,f,cat):
    
    if self.catcount(cat)==0: return 0

    # The total number of times this feature appeared in this 
    # category divided by the total number of items in this category
    return self.fcount(f,cat)/self.catcount(cat)

  def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
    
    # Calculate current probability
    basicprob=prf(f,cat)

    # Count the number of times this feature has appeared in
    # all categories
    totals=sum([self.fcount(f,c) for c in self.categories()])

    # Calculate the weighted average
    bp=((weight*ap)+(totals*basicprob))/(weight+totals)
    return bp




class naivebayes(classifier):
  
  def __init__(self,getfeatures):
    classifier.__init__(self,getfeatures)
    self.thresholds={}
  
  def docprob(self,item,cat):
    features=self.getfeatures(item)   

    # Multiply the probabilities of all the features together
    p=1
    for f in features: p*=self.weightedprob(f,cat,self.fprob)
    return p

  def prob(self,item,cat):
    catprob=self.catcount(cat)/self.totalcount()
    docprob=self.docprob(item,cat)
    return docprob*catprob
  
  def setthreshold(self,cat,t):
    self.thresholds[cat]=t
    
  def getthreshold(self,cat):
    if cat not in self.thresholds: return 1.0
    return self.thresholds[cat]
  
  def classify(self,item,default=None):
    probs={}
    # Find the category with the highest probability
    max=0.0
    for cat in self.categories():
      probs[cat]=self.prob(item,cat)
      if probs[cat]>max: 
        max=probs[cat]
        best=cat

    # Make sure the probability exceeds threshold*next best
    for cat in probs:
      if cat==best: continue
      if probs[cat]*self.getthreshold(best)>probs[best]: return default
    return best




class fisherclassifier(classifier):
  def cprob(self,f,cat):
    
    # The frequency of this feature in this category    
   
    clf=self.fprob(f,cat)

    if clf==0: return 0

    # The frequency of this feature in all the categories
    freqsum=sum([self.fprob(f,c) for c in self.categories()])

    # The probability is the frequency in this category divided by
    # the overall frequency
    #print(clf)
    p=clf/freqsum
    
    return p
  def fisherprob(self,item,cat):
    # Multiply all the probabilities together
    p=1
    
    features=self.getfeatures(item)
    for f in features:
      p*=(self.weightedprob(f,cat,self.cprob))

    # Take the natural log and multiply by -2
    fscore=-2*math.log(p)

    # Use the inverse chi2 function to get a probability
    return self.invchi2(fscore,len(features)*2)
  
  def invchi2(self,chi, df):
    #print('invchi2')
    m = chi / 2.0
    sum = term = math.exp(-m)
    for i in range(1, df//2):
        term *= m / i
        sum += term
    return min(sum, 1.0)
  
  def __init__(self,getfeatures):
    classifier.__init__(self,getfeatures)
    self.minimums={}

  def setminimum(self,cat,min):
    self.minimums[cat]=min
  
  def getminimum(self,cat):
    if cat not in self.minimums: return 0
    return self.minimums[cat]

  def classify(self,item,default=None):
    
    # Loop through looking for the best result
    best=default
    max=0.0
    for c in self.categories():
      #print('.........Category: {0}'.format(c))
      p=self.fisherprob(item,c)
      # Make sure it exceeds its minimum
      if p>self.getminimum(c) and p>max:
        best=c
        max=p
    return best


def sampletrain(cl):
  cl.train('Nobody owns the water.','good')
  cl.train('the quick rabbit jumps fences','good')
  cl.train('buy pharmaceuticals now','bad')
  cl.train('make quick money at the online casino','bad')
  cl.train('the quick brown fox jumps','good')
