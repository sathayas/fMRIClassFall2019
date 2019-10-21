import os  # system functions
import pandas as pd
import nipype.interfaces.fsl as fsl  # fsl
from nipype import Node, Workflow  # components to construct workflow
from nipype import SelectFiles  # to facilitate file i/o
from nipype.interfaces.io import DataSink  # datasink


##### PARAMETERS #####
indCope = '6'  # the contrast of interest, finger vs others
indSes = 'test'  # the session of interest


##### DIRECTORY BUSINESS ######
# original data directory
dataDir = '/tmp/Data/ds114'
# Output directory
outDir = os.path.join(dataDir,'WorkflowOutput')



###########
#
# A LIST OF COPE, VARCOPE, AND MASK FILES TO BE MEREGED
#
###########
# directory where preprocessed fMRI data is located
baseDir = os.path.join(dataDir, 'BatchOutput_FingerFootLips/feat_dir')

# a list of subjects
subject_list = ['%02d' % i for i in range(1,11)]

listCopeFiles = []
listVarcopeFiles = []
listMaskFiles = []
for iSubj in subject_list:
    # full path to a cope image
    pathCope = os.path.join(baseDir,
                            'sub-' + iSubj,
                            'ses-' + indSes,
                            'run0.feat',
                            'stats',
                            'cope' + indCope + '.nii.gz')
    listCopeFiles.append(pathCope)

    # full path to a varcope image
    pathVarcope = os.path.join(baseDir,
                            'sub-' + iSubj,
                            'ses-' + indSes,
                            'run0.feat',
                            'stats',
                            'varcope' + indCope + '.nii.gz')
    listVarcopeFiles.append(pathVarcope)

    # full path to a mask image
    pathMask = os.path.join(baseDir,
                            'sub-' + iSubj,
                            'ses-' + indSes,
                            'run0.feat',
                            'mask.nii.gz')
    listMaskFiles.append(pathMask)


###########
#
# SETTING UP THE SECOND LEVEL ANALYSIS NODES
#
###########
# reading the subject info
fileTable = os.path.join(dataDir,'participants.tsv')
ptData = pd.read_csv(fileTable, sep='\t')
leftHanded = list((ptData.dominant_hand=='left').astype(int))
rightHanded = list((ptData.dominant_hand=='right').astype(int))

# Dictionary with regressors

dictReg = {'reg1': leftHanded, # dummy variables for left handed people
           'reg2': rightHanded # dummy variables for right handed people
          }

# Contrasts
cont01 = ['left>right', 'T', ['reg1', 'reg2'], [1, -1]]
cont02 = ['right>left', 'T', ['reg1', 'reg2'], [-1, 1]]
cont03 = ['activation', 'T', ['reg1', 'reg2'], [0.5, 0.5]]

contrastList = [cont01, cont02]

# Setting up the second level analysis model node
level2design = Node(fsl.MultipleRegressDesign(contrasts=contrastList,
                                              regressors=dictReg),
                    name='level2design')

# Model calculation by FLAMEO
flameo = Node(fsl.FLAMEO(run_mode='fe'),
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

# merging mask files
maskmerge = Node(fsl.Merge(dimension='t',
                           in_files=listMaskFiles),
                 name="maskmerge")

# calculating the minimum across time points on merged mask image
minmask = Node(fsl.MinImage(),
               name="minmask")


# creating datasink to collect outputs
datasink = Node(DataSink(base_directory=
                         os.path.join(outDir,'FingerFootLips_Test_Cope6_Handedness')),
                name='datasink')


###########
#
# SETTING UP THE WORKFLOW NODES
#
###########

# creating the workflow
secondLevel = Workflow(name="Level2", base_dir=outDir)

# connecting nodes
secondLevel.connect(level2design, 'design_mat', flameo, 'design_file')
secondLevel.connect(level2design, 'design_con', flameo, 't_con_file')
secondLevel.connect(level2design, 'design_grp', flameo, 'cov_split_file')
secondLevel.connect(copemerge, 'merged_file', flameo, 'cope_file')
secondLevel.connect(varcopemerge, 'merged_file', flameo, 'var_cope_file')
secondLevel.connect(maskmerge, 'merged_file', minmask, 'in_file')
secondLevel.connect(minmask, 'out_file', flameo, 'mask_file')
secondLevel.connect(flameo, 'stats_dir', datasink, 'stats_dir')


# running the workflow
secondLevel.run()
