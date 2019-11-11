import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_circles
from sklearn.svm import SVC
from DecisionBoundary import plot_svm_margin



# Creating a toy data with circles
X, y = make_circles(100, factor=.1, noise=.1, random_state=88)

# plotting the data
plt.figure(figsize=[6,6])
plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap=plt.cm.coolwarm)
plt.show()

# calculating the radius
r = np.sum(X**2, axis=1)**0.5

# plotting the data, y-axis replaced with the radius
plt.figure(figsize=[6,6])
plt.scatter(X[:, 0], r, c=y, s=50, cmap=plt.cm.coolwarm)
plt.show()


# SVM
R = np.vstack([X[:, 0], r]).T
sv = SVC(kernel='linear', C=10000)
sv.fit(R,y)


# plotting the margin on the SVM of the transformed data
plt.figure(figsize=[6,6])
plot_svm_margin(R,y,sv)
plt.show()


# SVM with RBF kernel
svRBF = SVC(kernel='rbf', C=10000)
svRBF.fit(X,y)

# plotting the margin on the SVM with the RBF kernel
plt.figure(figsize=[6,6])
plot_svm_margin(X,y,svRBF)
plt.show()
