import numpy as np
import re

import requests
from bs4 import BeautifulSoup

def get_web_text(url):
	try:
		page = requests.get(url)
	except Exception as e:
		try:
			print("Failed to reached {}".format(url))
		except UnicodeEncodeError:
			print("Failed to reached and cant show the URL")
		return None

	soup = BeautifulSoup(page.text, 'html.parser')

	# Removing style blocks
	[tag.decompose() for tag in soup("style")]

	# Removing scripts
	[tag.decompose() for tag in soup("script")]

	text = re.sub('\n+', ' ', soup.get_text()).strip().lower()
	return text


def get_word_count(words, text):
	if type(words) == str:
		return text.count(words)
	elif type(words) == list:
		return sum([text.count(wordi) for wordi in words])



class KMeans_Clusterer():
	def __init__(self, k = 4, num_iter = 20):
		self.k = k
		self.num_iter = num_iter

		self.wordlist = []
		self.doclist = {}
		self.doc_vecs = {}
		
		self.clusters = {}
		self.cluster_centroids = {}


	def get_text_data(self, docfile):
		with open(docfile) as fp:
			content = list(map(str.lower, fp.readlines()))

		for textline in content:
			docname, doctext = textline.split(" : ")
			self.doclist[docname] = doctext


	def get_URL_data(self, docfile):
		with open(docfile) as fp:
			urls = list(map(str.strip, fp.readlines()))

		for url in urls:
			self.doclist[url] = get_web_text(url)


	def get_word_freq(self):
		for doc in self.doclist:
			self.doc_vecs[doc] = np.array([get_word_count(word, self.doclist[doc]) for word in self.wordlist])
		

	def get_doc_vec(self, doc):
		return self.doc_vecs[doc]


	def fit(self, wordlist, docfile, input_type = None):
		self.wordlist = wordlist
		if input_type == "TEXT":
			self.get_text_data(docfile)
		elif input_type == "URL":
			self.get_URL_data(docfile)
		else:
			print("Input type unspecified while fitting the data.")

		self.get_word_freq()
		self.freq_matrix = [[0 for i in range(self.k)] for i in range(len(self.doc_vecs.keys()))]

		
	def get_doc_dist(self, doc1, doc2, metric="manhattan"):
		if metric == "manhattan":
			return round(np.sum(abs(doc1 - doc2)), 4)
		elif metric == "euclidean":
			return round((sum((self.doc_vecs[doc1] - self.doc_vecs[doc2])**2))**(0.5), 4)


	def update_cluster_centroids(self):
		for curr_clus in sorted(self.clusters.keys()):
			clus_doc_vecs = [self.doc_vecs[doc] for doc in self.clusters[curr_clus]]
			# print(clus_doc_vecs)
			self.cluster_centroids[curr_clus] = np.around(np.mean(clus_doc_vecs, axis = 0), 4)


	def update_freq_matrix(self):
		for i, doci in enumerate(sorted(self.doc_vecs.keys())):
			for j, clusj in enumerate(sorted(self.clusters.keys())):
				self.freq_matrix[i][j] = self.get_doc_dist(self.doc_vecs[doci], self.cluster_centroids[clusj], metric="manhattan")


	def cluster_init(self):
		self.clusters = {"Cluster"+str(i): [sorted(self.doclist.keys())[i]] for i in range(self.k)}
		
		# Adding nearest Neighbour for the remaining documents
		for i, doci in enumerate(sorted(self.doclist.keys())[self.k:]):
			self.clusters[sorted(self.clusters.keys())[i % self.k]].append(doci)
		self.update_cluster_centroids()
		self.update_freq_matrix()


	def cluster(self):
		self.cluster_init()

		for i in range(self.num_iter):

			temp_clus = {clus : [] for clus in sorted(self.clusters.keys())}

			for i, doci in enumerate(sorted(self.doc_vecs.keys())):
				j = self.freq_matrix[i].index(min(self.freq_matrix[i]))
				temp_clus[sorted(temp_clus.keys())[j]].append(doci)

			if temp_clus == self.clusters:
				print("Clusters converged at {} iterations of {}.".format(i, self.num_iter))
				break
			else:
				self.clusters = temp_clus

			self.update_cluster_centroids()
			self.update_freq_matrix()


	def print_details(self):
		print("The clusters created are as follows:")
		for clus in self.clusters:
			print(clus, ":", self.clusters[clus])
		
		print("\n\nThe document vectors of these clusters are:")
		for clus in self.cluster_centroids:
			print(clus, ":", self.cluster_centroids[clus])



print("(a) Clustering given one line documents")

wordlist = ["automotive", "car", "motorcycle", "self-drive", "iot", "hire", "dhoni"]
docfile = "docfile.txt"

textcls = KMeans_Clusterer(k=4, num_iter=20)
textcls.fit(wordlist, docfile, input_type="TEXT")
textcls.cluster()
textcls.print_details()


print("\n\n(b) Clustering given URLs")

urlwordlist = ["tesla", "electric", ["car", "vehicle", "automobile"], "pollution", "de-monetisation" , "gst" , "black money"]
urldocfile = "urldocfile.txt"

urlcls = KMeans_Clusterer()
urlcls.fit(urlwordlist, urldocfile, input_type="URL")
urlcls.cluster()
urlcls.print_details()