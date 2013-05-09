import pickle
import numpy as np
from nltk.probability import FreqDist
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


USE_CHI_SQUARE = False
RESTRICT_TO_RESTAURANTS = False

if USE_CHI_SQUARE:
    pipeline = Pipeline([('tfidf', TfidfTransformer()),
                         ('chi2', SelectKBest(chi2, k=1000)),
                         ('nb', MultinomialNB())])
else:
    pipeline = Pipeline([('tfidf', TfidfTransformer()),
                         ('nb', MultinomialNB())])

dpath = "libsvm-3.17/python/infoProject/data/"

def log(message, file):
    print message
    file.write(str(message) + '\n')
    
    
def load(filename):
    f = open(filename, "r")
    result = pickle.load(f)
    f.close()
    return result

    
f = open("nb_classifier_logs", "w")


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
        classif = SklearnClassifier(pipeline)
        classif.train(zip(trainData,trainLabels))
        cf = None
        if USE_CHI_SQUARE:
            cf = open("nb_classifier_"+str(gram)+"gram_"+str(size)+"_large","w")
        else:
            cf = open("nb_classifier_"+str(gram)+"gram_"+str(size)+"_large_nochi","w")
        pickle.dump(classif, cf)
        
        
        
        matches = 0
        mismatches = 0
        scores = {1:0, 2:0, 3:0, 4:0, 5:0}
        for i in range(len(testLabels)):
            label = classif.classify(testData[i])
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
        
        