import os
import pandas as pd

# data directory & file
dataDir = '/tmp/Data/ds102'
fileTable = os.path.join(dataDir,'participants.tsv')

# Loading the data file as a data frame object
ptData = pd.read_csv(fileTable, sep='\t')


# Sorting by age in descending order
ptData.sort_values(by='age', inplace=True)

# output file name
fileOut = os.path.join(dataDir,'sorted_D.csv')

# selecting observations with gender=D, saving to a CSV file
ptData[ptData.gender=='D'].to_csv(fileOut)
