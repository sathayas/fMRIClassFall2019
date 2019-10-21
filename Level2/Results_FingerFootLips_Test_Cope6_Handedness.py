import os
import numpy as np
import pandas as pd
import nibabel as nib
import matplotlib.pyplot as plt
import nipype.interfaces.fsl as fsl  # fsl
from nipype import Node, Workflow  # components to construct workflow
from nipype.interfaces.io import DataSink  # datasink
from nilearn.plotting import plot_stat_map, view_img
from nilearn.image import math_img, coord_transform


# PARAMETERS
zThresh = 2.3  # a.k.a., p=0.01 uncorrected threshold
contInd = '1'  # contrast of interest

# FILE AND DIRECTORY BUSINESS
# original data directory
dataDir = '/tmp/Data/ds114'
# Output directory
outDir = os.path.join(dataDir,'WorkflowOutput')
# Datasink directory
datasinkDir = os.path.join(outDir,'FingerFootLips_Test_Cope6_Handedness')
# stats_dir directory
statsDir = os.path.join(datasinkDir,'stats_dir/stats')
# Z-stat image
imgZStat = os.path.join(statsDir, 'zstat' + condInd + '.nii.gz')


# FINDING CLUSTERS IN THE ANALYSIS RESULTS
# cluster node
cluster = Node(fsl.Cluster(in_file=imgZStat,
                           threshold=zThresh,
                           out_index_file=True,
                           out_threshold_file=True,
                           out_localmax_txt_file=True),
               name='cluster')

# data sink node
datasink = Node(DataSink(base_directory=statsDir),
                name='datasink')

# workflow connecting clustering to the datasink
clusterWF = Workflow(name="clusterWF", base_dir=outDir)
clusterWF.connect(cluster, 'index_file', datasink, 'index_file')
clusterWF.connect(cluster, 'threshold_file', datasink, 'threshold_file')
clusterWF.connect(cluster, 'localmax_txt_file', datasink, 'localmax_txt_file')
clusterWF.run()


# LOADING CLUSTER MAXIMA TABLE
fMaxTable = os.path.join(statsDir,'localmax_txt_file/zstat' + condInd + '_localmax.txt')
maxData = pd.read_csv(fMaxTable, sep='\t')   # reading the maxima file as a dataframe
maxData.dropna(how='all', axis=1, inplace=True)  # removing empty columns
print(maxData)



# CALCULATING CLUSTER SIZES
fClusInd = os.path.join(statsDir,'index_file/zstat' + condInd + '_index.nii.gz')
X_ClusInd = nib.load(fClusInd).get_data()  # getting the image of cluster IDs
clusterIDs = np.arange(1,X_ClusInd.max()+1)  # unique cluster IDs
print('Cluster ID\tCluster Size')
for iCluster in clusterIDs:
    clusterSize = len(X_ClusInd[X_ClusInd==iCluster])
    print('%3d' % iCluster + '\t\t%5d' % clusterSize)




# VISUALIZATION
# T1 weighted image for background
anatDir = os.path.join(dataDir,'derivatives_selected/fmriprep/sub-09/anat/')
imageT1 = os.path.join(anatDir,
                       'sub-09_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz')

# Thresholded zstat image
fThZStat=os.path.join(statsDir,'threshold_file/zstat' + condInd + '_threshold.nii.gz')
thImageStat=nib.load(fThZStat)

# global maximum cooridnates
X_zstat = nib.load(imgZStat).get_data()  # loading the zstat image
globalMax = np.unravel_index(np.argmax(X_zstat), X_zstat.shape) # voxel space
globalMaxMNI = coord_transform(globalMax[0],
                               globalMax[1],
                               globalMax[2],
                               thImageStat.affine)  # MNI space

# blob overlay at global max
plot_stat_map(thImageStat, bg_img=imageT1,
              colorbar=True, threshold=2.3, black_bg=True,
              draw_cross=True,
              cut_coords=globalMaxMNI)

# interactive visualization
view_img(thImageStat, bg_img=imageT1, cmap='black_red',
         symmetric_cmap=False, annotate=True,
         colorbar=True, threshold=2.3, black_bg=True,
         cut_coords=globalMaxMNI)
