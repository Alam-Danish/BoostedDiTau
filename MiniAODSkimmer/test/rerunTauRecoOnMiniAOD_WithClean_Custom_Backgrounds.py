import FWCore.ParameterSet.Config as cms
######
# Configuration to run tau ReReco+PAT at MiniAOD samples
# M. Bluj, NCBJ Warsaw
# based on work of J. Steggemann, CERN
# Created: 9 Nov. 2017
#With additional implementation for Muon/Electron Cleaning from Jets
# Redwan Md Habibullah 8 July 2021
######

######

import PhysicsTools.PatAlgos.tools.helpers as configtools
from PhysicsTools.PatAlgos.tools.helpers import cloneProcessingSnippet
from PhysicsTools.PatAlgos.tools.helpers import massSearchReplaceAnyInputTag
from FWCore.ParameterSet.MassReplace import massSearchReplaceParam


import sys
#inputfile = sys.argv[2]
###########
runType = 'background'      # Options: 'signal', 'background', or 'data'
year    = '2022preEE'       # Options: '2022preEE', '2022postEE', '2023preBPix', '2023postBPix', '2024'
maxEvents = -1              # -1: all
appendOutput = True
#isMC = True
########



# If 'reclusterJets' set true a new collection of uncorrected ak4PFJets is
# built to seed taus (as at RECO), otherwise standard slimmedJets are used
reclusterJets = True        # Options: True or False

# set true for upgrade studies
phase2 = False              # Options: True or False

# Output mode
# outMode = 0  # store original MiniAOD and new selectedPatTaus
# outMode = 1 #store original MiniAOD, new selectedPatTaus, and all PFtau products as in AOD (except of unsuported ones)
outMode = 2 # similar to outMode 0 but without skimming

print('Running Tau reco&id with MiniAOD inputs:')
print('\t Run type:', runType)
print('\t Recluster jets:', reclusterJets)
print('\t Use Phase2 settings:', phase2)
#print('\t Output mode:', outMode)

#####
from Configuration.Eras.Era_Run3_cff import Run3
#from Configuration.StandardSequences.Eras import eras
era = Run3
if phase2:
    from Configuration.Eras.Era_Phase2_timing_cff import Phase2_timing
    era = Phase2_timing
process = cms.Process("TAURECO", era)
# for CH reco
process.load("Configuration.StandardSequences.MagneticField_cff")
if not phase2:
    process.load("Configuration.Geometry.GeometryRecoDB_cff")
else:
    process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff')

#####
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()
process.source = cms.Source(
    "PoolSource", fileNames=readFiles, secondaryFileNames=secFiles)

process.maxEvents = cms.untracked.PSet(
    input=cms.untracked.int32(maxEvents)
)

process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring('ProductNotFound')
)

print('\t Max events:', process.maxEvents.input.value())

