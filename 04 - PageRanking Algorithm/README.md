Note: This part of the tutorial assumes that you have Python3 installed on your machine 

* If not installed, you can install them using the following commands in a UNIX terminal window:
	+ sudo apt-get install python3

This tutorial explores a rather interesting concept of web page indexing: Google's Page Ranking Algorithm. It is used by Google Search to rank web pages in their search engine results. PageRank works by counting the number and quality of links to a page to determine a rough estimate of how important the website is. The underlying assumption is that more important websites are likely to receive more links from other websites.

PageRank is a link analysis algorithm and it assigns a numerical weighting to each element of a hyperlinked set of documents, such as the World Wide Web, with the purpose of "measuring" its relative importance within the set. The algorithm may be applied to any collection of entities with reciprocal quotations and references. The numerical weight that it assigns to any given element E is referred to as the PageRank of E and denoted by PR(E). Other factors like Author Rank can contribute to the importance of an entity.

**So what is PageRank?**

In short PageRank is a “vote”, by all the other pages on the Web, about how important a page is. A link to a page counts as a vote of support. If there’s no link there’s no support (but it’s an abstention from voting rather than a vote against the page).

Quoting from the original Google paper, PageRank is defined like this:

We assume page A has pages T1...Tn which point to it (i.e., are citations). The parameter d is a damping factor which can be set between 0 and 1. We usually set d to 0.85. There are more details about d in the next section. Also C(A) is defined as the number of links going out of page A. The PageRank of a page A is given as follows:

	PR(A) = (1-d) + d*(PR(T1)/C(T1) + ... + PR(Tn)/C(Tn))

We also explore something called the weighted page rank algorithm, ax extenstion to the page rank algorithm that takes both the inlinks and outlinks of the pages into account when computing the rank of a page and is said to perform better when it comes to a highly interconnected large web document collection. It computes the rank of a page as follows:

Each outlink page gets a value proportional to its popularity (its number of inlinks and outlinks). The popularity from the number of inlinks and outlinks is recorded as W_in(v,u) and W_out(v,u), respectively

W_in(v,u) is the weight of link(v, u) calculated based on the number of inlinks of page u and the number of inlinks of all reference pages of page v. 

	W_in(v,u) = I_u / sum(I_p) for all p belonging to R(v)

where I_u and I_p represent the number of inlinks of page u and page p, respectively. R(v) denotes the reference page list of page v.

Similarly, W_out(v,u) is the weight of link(v, u) calculated based on the number of outlinks of page u and the number of outlinks of all reference pages of page v. 

	W_out(v,u) = O_u / sum(O_p) for all p belonging to R(v)

where O_u and O_p represent the number of outlinks of page u and page p, respectively. R(v) denotes the reference page list of page v.

And the weighted page rank of each page is computed as:

	PR(A) = (1-d) + d * sum(PR(p) * W_in(p, A) * W_out(p, A)) for all pages p which point to A

This tutorial provides a programmable solution to multiple iterations of the above equation to all the interlinked documents in a web collection.

In this program, the input is given in the form of a dictionary that includes the name of the page as the key value and a list of all the pages that it links to as value. A function converts this input frmat to an adjacency matrix-dictionary format for easy processing. After which, the pageranks of all the pages are computed repeatedly for a given number of iterations (usually large but computationaly feasible) so that they converge into low varied values, i.e. these values don't change much in the later iterations.

The PageRanker class has two very important functions: gen_inlinks and gen_outlinks that compute the number of inlinks and outlinks for each page in the collection which are very vital components in the computation using the above formula. Along these two functions there are two auxillary functions get_win and get_wout, which are used as components in computing the weighted page ranks if required.

The PageRanker object computes the ranks of the page by the simple algorithm and only computes the weighted ranks if it is initialized with weighted parameter as True.

In both the cases, the required formula is used to compute the ranks of all the pages in the given collection over a large number of iterations and displayed as a result.

Note: In the case of Page Ranking algorithm, the sum of all the page ranks is equal to the number of documents in the collection at any given iteration.