Note: This part of the tutorial assumes that you have Python3 installed on your machine along with the packages: numpy and pandas. Rest of the packages used in the tutorial are available by deault in Python2 and Python3

* If not installed, you can install them using the following commands in a UNIX terminal window:
	+ sudo apt-get install python3 python3-pip
	+ sudo pip3 install numpy
	+ sudo pip3 install pandas

A decision tree is a decision support tool that uses a tree-like model of decisions and their possible consequences, including chance event outcomes, resource costs, and utility. It is one way to display an algorithm that only contains conditional control statements.

Decision trees are commonly used in operations research, specifically in decision analysis, to help identify a strategy most likely to reach a goal, but are also a popular tool in machine learning.

One can visualize a decision tree as a flowchart, where every branch occuring at one of the internal node represents a test condition or a test on an attribute like whether it rained or not or whether the marks obtained by a student was more than a certain threshold or not, each branch represents the outcome of the test, and each leaf node represents a class label (decision taken after computing all attributes). The paths from root to leaf represent classification rules.

* Decision trees have several advantages. They: 

	+ Are simple to understand and interpret. People are able to understand decision tree models after a brief explanation.
	+ Have value even with little hard data. Important insights can be generated based on experts describing a situation (its alternatives, probabilities, and costs) and their preferences for outcomes.
	+ Help determine worst, best and expected values for different scenarios.
	+ Can be combined with other decision techniques.


This program is an implementation of the ID3 - CART algorithm to generate a decision tree from a given dataset and a target attibute.

The ID3 algorithm begins with the original set S as the root node. On each iteration of the algorithm, it iterates through every unused attribute of the set S and calculates the entropy H(S) (or information gain IG(S) of that attribute. It then selects the attribute which has the smallest entropy (or largest information gain) value. The set S is then split or partitioned by the selected attribute to produce subsets of the data. (For example, a node can be split into child nodes based upon the subsets of the population whose ages are less than 50, between 50 and 100, and greater than 100.) The algorithm continues to recur on each subset, considering only attributes never selected before.

* Recursion on a subset may stop in one of these cases:

	+ every element in the subset belongs to the same class; in which case the node is turned into a leaf node and labelled with the class of the examples.
	+ there are no more attributes to be selected, but the examples still do not belong to the same class. In this case, the node is made a leaf node and labelled with the most common class of the examples in the subset.
	+ there are no examples in the subset, which happens when no example in the parent set was found to match a specific value of the selected attribute. An example could be the absence of a person among the population with age over 100 years. Then a leaf node is created and labelled with the most common class of the examples in the parent node's set.

Throughout the algorithm, the decision tree is constructed with each non-terminal node (internal node) representing the selected attribute on which the data was split, and terminal nodes (leaf nodes) representing the class label of the final subset of this branch.

* The algorithm goes as follows: 

	+ 1. Calculate the entropy of every attribute a of the data set S.
	+ 2. Partition ("split") the set S into subsets using the attribute for which the resulting entropy after splitting is minimized; or, equivalently, information gain is maximum
	+ 3. Make a decision tree node containing that attribute.
	+ 4. Recur on subsets using remaining attributes.

The associated program is implements the algorithm exactly for every recursion step. The program accepts only categorical values but one can imporve upon the decision values to be taken for splitting the dataset in the case of quantitative values.