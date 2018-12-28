Note: This part of the tutorial assumes that you have Python3 installed on your machine along with the package requests.

* If not installed, you can install them using the following commands in a UNIX terminal window:
	+ sudo apt-get install python3 python3-pip
	+ sudo pip3 install requests

Web crawlers are pretty simple, at least at first pass (like most things they get harder once you start to take things like scalability and performance into consideration). Starting from a certain URL (or a list of URLs), they will check the HTML document at each URL for links (and other information) and then follow those links to repeat the process.

The aim of this program is to get a general overlook at how one can extract URLs (or anything that is enclosed inside a tag to is a tag itself) using 2 packages of python: requests and re.

The program is a simple representation of how one can extract all the URLs specified as a parameter to the "href" attribute of the anchor (<a>) tag of an HTML webpage and similarly the URLs of "src" attributes of image (<img>) tags given the URL of the seed webpage. A seed URL is the URL from where the crawling process begins from and continues depending on the requirements of the crawler.

This is achieved by using the "get" function of the request module which is used to fetch a web resource and using regular expressions to fetch the URL group in the specific required attributes of the tags. (Do not worry of the complexity of the regular expressions used. These are pretty common regex used can be understood on any online resource).

* To execute the file simply enter the following line in the terminal window after navigating to the directory of the file:
	+ python3 URL_Fetcher_Filter


The second part of the single page fetching and filtering process can be optimized to a great extent by using the BeautifulSoup (or bs4) package of python and will be used in the further programs (or tutorials).