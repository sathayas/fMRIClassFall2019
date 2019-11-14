import os  # system functions
import pandas as pd
import nipype.interfaces.fsl as fsl  # fsl
from nipype import Node, Workflow  # components to construct workflow
from nipype import SelectFiles  # to facilitate file i/o
from nipype.interfaces.io import DataSink  # datasink


##### PARAMETERS #####
indCope = '1'  # the contrast of interest, activation for both OVG and OWR


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
# directories where preprocessed fMRI data is located
baseOVGDir = os.path.join(dataDir, 'BatchOutput_OvertVerbGeneration/feat_dir')
baseOWRDir = os.path.join(dataDir, 'BatchOutput_OvertWordRepetition/feat_dir')
baseDir = [baseOVGDir, baseOWRDir]

# a list of subjects
subject_list = ['%02d' % i for i in range(1,11)]

# a list of task
task_list = ['overtverbgeneration', 'overtwordrepetition']

# session of interest
indSes = 'test'


# ininitializing lists to record file paths, subject ID, sessions
listCopeFiles = []
listVarcopeFiles = []
listMaskFiles = []
varSubj = []   # recording subject IDs
varTask = []    # recording tasks
for iSubj in subject_list:
    for i,iTask in enumerate(task_list):
        # recording subject ID and session
        varSubj.append(iSubj)
        varTask.append(iTask)

        # full path to a cope image
        pathCope = os.path.join(baseDir[i],
                                'sub-' + iSubj,
                                'ses-' + indSes,
                                'run0.feat',
                                'stats',
                                'cope' + indCope + '.nii.gz')
        listCopeFiles.append(pathCope)

        # full path to a varcope image
        pathVarcope = os.path.join(baseDir[i],
                                'sub-' + iSubj,
                                'ses-' + indSes,
                                'run0.feat',
                                'stats',
                                'varcope' + indCope + '.nii.gz')
        listVarcopeFiles.append(pathVarcope)

        # full path to a mask image
        pathMask = os.path.join(baseDir[i],
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
# creating a data frame for second-level analysis design matrix
expData = pd.DataFrame(list(zip(varSubj, varTask)),
                        columns=['Subject','Task'])

# creating a dummy variable for sessions (test:1, retest:-1)
expData['OVGvsOWR'] = (expData.Task=='overtverbgeneration').astype(int)
expData['OVGvsOWR'] -= (expData.Task=='overtwordrepetition').astype(int)

# creating dummy variables for subjects
for iSubj in subject_list:
    expData['sub'+iSubj] = (expData.Subject==iSubj).astype(int)

# converting the dummy variables into a dictionary of regressors
reg_list = list(expData.columns[2:]) # list of regressors
dictReg = expData[reg_list].to_dict('list')


# Contrasts
dummyZeros = [0] * len(subject_list)  # a list of n zeros (n=num of subj)
cont01 = ['OVG>OWR','T', reg_list, [1]+dummyZeros]
cont02 = ['OWR>OVG','T', reg_list, [-1]+dummyZeros]

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
                         os.path.join(outDir,'OVGvsOWR_Test')),
                name='datasink')


###########
#
# SETTING UP THE WORKFLOW NODES
#
###########

# creating the workflow
secondLevel = Workflow(name="secondLevel", base_dir=outDir)

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
