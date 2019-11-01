import os  # system functions
import nipype.interfaces.fsl as fsl  # fsl
from nipype import Node, Workflow  # components to construct workflow
from nipype import SelectFiles  # to facilitate file i/o
from nipype.interfaces.io import DataSink  # datasink
from nipype.interfaces.utility import Function  # for custom made function

# a dummy function -- just to get the file location of a file parameter
def FileNameExtract(fileObject):
    import os
    filePath = os.path.split(fileObject)
    fileOut = os.path.join(filePath,'FileName.txt')
    f = open(fileOut,'w')
    f.write(fileOut)
    f.close()
    return fileOut


##### PARAMETERS #####
indCope = '5'  # the contrast of interest, finger vs others
indSes = 'test'  # the session of interest


##### DIRECTORY BUSINESS ######
# original data directory
dataDir = '/tmp/Data/ds114'
# Output directory
outDir = os.path.join(dataDir,'WorkflowOutput')
# directory where preprocessed fMRI data is located
baseDir = os.path.join(dataDir, 'BatchOutput_FingerFootLips/feat_dir')


###########
#
# SETTING UP THE SECOND LEVEL ANALYSIS NODES
#
###########
# a list of subjects
subject_list = ['%02d' % i for i in range(1,11)]

# Dictionary with regressors
dictReg = {'reg1': [1]*len(subject_list) # vector of ones
          }

# Contrasts
cont01 = ['activation', 'T', list(dictReg.keys()), [1]]
cont02 = ['activation', 'T', list(dictReg.keys()), [-1]]

contrastList = [cont01, cont02]

# Setting up the second level analysis model node
level2design = Node(fsl.MultipleRegressDesign(contrasts=contrastList,
                                              regressors=dictReg),
                    name='level2design')

filenameextract = Node(interface=Function(input_names=['fileObject'],
                                          output_names=['fileOut'],
                                          function=FileNameExtract),
                       name='filenameextract')

# creating datasink to collect outputs
datasink = Node(DataSink(base_directory=
                         os.path.join(outDir,'DOFCalculation')),
                name='datasink')




# creating the workflow
dofCalc = Workflow(name="dofCalc", base_dir=outDir)

# connecting nodes
dofCalc.connect(level2design, 'design_mat', filenameextract, 'fileObject')
dofCalc.connect(filenameextraxt, 'fileOut', datasink, 'fileOut')


# running the workflow
dofCalc.run()
