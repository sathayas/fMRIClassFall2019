import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import nipype.interfaces.fsl as fsl  # fsl
from nipype import Node, Workflow  # components to construct workflow
from nilearn.plotting import plot_stat_map, view_img
from nilearn.image import math_img, coord_transform


# PARAMETERS
zThresh = 2.3  # a.k.a., p=0.01 uncorrected threshold

# FILE AND DIRECTORY BUSINESS
# original data directory
dataDir = '/tmp/Data/ds114'
# Output directory
outDir = os.path.join(dataDir,'WorkflowOutput')
# Datasink directory
datasinkDir = os.path.join(outDir,'FingerFootLips_Test_Cope5')
# stats_dir directory
statsDir = os.path.join(datasinkDir,'stats_dir/stats')
# Z-stat image
imgZStat = os.path.join(statsDir, 'zstat1.nii.gz')


# FINDING CLUSTERS IN THE ANALYSIS RESULTS
# cluster node
cluster = Node(fsl.Cluster(in_file=imgZStat,
                           threshold=zThresh),
               name='cluster')

# data sink node
datasink = Node(DataSink(base_directory=statsDir),
                name='datasink')

# workflow connecting clustering to the datasink
clusterWF = Workflow(name="clusterWF", base_dir=outDir)
clusterWF.connect(cluster, 'index_file', datasink, 'index_file')
clusterWF.connect(cluster, 'threshold_file', datasink, 'threshold_file')
clusterWF.connect(cluster, 'localmax_txt_file', datasink, 'localmax_txt_file')
clusterWF.connect(cluster, 'localmax_vol_file', datasink, 'localmax_vol_file')
clusterWF.connect(cluster, 'size_file', datasink, 'size_file')
clusterWF.connect(cluster, 'max_file', datasink, 'max_file')
clusterWF.connect(cluster, 'mean_file', datasink, 'mean_file')
clusterWF.connect(cluster, 'pval_file', datasink, 'pval_file')
clusterWF.run()
