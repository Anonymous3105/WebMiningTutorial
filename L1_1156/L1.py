import requests
from urllib.parse import urljoin
from pprint import pprint
import re

def pprint_data_to_file(data, fname):
	with open(fname, 'w') as out:
		pprint(data, stream=out)

def get_href_links(url):
	r = requests.get(url)
	pattern = re.compile('(?<=href=").*?(?=")')
	return list(set([urljoin(url, link) for link in pattern.findall(r.text)]))

def get_img_src_links(url):
	r = requests.get(url)
	pattern = re.compile('(?<=src=").*?(?=")')
	return list(set([urljoin(url, link) for link in pattern.findall(r.text)]))


url = "http://www.vit.ac.in"

urls = get_href_links(url)
pprint_data_to_file(urls, "urls.txt")

img_urls = get_img_src_links(url)
pprint_data_to_file(img_urls, "imgurls.txt")
