# Title: pdfLinks.py
# Description: Lists all the links in a webpage that lead to pdfs and lists their size in bytes
# Date: 1/28/15
# Author: Kevin R. Clemmons 

import urllib2
import urllib
import urlparse
import sys 
import httplib
import errno

from socket import error as SocketError
from bs4 import BeautifulSoup


verboseMode = True # Used to turn on status messages.


# Prints a list of links and whther or not they result in pdfs
def printResults(results):
	print("\nResults")
	for link in results:
		print("{0}".format(link['link'][0]))
		if len(link['link']) > 1:
			print("Redirected to:")
			for i in range(1,len(link['link'])):
				print("...{0}".format(link['link'][i]))
		print("size: {0} bytes\n".format(link['size']))

# If a link results in a pdf, return a number indicating the size
# If a link does not result in a pdf, return None
def linkResultsInPdf(link):
	size = None
	request = urllib2.Request(link)
	response = None 

	try:
		#print("Here")
		#urllib2.urlopen(request)
		request.add_header('User-agent','Mozilla 5.10')
		response = urllib2.urlopen(request)
	
	# Handling exception for error came from site: http://stackoverflow.com/questions/20568216/python-handling-socket-error-errno-104-connection-reset-by-peer
	except SocketError as e:
		if e.errno != errno.ECONNRESET:
			raise # Not error we are looking for
			pass # Handle error here.
	except urllib2.URLError as e:
		pass 
	except urllib2.HTTPError as e:
		pass 

	# If response is not none, then content was found.
	if response != None:
		# If a link results in a pdf, get the size of the link 
		if 'pdf' in response.info().getheader('Content-Type'):
			size = response.info().getheader('content-length')

	return size 

# Original Function came from page: http://www.zacwitte.com/resolving-http-redirects-in-python
# If a link results in redirect, continue to descend the url until it terminates
def resolve_http_redirect(url, depth=0,directed_path=[]):
    directed_path.append(url)
    o = urlparse.urlparse(url,allow_fragments=True)
    conn = httplib.HTTPConnection(o.netloc)
    path = o.path
    #if o.query:
    #    path +='?'+o.query
    conn.request("HEAD", path)
    res = conn.getresponse()
    headers = dict(res.getheaders())


    if headers.has_key('location') and headers['location'] != url:
    	#print(".........{0}".format(headers['location']))
        return resolve_http_redirect(headers['location'], depth+1,directed_path)
    else:
        return url

# Process a single link
def processLink(link):
	# If we get a size, then the link results in a pdf
	#print("......{0}".format(link))
	contentLength = linkResultsInPdf(link)
	newPath = []
	if contentLength != None:
		# Get a path to the contents if any
		a = resolve_http_redirect(link,depth=0,directed_path=newPath)

	return contentLength,newPath


# Processes a set of links and determines which ones have pdfs and which ones don't
def processLinks(linkUris):
	linksWithPdfs = []

	for link in linkUris:
		
		res = processLink(link)
		if res[0] != None:
			tmp = {'link':res[1],'size':res[0]}
			linksWithPdfs.append(tmp)
	return linksWithPdfs



# Extracts all the links and generates a list of links which result in pdfs 
def listPDFLinks(uriName,verboseMode):
	# Extract all links in page 
	# List all links that result in a pdf

	if verboseMode == True:
		print("Processing uri: {0}".format(uriName))
		print("...Creating request")
	
	# Create a request for the uri
	request = urllib2.Request(uriName)	

	#request.add_header('User-agent','Mozilla 5.10')
	if verboseMode == True: 
		print("...Sending request and fetching response")
	
	response = None # Stores the result of the response 

	# Try to get the uri
	try:
		request.add_header('User-agent','Mozilla 5.10')
		urllib2.urlopen(request)
		response = urllib2.urlopen(request)

	except urllib2.URLError as e:
		pass 

	except urllib2.HTTPError as e:
		pass 
	
	# If the response code results in an error, print the error message and do nothing else.
	# Otherwise, perform link analysis
	if response != None:
		if verboseMode == True:
			print("...Sucess")

		urlContent = response.read()
		response.close()

		if verboseMode == True:
			print("...Extracting links")

		soup = BeautifulSoup(urlContent,'html.parser')
		linkList = [] # A list of 

		# Find all the links in the page 
		for links in soup.find_all('a'):
			linkList.append(urlparse.urljoin(uriName,links.get('href')))
		
		if verboseMode == True:
			print("...Filtering all links that result in pdfs")
		
		# Process the links in the webpage 
		linksWithPdfs = processLinks(linkList)
		printResults(linksWithPdfs)
		return 0
	else:
		return -1


if __name__=="__main__":
	demonstrationMode = False # Used to turn on test cases
	verboseMode = True # Used to display messages as program operates 
	
	
	args = sys.argv



	if len(args) > 1:
		#flagsToDelete = []
		if args[1] == '-d':
			testWebpages = ["http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-088-introduction-to-c-memory-management-and-c-object-oriented-programming-january-iap-2010/lecture-notes/","http://www.cs.toronto.edu/~suzanne/publications.html","http://www.cs.odu.edu/~mln/teaching/cs532-s16/test/pdfs.html","http://www.cs.odu.edu/~mln/","http://www.macs.hw.ac.uk/~jim/112MH1/tuts/"]
			print("Demonstrating program...\n")
			for testPage in testWebpages:
				listPDFLinks(testPage,verboseMode)
		else:

			listPDFLinks(args[1],verboseMode)
	else:
		print("Usage: python pdfLinks.py <url> | -d\n-d: demonstration mode (Runs a series of tests).")




