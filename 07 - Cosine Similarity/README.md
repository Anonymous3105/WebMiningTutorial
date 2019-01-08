Note: This part of the tutorial assumes that you have Python3 installed on your machine along with the package: numpy. Rest of the packages used in the tutorial are available by deault in Python2 and Python3

* If not installed, you can install them using the following commands in a UNIX terminal window:
	+ sudo apt-get install python3 python3-pip
	+ sudo pip3 install numpy

Just a simple modification to the previous tutorial, this program tokenizes the given documents into document vectors using the term frequencies as the weights and uses cosine similarity as a metric to cluster the documents into groups.