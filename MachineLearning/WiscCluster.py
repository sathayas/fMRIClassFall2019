import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# loadin the data
wiscData = pd.read_csv(os.path.join('DataML','wiscsem.txt'), sep='\t')
wiscFeatures = np.array(wiscData.iloc[:,2:13])
featureNames = np.array(wiscData.columns[2:13])


# determinging the number of clusters (up to 20 clusters)
SSE = []
for iClus in range(1,21):
    # K-means clustering
    km = KMeans(n_clusters=iClus)  # K-means with a given number of clusters
    km.fit(wiscFeatures)  # fitting the principal components
    SSE.append(km.inertia_) # recording the sum of square distances

# plotting the sum of square distance
plt.plot(np.arange(1,21),SSE,marker = "o")
plt.xlabel('Number of clusters')
plt.ylabel('Sum of sq distances')
plt.show()


## We will go with 3 clusters
# K-means clustering again
km = KMeans(n_clusters=3)
km.fit(wiscFeatures)  # fitting the principal components
y_clus = km.labels_   # clustering info resulting from K-means


### plotting the clusters
# with two of the features
xFeature = 1 # index for the feature on the x-axis
yFeature = 9 # index for the feature on the y-axis
plt.scatter(wiscFeatures[:,xFeature],
            wiscFeatures[:,yFeature],c=y_clus,marker='+')
plt.xlabel(featureNames[xFeature])
plt.ylabel(featureNames[yFeature])
plt.title(featureNames[xFeature] + ' v.s. ' + featureNames[yFeature])
plt.show()
