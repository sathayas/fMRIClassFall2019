import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
from sklearn.svm import SVC
from DecisionBounary import plot_svm_margin

# producing a toy data set: two clusters, with some overlap
X, y = make_blobs(n_samples=100, centers=2,
                  random_state=23, cluster_std=3.75)


# plotting the toy data
plt.figure(figsize=[6,6])
plt.scatter(X[:, 0], X[:, 1], c=y, s=50)
plt.show()


# SVM
plt.figure(figsize=[9,9])

svL = SVC(kernel='linear', C=10)  # large C (C=10)
svL.fit(X,y)
plt.subplot(221)
plot_svm_margin(X,y,svL)
plt.title('Large C (C=10)')

svM = SVC(kernel='linear', C=1.0)  # medium C (C=1.0)
svM.fit(X,y)
plt.subplot(222)
plot_svm_margin(X,y,svM)
plt.title('Medium C (C=1.0)')

svS = SVC(kernel='linear', C=0.1)  # small C (C=0.1)
svS.fit(X,y)
plt.subplot(223)
plot_svm_margin(X,y,svS)
plt.title('Small C (C=0.1)')

svT = SVC(kernel='linear', C=0.01)  # tiny C (C=0.01)
svT.fit(X,y)
plt.subplot(224)
plot_svm_margin(X,y,svT)
plt.title('Tiny C (C=0.01)')

plt.show()