if runType == 'signal':
    readFiles.extend([
        'file:root://cmseos.fnal.gov//eos/uscms/store/user/nbower/Events/TCP_m_50_w_1_htj_0to100_slc6_amd64_gcc630_MINIAOD/TCP_m_50_w_1_htj_0to100_slc6_amd64_gcc630_MINIAOD_1.root',
        #'file:root://cmseos.fnal.gov//eos/uscms/store/user/nbower/Events/TCP_m_50_w_1_htj_0to100_slc6_amd64_gcc630_MINIAOD/TCP_m_50_w_1_htj_0to100_slc6_amd64_gcc630_MINIAOD_2.root',
        #'file:root://cmseos.fnal.gov//eos/uscms/store/user/nbower/Events/TCP_m_50_w_1_htj_0to100_slc6_amd64_gcc630_MINIAOD/TCP_m_50_w_1_htj_0to100_slc6_amd64_gcc630_MINIAOD_3.root',
        #'file:root://cmseos.fnal.gov//eos/uscms/store/user/nbower/Events/TCP_m_50_w_1_htj_0to100_slc6_amd64_gcc630_MINIAOD/TCP_m_50_w_1_htj_0to100_slc6_amd64_gcc630_MINIAOD_4.root',
        #'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer20UL17MiniAODv2/ZZ_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/230000/0571FD70-4526-9F4F-BD99-769E4256D634.root'
        #'file:root://cmseos.fnal.gov//eos/uscms/store/user/nbower/Events/TCP_m_50_w_1_htj_0to100_slc6_amd64_gcc630_MINIAOD/TCP_m_50_w_1_htj_0to100_slc6_amd64_gcc630_MINIAOD_2.root',
        #'file:root://cmseos.fnal.gov//eos/uscms/store/user/nbower/Events/TCP_m_50_w_1_htj_0to100_slc6_amd64_gcc630_MINIAOD/TCP_m_50_w_1_htj_0to100_slc6_amd64_gcc630_MINIAOD_3.root',
        #'file:root://cmseos.fnal.gov//eos/uscms/store/user/nbower/Events/TCP_m_50_w_1_htj_0to100_slc6_amd64_gcc630_MINIAOD/TCP_m_50_w_1_htj_0to100_slc6_amd64_gcc630_MINIAOD_4.root',
        #'file:patMiniAOD_standard.root'
        #'file:/eos/uscms/store/user/rhabibul/HtoAA/HtoAAMiniAODTest/4B62060B-AC2A-694A-8E56-B484FD41BCB2.root'
        #'file:/eos/uscms/store/user/rhabibul/HtoAA/HtoAAMiniAODTest/04905A2E-7E30-1942-A815-EC9B488A4391.root'
        #'file:/eos/uscms/store/user/rhabibul/HtoAA/HtoAAMiniAODTest/002C691B-A0CE-A24F-8805-03B4C52C9004.root'#
    ])
elif runType == 'background':
    readFiles.extend([
        #'file:patMiniAOD_standard.root'
        'file:root://cmsxrootd.fnal.gov//store/mc/Run3Summer22MiniAODv4/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/MINIAODSIM/pilot_nanov15_130X_mcRun3_2022_realistic_v5-v2/2830000/ff237c4f-1c3e-4203-a725-5ed674c657c3.root',
        #'/store/relval/CMSSW_10_5_0_pre1/RelValQCD_FlatPt_15_3000HS_13/MINIAODSIM/PU25ns_103X_mcRun2_asymptotic_v3-v1/20000/A5CBC261-E3AB-C842-896F-E6AFB38DD22F.root'
        #'file:/eos/uscms/store/user/rhabibul/HtoAA/HtoAAMiniAODTest/002C691B-A0CE-A24F-8805-03B4C52C9004.root'
        #'file:root://cmseos.fnal.gov//eos/uscms/store/user/zhangj/events/ALP/UL2017/TCP_m_30_w_1_htj_100to400_slc6_amd64_gcc630_MINIAOD/TCP_m_30_w_1_htj_100to400_slc6_amd64_gcc630_MINIAOD_1.root',
        #'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer20UL17MiniAODv2/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/120000/005B6A7C-B0B1-A745-879B-017FE7933B77.root',
        #'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer20UL18MiniAODv2/AToTauTau_ALP_M-30_HT-400toInf_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/050B7E1E-7335-EE43-82E3-42BE48F2BD58.root',
    ])
elif runType == 'data':
    readFiles.extend([
        #'/store/data/Run2018D/SingleMuon/MINIAOD/12Nov2019_UL2018-v4/710000/B7163712-7B03-D949-91C9-EB5DD2E1D4C3.root' # SingleMuon PD
        '/store/data/Run2018D/Tau/MINIAOD/12Nov2019_UL2018-v1/00000/01415E2B-7CE5-B94C-93BD-0796FC40BD97.root' # Tau PD
    ])
else:
    print('Unknown runType =',runType,'; Use \"signal\" or \"background\" or \"data\"')
    exit(1)


#####



import BoostedDiTau.MiniAODSkimmer.adaptToRunAtMiniAODCustom_Backgrounds as tauAtMiniToolsCustom

#####
print ('Step : 1 - Added Paths for RecoCleaned ')

#tauAtMiniToolsCustom.addTauReRecoCustom(process)


