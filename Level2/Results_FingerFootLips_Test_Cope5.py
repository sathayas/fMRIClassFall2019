import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import nipype.interfaces.fsl as fsl  # fsl
from nilearn.plotting import plot_stat_map, view_img
from nilearn.image import math_img, coord_transform
