import os
import json
import pandas as pd
from bids.layout import BIDSLayout

# Directory where your data set resides.
dataDir = '/tmp/Data/ds114'

# Creating the layout objects
layout = BIDSLayout(dataDir)


# Task events tsv file for fingerfootlips, all subjects, both sessions
taskTSV = layout.get(task='fingerfootlips',
                     suffix='events',
                     extension='tsv',
                     return_type='file')[0]

# reading the task info (as pandas data frame)
taskInfo = pd.read_csv(taskTSV, delimiter='\t')

# see whats in the task info
print(taskInfo)



# Other meta info from accompanying JSON file
taskJSON = layout.get(task='fingerfootlips',
                      suffix='bold',
                      extension='json',
                      return_type='file')[0]

# reading the JSON file
f = open(taskJSON,'r')
taskDict = json.load(f)
f.close()

# contents of the JSON file
for iKey, iValue in taskDict.items():
    print(iKey + ':   ' + str(iValue))
