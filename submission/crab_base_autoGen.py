import os
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'limits_forDM_3375_20170503_023706'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True


config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'dummyPSet.py'
config.JobType.scriptExe= 'runLimits'
config.JobType.scriptArgs= ['dummy=dummy.py','tarFile=gridPack.tar','outputTag=forDM','mass=3375','nIter=50000','nToys=10','expected=1','config=ICHEPDielectron_width350']
config.JobType.inputFiles= ['gridPack.tar',os.environ['CMSSW_BASE']+'/bin/'+os.environ['SCRAM_ARCH']+'/combine','FrameworkJobReport.xml']
config.JobType.outputFiles= ['expectedLimit_ICHEPDielectron_width350_forDM_3375.root']


config.section_("Data")
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = 100
config.Data.outputPrimaryDataset = 'forDM'
config.Data.outputDatasetTag = 'test'
config.Data.outLFNDirBase = '/store/user/jschulte/limits/ICHEPDielectron_width350'
 
config.section_("Site")
config.Site.storageSite = "T2_DE_RWTH"
config.Site.blacklist = ["T2_US_Nebraska","T2_US_Wisconsin","T2_US_Purdue","T3_UK_ScotGrid_GLA","T2_US_UCSD","T2_US_Caltech"]
config.section_("User")
