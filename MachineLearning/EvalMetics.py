import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score, adjusted_mutual_info_score


# Loading the iris data
iris = datasets.load_iris()
X_raw = iris.data    # Data
y = iris.target  # Target i.e., true clusters
varNames = iris.feature_names  # variable names
targetNames = iris.target_names  # names of irises
nVar = X.shape[1]  # number of features

# standardizing the features
irisNorm = StandardScaler().fit(X_raw)  # learning standardization
X = irisNorm.transform(X_raw)  # transforming the raw features



# K-means clustering, raw data
numClus = 3  # number of clusters
kmRaw = KMeans(n_clusters=numClus)  # defining the clustering object
kmRaw.fit(X_raw)  # actually fitting the data
yRaw_clus = kmRaw.labels_   # clustering info resulting from K-means


# K-means clustering, normalized data
kmNorm = KMeans(n_clusters=numClus)  # defining the clustering object
kmNorm.fit(X)  # actually fitting the data
yNorm_clus = kmNorm.labels_   # clustering info resulting from K-means


# ARI
print('ARI (raw)=  %6.4' % adjusted_rand_score(y, yRaw_clus))
print('ARI (norm)=  %6.4' % adjusted_rand_score(y, yNorm_clus))
