import os  # system functions
import pandas as pd
import nipype.interfaces.fsl as fsl  # fsl
from nipype import Node, Workflow  # components to construct workflow
from nipype import SelectFiles  # to facilitate file i/o
from nipype.interfaces.io import DataSink  # datasink


##### PARAMETERS #####
indCope = '7'  # the contrast of interest, finger vs others


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

# a list of sessions
ses_list = ['test', 'retest']

# ininitializing lists to record file paths, subject ID, sessions
listCopeFiles = []
listVarcopeFiles = []
listMaskFiles = []
varSubj = []   # recording subject IDs
varSes = []    # recording sessions
for iSubj in subject_list:
    for iSes in ses_list:
        # recording subject ID and session
        varSubj.append(iSubj)
        varSes.append(iSes)

        # full path to a cope image
        pathCope = os.path.join(baseDir,
                                'sub-' + iSubj,
                                'ses-' + iSes,
                                'run0.feat',
                                'stats',
                                'cope' + indCope + '.nii.gz')
        listCopeFiles.append(pathCope)

        # full path to a varcope image
        pathVarcope = os.path.join(baseDir,
                                'sub-' + iSubj,
                                'ses-' + iSes,
                                'run0.feat',
                                'stats',
                                'varcope' + indCope + '.nii.gz')
        listVarcopeFiles.append(pathVarcope)

        # full path to a mask image
        pathMask = os.path.join(baseDir,
                                'sub-' + iSubj,
                                'ses-' + iSes,
                                'run0.feat',
                                'mask.nii.gz')
        listMaskFiles.append(pathMask)


###########
#
# SETTING UP THE SECOND LEVEL ANALYSIS NODES
#
###########
# creating a data frame for second-level analysis design matrix
expData = pd.DataFrame(list(zip(varSubj, varSes)),
                        columns=['Subject','Session'])

# creating dummy variables for sessions
for iSes in ses_list:
    expData[iSes] = (expData.Session==iSes).astype(int)

# creating dummy variables for subjects
for iSubj in subject_list:
    expData['sub'+iSubj] = (expData.Subject==iSubj).astype(int)

# converting the dummy variables into a dictionary of regressors
reg_list = list(expData.columns[2:]) # list of regressors
dictReg = expData[reg_list].to_dict('list')


# Contrasts
dummyZeros = [0] * len(subject_list)  # a list of n zeros (n=num of subj)
cont01 = ['test',       'T', reg_list, [1, 0]+dummyZeros]
cont02 = ['retest',     'T', reg_list, [0, 1]+dummyZeros]
cont03 = ['both',       'T', reg_list, [1, 1]+dummyZeros]
cont04 = ['test>retest','T', reg_list, [1,-1]+dummyZeros]
cont05 = ['retest>test','T', reg_list, [-1,1]+dummyZeros]

contrastList = [cont01, cont02, cont03, cont04, cont05]


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
                         os.path.join(outDir,'FingerFootLips_TestVsRetest_Cope7')),
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
