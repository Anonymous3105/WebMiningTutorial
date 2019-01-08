Note: This part of the tutorial assumes that you have Python3 installed on your machine along with the packages: numpy and pandas. Rest of the packages used in the tutorial are available by deault in Python2 and Python3

* If not installed, you can install them using the following commands in a UNIX terminal window:
	+ sudo apt-get install python3 python3-pip
	+ sudo pip3 install numpy
	+ sudo pip3 install pandas

* Sessionization is the act of turning event-based data into sessions, the ordered list of a user’s actions in completing a task. It is widely used in several domains, such as:

	+ Web analytics. This is the most common use, where a session is composed of a user’s actions during one particular visit to the website. You can think of this as a buying session on a e-business website for example. Using sessions enables you to answer the following questions: what are the most frequent paths to purchase on my website? How do my users get to a specific page? When / why do they leave? Are some acquisition funnels more efficient than others?

	+ Trip analytics. Given the GPS coordinates history of a vehicle, you can compute sessions in order to extract the different trips. Each trip can then be labelled distinctly (user going to work, on holidays, …).

	+ Predictive maintenance. Here a session can be all information relative to a machine’s behavior (machine working, on idle … etc.) until a change in its assignation.

The associated program uses the Pandas Grouper to group the dataset by taking one attribue at a time.