import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import nibabel as nib   # nibabel to read TR from image header
import nipype.interfaces.fsl as fsl # importing FSL interface functions
from nipype import Node, Workflow  # components to construct workflow
from nipype.interfaces.io import DataSink  # datasink
from nipype.algorithms import modelgen  # GLM model generator
from nipype.interfaces.base import Bunch
from bids.layout import BIDSLayout  # BIDSLayout object to specify file(s)

##### DIRECTORY BUSINESS ######
# original data directory
dataDir = '/tmp/Data/ds102'
# Output directory
outDir = os.path.join(dataDir,'WorkflowOutput')


###########
#
# SPECIFYING THE FMRI DATA AND OTHER IMAGE FILES
#
###########

# directory where preprocessed fMRI data is located
baseDir = os.path.join(dataDir, 'derivatives_selected/fmriprep')
subjDir = os.path.join(baseDir, 'sub-26/func')
runID = 'run-1'  # indentifying the run of interest

# location of the pre-processed fMRI & mask
# NB: Assuming that the preprocessing is done with fMRIprep
fList = os.listdir(subjDir)  # getting the directory contents
imagefMRI = [x for x in fList if
                (runID in x) and   # selecting the run of interest
                ('preproc_bold.nii.gz' in x)][0]   # identifying the bold data
imageMask = [x for x in fList if
                (runID in x) and   # selecting the run of interest
                ('brain_mask.nii.gz' in x)][0]   # identifying the bold data

filefMRI = os.path.join(subjDir,imagefMRI)
fileMask = os.path.join(subjDir,imageMask)


###########
#
# FMRI PREPROCESSING NODES
#
###########

# smoothing with SUSAN
susan = Node(fsl.SUSAN(brightness_threshold = 2000.0,
                       fwhm=6.0),    # smoothing filter width (6mm, isotropic)
             name='susan')

# masking the fMRI with a brain mask
applymask = Node(fsl.ApplyMask(mask_file=fileMask),
                 name='applymask')


###########
#
# READ TASK INFO IN PREPRARATION FOR THE ANALYSIS
#
###########


# getting TR from the image header
fMRI = nib.load(filefMRI)   # image object
hdr_fMRI = fMRI.header
TR = hdr_fMRI['pixdim'][4]
onsetOffset = nDelfMRI * TR  # time adjustement due to deleted fMRI volumes

# Creating the layout object for this BIDS data set
layout = BIDSLayout(dataDir)

# task information file
fileEvent = layout.get(suffix='events',
                       subject='26',
                       run='1',
                       task='flanker',
                       extension='tsv',
                       return_type='file')[0]

## Getting experiment info from the event file, into a Bunch object
##############################
#
# Fill in the blank: Solution for your excercise
#
##############################


## Defining contrasts
##############################
#
# Fill in the blank: Solution for your excercise
#
##############################



###########
#
# SETTING UP THE FIRST LEVEL ANALYSIS NODES
#
###########

# model specification
modelspec = Node(modelgen.SpecifyModel(subject_info=subject_info,
                                       input_units='secs',
                                       time_repetition=TR,
                                       high_pass_filter_cutoff=100),
                 name="modelspec")

# first-level design
level1design = Node(fsl.Level1Design(bases={'dgamma':{'derivs': True}},
                                     interscan_interval=TR,
                                     model_serial_correlations=True,
                                     contrasts=contrast_list),
                    name="level1design")

# creating all the other files necessary to run the model
modelgen = Node(fsl.FEATModel(),
                name='modelgen')

# then running through FEAT
feat = Node(fsl.FEAT(),
            name="feat")

# creating datasink to collect outputs
datasink = Node(DataSink(base_directory=outDir),
                name='datasink')


###########
#
# SETTING UP THE WORKFLOW NODES
#
###########

##############################
#
# Fill in the blank: Solution for your excercise
#
##############################

# writing out graphs
firstLevel.write_graph(graph2use='orig', dotfilename='graph_orig.dot')

# showing the graph
plt.figure(figsize=[6,6])
img=mpimg.imread(os.path.join(outDir,"Level1_FingerFootLips","graph_orig.png"))
imgplot = plt.imshow(img)
plt.axis('off')
plt.show()

# running the workflow
firstLevel.run()
