Note: This part of the tutorial assumes that you have Python3 installed on your machine along with the packages: numpy and pandas. Rest of the packages used in the tutorial are available by deault in Python2 and Python3

* If not installed, you can install them using the following commands in a UNIX terminal window:
	+ sudo apt-get install python3 python3-pip
	+ sudo pip3 install numpy
	+ sudo pip3 install pandas


**What is Naive Bayes algorithm?**

It is a classification technique based on Bayes’ Theorem with an assumption of independence among predictors. In simple terms, a Naive Bayes classifier assumes that the presence of a particular feature in a class is unrelated to the presence of any other feature. For example, a fruit may be considered to be an apple if it is red, round, and about 3 inches in diameter. Even if these features depend on each other or upon the existence of the other features, all of these properties independently contribute to the probability that this fruit is an apple and that is why it is known as ‘Naive’.

Naive Bayes model is easy to build and particularly useful for very large data sets. Along with simplicity, Naive Bayes is known to outperform even highly sophisticated classification methods.

Bayes theorem provides a way of calculating posterior probability P(c|x) from P(c), P(x) and P(x|c).

	P(c|x) = P(x|c) * P(c) / P(x)


* where
	+ P(c|x) is the posterior probability of class (c, target) given predictor (x, attributes).
	+ P(c) is the prior probability of class.
	+ P(x|c) is the likelihood which is the probability of predictor given class.
	+ P(x) is the prior probability of predictor.

* Naive Bayes algorithm has several advantages:
	
	+ It is easy and fast to predict class of test data set. It also perform well in multi class prediction
	+ When assumption of independence holds, a Naive Bayes classifier performs better compare to other models like logistic regression and you need less training data.
	+ It perform well in case of categorical input variables compared to numerical variable(s). For numerical variable, normal distribution is assumed (bell curve, which is a strong assumption).

