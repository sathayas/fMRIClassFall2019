import os
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

# Creating a workflow object
wf = Workflow(name="fslNorm", base_dir=outDir)

# connecting nodes as a workflow
wf.connect(fslBET, "out_file", fslFLIRT, "in_file")
wf.connect([(fslBET, fslFNIRT, [('out_file', 'in_file')]),
            (fslFLIRT,fslFNIRT, [('out_matrix_file', 'affine_file')])])


# writing out graphs
wf.write_graph(graph2use='orig', dotfilename='graph_orig.dot')

# DataSink to collect intermediate outputs
datasink = Node(DataSink(base_directory=outDir),
                name='datasink')

# adding datasink
wf.connect(fslFLIRT, 'out_file', datasink, 'NormFSL.@flirt')
wf.connect(fslFNIRT, 'warped_file', datasink, 'NormFSL.@fnirt')


# writing out graphs
wf.write_graph(graph2use='orig', dotfilename='graph_orig_datasink.dot')


# running the workflow
wf.run()
