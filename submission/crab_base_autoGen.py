import os
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'limits_crabTest_4500_20170112_225359'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True


config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'dummyPSet.py'
config.JobType.scriptExe= 'runLimits'
config.JobType.scriptArgs= ['dummy=dummy.py','tarFile=gridPack.tar','outputTag=crabTest','mass=4500','nIter=500000','nToys=10','expected=1']
config.JobType.inputFiles= ['gridPack.tar',os.environ['CMSSW_BASE']+'/bin/'+os.environ['SCRAM_ARCH']+'/combine','FrameworkJobReport.xml']
config.JobType.outputFiles= ['expectedLimit_ICHEPDimuon_crabTest_4500.root']


config.section_("Data")
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = 100
config.Data.outputPrimaryDataset = 'crabTest'
config.Data.outputDatasetTag = 'test'
config.Data.outLFNDirBase = '/store/user/jschulte/limits/test'
 
config.section_("Site")
config.Site.storageSite = "T2_DE_RWTH"

config.section_("User")
