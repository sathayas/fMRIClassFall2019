import os
import numpy as np
import pandas as pd
import matoplotlib.pyplot as plt

# loading the data
resDir = '/tmp/Data/ds102/WorkflowOutput/Results/par_file'
resFname = 'sub-26_task-flanker_run-1_bold_roi_mcf.nii.gz.par'
moData = pd.read_csv(os.path.join(resDir,resFname),
                     header=None,
                     delimiter=r"\s+")