#####
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
if not phase2:
    print('Year :', year)
    if year == '2022preEE':
        process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2022_realistic', '')
    elif year == '2022postEE':
        process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2022_realistic_postEE', '')
    elif year == '2023preBPix':
        process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2023_realistic', '')
    elif year == '2023postBPix':
        process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2023_realistic_postBPix', '')
    elif year == '2024':
        process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2024_realistic', '')
    else:
        raise RuntimeError('No GlobalTag defined for year={}, runType={}'.format(year, runType))
else:
    process.GlobalTag = GlobalTag(
        process.GlobalTag, 'auto:phase2_realistic', '')

tauAtMiniToolsCustom.addTauReRecoCustom(process)

#####
# mode = 0: store original MiniAOD and new selectedPatTaus
# mode = 1: store original MiniAOD, new selectedPatTaus, and all PFtau products as in AOD (except of unsuported ones)
print ('Step : 2 - Declare Outputs')

#process.output = tauAtMiniToolsCustom.setOutputModule(mode=outMode)


#if runType == 'signal':
#    process.output.fileName = 'miniAOD_TauReco_ggH_'+year+'.root'
#    if reclusterJets:
#        process.output.fileName = 'miniAOD_TauReco_ak4PFJets_ggH_'+year+'.root'
#elif runType == 'background':
#    process.output.fileName = 'miniAOD_TauReco_Background_'+year+'.root'
#    if reclusterJets:
#        process.output.fileName = 'miniAOD_TauReco_ak4PFJets_Background_'+year+'.root'
#else: # data
#    process.output.fileName = 'miniAOD_TauReco_data_'+year+'.root'
#    if reclusterJets:
#        process.output.fileName = 'miniAOD_TauReco_ak4PFJets_data'+year+'.root'
#process.out = cms.EndPath(process.output)


##### Modify ouput by Hand#####

#if appendOutput:
#    #process.output.outputCommands.append('keep *_selectedPatTaus_*_*')
#    #process.output.outputCommands.append('keep *_selectedPatTausElectronCleaned_*_*')
#    #process.output.outputCommands.append('keep *_selectedPatTausMuonCleaned_*_*')
#    process.output.outputCommands.append('keep *_slimmedTausUnCleaned_*_*')
#    process.output.outputCommands.append('keep *_slimmedTausElectronCleaned_*_*')
#    process.output.outputCommands.append('keep *_slimmedTausLowPtElectronCleaned_*_*')
#    process.output.outputCommands.append('keep *_slimmedTausMuonCleaned_*_*')
#    process.output.outputCommands.append('keep *_slimmedTausBoosted_*_*')
#    process.output.outputCommands.append('keep *_lumiSummary_*_*')
    
 

#####

#tauAtMiniToolsCustom.addTauReRecoCustom(process)

#process.out = cms.EndPath(process.output)
#process.schedule.append(process.out)
#####
print ('Step : 3 - Adapt Tau Reco to MiniAOD inputs')

tauAtMiniToolsCustom.adaptTauToMiniAODReReco(process, runType, reclusterJets)
#######



print ('Step : 4 - Lower Pt Standard Taus')
###### lowering Pt of Standard Taus ######
minJetPt = 5

process.ak4PFJetsLegacyHPSPiZeros.minJetPt = minJetPt
process.combinatoricRecoTaus.minJetPt = minJetPt
process.recoTauAK4Jets08RegionPAT.minJetPt = minJetPt
process.ak4PFJetsRecoTauChargedHadrons.minJetPt = minJetPt
process.selectedPatTaus.cut = cms.string('pt > 8.0 && abs(eta)<2.3 && tauID(\'decayModeFinding\')> 0.5')
##########################################
#### Lower Tau Pt Boosted Taus###########

print ('Step : 5 - Lower Pt Boosted Taus')

jetPt=5
tauPt=8

getattr(process,'selectedPatTausBoosted').cut = cms.string("pt > {} && abs(eta) < 2.3 && tauID(\'decayModeFinding\')> 0.5".format(tauPt))
process.ak4PFJetsLegacyHPSPiZerosBoosted.minJetPt = jetPt
process.combinatoricRecoTausBoosted.minJetPt = jetPt
process.recoTauAK4Jets08RegionPATBoosted.minJetPt = jetPt
process.ak4PFJetsRecoTauChargedHadronsBoosted.minJetPt = jetPt
## for boosted taus, also change min jet value in CA8 jet and it's subjets
process.ca8PFJetsCHSprunedForBoostedTausPAT.subjetPtMin = jetPt
process.ca8PFJetsCHSprunedForBoostedTausPAT.jetPtMin = 10

