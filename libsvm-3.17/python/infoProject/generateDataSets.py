import json
import re
import pickle

WORD_RE = re.compile(r"[\w']+")

STAR = True
RESTRICT_TO_RESTAURANTS = False
USE_GRAM_HASHES = False
USE_REVIEW_LENGTH = True

stable = {}
lookup = []
counter = 0
def getFeatureVector(text, grams):
    global counter
    global stable
    global lookup
    result = {}
    words = WORD_RE.findall(text)
    if USE_REVIEW_LENGTH:
        return len(words)
    if USE_GRAM_HASHES:
        # unigrams
        for word in words:
            if word not in stable:
                stable[word] = counter
                counter += 1
                lookup.append(word)
            if stable[word] not in result:
                result[stable[word]] = 0
            result[stable[word]] += 1
        if grams > 1:
            # bigrams
            for i in range(len(words)-1):
                word = words[i] + ' ' + words[i+1]
                if word not in stable:
                    stable[word] = counter
                    counter += 1
                    lookup.append(word)
                if stable[word] not in result:
                    result[stable[word]] = 0
                result[stable[word]] += 1
        if grams > 2:
            # trigrams
            for i in range(len(words)-2):
                word = words[i] + ' ' + words[i+1] + ' ' + words[i+2]
                if word not in stable:
                    stable[word] = counter
                    counter += 1
                    lookup.append(word)
                if stable[word] not in result:
                    result[stable[word]] = 0
                result[stable[word]] += 1
    return result


f = open("yelp_academic_dataset.json", "r")
bf = open("data/businesses.json", "r")
businesses = pickle.load(bf)

slabelsf = None
sdataf = None
clabelsf = None
cdataf = None
csvf = None

for gram in [1,2,3]:
    slabels = []
    clabels = []
    sdata = []
    cdata = []
    scount = {1:0, 2:0, 3:0, 4:0, 5:0}
    count = 0
    if gram == 2 and not USE_GRAM_HASHES:
        break
    if USE_REVIEW_LENGTH:
        csvf = open("data/review_lengths.csv","w")
    for i, size in enumerate([100,1000,10000,100]):
        if gram == 3 and i == 2:
            continue
        print gram
        print size
        if i == 3:
            scount = {1:0, 2:0, 3:0, 4:0, 5:0}
            count = 0
            slabels = []
            clabels = []
            sdata = []
            cdata = []            
        if STAR:
            addon = ""
            if RESTRICT_TO_RESTAURANTS:
                addon = "_restaurants"
            if USE_REVIEW_LENGTH:
                addon = "_length_only"
            if i == 3:
                slabelsf = open("data/star_test_labels_"+str(gram)+"gram_"+str(size)+"_large"+addon+".json", "w")
                sdataf = open("data/star_test_data_"+str(gram)+"gram_"+str(size)+"_large"+addon+".json", "w")
            else:
                slabelsf = open("data/star_labels_"+str(gram)+"gram_"+str(size)+"_large"+addon+".json", "w")
                sdataf = open("data/star_data_"+str(gram)+"gram_"+str(size)+"_large"+addon+".json", "w")
        else:
            clabelsf = open("data/category_labels_"+str(gram)+"gram_"+str(size)+"_large"+addon+".json", "w")
            cdataf = open("data/category_data_"+str(gram)+"gram_"+str(size)+"_large"+addon+".json", "w")
        for line in f:
            if count >= size * 5:
                break
            l = json.loads(line)
            if l['type'] == 'review':
                feature = getFeatureVector(l['text'], gram)
                if STAR:
                    business = l['business_id']
                    if (not RESTRICT_TO_RESTAURANTS) or ('Restaurants' in businesses[business]):
                        star = int(l['stars'])
                        if scount[star] >= size:
                            continue
                        else:
                            scount[star] += 1
                            count += 1
                        if USE_REVIEW_LENGTH:
                            csvf.write(str(star)+","+str(feature)+"\n")
                        slabels.append(star)
                        sdata.append(feature)
                else:
                    business = l['business_id']
                    if business in businesses:
                        for category in businesses[business]:
                            clabels.append(category)
                            cdata.append(feature)
        if STAR:
            pickle.dump(slabels, slabelsf)
            pickle.dump(sdata, sdataf)
            sdataf.close()
            slabelsf.close()
        else:
            pickle.dump(clabels, clabelsf)
            pickle.dump(cdata, cdataf)
            cdataf.close()
            clabelsf.close()
    if USE_REVIEW_LENGTH:
        csvf.close()
    f.close()
    f = open("yelp_academic_dataset.json", "r")
    
        

lookupf = open("data/lookup", "w")
pickle.dump(lookup, lookupf)
lookupf.close()

bf.close()