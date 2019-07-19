import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import nipype.interfaces.fsl as fsl # importing FSL interface functions
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

# Output directory
outDir = os.path.join(dataDir, 'WorkflowOutput')


# node to skip dummy scans
extract = Node(fsl.ExtractROI(in_file=imagefMRI,  # input image
                              t_min=4,            # first 4 volumes are deleted
                              t_size=-1),
               name="extract")

# creating motion correction node
mcflirt = Node(fsl.MCFLIRT(save_rms=True),   # saving displacement parameters
               name="mcflirt")

# creating datasink to collect outputs
datasink = Node(DataSink(base_directory=outDir),
                name='datasink')
