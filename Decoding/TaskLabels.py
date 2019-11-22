import os
import numpy as np
import pandas as pd

# data directory
dataDir = '/tmp/Data/ds114'

# parameters
TR = 2.5
nTime = 184

# event timing data
fEvent = os.path.join(dataDir, 'task-fingerfootlips_events.tsv')
taskData = pd.read_csv(fEvent, sep='\t')

# function to return task label based on the timepoint
def returnTask(t, TR, tableTask):
    # the time point in sec
    tSec = t*TR
    # if t is before the first onset
    if tSec < tableTask.iloc[0].onset:
        returnLabel = 'Rest'
    else:
        # interval where t falls in
        tOnset = tableTask[tableTask.onset<=tSec].tail(1).onset.squeeze()
        tEnd = tOnset + tableTask[tableTask.onset<=tSec].tail(1).duration.squeeze()
        tTask = tableTask[tableTask.onset<=tSec].tail(1).trial_type.squeeze()
        # if t falls between tOnset and tEnd
        if np.logical_and((tOnset<= tSec), (tSec <=tEnd)):
            returnLabel = tTask
        else:  # otherwise its rest
            returnLabel = 'Rest'
    return returnLabel


# # sanity check
# for iTR in range(nTime):
#     print('%5.1f' % (iTR*TR), end='')
#     print('\t' + returnTask(iTR,TR,taskData))



# list of subjects to be included
listSub = ['01', '02', '05', '06']
# list of sessions to be included
listSes = ['test', 'retest']
# handedness dictionary
handDict = {'01':'Left',
            '02':'Right',
            '05':'Right',
            '06':'Left'}

# initializing lists to record labels
colSub = []
colSes = []
colHand = []
colTask = []
# loop over subjects, session, time points
for iSub in listSub:
    for iSes in listSes:
        for t in range(nTime):
            colSub.append('sub-'+iSub)
            colSes.append(iSes)
            colHand.append(handDict[iSub])
            colTask.append(returnTask(t, TR, taskData))

# creating task labels
colLabel = []
for i in range(len(colTask)):
    if colTask[i] in ['Finger', 'Foot']:
        colLabel.append(colHand[i]+'_'+colTask[i])
    else:
        colLabel.append(colTask[i])

# task label, numeric
dictTask = {'Rest': 0,
            'Left_Finger':1,
            'Right_Finger':2,
            'Left_Foot':3,
            'Right_Foot':4,
            'Lips':5}
colNumLabel = []
for iLabel in colLabel:
    colNumLabel.append(dictTask[iLabel])


# creating a data frame
tableTrain = pd.DataFrame()
tableTrain['Subject'] = colSub
tableTrain['Session'] = colSes
tableTrain['Handedness'] = colHand
tableTrain['Condition'] = colTask
tableTrain['Label'] = colLabel
tableTrain['NumLabel'] = colNumLabel

tableTrain.to_csv('TaskInfo_Train.csv', index=False)
