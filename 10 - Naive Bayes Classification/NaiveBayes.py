import pandas as pd
from operator import itemgetter
from pprint import pprint


def preprocess_data(data, return_thresholds=False):
	columns = data.columns
	thresholds = []
	for column in columns[:-1]:
		min_val = 0
		max_val = data.loc[:, column].max()
		threshold = (max_val + min_val) / 2
		thresholds.append(threshold)
		data.loc[(data[column] <= threshold), column] = 0
		data.loc[(data[column] > threshold), column] = 1
	thresholds = pd.DataFrame(
		{'column': columns[:-1], 'threshold': thresholds}
	).set_index(keys=['column'])

	if return_thresholds:
		return data, thresholds
	else:
		return data


class NBClassifier():
	def __init__(self):
		pass

	def load_data(self, train_data, target=None):
		self.train_data = train_data
		if not target:
			self.target = self.train_data.columns[-1]
		else:
			self.target = target

		self.outcomes = self.train_data[self.target].unique()

		self.outcomeProb = {}
		total_count = self.train_data.shape[0]
		for outcome in self.outcomes:

			count = self.train_data.loc[
				(self.train_data[self.target] == outcome)
			].shape[0]
			self.outcomeProb[outcome] = count / total_count

		self.probTable = pd.DataFrame(columns=['key'].append(self.outcomes))
		for column in train_data.columns[:-1]:
			for entry in train_data[column].unique():
				temp = {}
				temp['key'] = column + '_' + str(entry)

				for outcome in self.outcomes:
					temp[outcome] = self.calcProb(column, entry, outcome)

				self.probTable = self.probTable.append(
					pd.DataFrame(temp.copy(), index=[0]), ignore_index=True
				)

		self.probTable = self.probTable.set_index('key')

		print("\nThe probabilites for each entry for each column is as follows: ")
		pprint(self.probTable)

	def calcProb(self, column, entry, outcome):
		tot_count = self.train_data.loc[
			self.train_data[self.target] == outcome
		].shape[0]

		count = self.train_data.loc[
			(self.train_data[column] == entry) & (self.train_data[self.target] == outcome)
		].shape[0]

		return count / tot_count

	def predict(self, test_data):
		labels = []
		for _, test_instance in test_data.iterrows():
			results = {}
			for outcome in self.outcomes:
				results[outcome] = 1

				for key in test_instance.keys():
					results[outcome] *= self.probTable.loc[
						key + '_' + str(test_instance.loc[key]), outcome
					]

				results[outcome] *= self.outcomeProb[outcome]

			labels.append(max(results.items(), key=itemgetter(1))[0])
		return list(enumerate(labels))


print("Sample Question Part - A -------------------------------------------\n")

train_data = pd.read_csv("train_A.csv")
print("\nThe training data looks like :")
pprint(train_data)

target = "Buys_computer"

test_data = pd.read_csv("test_A.csv")
print("\nThe testing data looks like :")
pprint(test_data)

nbc = NBClassifier()
nbc.load_data(train_data, target)
print("\nThe output for the test instances are: \n")
for outcome in nbc.predict(test_data):
	print(outcome[0], ": ", outcome[1])


print("\nSample Question Part - B -----------------------------------------\n")

train_data = pd.read_csv("train_B.csv")
train_data, threasholds = preprocess_data(train_data, return_thresholds=True)
print("\nThe training data after preprocessing looks like :")
pprint(train_data)

target = "Category"

test_data = pd.read_csv("test_B.csv")
test_data = preprocess_data(test_data)
print("\nThe testing data after preprocessing looks like :")
pprint(test_data)


nbc2 = NBClassifier()
nbc2.load_data(train_data, target)
print("\nThe output for the test instances are: \n")
for outcome in nbc2.predict(test_data):
	print(outcome[0], ": ", outcome[1])
