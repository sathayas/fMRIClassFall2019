import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans


##### Loading the data
infile = np.load(os.path.join('DataML',
                              'Leiden_sub39335_Rt2_K200_Rmat.npz'))
Rmat = infile['Rmat']
nodes = infile['nodes']
xyz = infile['xyz']


##### Examples of correlation matrices
indTime = 0
plt.imshow(Rmat[indTime,:,:], cmap=plt.cm.rainbow)
plt.title('Correlation matrix, t=%-3d' % indTime)
plt.xlabel('Nodes')
plt.ylabel('Nodes')
plt.colorbar()

plt.show()


##### loading the efficiency metrics that have been pre-calculated
f = np.load(os.path.join('DataML',
                         'Leiden_sub39335_Rt2_K200_Efficiency.npz'))
ElocMat = f['ElocMat']
EglobMat = f['EglobMat']


##### plotting efficiency over time
plt.figure(figsize=[9,5])
plt.subplot(121)
plt.imshow(ElocMat, cmap=plt.cm.rainbow)
plt.title('Local efficiency')
plt.xlabel('Time')
plt.ylabel('Nodes')
plt.colorbar()

plt.subplot(122)
plt.imshow(EglobMat, cmap=plt.cm.rainbow)
plt.title('Global efficiency')
plt.xlabel('Time')
plt.ylabel('Nodes')
plt.colorbar()

plt.show()



##### Converting correlation matrices to vectors
nNodes = Rmat.shape[-1]
nTime = Rmat.shape[0]
indR = np.triu_indices(nNodes,1) # indices for the upper triangle of R
# initializing the data array, rows = time, cols = correlation
Rdata = np.zeros((nTime,len(indR[0])))
for iTime in range(nTime):
    R = Rmat[iTime,:,:]
    Rdata[iTime,:] = R[indR]




###### Clustering --- Figuring out the  number of clusters
# determinging the number of clusters (up to 30 clusters)
SSE = []
for iClus in range(1,31):
    #print('Number of clusters: %d' % iClus)
    # K-means clustering
    km = KMeans(n_clusters=iClus)  # K-means with a given number of clusters
    km.fit(Rdata)  # fitting the principal components
    SSE.append(km.inertia_) # recording the sum of square distances

# plotting the sum of square distance
plt.plot(np.arange(1,31),SSE,marker = "o")
plt.xlabel('Number of clusters')
plt.ylabel('Sum of sq distances')
plt.show()



###### Clustering --- with K=6
km = KMeans(n_clusters=6)  # defining the clustering object
km.fit(Rdata)  # actually fitting the data
y_clus = km.labels_   # clustering info resulting from K-means
y_cent = km.cluster_centers_  # centroid coordinates



####### plotting cluster over time
plt.figure(figsize=[4,7])
plt.subplot(211)
plt.plot(y_clus)
plt.title('States over time')
plt.xlabel('Time')
plt.ylabel('State')
plt.xlim(1,nTime)

plt.subplot(212)
plt.imshow(EglobMat, cmap=plt.cm.rainbow, aspect='auto')
plt.title('Global efficiency')
plt.xlabel('Time')
plt.ylabel('Nodes')
plt.xlim(1,nTime)

plt.subplots_adjust(left=0.15, right=0.975, top=0.95, bottom=0.075,
                    hspace=0.4)
plt.show()
