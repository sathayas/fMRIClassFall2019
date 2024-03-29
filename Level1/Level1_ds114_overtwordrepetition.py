import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import nibabel as nib   # nibabel to read TR from image header
import nipype.interfaces.fsl as fsl # importing FSL interface functions
from nipype import Node, Workflow  # components to construct workflow
from nipype import SelectFiles  # to facilitate file i/o
from nipype.interfaces.io import DataSink  # datasink
from nipype.algorithms import modelgen  # GLM model generator
from nipype.interfaces.base import Bunch
from bids.layout import BIDSLayout  # BIDSLayout object to specify file(s)

##### DIRECTORY BUSINESS ######
# original data directory
dataDir = '/tmp/Data/ds114'
# Output directory
outDir = os.path.join(dataDir,'BatchOutput')


##### PARAMETERS TO BE USED #####
nDelfMRI = 4  # number of first scans to be deleted
TR = 5.0 # this should be read from an image file, but for simplicity hard coded

###########
#
# SETTING UP ITERABLES
#
###########
# directory where preprocessed fMRI data is located
baseDir = os.path.join(dataDir, 'derivatives_selected/fmriprep')

# list of values for the iterables
subject_list = ['%02d' % i for i in range(1,11)]
session_list = ['test', 'retest']
task_name = 'overtwordrepetition'

# String template with {}-based strings
templates = {'func': os.path.join(baseDir,
                                  'sub-{subject_id}',
                                  'ses-{subsession_id}',
                                  'func',
                                  ('sub-{subject_id}' +
                                   '_ses-{subsession_id}' +
                                   '_task-' + task_name +
                                   '_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz')),
             'mask': os.path.join(baseDir,
                                  'sub-{subject_id}',
                                  'ses-{subsession_id}',
                                  'func',
                                  ('sub-{subject_id}' +
                                   '_ses-{subsession_id}' +
                                   '_task-' + task_name +
                                   '_space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz'))
             }

# Create SelectFiles node
sf = Node(SelectFiles(templates, sort_filelist=True),
          name='sf')
sf.iterables = [('subject_id', subject_list),
                ('subsession_id', session_list)]



###########
#
# FMRI PREPROCESSING NODES
#
###########

# skip dummy scans
extract = Node(fsl.ExtractROI(t_min=nDelfMRI,    # first volumes to be deleted
                              t_size=-1),
               name="extract")

# smoothing with SUSAN
susan = Node(fsl.SUSAN(brightness_threshold = 2000.0,
                       fwhm=6.0),    # smoothing filter width (6mm, isotropic)
             name='susan')

# masking the fMRI with a brain mask
applymask = Node(fsl.ApplyMask(),
                 name='applymask')


###########
#
# READ TASK INFO IN PREPRARATION FOR THE ANALYSIS
#
###########

# Creating the layout object for this BIDS data set
layout = BIDSLayout(dataDir)

# task information file
fileEvent = layout.get(suffix='events',
                       task=task_name,
                       extension='tsv',
                       return_type='file')[0]

# Offset for onset times
onsetOffset = nDelfMRI * TR  # time adjustement due to deleted fMRI volumes

## Getting experiment info from the event file, into a Bunch object
trialInfo = pd.read_csv(fileEvent, sep='\t')
conditions = sorted(list(set(trialInfo.trial_type)))
onsets = []
durations = []

for itrial in conditions:
    onsets.append(list(trialInfo[trialInfo.trial_type==itrial].onset-onsetOffset))
    durations.append(list(trialInfo[trialInfo.trial_type==itrial].duration))

subject_info = [Bunch(conditions=conditions,
                      onsets=onsets,
                      durations=durations,
                      )]


## Defining contrasts
cont01 = ['activation',     'T', conditions, [1]]
cont02 = ['deactivation',   'T', conditions, [-1]]

contrast_list = [cont01, cont02]



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

## Use the following DataSink output substitutions
substitutions = [('_subject_id_', 'sub-'),
                 ('_subsession_id_', '/ses-')
                 ]

datasink.inputs.substitutions = substitutions

###########
#
# SETTING UP THE WORKFLOW NODES
#
###########

# creating the workflow
firstLevel = Workflow(name="Level1_OvertWordRepetition", base_dir=outDir)

# connecting nodes
firstLevel.connect(sf, 'func', extract, 'in_file')
firstLevel.connect(sf, 'mask', applymask, 'mask_file')
firstLevel.connect(extract, 'roi_file', susan, 'in_file')
firstLevel.connect(susan, 'smoothed_file', applymask, 'in_file')
firstLevel.connect(applymask, 'out_file', modelspec, 'functional_runs')
firstLevel.connect(modelspec, 'session_info', level1design, 'session_info')
firstLevel.connect(level1design, 'fsf_files', modelgen, 'fsf_file')
firstLevel.connect(level1design, 'ev_files', modelgen, 'ev_files')
firstLevel.connect(level1design, 'fsf_files', feat, 'fsf_file')
firstLevel.connect(feat, 'feat_dir', datasink, 'feat_dir')
firstLevel.connect(applymask, 'out_file', datasink, 'preproc_out_file')

# running the workflow
firstLevel.run('MultiProc', plugin_args={'n_procs': 10})
