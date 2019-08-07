import os
import matplotlib.pyplot as plt
import nipype.interfaces.fsl as fsl # importing FSL interface functions
from nipype import Node, Workflow  # components to construct workflow
from nipype.interfaces.io import DataSink  # datasink
from bids.grabbids import BIDSLayout  # BIDSLayout object to specify file(s)


# Directory where your data set resides.
dataDir = '/tmp/Data/ds102'

# Creating the layout object for this BIDS data set
layout = BIDSLayout(dataDir)

# an T1 weighted image from one of the subjects
imageT1 = layout.get(subject='26',
                     suffix='T1w',
                     extension='nii.gz',
                     return_type='file')[0]

# template image (from FSL)
fMNI = '/usr/local/fsl/data/standard/MNI152_T1_2mm_brain.nii.gz'

# Output directory
outDir = os.path.join(dataDir, 'WorkflowOutput')


# Skullstrip process node
fslBET = Node(fsl.BET(in_file=imageT1),
              name="fslBET")


# Linear normalization node
fslFLIRT = Node(fsl.FLIRT(reference=fMNI,
                          cost_func='normmi'),
                name="fslFLIRT")

# Non-linear normalization node
fslFNIRT = Node(fsl.FNIRT(ref_file=fMNI),
                name='fslFNIRT')


# DataSink to collect intermediate outputs
datasink = Node(DataSink(base_directory=outDir),
                name='datasink')



# Creating a workflow object
wfNormT1 = Workflow(name="wfNormT1", base_dir=outDir)

# connecting nodes as a workflow
wfNormT1.connect(fslBET, "out_file", fslFLIRT, "in_file")
wfNormT1.connect(fslBET, 'out_file', fslFNIRT,'in_file')
wfNormT1.connect(fslFLIRT, 'out_matrix_file', fslFNIRT, 'affine_file')

# adding datasink
wfNormT1.connect(fslFLIRT, 'out_file', datasink, 'NormLinear')
wfNormT1.connect(fslFNIRT, 'warped_file', datasink, 'NormNonLinear')



# writing out graphs
wf.write_graph(graph2use='orig', dotfilename='graph_orig_datasink.dot')

# showing the graph
plt.figure(figsize=[6,6])
img=mpimg.imread(os.path.join(outDir,"coReg","graph_orig.png"))
imgplot = plt.imshow(img)
plt.axis('off')
plt.show()

# running the workflow
wf.run()
