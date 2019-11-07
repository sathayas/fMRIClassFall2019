import os
import matplotlib.pyplot as plt
import numpy as np

##### Parameters
targetDeg = 20

##### Loading the data
infile = np.load('DataML/Leiden_sub39335_Rt2_K200_Rmat.npz')
Rmat = infile['Rmat']
nodes = infile['nodes']
xyz = infile['xyz']
