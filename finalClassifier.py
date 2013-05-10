import pickle, re

dpath = "infoProject/data/"

WORD_RE = re.compile(r"[\w']+")

def log(message, file):
    print message
    file.write(str(message) + '\n')
 
def load(filename):
    f = open(filename, "r")
    result = pickle.load(f)
    f.close()
    return result

def getFeatureVector(text, symTable):
    words = WORD_RE.findall(text)
    result = {}
    for word in words:
        if word in symTable:
            if symTable[word] not in result:
                result[symTable[word]] = 0
            result[symTable[word]] += 1
    return result
    
f = open("final_classifier_logs", "w")
print "Welcome!"
print "Loading Naive Bayes classifier..."

nbClassifier = load("nb_classifier_1gram_10000_large_nochi")

print "Loaded."

print "Loading symbol table..."

symTable = load("libsvm-3.17/python/infoProject/symTable_1gram")

print "Loaded."
print ""
print "Done."
print ""
print "Please input a review. Then we will return what number of stars we think it should have."

while(True):
    text = raw_input("Input a review: ")
    label = nbClassifier.classify(getFeatureVector(text, symTable))
    print ""
    if label != 1:
        print "We predict that this review should have "+str(label)+" stars"
    else:
        print "We predict that this review should have 1 star"
    print ""
    print ""
    
        