##########################################
#### Lower Tau Pt ElectronCleaned Taus###########

print ('Step : 6 - Lower Pt ElectronCleaned Taus')

jetPt=5
tauPt=8

getattr(process,'selectedPatTausElectronCleaned').cut = cms.string("pt > {} && abs(eta) < 2.3 && tauID(\'decayModeFinding\')> 0.5".format(tauPt))
process.ak4PFJetsLegacyHPSPiZerosElectronCleaned.minJetPt = jetPt
process.combinatoricRecoTausElectronCleaned.minJetPt = jetPt
process.recoTauAK4Jets08RegionPATElectronCleaned.minJetPt = jetPt
process.ak4PFJetsRecoTauChargedHadronsElectronCleaned.minJetPt = jetPt

##########################################
#### Lower Tau Pt MuonCleaned Taus###########

print ('Step : 7 - Lower Pt MuonCleaned Taus')

process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring("ProductNotFound")
)

getattr(process,'selectedPatTausMuonCleaned').cut = cms.string("pt > {} && abs(eta) < 2.3 && tauID(\'decayModeFinding\')> 0.5".format(tauPt))
process.ak4PFJetsLegacyHPSPiZerosMuonCleaned.minJetPt = jetPt
process.combinatoricRecoTausMuonCleaned.minJetPt = jetPt
process.recoTauAK4Jets08RegionPATMuonCleaned.minJetPt = jetPt
process.ak4PFJetsRecoTauChargedHadronsMuonCleaned.minJetPt = jetPt

#############################################
#### Lower Pt LowPtElectronCleaned Taus #####

#print ('Step : 8 - Lower Pt LowPtElectronCleaned Taus')

#getattr(process,'selectedPatTausLowPtElectronCleaned').cut = cms.string("pt > {} && abs(eta) < 2.5 && tauID(\'decayModeFindingNewDMs\')> 0.5".format(tauPt))
#process.ak4PFJetsLegacyHPSPiZerosLowPtElectronCleaned.minJetPt = jetPt
#process.combinatoricRecoTausLowPtElectronCleaned.minJetPt = jetPt
#process.recoTauAK4Jets08RegionPATLowPtElectronCleaned.minJetPt = jetPt
#process.ak4PFJetsRecoTauChargedHadronsLowPtElectronCleaned.minJetPt = jetPt

tauAtMiniToolsCustom.addFurtherSkimming(process)
tauAtMiniToolsCustom.addTCPNtuples(process)

#process.out = cms.EndPath(process.output)
#process.schedule.append(process.out)

###########################################
process.load('FWCore.MessageService.MessageLogger_cfi')
if process.maxEvents.input.value() > 10:
    process.MessageLogger.cerr.FwkReport.reportEvery = process.maxEvents.input.value()//10
if process.maxEvents.input.value() > 10000 or process.maxEvents.input.value() < 0:
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000

#####
#process.options = cms.untracked.PSet(
#)
#process.options.numberOfThreads = cms.untracked.uint32(4)
#process.options.numberOfThreads=cms.untracked.uint32(1)
#process.options.numberOfStreams = cms.untracked.uint32(0)
#print('\t No. of threads:', process.options.numberOfThreads.value(), ', no. of streams:', process.options.numberOfStreams.value())

#process.options = cms.untracked.PSet(
#    process.options,
#    wantSummary=cms.untracked.bool(True)
#)

process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring('ProductNotFound')
)

process.options = dict( # numberOfThreads = 4,
    numberOfThreads = 1,
                      #  numberOfStreams = 0,
    wantSummary = True
)
print('\t No. of threads:', process.options.numberOfThreads.value(), ', no. of streams:', process.options.numberOfStreams.value())

dump_file = open('dump_rerunMiniAODClean.py','w')
dump_file.write(process.dumpPython())

SimpleMemoryCheck = cms.Service("SimpleMemoryCheck",ignoreTotal = cms.untracked.int32(1) )
