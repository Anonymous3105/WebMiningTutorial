Note: This part of the tutorial assumes that you have Python3 installed on your machine along with the packages: numpy, requests and bs4. Rest of the packages used in the tutorial are available by deault in Python2 and Python3

* If not installed, you can install them using the following commands in a UNIX terminal window:
	+ sudo apt-get install python3 python3-pip
	+ sudo pip3 install numpy
	+ sudo pip3 install requests
	+ sudo pip3 install bs4

In Web Text Mining clustering is of the data mining tool used for grouping web documents into clusters such that the objects from the same cluster are similar and objects from different cluster are dissimilar. In the statistically based vector-space model, a document is conceptually represented by a vector of keywords extracted from the document, with associated weights representing the importance of the keywords in the document and within the whole document collection. Likewise, a query is modelled as a list of keywords with associated weights representing the importance of the keywords in the query. 

The weight of a term in a document vector can be determined in many ways. It can be a binary value representing the presence or absence of the term in the document or the frquency of the term in the document, or the most common approach called the TF * IDF method, in which the weight of a term is determined by two factors: how often the term j occurs in the document i (the term frequency tf_(i,j)) and how often it occurs in the whole document collection (the document frequency df_j).

Once the weight metric has been finalized, all the documents are then processed into vectors. Then these vectors can be used as a measure of how similar or dissimilar two or more documents are. In other words these vectors can be used to cluster the documents based on either a distance metric like euclidean distance, manhattan distance etc. or a similarity metric like cosine similarity or Pearson's coefficient etc. 

In this program for a given document set which can be procured from source files or associated webpages are tokenized into vectors and then are clustered using K-Means Clustering.

**What is K-Means Clustering**

K-means clustering is a method of vector quantization, originally from signal processing, that is popular for cluster analysis in data mining. k-means clustering aims to partition n observations into k clusters in which each observation belongs to the cluster with the nearest mean, serving as a prototype of the cluster.

* The algorithm works iteratively to assign each data point to one of K groups based on the features that are provided. Data points are clustered based on feature similarity. The results of the K-means clustering algorithm are:

	+ The centroids of the K clusters, which can be used to label new data
	+ Labels for the training data (each data point is assigned to a single cluster)

Rather than defining groups before looking at the data, clustering allows you to find and analyze the groups that have formed organically. 

* The algorithm is pretty simple to explain and implement: 
	+ Start by picking any k random points from the given set as cluster centres.
	+ Cluster all the points based on the proximity of them to the neares cluster centroid.
	+ Once all the clusters have been formed, recompute the cluster centroid as the average of all the points that belong to the cluster.
	+ Repeat the above steps until the cluster do not change or have converged to equilibrium


* The following are the specifications of the associated program code:
	+ The program uses term frequencies as weights to tokenize the words into vectors but can be changed by modifying the get_word_freq() function.
	+ Manhattan or city-block distance is being used by default as the distance metric but can be changed by modifying the get_doc_dist() function.
	+ The cluster centroid update rule computes the coordinate wise average of all the points belonging to the cluster as the new cluster centroid.
