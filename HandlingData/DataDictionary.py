import os
import json

# data directory
dataDir = '/tmp/Data/ds102'

# specifying the desciption JSON file
fDesc = os.path.join(dataDir,'dataset_description.json')

# Loading the JSON
h = open(fDesc, 'r')
dataDesc = json.load(h)
h.close()

# printing out the keys only from the resulting dictionary
print(dataDesc.keys())
