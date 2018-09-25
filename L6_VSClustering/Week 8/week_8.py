import requests
from bs4 import BeautifulSoup as bs
from sys import exit
import string
import math
from pprint import pprint

def readFromFile(filename):
    try:
        with open(filename, 'r') as file:
            return(file.read().strip())
    except IOError:
        print("Invalid Filename! ({})".format(filename))
        return None

def readFromURL(url):
    res = None
    try:
        res = requests.get(url)
    except Exception:
        try:
            print("Could not reach the URL ({})".format(url))
        except UnicodeEncodeError:
            print("Could not reach the URL (Unable to parse URL)")
        return None

    if res.status_code == requests.codes.ok:    #pylint: disable=E1101
        soup = bs(res.text, 'html.parser')

        # Removing style blocks
        [tag.decompose() for tag in soup("style")]

        # Removing scripts
        [tag.decompose() for tag in soup("script")]
        
        # Removing tables
        [tag.decompose() for tag in soup("table")]
        
        return soup.get_text().strip()
    else:
        try:
            print("Could not reach the URL ({})".format(url))
        except UnicodeEncodeError:
            print("Could not reach the URL (Unable to parse URL)")
        return None

# Document content extractor
def getTextsFromSource(sourceFile):
    sources = []
    contents = []
    # Get sources from source file
    print("Reading sources from file")
    try:
        sources = readFromFile(sourceFile).strip().split('\n')
    except IOError:
        print("Couldn't read from sources file! Check if sources.txt exists")
        exit()
    print("DONE\n")

    print("Beginning scraping operation")
    for source in sources:
        print("Scraping from {}".format(source))

        content = None
        if source[:7] == "http://" or source[:8] == "https://":
            content = readFromURL(source)
        else:
            content = readFromFile(source)
        if not content:
            continue
        contents.append(content)
    print("DONE\n")
    return(contents)

def sanitizeText(text):
    if type(text) == list:
        for index in range(len(text)):
            text[index] = sanitizeText(text[index])
    else:
        text = text.lower()
        for c in string.punctuation:
            text = text.replace(c, '')
        text = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
    return text

def makeTokens(raw, special_tokens=[], limit=500):
    tokens = []

    raw = sanitizeText(raw)

    for exception in special_tokens:
        clean = exception.replace(' ', '')
        raw = raw.replace(exception, clean)

    tokens = raw.split(" ")[:limit]
    return tokens

def makeVectors(documents, keywords):
    vectors = []

    template = []
    for _ in range(len(keywords)):
        template.append(0)
    
    special_tokens = []
    for index in range(len(keywords)):
        if type(keywords[index]) is list:
            for subindex in range(len(keywords[index])):
                if ' ' in keywords[index][subindex]:
                    special_tokens.append(keywords[index][subindex])
                    keywords[index][subindex] = keywords[index][subindex].replace(' ', '')
        else:
            if ' ' in keywords[index]:
                special_tokens.append(keywords[index])
                keywords[index] = keywords[index].replace(' ', '')

    for document in documents:
        document = makeTokens(document, special_tokens)
        new_vec = template.copy()
        for index in range(len(keywords)):
            for word in document:
                if type(keywords[index]) is list:
                    if word in keywords[index]:
                        new_vec[index] += 1
                else:
                    if word == keywords[index]:
                        new_vec[index] += 1

        vectors.append(new_vec)
    return vectors

def printClusters(clusters):
    print("\nClusters are:")
    for cluster in list(set(clusters)):
        print("In cluster {}".format(cluster))
        print("--------------")
        for index in range(len(clusters)):
            if clusters[index] == cluster:
                print(index)
    print()

