import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import nipype.interfaces.fsl as fsl # importing FSL interface functions
from nilearn import image
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


# creating datasink to collect outputs
datasink = Node(DataSink(base_directory=outDir),
                name='datasink')



# creating a workflow
coReg = Workflow(name="coReg", base_dir=outDir)

# and connecting nodes
coReg.connect(extract,'roi_file', mcflirt, 'in_file')
# mcflirt mean image as input for the first FLIRT
coReg.connect(mcflirt, 'mean_img', coreg, 'in_file')
# mcflirt fMRI as input for the second FLIRT
coReg.connect(mcflirt, 'out_file', applywarp, 'in_file')
# and passing on the rigid-body transformation parameters from first FLIRT
coReg.connect(coreg, 'out_matrix_file', applywarp,'in_matrix_file')

# second FLIRT node to data sink
coReg.connect(applywarp, 'out_file', datasink, 'CoRegfMRI')
# second motion corredted mean fMRI to data sink
coReg.connect(mcflirt, 'mean_img', datasink, 'MoCorMean')



# writing out graph
coReg.write_graph(graph2use='orig', dotfilename='graph_orig.dot')

# showing the graph
plt.figure(figsize=[6,6])
img=mpimg.imread(os.path.join(outDir,"coReg","graph_orig.png"))
imgplot = plt.imshow(img)
plt.axis('off')
plt.show()



# running the workflowhaxby_anat_filename
coReg.run()



# examining the coregistration results
# Coregistered fMRI
imageCoRegfMRI = os.path.join(os.path.join(outDir,'CoRegfMRI'),
                              'sub-26_task-flanker_run-1_bold_roi_mcf_flirt.nii.gz')
# mean of the co-registered fMRI
mean_imageCoRegfMRI = image.mean_img(imageCoRegfMRI)


# displaying the mean of the co-registered fMRI (axial)
display = plot_anat(mean_imageCoRegfMRI,
                    display_mode='z',
                    cut_coords=6)

# adding edges from the corresponding T1w image
display.add_edges(imageT1)


# displaying the mean of the co-registered fMRI (sagittal)
display = plot_anat(mean_imageCoRegfMRI,
                    display_mode='x',
                    cut_coords=6)

# adding edges from the corresponding T1w image
display.add_edges(imageT1)


# displaying the mean of the co-registered fMRI (coronal)
display = plot_anat(mean_imageCoRegfMRI,
                    display_mode='y',
                    cut_coords=6)

# adding edges from the corresponding T1w image
display.add_edges(imageT1)




# Just for fun; original fMRI and T1 -- how different they are
# mean fMRI from motion corrected
imageCoRegfMRI = os.path.join(os.path.join(outDir,'moCor'),
                              'sub-26_task-flanker_run-1_bold_roi_mcf_flirt.nii.gz')
