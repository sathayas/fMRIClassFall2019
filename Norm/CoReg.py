import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import nipype.interfaces.fsl as fsl # importing FSL interface functions
from nilearn.plotting import plot_anat, plot_epi, view_img
from nipype import Node, Workflow  # components to construct workflow
from nipype.interfaces.io import DataSink  # datasink
from bids.layout import BIDSLayout  # BIDSLayout object to specify file(s)


# Directory where your data set resides.
dataDir = '/tmp/Data/ds102'

# Creating the layout object for this BIDS data set
layout = BIDSLayout(dataDir)

# an fMRI image from one of the subjects (run 1 only)
imagefMRI = layout.get(subject='26',
                       run='1',
                       suffix='bold',
                       extension='nii.gz',
                       return_type='file')[0]

# T1 image from the layout object
imageT1 = layout.get(subject='26',
                       suffix='T1w',
                       extension='nii.gz',
                       return_type='file')[0]

# Output directory
outDir = os.path.join(dataDir, 'WorkflowOutput')



# node to skip dummy scans
extract = Node(fsl.ExtractROI(in_file=imagefMRI,  # input image
                              t_min=4,            # first 4 volumes are deleted
                              t_size=-1),
               name="extract")

# creating motion correction node
mcflirt = Node(fsl.MCFLIRT(save_rms=True,
                           save_plots=True,
                           mean_vol=True),   # saving displacement parameters
               name="mcflirt")

# creating co-registration node (estimating the coregistration parameters)
coreg = Node(fsl.FLIRT(reference=imageT1,  # target: T1-weighted
                       dof=6,       # specifying rigid-body (6-parameters)
                       cost='normmi'), # normizied mutual info
             name="coreg")

# applying the coregistration parameters to the entire time series
applywarp = Node(fsl.FLIRT(reference=imageT1,
                           apply_isoxfm=4),  # forcing the voxel size = 4mm
                 name="applywarp")
