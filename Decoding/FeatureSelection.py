import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nilearn import datasets
from nilearn.input_data import NiftiMasker
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report

###### PARAMETERS
###### LOADING IMAGE DATA
###### LOADING BEHAVIORAL DATA
###### MASKING FOR SELECTED STIMS
###### FEATURE SELECTION
###### VISUALIZING FEATURE LOCATIONS
###### SVM CLASSIFIER
