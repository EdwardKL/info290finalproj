from svmutil import *
import pickle

RESTRICT_TO_RESTAURANTS = False
CROSS_VALIDATE = False

def load(filename):
    f = open(filename, "r")
    result = pickle.load(f)
    f.close()
    return result

def log(message, file):
    print message
    file.write(str(message) + '\n')
    
def saveAndPredict(file, model, labels, features, lookup=None):
    svm_save_model(file, model)
    p_labs, p_acc, p_vals = svm_predict(labels, features, model)

    f = open(file +"_results", "w")
    log(p_acc, f)
    log('results for '+file+':',f)
    matches = 0
    mismatches = 0
    guesses = {}
    for i in range(len(p_labs)):
        if (p_labs[i] not in guesses):
            guesses[p_labs[i]] = 0
        guesses[p_labs[i]] += 1
        log("test data id: "+str(i),f)
    
        if lookup == None:
            log('predicted: '+ repr(p_labs[i]) + '  actual: ' + repr(labels[i]), f)
        else:
            log('predicted: '+ lookup(p_labs[i]) + ' actual: ' + lookup(labels[i]), f)
        if (p_labs[i] == labels[i]):
            matches += 1
        else:
            mismatches += 1        
    log('matches: '+str(matches), f)
    log('mismatches: '+str(mismatches),f)
    log('guess summary: ' + repr(guesses),f)
    f.close()

if CROSS_VALIDATE:
    gram = 1
    size = 10000
    for v in [2,3,4,5,6,7,8,9,10,11,12]:
        testLabels = load("infoProject/data/star_test_labels_"+str(gram)+"gram_100_large.json")
        testData = load("infoProject/data/star_test_data_"+str(gram)+"gram_100_large.json")
        trainLabels = load("infoProject/data/star_labels_"+str(gram)+"gram_"+str(size)+"_large.json")
        trainData = load("infoProject/data/star_data_"+str(gram)+"gram_"+str(size)+"_large.json")
        model = svm_train(trainLabels, trainData, '-h 0 -v '+str(v))
        saveAndPredict('infoProject/models/star_unigram_model_'+str(gram)+"gram_"+str(size)+"_large_"+str(v)+"_validation.model", model, testLabels, testData)
    
else:
    if RESTRICT_TO_RESTAURANTS:
        gram = 1
        for size in [100,1000,10000]:
            testLabels = load("infoProject/data/star_test_labels_"+str(gram)+"gram_100_large_restaurants.json")
            testData = load("infoProject/data/star_test_data_"+str(gram)+"gram_100_large_restaurants.json")
            trainLabels = load("infoProject/data/star_labels_"+str(gram)+"gram_"+str(size)+"_large_restaurants.json")
            trainData = load("infoProject/data/star_data_"+str(gram)+"gram_"+str(size)+"_large_restaurants.json")
            model = svm_train(trainLabels, trainData, '-h 0')
            saveAndPredict('infoProject/models/star_unigram_model_'+str(gram)+"gram_"+str(size)+"_large_restaurants.model", model, testLabels, testData)
    else:
        for gram in [1,2,3]:
            for size in [100,1000,10000]:
                if gram == 3 and size == 10000:
                    continue
                testLabels = load("infoProject/data/star_test_labels_"+str(gram)+"gram_100_large.json")
                testData = load("infoProject/data/star_test_data_"+str(gram)+"gram_100_large.json")
                trainLabels = load("infoProject/data/star_labels_"+str(gram)+"gram_"+str(size)+"_large.json")
                trainData = load("infoProject/data/star_data_"+str(gram)+"gram_"+str(size)+"_large.json")
                model = svm_train(trainLabels, trainData, '-h 0')
                saveAndPredict('infoProject/models/star_unigram_model_'+str(gram)+"gram_"+str(size)+"_large.model", model, testLabels, testData)

