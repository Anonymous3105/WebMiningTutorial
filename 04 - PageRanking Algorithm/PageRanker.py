from pprint import pprint


def maptodictmat(nodemap):
	n = len(nodemap.keys())
	sitemat = {k: [0 for j in range(n)] for k in sorted(nodemap.keys())}
	for k1 in sorted(nodemap.keys()):
		for j, k2 in enumerate(sorted(nodemap.keys())):
			if k2 in nodemap[k1]:
				sitemat[k1][j] = 1

	return sitemat


class PageRanker(object):
	def __init__(self, dampening=0.85, num_iter=100, weighted=False):
		self.dampening = dampening
		self.num_iter = num_iter
		self.weighted = weighted

	def gen_inlinks(self):
		inlinks = {}
		for index, k in enumerate(sorted(self.idx.keys())):
			inlinks[k] = sum([self.idxmat[i][index] for i in range(len(self.idxmat))])

		return inlinks

	def gen_outlinks(self):
		outlinks = {}
		for k in self.idx.keys():
			outlinks[k] = sum(self.idx[k])

		return outlinks

	def get_win(self, a, b):
		win_sum = 0
		id1 = self.revidxmap[a]
		for id2, k in enumerate(sorted(self.idx.keys())):
			if self.idxmat[id2][id1]:
				win_sum += self.inlinks[k]
		return self.inlinks[k] / win_sum

	def get_wout(self, a, b):
		win_sum = 0
		id1 = self.revidxmap[a]
		for id2, k in enumerate(sorted(self.idx.keys())):
			if self.idxmat[id2][id1]:
				win_sum += self.outlinks[k]
		return self.outlinks[k] / win_sum

	def fit(self, idx):
		self.idx = idx
		self.idxmat = [self.idx[k] for k in sorted(self.idx.keys())]
		self.idxmap = {i: sorted(self.idx.keys())[i] for i in range(
			len(self.idx.keys()))
		}
		self.inlinks = self.gen_inlinks()
		self.outlinks = self.gen_outlinks()
		self.pageranks = {k: 1 for k in self.idx.keys()}
		self.revidxmap = {self.idxmap[k]: k for k in sorted(self.idxmap.keys())}

	def calculatePR(self):
		for i in range(self.num_iter):
			new_page_ranks = {}
			for id1, curr_page in enumerate(sorted(self.idx.keys())):
				# for pg in self.inlinks.keys():
				new_page_ranks[curr_page] = 1 - self.dampening
				sum_of_inlinks = 0

				for id2, page in enumerate(sorted(self.idx.keys())):
					# for page in range(len(self.idxmat)):
					if self.idxmat[id2][id1]:
						if self.weighted:
							sum_of_inlinks += self.pageranks[page] * self.get_win(
								curr_page, page
							) * self.get_wout(
								curr_page, page
							)
						else:
							sum_of_inlinks += self.pageranks[page] / self.outlinks[page]

				new_page_ranks[curr_page] += self.dampening * sum_of_inlinks

			self.pageranks = new_page_ranks.copy()

	def print_details(self):
		print("The inlinks of the graph are:")
		pprint(self.inlinks)

		print("The outlinks of the graph are:")
		pprint(self.outlinks)

		print("The page ranks of the page after {} iterations are: ".format(
			self.num_iter
		))
		pprint(self.pageranks)

		print("Sum of page ranks", sum(self.pageranks.values()))


if __name__ == "__main__":
	dummy_nodemap = {
		"A": ["B", "C", "D"],
		"B": ["A", "C", "D"],
		"C": ["D"],
		"D": ["C", "E"],
		"E": ["B", "C", "D"]
	}

	pr = PageRanker(0.85, 1000)
	pr.fit(maptodictmat(dummy_nodemap))
	pr.calculatePR()
	pr.print_details()

	wpr = PageRanker(0.85, 1000, weighted=True)
	wpr.fit(maptodictmat(dummy_nodemap))
	wpr.calculatePR()
	wpr.print_details()
