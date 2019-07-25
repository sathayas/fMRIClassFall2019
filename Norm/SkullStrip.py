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

# T1 image from the layout object
imageT1 = layout.get(subject='26',
                       suffix='T1w',
                       extension='nii.gz',
                       return_type='file')[0]

# template image (from FSL)
fMNI = '/usr/local/fsl/data/standard/MNI152_T1_2mm_brain.nii.gz'

# Output directory
outDir = os.path.join(dataDir, 'WorkflowOutput')



# Skullstrip process node
fslBET = Node(fsl.BET(in_file=imageT1),
              name="fslBET")

# DataSink to collect intermediate outputs
datasink = Node(DataSink(base_directory=outDir),
                name='datasink')


# Creating a workflow object
wf = Workflow(name="fslNorm", base_dir=outDir)

# connecting nodes as a workflow
wf.connect(fslBET, "out_file", fslFLIRT, "in_file")


# running the workflow
wf.run()





# Skull-stripped image
imageT1BET = os.path.join(os.path.join(outDir,'WorkflowOutput'),
                          'sub-26_T1w_brain.nii.gz')

# displaying image (skull-sripped)
plot_anat(imageT1BET,
          display_mode='ortho',
          dim=-1,
          draw_cross=True,
          annotate=True)

# interactive visualization (skull-sripped)
view_img(imageT1BET, bg_img=False, cmap='gray', symmetric_cmap=False,
         black_bg=True)



# displaying image (original T1)
plot_anat(imageT1,
          display_mode='ortho',
          dim=-1,
          draw_cross=True,
          annotate=True)
