from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import pickle

RESTRICT_TO_RESTAURANTS = False
USE_TREE = False
dpath = "libsvm-3.17/python/infoProject/data/"

def log(message, file):
    print message
    file.write(str(message) + '\n')
    
    
def load(filename):
    f = open(filename, "r")
    result = pickle.load(f)
    f.close()
    return result

    
f = open("tree_classifier_logs", "w")

# find the best features for 1 gram
gram = 1
size = 100
if RESTRICT_TO_RESTAURANTS:
    testLabels = load(dpath+"star_test_labels_"+str(gram)+"gram_100_large_restaurants.json")
    testData = load(dpath+"star_test_data_"+str(gram)+"gram_100_large_restaurants.json")
    trainLabels = load(dpath+"star_labels_"+str(gram)+"gram_"+str(size)+"_large_restaurants.json")
    trainData = load(dpath+"star_data_"+str(gram)+"gram_"+str(size)+"_large_restaurants.json")
else:
    testLabels = load(dpath+"star_test_labels_"+str(gram)+"gram_100_large.json")
    testData = load(dpath+"star_test_data_"+str(gram)+"gram_100_large.json")
    trainLabels = load(dpath+"star_labels_"+str(gram)+"gram_"+str(size)+"_large.json")
    trainData = load(dpath+"star_data_"+str(gram)+"gram_"+str(size)+"_large.json")

classif = None
if USE_TREE:
    classif = DecisionTreeClassifier(random_state=0,compute_importances=True)
else:
    classif = RandomForestClassifier(random_state=0,compute_importances=True)
# tree classifier needs a matrix for its inputs
# first find the length of the matrix
maxSoFar = 0
for data in trainData+testData:
    temp = max([int(key) for key in data.keys()]+[0]) # add the 0 to avoid max of empty seq errors
    if temp > maxSoFar:
        maxSoFar = temp
maxSoFar +=1 # to avoid out of bounds errors
X = []
for data in trainData:
    row = [0]*maxSoFar
    for key in data.keys():
        row[int(key)] = int(data[key])
    X.append(row)
    
classif.fit(X,trainLabels).transform(X)

importantFeatures = sorted([(freq,i) for i, freq in enumerate(classif.feature_importances_)])

# symbol table. Maps the data's index to the index of our new, smaller feature vector
symTable = {}
length = 1000 # size of our new feature vector
for i in range(length): # get the first 1000 features
    symTable[importantFeatures[i][0]] = i

for gram in [1,2,3]:
    for size in [100,1000,10000]:
        if (gram == 3 or gram == 2) and size == 10000:
            continue
        testLabels = None
        testData = None
        trainLabels = None
        trainData = None
        
        if RESTRICT_TO_RESTAURANTS:
            testLabels = load(dpath+"star_test_labels_"+str(gram)+"gram_100_large_restaurants.json")
            testData = load(dpath+"star_test_data_"+str(gram)+"gram_100_large_restaurants.json")
            trainLabels = load(dpath+"star_labels_"+str(gram)+"gram_"+str(size)+"_large_restaurants.json")
            trainData = load(dpath+"star_data_"+str(gram)+"gram_"+str(size)+"_large_restaurants.json")
        else:
            testLabels = load(dpath+"star_test_labels_"+str(gram)+"gram_100_large.json")
            testData = load(dpath+"star_test_data_"+str(gram)+"gram_100_large.json")
            trainLabels = load(dpath+"star_labels_"+str(gram)+"gram_"+str(size)+"_large.json")
            trainData = load(dpath+"star_data_"+str(gram)+"gram_"+str(size)+"_large.json")
        
        classif = RandomForestClassifier()
        X = []
        for data in trainData:
            row = [0]*length
            for key in data.keys():
                key = int(key)
                if key in symTable:
                    row[symTable[key]] = int(data[key])
            X.append(row)
            
        classif = classif.fit(X, trainLabels)
        cf = open("rf_classifier_"+str(gram)+"gram_"+str(size)+"_large","w")
        pickle.dump(classif, cf)
        matches = 0
        mismatches = 0
        scores = {1:0, 2:0, 3:0, 4:0, 5:0}
        for i in range(len(testLabels)):
            data = testData[i]
            row = [0]*length
            for key in data.keys():
                key = int(key)
                if key in symTable:
                    row[symTable[key]] = int(data[key])
            label = classif.predict(row)
            if label == testLabels[i]:
                matches += 1
                log("matched: label: "+str(label),f)
            else:
                mismatches += 1
                log("mismatched: label: "+str(label)+" was supposed to be: "+str(testLabels[i]),f)
            scores[int(label)]+=1
        log("summary of results for: gram: "+str(gram) +" size: "+str(size),f)
        log("matches = "+str(matches),f)        
        log("mismatches = "+str(mismatches),f)
        log("guesses = "+repr(scores),f)
        log("="*20,f)
        log("="*20,f)
        log("="*20,f)