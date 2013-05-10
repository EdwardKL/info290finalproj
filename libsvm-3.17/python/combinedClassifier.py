import pickle
from svmutil import *


dpath = "infoProject/data/"

def log(message, file):
    print message
    file.write(str(message) + '\n')
    
    
def load(filename):
    f = open(filename, "r")
    result = pickle.load(f)
    f.close()
    return result

    
f = open("combined_classifier_logs", "w")

testLabels = load(dpath+"star_test_labels_1gram_100_large.json")
testData = load(dpath+"star_test_data_1gram_100_large.json")

nbClassifier = load("../../nb_classifier_1gram_10000_large_nochi")
treeClassifier = load("../../tree_classifier_1gram_100_large")
svmClassifier = svm_load_model("infoProject/models/star_unigram_model_1gram_10000_large.model")


matches = 0
mismatches = 0
scores = {1:0, 2:0, 3:0, 4:0, 5:0}
for i in range(len(testLabels)):
    
    data = testData[i]
    row = [0]*137908 # hardcoded, was determined during tree classification stage
    for key in data.keys():
        row[int(key)] = int(data[key])
    treelabel = treeClassifier.predict(row)[0]

    nblabel = nbClassifier.classify(data)
    
    svmlabels, p_acc, p_vals = svm_predict([0], [data], svmClassifier)
    svmlabel = svmlabels[0]
    
    labels = set([treelabel,nblabel,svmlabel])
    
    if len(labels) == 3:
        label = nblabel
    elif nblabel == treelabel or nblabel == svmlabel:
        label = nblabel
    elif treelabel == svmlabel:
        label = treelabel
    else:
        print "error, missed case"
    
    
    if label == testLabels[i]:
        matches += 1
        log("matched: label: "+str(label),f)
    else:
        mismatches += 1
        log("mismatched: label: "+str(label)+" was supposed to be: "+str(testLabels[i]),f)
    scores[int(label)]+=1
log("summary of results",f)
log("matches = "+str(matches),f)        
log("mismatches = "+str(mismatches),f)
log("guesses = "+repr(scores),f)
log("="*20,f)
log("="*20,f)
log("="*20,f)
        
        