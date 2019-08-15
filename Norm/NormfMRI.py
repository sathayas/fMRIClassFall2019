import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import nipype.interfaces.fsl as fsl # importing FSL interface functions
from nipype import Node, Workflow  # components to construct workflow
from nipype.interfaces.io import DataSink  # datasink
from bids.layout import BIDSLayout  # BIDSLayout object to specify file(s)
from nilearn import image
from nilearn.plotting import plot_anat, view_img


# Directory where your data set resides.
dataDir = '/tmp/Data/ds114'


# Creating the layout object for this BIDS data set
layout = BIDSLayout(dataDir)

# an fMRI image from one of the subjects (finger foot lips, test)
imagefMRI = layout.get(subject='09',
                       session='test',
                       suffix='bold',
                       task='fingerfootlips',
                       extension='nii.gz',
                       return_type='file')[0]

# an T1 image for the same subject (test)
imageT1 = layout.get(subject='09',
                     session='test',
                     suffix='T1w',
                     extension='nii.gz',
                     return_type='file')[0]

# template image (from FSL)
fMNI = '/usr/share/fsl/data/standard/MNI152_T1_2mm_brain.nii.gz'

# brain mask in MNI space (from FSL)
fmask = '/usr/share/fsl/data/standard/MNI152_T1_2mm_brain_mask_dil.nii.gz'



# Output directory
outDir = os.path.join(dataDir, 'WorkflowOutput')


#
#    T1 Normalization workflow
#
# Skullstrip process node
fslBET = Node(fsl.BET(in_file=imageT1),
              name="fslBET")


# Linear normalization node
fslFLIRT = Node(fsl.FLIRT(reference=fMNI,
                          cost_func='normmi'),
                name="fslFLIRT")

# Non-linear normalization node
fslFNIRT = Node(fsl.FNIRT(ref_file=fMNI,
                          fieldcoeff_file=True),
                name='fslFNIRT')

# Creating a workflow object
normT1wf = Workflow(name="normT1wf", base_dir=outDir)

# connecting nodes as a T1 normalization workflow
normT1wf.connect(fslBET, "out_file", fslFLIRT, "in_file")
normT1wf.connect(fslBET, 'out_file', fslFNIRT, 'in_file')
normT1wf.connect(fslFLIRT, 'out_matrix_file', fslFNIRT, 'affine_file')



#
#   fMRI pre-processing
#
# skip dummy scans
extract = Node(fsl.ExtractROI(in_file=imagefMRI,  # input image
                              t_min=4,            # first 4 volumes are deleted
                              t_size=-1),
               name="extract")

# creating motion correction node
mcflirt = Node(fsl.MCFLIRT(save_rms=True,   # saving displacement parameters
                           save_plots=True, #
                           mean_vol=True),  # saving mean image
               name="mcflirt")

# creating co-registration node (estimating the coregistration parameters)
coreg = Node(fsl.FLIRT(dof=6,       # specifying rigid-body (6-parameters)
                       cost='normmi'), # normizied mutual info
             name="coreg")

# applying the coregistration and normalization parameters to fMRI data
applywarp = Node(fsl.ApplyWarp(ref_file=fMNI),
                 name="applywarp")

# smoothing with SUSAN
susan = Node(fsl.SUSAN(brightness_threshold = 2000.0,  # brightness threshold
                       fwhm=6.0),    # smoothing filter width (6mm, isotropic)
             name='susan')



# creating datasink to collect outputs
datasink = Node(DataSink(base_directory=outDir),
                name='datasink')


# creating a workflow
preprocfMRI = Workflow(name="PreprocfMRI", base_dir=outDir)

# connecting the nodes to the main workflow
preprocfMRI.connect(extract, 'roi_file', mcflirt, 'in_file')
preprocfMRI.connect(mcflirt, 'mean_img', coreg, 'in_file')
preprocfMRI.connect(normT1wf, 'fslBET.out_file', coreg, 'reference')
preprocfMRI.connect(mcflirt, 'out_file', applywarp, 'in_file')
preprocfMRI.connect(coreg, 'out_matrix_file', applywarp, 'premat')
preprocfMRI.connect(normT1wf, 'fslFNIRT.fieldcoeff_file', applywarp, 'field_file')
preprocfMRI.connect(applywarp, 'out_file', susan, 'in_file')
preprocfMRI.connect(susan, 'smoothed_file', applymask, 'in_file')

# connection to data sink
preprocfMRI.connect(mcflirt,'par_file', datasink, 'par_file')
preprocfMRI.connect(mcflirt,'rms_files', datasink, 'rms_file')
preprocfMRI.connect(normT1wf, 'fslFNIRT.warped_file', datasink, 'NormT1')
preprocfMRI.connect(applywarp, 'out_file', datasink, 'NormfMRI')
preprocfMRI.connect(applymask, 'out_file', datasink, 'MaskSmoNormfMRI')




# writing out graphs
preprocfMRI.write_graph(graph2use='orig', dotfilename='graph_orig.dot')

# showing the graph
plt.figure(figsize=[6,6])
img=mpimg.imread(os.path.join(outDir,"preprocfMRI","graph_orig.png"))
imgplot = plt.imshow(img)
plt.axis('off')
plt.show()

# running the workflow
preprocfMRI.run()





# examining the normalization results
# Normalized fMRI
imageNormfMRI = os.path.join(os.path.join(outDir,'NormfMRI'),
                             'sub-09_ses-test_task-fingerfootlips_bold_roi_mcf_warp.nii.gz')
# Normalized T1
imageNormT1 = os.path.join(os.path.join(outDir,'NormT1'),
                           'sub-09_ses-test_T1w_brain_warped.nii.gz')
# mean of the normalized fMRI
mean_imageNormfMRI = image.mean_img(imageNormfMRI)

#
# VISUALIZING NORMLAIZED FMRI VS NORMALIZED T1
#
# displaying the mean of the normalized fMRI (axial)
display = plot_anat(mean_imageNormfMRI,
                    display_mode='z',
                    cut_coords=6)

# adding edges from the corresponding T1w image
display.add_edges(imageNormT1)

# displaying the mean of the normalized fMRI (sagittal)
display = plot_anat(mean_imageNormfMRI,
                    display_mode='x',
                    cut_coords=6)

# adding edges from the corresponding T1w image
display.add_edges(imageNormT1)

# displaying the mean of the normalized fMRI (coronal)
display = plot_anat(mean_imageNormfMRI,
                    display_mode='y',
                    cut_coords=6)

# adding edges from the corresponding T1w image
display.add_edges(imageNormT1)
