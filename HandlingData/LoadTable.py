import os
import pandas as pd

# data directory & file
dataDir = '/tmp/Data/ds102'
fileTable = os.path.join(dataDir,'participants.tsv')

# Loading the data file as a data frame object
ptData = pd.read_csv(fileTable, sep='\t')
