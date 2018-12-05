import requests
from bs4 import BeautifulSoup
from pprint import pprint

try:
	# Python 3
	from urllib.parse import urlparse, urljoin
except ImportError:
	# Python 2
	from urlparse import urljoin, urlparse


def pprint_data_to_file(data, fname):
	""" Function to print the incoming data structre """
	with open(fname, 'w+') as out:
		pprint(data, stream=out)


class Crawler(object):
	def __init__(self):
		self.pagetable = {}
		self.rev_pagetable = {}

	def get_seed(self):
		# self.seed_url = "http://www.vit.ac.in"
		self.seed_url = input("Enter the seed URL: ").strip()
		self.hostname = urlparse(self.seed_url).hostname
		self.frontier = [self.seed_url]

	def seed_test(self, url):
		return True if self.hostname in url else False

	def get_all_urls(self, url):
		try:
			page = requests.get(url)
		except Exception:
			try:
				print("Failed to reached {}".format(url))
			except UnicodeEncodeError:
				print("Failed to reached and cant show the URL")
			return None

		try:
			soup = BeautifulSoup(page.text, 'html.parser')
		except Exception:
			return []

		urls = []
		for link in soup.find_all('a', href=True):
			if link.get('href') in [None, "#", ""]:
				continue
			urls.append(urljoin(self.seed_url, link.get('href')))

		return list(set(urls))

	def crawl(self):
		for curr_url in self.frontier:

			urls = self.get_all_urls(curr_url)
			if not urls:
				continue

			oldFronLen = len(self.frontier)

			for url in urls:
				if curr_url in self.pagetable:
					self.pagetable[curr_url].append(url)
				else:
					self.pagetable[curr_url] = [url]

				if url not in self.frontier and self.seed_test(url):
					self.frontier.append(url)

			if len(self.frontier) > oldFronLen:
				try:
					print("Added {} links in the frontier for the link: {}".format(
						len(self.frontier) - oldFronLen, curr_url)
					)
				except UnicodeEncodeError:
					print("Added {} links in the frontier for the link: NOT ABLE TO PRINT"
											.format(len(self.frontier) - oldFronLen))

	def rev_table_gen(self):

		self.rev_pagetable = {}
		for k, v in self.pagetable.items():
			for x in v:
				self.rev_pagetable.setdefault(x, []).append(k)


vitc = Crawler()
vitc.get_seed()
vitc.crawl()

pprint_data_to_file(vitc.pagetable, "pagetable.txt")
pprint_data_to_file(vitc.rev_pagetable, "rev_pagetable.txt")
pprint_data_to_file(vitc.frontier, "frontier.txt")
