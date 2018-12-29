Note: This part of the tutorial assumes that you have Python3 installed on your machine 

* If not installed, you can install them using the following commands in a UNIX terminal window:
	+ sudo apt-get install python3

Like the PageRank algorithm explored in the last tutorial, the Hyperlink-Induced Topic Search (HITS; also known as hubs and authorities) is also a way by which webpages can be rated. The idea behind Hubs and Authorities stemmed from a particular insight into the creation of web pages when the Internet was originally forming; that is, certain web pages, known as hubs, served as large directories that were not actually authoritative in the information that they held, but were used as compilations of a broad catalog of information that led users direct to other authoritative pages. In other words, a good hub represented a page that pointed to many other pages, and a good authority represented a page that was linked by many different hubs. 

The scheme therefore assigns two scores for each page: its authority, which estimates the value of the content of the page, and its hub value, which estimates the value of its links to other pages. 

* The algorithm performs a series of iterations, each consisting of two basic steps:
	+ **Authority update**: Update each node's authority score to be equal to the sum of the hub scores of each node that points to it. That is, a node is given a high authority score by being linked from pages that are recognized as Hubs for information.
	
			auth(p) = sum(hub(i)) where i area all the pages connected to p.

	+ **Hub update**: Update each node's hub score to be equal to the sum of the authority scores of each node that it points to. That is, a node is given a high hub score by linking to nodes that are considered to be authorities on the subject.

			hub(p) = sum(auth(i)) where i area all the pages that p connects to.

* The Hub score and Authority score for a node is calculated with the following algorithm:
	+ Start with each node having a hub score and authority score of 1.
	+ Run the authority update rule
	+ Run the hub update rule
	+ Normalize the values by dividing each Hub score by square root of the sum of the squares of all Hub scores, and dividing each Authority score by square root of the sum of the squares of all Authority scores.
	+ Repeat from the second step as necessary.

The program gives a very simple programmatic approach of simulating the HITS algorithm. Like the PageRank the input to the program is a dictionary containing all the pages of the collection as keys and the pages that they connect to as a list of values.

This input is converted to a more convinient to handle adjacency matrix-dictionary format and used in the computation of all the finding the hub and authority scores of all the pages in the collection over a number of pre-defined iterations.

The hub and authority scores of the collection can be displayed at the end of the program.
