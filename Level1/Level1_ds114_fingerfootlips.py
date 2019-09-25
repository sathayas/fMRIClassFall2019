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
from bids.grabbids import BIDSLayout  # BIDSLayout object to specify file(s)


# data directory
dataDir = '/Users/sh45474/Documents/Teaching/fMRI_Fall_2018/Data/ds114'

# base directory - where preprocessed fMRI data is located
baseDir = os.path.join(dataDir, 'WorkflowOutput/FSL_Preproc_fMRI')

# Creating the layout object for this BIDS data set
layout = BIDSLayout(dataDir)

# pre-processed fMRI data
imagefMRI = os.path.join(baseDir,
                         'sub-09_ses-test_task-fingerfootlips_bold_roi_mcf_warp_smooth_masked.nii.gz')

# task information file
eventFile = layout.get(type='events',
                       task='fingerfootlips',
                       extensions='tsv',
                       return_type='file')[0]


# Output directory
outDir = os.path.join(dataDir,'WorkflowOutput')

# getting TR from the image header
fMRI = nib.load(imagefMRI)   # image object
hdr_fMRI = fMRI.header
TR = hdr_fMRI['pixdim'][4]


## Getting experiment info from the event file, into a Bunch object
trialInfo = pd.read_table(eventFile)
conditions = sorted(list(set(trialInfo.trial_type)))
onsets = []
durations = []

for itrial in conditions:
    onsets.append(list(trialInfo[trialInfo.trial_type==itrial].onset-10)) # subtracting 10s due to removing of 4 dummy scans
    durations.append(list(trialInfo[trialInfo.trial_type==itrial].duration))

subject_info = [Bunch(conditions=conditions,
                      onsets=onsets,
                      durations=durations,
                      )]


## Defining contrasts
cont01 = ['average',        'T', conditions, [1/3., 1/3., 1/3.]]
cont02 = ['Finger',         'T', conditions, [1, 0, 0]]
cont03 = ['Foot',           'T', conditions, [0, 1, 0]]
cont04 = ['Lips',           'T', conditions, [0, 0, 1]]
cont05 = ['Finger > others','T', conditions, [1, -0.5, -0.5]]
cont06 = ['Foot > others',  'T', conditions, [-0.5, 1, -0.5]]
cont07 = ['Lips > others',  'T', conditions, [-0.5, -0.5, 1]]

cont08 = ['activation',     'F', [cont02, cont03, cont04]]

contrast_list = [cont01, cont02, cont03, cont04, cont05, cont06, cont07, cont08]


# model specification
modelspec = Node(modelgen.SpecifyModel(functional_runs=imagefMRI,
                                       subject_info=subject_info,
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


# creating the workflow
firstLevel = Workflow(name="Level1_FSL", base_dir=outDir)

# connecting nodes
firstLevel.connect([(modelspec, level1design, [('session_info', 'session_info')])])
firstLevel.connect([(level1design, modelgen, [('fsf_files', 'fsf_file'),
                                              ('ev_files','ev_files')])])
firstLevel.connect([(level1design, feat, [('fsf_files', 'fsf_file')])])
firstLevel.connect([(feat, datasink, [('feat_dir', 'FSL_Level1.@feat')])])


# running the workflow
firstLevel.run()

