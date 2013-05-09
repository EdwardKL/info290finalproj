import json

f = open("yelp_academic_dataset.json")
bf = open("data/businesses.json", "w")
result = {}
for line in f:
    l = json.loads(line)
    if l['type'] == 'business':
        categories = l['categories']
        if (len(categories) > 0):
            result[l['business_id']] = categories
bf.write(json.dumps(result))
bf.close()
f.close()