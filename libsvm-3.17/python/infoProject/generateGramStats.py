import json
import re
import pickle

WORD_RE = re.compile(r"[\w']+")

STAR = True
RESTRICT_TO_RESTAURANTS = False
USE_GRAM_HASHES = True
USE_REVIEW_LENGTH = False

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

for gram in [1,2,3]:
    slabels = []
    clabels = []
    sdata = []
    cdata = []
    scount = {1:0, 2:0, 3:0, 4:0, 5:0}
    count = 0
    if gram == 2 and not USE_GRAM_HASHES:
        break
    for i, size in enumerate([100,1000,10000]):
        if gram == 3 and i == 2:
            continue
        print gram
        print size      
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
    ggram = {}
    csvf1 = open("gram_stats_"+str(gram)+"gram_1star.csv","w")
    csvf2 = open("gram_stats_"+str(gram)+"gram_2star.csv","w")
    csvf3 = open("gram_stats_"+str(gram)+"gram_3star.csv","w")
    csvf4 = open("gram_stats_"+str(gram)+"gram_4star.csv","w")
    csvf5 = open("gram_stats_"+str(gram)+"gram_5star.csv","w")
    for i, data in enumerate(sdata):
        for g, c in data.iteritems():
            if (slabels[i],g) not in ggram:
                ggram[(slabels[i],g)] = c
            else:
                ggram[(slabels[i],g)] += c
    for (star, g), c in ggram.iteritems():
        if star == 1:
            csvf1.write(str(lookup[g])+","+str(c)+"\n")
        elif star == 2:
            csvf2.write(str(lookup[g])+","+str(c)+"\n")
        elif star == 3:
            csvf3.write(str(lookup[g])+","+str(c)+"\n")
        elif star == 4:
            csvf4.write(str(lookup[g])+","+str(c)+"\n")
        else:
            csvf5.write(str(lookup[g])+","+str(c)+"\n")
    ggram = {}
    csvf1.close()
    csvf2.close()
    csvf3.close()
    csvf4.close()
    csvf5.close()
    f.close()
    f = open("yelp_academic_dataset.json", "r")
    
        

lookupf = open("data/lookup", "w")
pickle.dump(lookup, lookupf)
lookupf.close()

bf.close()
