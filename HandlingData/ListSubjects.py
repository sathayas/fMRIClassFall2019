import os

# Directory where your data set resides.
dataDir = '/tmp/Data/ds102'
listDirContents = os.listdir(dataDir)

# getting a list of directory contents
dirContents = os.listdir(dataDir)
dirContents.sort()

# printing out a list of subjects (i.e., directories starting with sub-)
for iFile in dirContents:
    if 'sub-' in iFile:
        print(iFile)
