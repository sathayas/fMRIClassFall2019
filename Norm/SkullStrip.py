import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import nipype.interfaces.fsl as fsl # importing FSL interface functions

# Directory where your data set resides. This needs to be customized
dataDir = '/home/satoru/Teaching/fMRI_Fall_2018/Data/ds102'

# creating an object for BET process
mybet = fsl.BET()

# an T1 weighted image from one of the subjects
imageT1 = os.path.join(dataDir,'sub-26/anat/sub-26_T1w.nii.gz')

# output image file name
imageT1Out = os.path.join(dataDir,'sub-26/anat/sub-26_T1w_brain.nii.gz')

# specifying the input and output file names in the BET object
mybet.inputs.in_file = imageT1
mybet.inputs.out_file = imageT1Out

# running BET
mybet.run()




# Importing custom functions for displaying sections
import sys
sys.path.append('functions')
from DisplaySection import show_section, load_nii_data

# loading the data matrices
X = load_nii_data(imageT1)
Xbet = load_nii_data(imageT1Out)

# showing the before and after images
plt.subplot(121)
show_section(X, 'xy', 140)
plt.title('Original')
plt.subplot(122)
show_section(Xbet, 'xy', 140)
plt.title('After BET')
plt.show()



# playing with thresholds, then the output file
# first, threshold = 0.2
imageT1Out02 = os.path.join(dataDir,'sub-26/anat/sub-26_T1w_brain_f02.nii.gz')
mybet.inputs.frac = 0.2  # here, actually specifying the threshold
mybet.inputs.out_file = imageT1Out02
mybet.run()

# second, threshold = 0.8
imageT1Out08 = os.path.join(dataDir,'sub-26/anat/sub-26_T1w_brain_f08.nii.gz')
mybet.inputs.frac = 0.8  # here, actually specifying the threshold
mybet.inputs.out_file = imageT1Out08
mybet.run()


# showing the skull stripping with various parameters
plt.figure(figsize=[10,2.5])
# loading the data matrices
X = load_nii_data(imageT1)
Xbet02 = load_nii_data(imageT1Out02)
Xbet = load_nii_data(imageT1Out)
Xbet08 = load_nii_data(imageT1Out08)

# showing the before and after images
plt.subplot(141)
show_section(X, 'xy', 140)
plt.title('Original')
plt.subplot(142)
show_section(Xbet02, 'xy', 140)
plt.title('Threshold 0.2')
plt.subplot(143)
show_section(Xbet, 'xy', 140)
plt.title('Threshold 0.5 (default)')
plt.subplot(144)
show_section(Xbet08, 'xy', 140)
plt.title('Threshold 0.8')
plt.show()






