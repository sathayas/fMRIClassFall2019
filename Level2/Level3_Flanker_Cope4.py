import os  # system functions
import pandas as pd
import nipype.interfaces.fsl as fsl  # fsl
from nipype import Node, Workflow  # components to construct workflow
from nipype import SelectFiles  # to facilitate file i/o
from nipype.interfaces.io import DataSink  # datasink


##### DIRECTORY BUSINESS ######
# original data directory
dataDir = '/tmp/Data/ds102'
# Output directory
outDir = os.path.join(dataDir,'WorkflowOutput')



###########
#
# A LIST OF COPE FILES TO BE MEREGED
#
###########
# directory where 2nd level analysis cope images are located
baseDir = os.path.join(outDir, 'Flanker_Cope4_Level2/stats_dir/stats')

# a list of subjects
subject_list = ['%d' % i for i in range(1,27)]  # not zero padded anymore

listCopeFiles = []
listVarcopeFiles = []
for iSubj in subject_list:
    # full path to a cope image
    pathCope = os.path.join(baseDir,
                            'cope' + iSubj + '.nii.gz')
    listCopeFiles.append(pathCope)

    # full path to a varcope image
    pathVarcope = os.path.join(baseDir,
                            'varcope' + iSubj + '.nii.gz')
    listVarcopeFiles.append(pathVarcope)

fileMask = os.path.join(baseDir,'mask.nii.gz')  # single mask image


###########
#
# SETTING UP THE THIRD LEVEL ANALYSIS NODES
#
###########
# Dictionary with regressors
dictReg = {'reg1': [1]*len(subject_list) # vector of ones
          }

# Contrasts
cont01 = ['incong>cong', 'T', list(dictReg.keys()), [1]]
cont02 = ['cong>incong', 'T', list(dictReg.keys()), [-1]]

contrastList = [cont01, cont02]


# Setting up the second level analysis model node
level2design = Node(fsl.MultipleRegressDesign(contrasts=contrastList,
                                              regressors=dictReg),
                    name='level2design')

# Model calculation by FLAMEO
flameo = Node(fsl.FLAMEO(mask_file=fileMask,  # specifying mask image in flameo
                         run_mode='fe'),
              name="flameo")



###########
#
# NODES FOR THE MERGING IMAGES
#
###########
# merging cope files
copemerge = Node(fsl.Merge(dimension='t',
                           in_files=listCopeFiles),
                 name="copemerge")

# merging varcope files
varcopemerge = Node(fsl.Merge(dimension='t',
                              in_files=listVarcopeFiles),
                    name="varcopemerge")

# creating datasink to collect outputs
datasink = Node(DataSink(base_directory=
                         os.path.join(outDir,'Flanker_Cope4_Level3')),
                name='datasink')


###########
#
# SETTING UP THE WORKFLOW NODES
#
###########

# creating the workflow
thirdLevel = Workflow(name="thirdLevel", base_dir=outDir)

# connecting nodes
thirdLevel.connect(level2design, 'design_mat', flameo, 'design_file')
thirdLevel.connect(level2design, 'design_con', flameo, 't_con_file')
thirdLevel.connect(level2design, 'design_grp', flameo, 'cov_split_file')
thirdLevel.connect(copemerge, 'merged_file', flameo, 'cope_file')
thirdLevel.connect(varcopemerge, 'merged_file', flameo, 'var_cope_file')
thirdLevel.connect(flameo, 'stats_dir', datasink, 'stats_dir')


# running the workflow
thirdLevel.run()
