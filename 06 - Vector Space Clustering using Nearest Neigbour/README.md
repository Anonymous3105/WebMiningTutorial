Note: This part of the tutorial assumes that you have Python3 installed on your machine along with the packages: numpy, requests and bs4. Rest of the packages used in the tutorial are available by deault in Python2 and Python3

* If not installed, you can install them using the following commands in a UNIX terminal window:
	+ sudo apt-get install python3 python3-pip
	+ sudo pip3 install numpy
	+ sudo pip3 install requests
	+ sudo pip3 install bs4

In Web Text Mining clustering is of the data mining tool used for grouping web documents into clusters such that the objects from the same cluster are similar and objects from different cluster are dissimilar. In the statistically based vector-space model, a document is conceptually represented by a vector of keywords extracted from the document, with associated weights representing the importance of the keywords in the document and within the whole document collection. Likewise, a query is modelled as
a list of keywords with associated weights representing the importance of the keywords in the query. 

The weight of a term in a document vector can be determined in many ways. It can be a binary value representing the presence or absence of the term in the document or the frquency of the term in the document, or the most common approach called the TF * IDF method, in which the weight of a term is determined by two factors: how often the term j occurs in the document i (the term frequency tf_(i,j)) and how often it occurs in the whole document collection (the document frequency df_j).

Once the weight metric has been finalized, all the documents are then processed into vectors. Then these vectors can be used as a measure of how similar or dissimilar two or more documents are. In other words these vectors can be used to cluster the documents based on either a distance metric like euclidean distance, manhattan distance etc. or a similarity metric like cosine similarity or Pearson's coefficient etc. 

The associated program uses term frequency as the weights of a term for a document and uses nearest neighbours based on euclidean distance as a parameter to cluster the documents into groups of similar nature.