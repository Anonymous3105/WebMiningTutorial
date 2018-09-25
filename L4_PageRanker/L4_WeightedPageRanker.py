from pprint import pprint
from L4_PageRanker_1156 import PageRanker
	

class WeightedPageRanker(PageRanker):
	
	def fit(self, idx):
		super(WeightedPageRanker, self).fit(idx)
		self.revidxmap = {self.idxmap[k]:k for k in sorted(self.idxmap.keys())}
		
		

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

	def calculateWeightedPR(self):
		for i in range(self.num_iter):
			new_page_ranks = {}
			for id1, curr_page in enumerate(sorted(self.idx.keys())):
				new_page_ranks[curr_page] = 1 - self.dampening
				sum_of_inlinks = 0
				for id2, page in enumerate(sorted(self.idx.keys())):
					if self.idxmat[id2][id1]:
						sum_of_inlinks += self.pageranks[page] * self.get_win(curr_page, page) * self.get_wout(curr_page, page)
				new_page_ranks[curr_page] += self.dampening * sum_of_inlinks

			self.pageranks = new_page_ranks.copy()

	
if __name__ == "__main__":
	dummy_index = {
		"A" : [0, 1, 1, 1, 0],
		"B" : [1, 0, 1, 1, 0],
		"C" : [0, 0, 0, 1, 0],
		"D" : [0, 0, 1, 0, 1],
		"E" : [0, 1, 1, 1, 0],
	}


	pr = WeightedPageRanker(0.85, 1000)
	pr.fit(dummy_index)
	pr.calculateWeightedPR()
	pr.print_details()
