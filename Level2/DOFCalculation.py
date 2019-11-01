import os  # system functions
import nipype.interfaces.fsl as fsl  # fsl
from nipype import Node, Workflow  # components to construct workflow
from nipype import SelectFiles  # to facilitate file i/o
from nipype.interfaces.io import DataSink  # datasink
from nipype.interfaces.utility import Function  # for custom made function

# a function to calculate error DOF
def DOFCalc(targetDir, desMtx):
    import os
    import numpy as np
    # calculating the design matrix rank
    dofModel = np.linalg.matrix_rank(np.array(list(desMtx.values())))
    # calculating the error dof
    dofFull = np.max(np.array(list(desMtx.values())).shape)
    dofError = dofFull - dofModel
    # writing out dof to a file
    fileOut = os.path.join(targetDir,'dof')
    f = open(fileOut,'w')
    f.write(str(dofError))
    f.close()
    return fileOut


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

dofCalc = Node(interface=Function(input_names=['targetDir', 'desMtx'],
                                              output_names=['fileOut'],
                                              function=DOFCalc),
               name='dofCalc')

# creating datasink to collect outputs
datasink = Node(DataSink(base_directory=
                         os.path.join(outDir,'DOFCalculation')),
                name='datasink')

# directory where we create a DOF file
DOFCalc.inputs.targetDir = datasink.inputs.base_directory
# passing on the design matrix to the DOF calculation file
DOFCalc.inputs.desMtx = dictReg

# passing

# creating the workflow
dofCalc = Workflow(name="dofCalc", base_dir=outDir)

# connecting nodes
dofCalc.connect(DOFCalc, 'fileOut', datasink, 'fileOut')


# running the workflow
dofCalc.run()
