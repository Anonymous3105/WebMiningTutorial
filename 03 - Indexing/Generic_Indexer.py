import requests
from bs4 import BeautifulSoup

import re
from pprint import pprint

try:
	# Python 3
	from urllib.parse import urlparse
except ImportError:
	from urlparse import urlparse


def pprint_data_to_file(data, fname):
	with open(fname, 'w') as out:
		pprint(data, stream=out)


class Indexer():
	def __init__(self):
		self.index_list = {}
		self.data_dict = {}

	def get_words(self, text):
		text = re.sub(r'[^\w\s]', '', text)
		return re.split(r'\s*', text)

	def get_data_from_file(self, fname):
		try:
			with open(fname) as file:
				self.data_dict[fname] = self.get_words(file.read().lower())
		except IOError:
			print("File does not exist!")

	def get_data_from_url(self, url):
		try:
			page = requests.get(url)
		except Exception:
			try:
				print("Failed to reached {}".format(url))
			except UnicodeEncodeError:
				print("Failed to reached and cant show the URL")
			return None

		soup = BeautifulSoup(page.text, 'html.parser')
		self.data_dict[url] = self.get_words(soup.text.lower())

	def add_word_to_index(self, off, fname, word):
		if word not in self.index_list:
			self.index_list[word] = [1, [(fname, off)]]
		else:
			self.index_list[word][0] += 1
			self.index_list[word][1].append((fname, off))

	def index_data(self):
		for fname in self.data_dict.keys():
			print("Indexing {} words from the source: {}".format(
				len(self.data_dict[fname]), fname)
			)
			for i in range(len(self.data_dict[fname])):
				self.add_word_to_index(i, fname, self.data_dict[fname][i])

	def get_data(self, srcfname):
		try:
			with open(srcfname, 'r') as infile:
				srcs = re.split(r',', infile.read())
		except IOError:
			print("Source file not found.")

		for src in srcs:
			if urlparse(src).scheme == 'http':
				self.get_data_from_url(src)
			else:
				self.get_data_from_file(src)


viti = Indexer()
viti.get_data("srcfile.txt")
viti.index_data()

pprint_data_to_file(viti.index_list, 'index.idx')
