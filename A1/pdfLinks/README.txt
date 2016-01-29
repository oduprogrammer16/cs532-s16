Program: pdfLinks.py 
Author: Kevin R. Clemmons 

Description: 
	- For a given website, lists all the links which result in pdf files, their sizes and if any redirections occur.

Libraries Used: 
	- urllib2
	- urllib
	- urlparse
	- sys 
	- httplib
	- errno
	- socket
	- bs4 

Compiliation:
	- Not needed. 

Running: 
	- To run, enter the command python pdfLinks.py <url-name>


	Notes: 
	- This program was tested with the following links : 
		+ http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-088-introduction-to-c-memory-management-and-c-object-oriented-programming-january-iap-2010/lecture-notes/
	
		+ http://www.cs.toronto.edu/~suzanne/publications.html

		+ http://www.cs.odu.edu/~mln/teaching/cs532-s16/test/pdfs.html

		+ http://www.cs.odu.edu/~mln/"

		+ http://www.macs.hw.ac.uk/~jim/112MH1/tuts/

	- If you would like a demonstration of the test cases 
		+ Enter the command python pdfLinks.py -d 

Sources: 
	- Exception handling in lines 42-45
		url:  http://stackoverflow.com/questions/20568216/python-handling-socket-error-errno-104-connection-reset-by-peer
			* Accessed: 1/28/15

	- Exception handline for requests
		url: http://stackoverflow.com/questions/666022/what-errors-exceptions-do-i-need-to-handle-with-urllib2-request-urlopen
			* Accessed: 1/24/15
			
	- Handling link-redirections in line 62-77
		url: http://www.zacwitte.com/resolving-http-redirects-in-python
			* Accessed: 1/28/15

	- Handling incomplete links in line 152-153
		url: http://stackoverflow.com/questions/27397990/python-parsing-html-for-complete-links-urls
			* Accessed: 1/28/15


