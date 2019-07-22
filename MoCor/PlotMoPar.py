import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# loading the data
resDir = '/tmp/Data/ds102/WorkflowOutput/Results/par_file'
resFname = 'sub-26_task-flanker_run-1_bold_roi_mcf.nii.gz.par'
moData = pd.read_csv(os.path.join(resDir,resFname),
                     header=None,
                     delimiter=r"\s+")

# plotting rotations
plt.plot(moData[0],'r', label='roll')
plt.plot(moData[1],'g', label='picth')
plt.plot(moData[2],'b', label='yaw')
plt.title('Rotation')
plt.xlabel('time points')
plt.ylabel('ratation (radian)')
plt.legend()
plt.show()


# plotting shifts
plt.plot(moData[3],'r', label='x')
plt.plot(moData[4],'g', label='y')
plt.plot(moData[5],'b', label='z')
plt.title('Shift')
plt.xlabel('time points')
plt.ylabel('shift (mm)')
plt.legend()
plt.show()
