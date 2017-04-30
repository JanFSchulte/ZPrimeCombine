import os
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'limits_forDM_1500_20170430_151406'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True


config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'dummyPSet.py'
config.JobType.scriptExe= 'runLimits'
config.JobType.scriptArgs= ['dummy=dummy.py','tarFile=gridPack.tar','outputTag=forDM','mass=1500','nIter=50000','nToys=20','expected=1','config=ICHEP_width050']
config.JobType.inputFiles= ['gridPack.tar',os.environ['CMSSW_BASE']+'/bin/'+os.environ['SCRAM_ARCH']+'/combine','FrameworkJobReport.xml']
config.JobType.outputFiles= ['expectedLimit_ICHEP_width050_forDM_1500.root']


config.section_("Data")
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = 50
config.Data.outputPrimaryDataset = 'forDM'
config.Data.outputDatasetTag = 'test'
config.Data.outLFNDirBase = '/store/user/jschulte/limits/ICHEP_width050'
 
config.section_("Site")
config.Site.storageSite = "T2_DE_RWTH"

config.section_("User")
