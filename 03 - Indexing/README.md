Note: This part of the tutorial assumes that you have Python3 installed on your machine along with the packages: requests and bs4. Rest of the packages used in the tutorial are available by deault in Python2 and Python3

* If not installed, you can install them using the following commands in a UNIX terminal window:
	+ sudo apt-get install python3 python3-pip
	+ sudo pip3 install requests
	+ sudo pip3 install bs4

In this tutorial, we explore how to index fetched or procured documents in the form of stored files or webpage URIs which are indexed in the form of a dictionary of a word that can appear in one or more documents as key and amd the value as the number of occurence of the word in the different documents in the collection along with the offsets in each document that the word occurs in.

The source files from which the index table is generated can be a locally stored file or a URI which can be used to fetch the webpage and proces it further. 

* The basic functions of the Indexer class include 
	+ Fetching text from a local file given its local address
	+ Fetching text from a webpage given its URI and filter all non-required tags
	+ A wrapper function that gets sources from text file and fetches texts depending on whether the source is a local file address or URI
	+ Index the words obtained from the fetched texts into a dictionary
	+ Print the index dictionary to a file