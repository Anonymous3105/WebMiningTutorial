import numpy as np
from pprint import pprint
from math import inf, sqrt


def get_word_count(words, text):
	if type(words) == str:
		return text.count(words)
	elif type(words) == list:
		return sum([text.count(wordi) for wordi in words])


class CosineSimilarityClusterer():
	def __init__(self, threshold=0.25):
		self.threshold = threshold
		self.wordlist = []
		self.doclist = {}
		self.doc_vecs = {}

		self.clusters = {}

	def get_text_data(self, docfile):
		with open(docfile) as fp:
			content = list(map(str.lower, fp.readlines()))

		for textline in content:
			docname, doctext = textline.split(" : ")
			self.doclist[docname] = doctext

	def get_word_freq(self):
		for doc in self.doclist:
			self.doc_vecs[doc] = np.array(
				[get_word_count(word, self.doclist[doc]) for word in self.wordlist]
			)

	def get_dot_prod(self, doc1, doc2):
		return self.doc_vecs[doc1].T.dot(self.doc_vecs[doc2])

	def get_doc_length(self, doc):
		return sqrt(self.get_dot_prod(doc, doc))

	def get_cos_angle(self, doc1, doc2):
		return self.get_dot_prod(doc1, doc2) / (
			self.get_doc_length(doc1) * self.get_doc_length(doc2)
		)

	def get_nearest_doc(self, i, doc):
		return sorted(
			self.doc_vecs.keys()
		)[
			max(range(len(self.doc_vecs)), key=lambda k: self.cos_mat[i][k])
		]

	def compute_cosine_matrix(self):
		for i, doci in enumerate(sorted(self.doc_vecs.keys())):
			for j, docj in enumerate(sorted(self.doc_vecs.keys())):
				if i == j:
					# Similar docs will have cos value as 1
					# and will be redundant in the calculation
					self.cos_mat[i][j] = -inf
				else:
					self.cos_mat[i][j] = round(self.get_cos_angle(doci, docj), 2)

	def fit(self, wordlist, docfile):
		self.wordlist = wordlist
		self.get_text_data(docfile)
		self.get_word_freq()

		self.cos_mat = [
			[0 for i in range(len(self.doc_vecs))] for j in range(len(self.doc_vecs))
		]
		self.compute_cosine_matrix()

	def cluster(self):
		clusters = []
		for i, doc in enumerate(sorted(self.doc_vecs.keys())):
			nearest_doc = self.get_nearest_doc(i, doc)
			clusters.append({doc, nearest_doc})

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

		self.clusters = {
			"Cluster " + str(i): end_clusters[i] for i in range(len(end_clusters))
		}

	def print_details(self):
		print("The document vectors look as follows:")
		pprint(self.doc_vecs)

		print("\nThe cosine similarity matrix looks as follows: ")
		pprint(self.cos_mat)

		print("\nThe documents are clustered as follows:")
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

	csc = CosineSimilarityClusterer()
	csc.fit(wordlist, docfile)
	csc.cluster()
	csc.print_details()
