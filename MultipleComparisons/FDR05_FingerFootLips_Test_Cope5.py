import os

##### PARAMETERS #####

##### DIRECTORY BUSINESS ######
# original data directory
dataDir = '/tmp/Data/ds114'
# Statistics directory from the 2nd level analysis
wfDir = os.path.join(dataDir,'WorkflowOutput')
statDir = os.path.join(wfDir,'FingerFootLips_Test_Cope5/stats_dir/stats/')
# FDR results directory
fdrDir = os.path.join(statDir,'FDR')

# create the FDR directory if it doesnt already exist
if not os.path.exists(fdrDir):
        os.makedirs(fdrDir)


##### T-STATISTIC IMAGE TO P-VALUE IMAGE #####
# First, re-creating the design
