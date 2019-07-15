import numpy as np

# subject ID
subjID = np.array(['sub001']*3 + ['sub005']*4 + ['sub010']*3)
# response time (ms)
RT = np.array([ 98,  96,  86,  90,  95,  80, 117,  90, 114, 113])
# score
score = np.array([0, 0, 1, 0, 1, 0, 0, 0, 1, 0])

print('ID\tRT\tScore')
for i,iID in enumerate(subjID):
    print(iID, RT[i], score[i], sep='\t')
