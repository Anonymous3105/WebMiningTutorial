import requests
from pprint import pprint
import re

try:
	# Python 3
	from urllib.parse import urljoin
except ImportError:
	# Python 2
	from urlparse import urljoin


def pprint_data_to_file(data, fname):
	with open(fname, 'w+') as out:
		pprint(data, stream=out)


def get_href_links(url):
	page = requests.get(url)
	pattern = re.compile('(?<=href=").*?(?=")')
	return list(set([urljoin(url, link) for link in pattern.findall(page.text)]))


def get_img_src_links(url):
	page = requests.get(url)
	pattern = re.compile('(?<=src=").*?(?=")')
	return list(set([urljoin(url, link) for link in pattern.findall(page.text)]))


# Sample URL = "http://www.vit.ac.in"
url = input("Enter the URL you wish to crawl: ")

urls = get_href_links(url)
pprint_data_to_file(urls, "urls.txt")

img_urls = get_img_src_links(url)
pprint_data_to_file(img_urls, "imgurls.txt")
