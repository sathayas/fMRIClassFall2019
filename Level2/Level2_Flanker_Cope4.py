import os  # system functions
import pandas as pd
import nipype.interfaces.fsl as fsl  # fsl
from nipype import Node, Workflow  # components to construct workflow
from nipype import SelectFiles  # to facilitate file i/o
from nipype.interfaces.io import DataSink  # datasink


##### PARAMETERS #####
indCope = '4'  # the contrast of interest, finger vs others


##### DIRECTORY BUSINESS ######
# original data directory
dataDir = '/tmp/Data/ds102'
# Output directory
outDir = os.path.join(dataDir,'WorkflowOutput')



###########
#
# A LIST OF COPE, VARCOPE, AND MASK FILES TO BE MEREGED
#
###########
# directory where preprocessed fMRI data is located
baseDir = os.path.join(dataDir, 'BatchOutput_FeatDir/feat_dir')

# a list of subjects
subject_list = ['%02d' % i for i in range(1,27)]

# a list of runs
run_list = ['1', '2']

listCopeFiles = []
listVarcopeFiles = []
listMaskFiles = []
varSubj = []   # recording subject IDs
varRun = []    # recording sessions
for iSubj in subject_list:
    for iRun in run_list:
        # recording subject ID and session
        varSubj.append(iSubj)
        varRun.append(iRun)

        # full path to a cope image
        pathCope = os.path.join(baseDir,
                                'run-' + iRun,
                                'sub-' + iSubj,
                                'run0.feat',
                                'stats',
                                'cope' + indCope + '.nii.gz')
        listCopeFiles.append(pathCope)

        # full path to a varcope image
        pathVarcope = os.path.join(baseDir,
                                'run-' + iRun,
                                'sub-' + iSubj,
                                'run0.feat',
                                'stats',
                                'varcope' + indCope + '.nii.gz')
        listVarcopeFiles.append(pathVarcope)

        # full path to a mask image
        pathMask = os.path.join(baseDir,
                                'run-' + iRun,
                                'sub-' + iSubj,
                                'run0.feat',
                                'mask.nii.gz')
        listMaskFiles.append(pathMask)



###########
#
# SETTING UP THE FIRST LEVEL ANALYSIS NODES
#
###########
# creating a data frame for second-level analysis design matrix
expData = pd.DataFrame(list(zip(varSubj, varRun)),
                        columns=['Subject','Run'])

# creating dummy variables for subjects
for iSubj in subject_list:
    expData['sub'+iSubj] = (expData.Subject==iSubj).astype(int)

# converting the dummy variables into a dictionary of regressors
reg_list = list(expData.columns[2:]) # list of regressors
dictReg = expData[reg_list].to_dict('list')


# Contrasts
# creating an empty list of contrasts
contrastList = []
# each contrast is the sum for a particular subject -- added to the contrastlist
for i,iSubj in enumerate(subject_list):
    dummySubj = [0] * len(subject_list)  # list of zeros
    dummySubj[i] = 1   # indicator for this subject
    tmpCont = [reg_list[i], 'T', reg_list, dummySubj]  # contrast for this subject
    contrastList.append(tmpCont)



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
                         os.path.join(outDir,'Flanker_Cope4_Level2')),
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
