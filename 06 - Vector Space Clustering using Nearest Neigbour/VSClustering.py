import numpy as np
from math import inf

from pprint import pprint
import re

import requests
from bs4 import BeautifulSoup


def get_web_text(url):
	try:
		page = requests.get(url)
	except Exception:
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


def get_set_index(doc, set_list):
	for i, curr_set in enumerate(set_list):
		if doc in curr_set:
			return i


class VSCluster():
	def __init__(self, threshold):
		self.threshold = threshold
		self.doclist = {}
		self.wordmap = {}
		self.freq_matrix = []
		self.clusterlist = {}

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

	def get_hier_data(self, doclist=None, wordmap=None):
		if doclist is None or wordmap is None:
			print("Given empty doclist or wordmap. Can't fit it")
		else:
			self.doclist = doclist
			self.wordmap = wordmap

	def get_word_freq(self):
		for doc in self.doclist:
			self.wordmap[doc] = np.array(
				[get_word_count(word, self.doclist[doc]) for word in self.wordlist]
			)

	def get_doc_vec(self, doc):
		return self.wordmap[doc]

	def fit(self, wordlist, docfile, input_type, wordmap=None):
		# self.wordlist = list(map(str.lower, wordlist))
		self.wordlist = wordlist
		self.input_type = input_type

		if input_type == "URL":
			self.get_URL_data(docfile)
			self.get_word_freq()
		elif input_type == "TEXT":
			self.get_text_data(docfile)
			self.get_word_freq()
		elif input_type == "HIER":
			self.get_hier_data(docfile, wordmap)

		self.freq_matrix = [
			[0 for i in range(len(self.doclist.keys()))] for i in range(
				len(self.doclist.keys())
			)
		]
		self.clusterlist = {doc: [] for doc in self.doclist.keys()}

		self.compute_difference()

	def get_doc_dist(self, doc1, doc2):
		return round((sum((self.wordmap[doc1] - self.wordmap[doc2])**2))**(0.5), 4)

	def compute_difference(self):
		for i, doci in enumerate(sorted(self.wordmap.keys())):
			for j, docj in enumerate(sorted(self.wordmap.keys())):
				if i == j:
					self.freq_matrix[i][j] = inf
				else:
					self.freq_matrix[i][j] = self.get_doc_dist(doci, docj)

	def get_min_doc_dist(self, docindex, return_dist=False):

		doc_vec = self.freq_matrix[docindex]

		mind = min(doc_vec)
		mindocs = [
			sorted(self.clusterlist.keys())[j] for j in range(
				len(doc_vec)
			) if doc_vec[j] == mind
		]

		if return_dist:
			return mind, mindocs

		return mindocs[0]

	def cluster(self, return_for_hier=False):
		for i, doci in enumerate(sorted(self.doclist.keys())):
			for j, docj in enumerate(sorted(self.doclist.keys())):
				if i != j and self.freq_matrix[i][j] < self.threshold and docj not in self.clusterlist[doci]:
					self.clusterlist[doci].append(docj)

		clusters = []
		for curr_docindex, curr_doc in enumerate(sorted(self.clusterlist.keys())):
			nearest_doc = self.get_min_doc_dist(curr_docindex)
			clusters.append({curr_doc, nearest_doc})

		end_clusters = []

		while clusters:
			flag_merged = True
			first = clusters.pop(0)
			while flag_merged:
				flag_merged = False
				for i in range(len(clusters)):
					if first.intersection(clusters[i]):
						first.update(clusters[i])
						clusters[i] = set()
						flag_merged = True

			clusters = [j for j in clusters if len(j) != 0]
			end_clusters.append(first)

		if self.input_type != "HIER":
			self.clusters = {
				"Cluster " + str(i): end_clusters[i] for i in range(len(end_clusters))
			}
		else:
			self.clusters = {
				"Topic " + str(i): end_clusters[i] for i in range(len(end_clusters))
			}

		if return_for_hier:
			hier_data = {}

			for curr_clus in self.clusters.keys():
				# centroid = np.empty((self.wordmap[0], 1), np.float64)
				centroid = np.array([0 for i in range(len(self.wordlist))])
				for doc in self.clusters[curr_clus]:
					centroid += self.wordmap[doc]

				centroid = centroid / len(self.clusters[curr_clus])
				hier_data[curr_clus] = np.round(centroid, 4)

			return(self.clusters, hier_data)

	def print_details(self):
		print("The document vectors look as follows:")
		pprint(self.wordmap)

		print(
			"The documents are clustered using the Nearest Neighbour method as follows:"
		)
		pprint(self.clusters)


if __name__ == "__main__":
	wordlist = [
		"automotive",
		"car",
		"motorcycle",
		"self-drive",
		"iot",
		"hire",
		"dhoni"
	]
	docfile = "docfile.txt"

	print("\nClustering of document files", '-' * 15)
	vsobj = VSCluster(threshold=1.5)
	vsobj.fit(wordlist, docfile, input_type="TEXT")
	lvl1_cluslist, lvl1_clusmap = vsobj.cluster(return_for_hier=True)
	vsobj.print_details()

	print("\nHierrachial/Topical Clustering of document files", '-' * 15)
	vsobj_hier = VSCluster(threshold=0.1)
	vsobj_hier.fit(
		wordlist=wordlist,
		docfile=lvl1_cluslist,
		input_type="HIER",
		wordmap=lvl1_clusmap
	)
	vsobj_hier.cluster()
	vsobj_hier.print_details()

	urlwordlist = [
		"tesla",
		"electric",
		["car", "vehicle", "automobile"],
		"pollution", "de-monetisation",
		"gst",
		"black money"
	]
	urldocfile = "urldocfile.txt"

	print("\nClustering of document Webpages", '-' * 15)
	vsobj2 = VSCluster(threshold=75)
	vsobj2.fit(urlwordlist, urldocfile, input_type="URL")
	url_cluslist, url_clusmap = vsobj2.cluster(return_for_hier=True)
	vsobj2.print_details()

	print("\nHierrachial/Topical Clustering of document Webpages", '-' * 15)
	vsobj2_hier = VSCluster(threshold=0.1)
	vsobj2_hier.fit(
		wordlist=urlwordlist,
		docfile=url_cluslist,
		input_type="HIER",
		wordmap=url_clusmap
	)
	vsobj2_hier.cluster()
	vsobj2_hier.print_details()