class DocumentClusterer:
    def __init__(self):
       pass
    
    def calc_dist(self, vec1, vec2):
        dist = 0.0
        # Calculating Euclidean Distance
        for index in range(len(vec1)):
            dist += (vec1[index] - vec2[index])**2
        dist = dist**(0.5)
        return dist
    
    def find_closest(self, source):
        closest = []
        # If there are documents within threshold distance
        if self.closeMatrix[source]: 
            minDist = self.distMatrix[source][self.closeMatrix[source][0]]
            for document in self.closeMatrix[source]:
                # If found a closer document, replace list with new one
                if self.distMatrix[source][document] < minDist:
                    closest = [[source, document]]
                    minDist = self.distMatrix[source][document]
                # If found document at same distance, add to list
                elif self.distMatrix[source][document] == minDist:
                    closest.append([source, document])
        return closest
    
    def load(self, vectors):
        self.vectors = vectors
        self.distMatrix = []
        self.closeMatrix = []
        
        template = []
        # Initialtizing distance matrix and closest neighbours matrix
        for _ in range(len(self.vectors)):
            template.append(0.0)
            self.closeMatrix.append([])
        for _ in range(len(self.vectors)):
            self.distMatrix.append(template.copy())

        maxDist = 0
        minDist = math.inf

        for i in range(len(self.vectors)):
            for j in range(len(self.vectors)):
                # Calculate distances between vectors
                if (i != j) and (self.distMatrix[i][j] == 0.0):
                    distance = self.calc_dist(self.vectors[i], self.vectors[j])
                    if distance > maxDist:
                        maxDist = distance
                    if distance < minDist:
                        minDist = distance
                    self.distMatrix[i][j] = self.distMatrix[j][i] = distance

        threshold = (maxDist + minDist)/2
        for i in range(len(self.vectors)):
            for j in range(i+1, len(self.vectors)):
                # add vectors to closeMatrix if within threshold
                if self.distMatrix[i][j] < threshold:
                    self.closeMatrix[i].append(j)
                    self.closeMatrix[j].append(i)
        return threshold

    def cluster(self):
        self.labels = []
        # each document in its own cluster
        for label in range(len(self.vectors)):
            self.labels.append(label)
          
        # Performing clustering
        for document in range(len(self.closeMatrix)):
            # find closest neighbours
            closest = self.find_closest(document)

            # refining clusters by relabelling as same cluster
            for pair in closest:
                for index in range(len(self.labels)):
                    if self.labels[index] == self.labels[pair[1]]:
                        self.labels[index] = self.labels[pair[0]]

        # Relabelling clusters
        old_labels = list(set(self.labels))
        for index in range(len(self.labels)):
            self.labels[index] = old_labels.index(self.labels[index])
        
        # Determining cluster centers
        self.centroids = []
        clusters_count = [] 
        
        template = []
        no_of_keywords = 0 
        for _ in self.vectors[0]:
            template.append(0.0)
            no_of_keywords += 1
        
        # Initialize centroids
        for _ in list(set(self.labels)):
            self.centroids.append(template.copy())
            clusters_count.append(0)

        # Generate cluster centers
        for index in range(len(self.labels)):
            clusters_count[self.labels[index]] += 1
            curr_vector = self.vectors[index]
            for component in range(no_of_keywords):
                self.centroids[self.labels[index]][component] += curr_vector[component]
        
        for index in range(len(self.centroids)):
            for component in range(no_of_keywords):
                self.centroids[index][component] /= clusters_count[index]

        return self.labels


keywords_A = [
    'Automotive',
    ['Car', 'Cars'],
    'motorcycles',
    'self-drive',
    'IoT',
    'hire',
    'Dhoni',
]

keywords_B = [
    'Tesla',
    'Electric',
    ['Car', 'Cars', 'Vehicle', 'Vehicles', 'Automobile', 'Automobiles'],
    'pollution',
    'de-monetisation',
    'GST',
    'black money'
]

# keywords = sanitizeText(keywords_A)
keywords = sanitizeText(keywords_B)

# documents = getTextsFromSource('./sources_A.txt')
documents = getTextsFromSource('./sources_B.txt')

vectors = makeVectors(documents, keywords)

print("Performing Nearest Neighbour Clustering")
print("---------------------------------------")
print("Vectors are: ")
pprint(vectors)

dc = DocumentClusterer()
threshold = dc.load(vectors)
print("\nDistance Matrix is ")
pprint(dc.distMatrix)
print("Generated threshold is {}".format(threshold))

clusters = dc.cluster()
printClusters(clusters)


print("Performing Hierarchical Clustering")
print("----------------------------------")
print("Centroids are: ")
pprint(dc.centroids)

hdc = DocumentClusterer()
hdc_threshold = hdc.load(dc.centroids)
print("\nDistance Matrix is ")
pprint(hdc.distMatrix)
print("Generated threshold is {}".format(hdc_threshold))
hdc_clusters = hdc.cluster()
printClusters(hdc_clusters)
