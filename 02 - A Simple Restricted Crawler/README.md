Note: This part of the tutorial assumes that you have Python3 installed on your machine along with the packages: requests and bs4. Rest of the packages used in the tutorial are available by deault in Python2 and Python3

* If not installed, you can install them using the following commands in a UNIX terminal window:
	+ sudo apt-get install python3 python3-pip
	+ sudo pip3 install requests
	+ sudo pip3 install bs4

This tutorial builds from the previous tutorial about how to fetch a webpage using "get" function from requests module and how to extract required URLs using regex filters. In this tutorial, we'll replace the URLs filtering portion from regex to BeautifulSoup class from bs4 and using a URL frontier to enqueue and dequeue URLs so as to produce a Breadth First Search in the URL crawling process starting from a given seed URL.

The URLs are then indexed into a pagetable dictionary which maintains the hierarchy of all the URLs that can be accessed from a certain URL. And a inverse page table is created by a simple set default operation of the python dictionaries.

One has to note that on any this will create uncontrolled crawling process that can go on forever if not stopped manually. So to control this to a restrictive domain, say all the URLs crawled from starting seed URL "https://www.amazon.co.in" have to be restricted to the "amazon.co.in" domain and should not "leak" out of them. One simple way to do this is to apply an entry filter for the URLs to be queued in the frontier. This is achieved by determining the hostname domain from the seed URL by using the "urlparse" function from the urlparse module and checking that the hostname of the URL of the URL to be queued in the frontier is the same as that of the starting seed URL.

The rest of the code is pretty straight forward to understand and encorporate into other python modules. The output of the program will be 3 different files: the frontier of the URLs crawled in the process, the pagetable and the reverse pagetable of the URLs generated.