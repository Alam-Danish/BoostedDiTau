
from CRABClient.UserUtilities import config

config = config()
config.General.requestName = 'Ntuple_SingleMuon_Run2022B_MiniAODv4_v3'

config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.allowUndistributedCMSSW = True

config.JobType.psetName = '../rerunTauRecoOnMiniAOD_WithClean_Custom.py'
#config.JobType.numCores = 4
#config.JobType.maxMemoryMB = 10000

config.Data.inputDataset = '/SingleMuon/Run2022B-22Sep2023-v1/MINIAOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'Automatic'
#config.Data.splitting = 'LumiBased'                                                                                                                         
#config.Data.unitsPerJob = 50
config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/Cert_Collisions2022_eraB_355100_355769_Golden.json'

config.Data.outLFNDirBase = '/store/user/dalam/TCPNtuple/Run3/2022preEE'
config.Data.publication = False
config.Data.outputDatasetTag = 'Ntuple_SingleMuon_Run2022B_v3'  

config.Site.storageSite = 'T2_US_Florida'

config.Site.ignoreGlobalBlacklist = True

#config.Site.blacklist = ['T2_US_Nebraska','T2_IT_Pisa']
