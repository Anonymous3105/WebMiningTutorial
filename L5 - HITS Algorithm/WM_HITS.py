from pprint import pprint

def maptodictmat(nodemap):
	n = len(nodemap.keys())
	sitemat = {k:[0 for j in range(n)] for k in sorted(nodemap.keys())}
	for k1 in sorted(nodemap.keys()):
		for j, k2 in enumerate(sorted(nodemap.keys())):
			if k2 in nodemap[k1]:
				sitemat[k1][j] = 1

	return sitemat
		
class HITSRanker():
	def __init__(self, num_iter):
		self.num_iter = num_iter

	def fit(self, nodemap):
		self.nodemap = nodemap
		self.idx = maptodictmat(self.nodemap)
		self.idxmat = [self.idx[k] for k in sorted(self.idx.keys())]
		
		self.authorityscore = {k:1 for k in self.idx.keys()}
		self.hubscore = {k:1 for k in self.idx.keys()}


	def normalize_vec(self, vec):
		temp_sum = sum(vec.values())
		return {k:vec[k]/temp_sum for k in sorted(vec.keys())}


	def calculateA(self):
		for curr_page_index, curr_page in enumerate(sorted(self.idx.keys())):
			 for page_index, page in enumerate(sorted(self.idx.keys())):
			 	if self.idxmat[curr_page_index][page_index]:
			 		self.authorityscore[curr_page] += self.hubscore[page]

		self.authorityscore = self.normalize_vec(self.authorityscore)

	def calculateH(self):
		for curr_page_index, curr_page in enumerate(sorted(self.idx.keys())):
			 for page_index, page in enumerate(sorted(self.idx.keys())):
			 	if self.idxmat[page_index][curr_page_index]:
			 		self.hubscore[curr_page] += self.authorityscore[page]

		self.hubscore = self.normalize_vec(self.hubscore)

	def calculate_HA_score(self):
		for _ in range(self.num_iter):
			self.calculateA()
			self.calculateH()

	def print_details(self):

		print("The hub score of all the nodes are:")
		pprint(self.hubscore)

		print("The authority score of all the nodes are:")
		pprint(self.authorityscore)

		print("Sum of hub score in the end", sum(self.hubscore.values()))
		print("Sum of authority score in the end", sum(self.authorityscore.values()))


if __name__ == '__main__':
	
	dummy_nodemap = {
		"A" : ["B", "C", "D"],
		"B" : ["A", "C", "D"],
		"C" : ["D"],
		"D" : ["C", "E"],
		"E" : ["B", "C", "D"]
	}

	hs = HITSRanker(num_iter=50)
	hs.fit(dummy_nodemap)
	hs.calculate_HA_score()
	hs.print_details()


	# dummy_nodemap2 = {
	# 	"Home" : ["About", "Product", "Links"],
	# 	"About" : ["Home"],
	# 	"Product" : ["Home"],
	# 	"Links" : ["Home", "Review A", "Review B", "Review C", "Review D", "External Site A", "External Site B", "External Site C", "External Site D"],
	# 	"Review A" : ["Home"],
	# 	"Review B" : ["Home"],
	# 	"Review C" : ["Home"],
	# 	"Review D" : ["Home"],
	# 	"External A" : [],
	# 	"External B" : [],
	# 	"External C" : [],
	# 	"External D" : [],
	# }

	# hs2 = HITSRanker(num_iter=50)
	# hs2.fit(dummy_nodemap2)
	# hs2.calculate_HA_score()
	# hs2.print_details()

