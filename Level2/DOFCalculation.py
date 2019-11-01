import os  # system functions
import nipype.interfaces.fsl as fsl  # fsl
from nipype import Node, Workflow  # components to construct workflow
from nipype import SelectFiles  # to facilitate file i/o
from nipype.interfaces.io import DataSink  # datasink


##### PARAMETERS #####
indCope = '5'  # the contrast of interest, finger vs others
indSes = 'test'  # the session of interest


##### DIRECTORY BUSINESS ######
# original data directory
dataDir = '/tmp/Data/ds114'
# Output directory
outDir = os.path.join(dataDir,'WorkflowOutput')
# directory where preprocessed fMRI data is located
baseDir = os.path.join(dataDir, 'BatchOutput_FingerFootLips/feat_dir')


###########
#
# SETTING UP THE SECOND LEVEL ANALYSIS NODES
#
###########
# a list of subjects
subject_list = ['%02d' % i for i in range(1,11)]

# Dictionary with regressors
dictReg = {'reg1': [1]*len(subject_list) # vector of ones
          }

# Contrasts
cont01 = ['activation', 'T', list(dictReg.keys()), [1]]
cont02 = ['activation', 'T', list(dictReg.keys()), [-1]]

contrastList = [cont01, cont02]

# Setting up the second level analysis model node
level2design = Node(fsl.MultipleRegressDesign(contrasts=contrastList,
                                              regressors=dictReg),
                    name='level2design')

# Model calculation by FLAMEO
flameo = Node(fsl.FLAMEO(run_mode='fe'),
              name="flameo")
