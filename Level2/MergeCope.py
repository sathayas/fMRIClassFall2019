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



###########
#
# A LIST OF COPE AND VARCOPE FILES TO BE MEREGED
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
# NODES FOR THE WORKFLOW
#
###########
# merging cope images
copemerge = Node(fsl.Merge(dimension='t',
                           in_files=listCopeFiles),
                 name="copemerge")

# merging varcope images
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
datasink = Node(DataSink(base_directory=outDir),
                name='datasink')


###########
#
# SETTING UP THE WORKFLOW NODES
#
###########

# creating the workflow
mergeCopes = Workflow(name="Level1", base_dir=outDir)

# connecting nodes
mergeCopes.connect(copemerge, 'merged_file', datasink, 'copeMerged')
mergeCopes.connect(varcopemerge, 'merged_file', datasink, 'varcopeMerged')
mergeCopes.connect(maskmerge, 'merged_file', datasink, 'maskMerged')
mergeCopes.connect(maskmerge, 'merged_file', minmask, 'in_file')
mergeCopes.connect(minmask, 'out_file', datasink, 'groupmask')


# running the workflow
mergeCopes.run()
