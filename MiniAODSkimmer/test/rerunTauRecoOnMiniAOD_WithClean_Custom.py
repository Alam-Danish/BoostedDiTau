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
#inputfile = 'file:root://cmseos.fnal.gov//eos/uscms/store/user/zhangj/events/ALP/UL2017/TCP_m_10_w_1_htj_400toInf_slc6_amd64_gcc630_MINIAOD/TCP_m_10_w_1_htj_400toInf_slc6_amd64_gcc630_MINIAOD_1.root'
###########
runType = 'signal'          # Options: 'signal', 'background', or 'data'
year    = '2024'       # Options: '2022', '2022EE', '2023', '2023BPix', '2024'
maxEvents = -1              # -1: all
appendOutput = True
#isMC = True
########



# If 'reclusterJets' set true a new collection of uncorrected ak4PFJets is
# built to seed taus (as at RECO), otherwise standard slimmedJets are used
reclusterJets = True            # Options: True or False

# set true for upgrade studies
phase2 = False                  # Options: True or False

# Output mode
# outMode = 0  # store original MiniAOD and new selectedPatTaus
# outMode = 1 #store original MiniAOD, new selectedPatTaus, and all PFtau products as in AOD (except of unsuported ones)
#outMode = 2 # similar to outMode 0 but without skimming

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
        #'file:../../../../../../test_TCP/CMSSW_13_0_13/src/AToTauTau/mode/ALP_M-30_HT-100to400_2022preEE_mode0_MiniAODv4_mode0_1142441_0.root',
        #'file:../../../../../../test_TCP/CMSSW_13_0_13/src/AToTauTau/ALP/ALP_M-30_HT-100to400_2022preEE_MiniAODv4_1160458_0.root'
        #'file:../../../../../../test_TCP/CMSSW_13_0_13/src/AToTauTau/ALP/ALP_M-30_HT-100to400_2022preEE_MiniAODv4_1160458_1.root'
        #'root://cmseos.fnal.gov//eos/uscms/store/user/zhangj/events/ALP/UL2017/TCP_m_30_w_1_htj_400toInf_slc6_amd64_gcc630_MINIAOD/TCP_m_30_w_1_htj_400toInf_slc6_amd64_gcc630_MINIAOD_1.root',
        #'root://cmseos.fnal.gov//eos/uscms/store/user/zhangj/events/ALP/UL2017/TCP_m_30_w_1_htj_100to400_slc6_amd64_gcc630_MINIAOD/TCP_m_30_w_1_htj_100to400_slc6_amd64_gcc630_MINIAOD_2.root',
        #'root://cmseos.fnal.gov//store/user/mwulansa/Events/TCP_m10_ht_100to400_slc7_amd64_gcc10_MINIAOD/TCP_m10_ht_100to400_slc7_amd64_gcc10_MINIAOD_1.root',
        #'file:root://cmseos.fnal.gov//eos/uscms/store/user/nbower/Events/TCP_m_50_w_1_htj_0to100_slc6_amd64_gcc630_MINIAOD/TCP_m_50_w_1_htj_0to100_slc6_amd64_gcc630_MINIAOD_2.root',
        #'file:patMiniAOD_standard.root'
        #'file:/eos/uscms/store/user/rhabibul/HtoAA/HtoAAMiniAODTest/4B62060B-AC2A-694A-8E56-B484FD41BCB2.root'
        #'root://eos.grif.fr:11000/eos/grif/cms/grif/store/mc/RunIII2024Summer24MiniAODv6/GluGluALPtoTauTau_Bin-HT-400toInf_Par-M-10_TuneCP5_13p6TeV_madgraphMLM-pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/2550000/11315589-2c14-434d-9758-453df962c4ef.root',
        'root://cmsxrootd.fnal.gov//store/mc/RunIII2024Summer24MiniAODv6/GluGluALPtoTauTau_Bin-HT-100to400_Par-M-10_TuneCP5_13p6TeV_madgraphMLM-pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v3/120000/979834f5-d140-4ad4-9bf0-4e92b18147ad.root',
    ])
elif runType == 'background':
    readFiles.extend([
        #'file:patMiniAOD_standard.root'
        #'/store/relval/CMSSW_10_5_0_pre1/RelValQCD_FlatPt_15_3000HS_13/MINIAODSIM/PU25ns_103X_mcRun2_asymptotic_v3-v1/20000/A5CBC261-E3AB-C842-896F-E6AFB38DD22F.root'
        #'file:/eos/uscms/store/user/rhabibul/HtoAA/HtoAAMiniAODTest/002C691B-A0CE-A24F-8805-03B4C52C9004.root'
        #'root://cmsxrootd.fnal.gov//store/mc/Run3Summer22MiniAODv4/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/MINIAODSIM/pilot_nanov15_130X_mcRun3_2022_realistic_v5-v2/2830000/ff237c4f-1c3e-4203-a725-5ed674c657c3.root'
        #'file:root://cmsxrootd.fnal.gov//store/mc/Run3Summer22MiniAODv4/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/MINIAODSIM/pilot_nanov15_130X_mcRun3_2022_realistic_v5-v2/2830000/ff237c4f-1c3e-4203-a725-5ed674c657c3.root',
        'file:root://cmsxrootd.hep.wisc.edu:1094//store/mc/RunIII2024Summer24MiniAODv6/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/MINIAODSIM/Pilot2024wmLHEGS_150X_mcRun3_2024_realistic_v2-v2/2820000/aeaa8a79-c6ca-4c04-8428-9e7d41662125.root'
    ])
elif runType == 'data':
    readFiles.extend([
        #'/store/data/Run2018D/SingleMuon/MINIAOD/12Nov2019_UL2018-v4/710000/B7163712-7B03-D949-91C9-EB5DD2E1D4C3.root' # SingleMuon PD
        #'/store/data/Run2018D/Tau/MINIAOD/12Nov2019_UL2018-v1/00000/01415E2B-7CE5-B94C-93BD-0796FC40BD97.root' # Tau PD
        #'file:root://storage01.lcg.cscs.ch//pnfs/lcg.cscs.ch/cms/trivcat/store/data/Run2022D/MuonEG/MINIAOD/27Jun2023-v2/2530000/0f3cef9d-da97-42a8-995c-9d85a744b6ef.root',
        #'file:root://cmsxrootd.fnal.gov//store/data/Run2022C/MuonEG/MINIAOD/27Jun2023-v1/2530000/265a542a-072a-47dc-ac27-3f34e63b70a7.root'

    ])
else:
    print('Unknown runType =',runType,'; Use \"signal\" or \"background\" or \"data\"')
    exit(1)


#####

if runType == 'signal':
    import BoostedDiTau.MiniAODSkimmer.adaptToRunAtMiniAODCustom as tauAtMiniToolsCustom
elif runType == 'background':
    import BoostedDiTau.MiniAODSkimmer.adaptToRunAtMiniAODCustom as tauAtMiniToolsCustom
elif runType == 'data':
    import BoostedDiTau.MiniAODSkimmer.adaptToRunAtMiniAODCustom_Data as tauAtMiniToolsCustom
else:
    print('Unknown runType =',runType,'; Use \"signal\" or \"background\" or \"data\"')
    exit(1)

#####
print ('Step : 1 - Added Paths for RecoCleaned ')

#tauAtMiniToolsCustom.addTauReRecoCustom(process)           #This has moved after loading GT


#####
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
if not phase2:
    print('Year :', year)
    if year == '2022':
        process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2022_realistic', '')
    elif year == '2022EE':
        process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2022_realistic_postEE', '')
    elif year == '2023':
        process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2023_realistic', '')
    elif year == '2023BPix':
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
process.selectedPatTaus.cut = cms.string('pt > 8.0 && abs(eta)<2.5 && tauID(\'decayModeFindingNewDMs\')> 0.5')
##########################################
#### Lower Tau Pt Boosted Taus###########

print ('Step : 5 - Lower Pt Boosted Taus')

jetPt=5
tauPt=8

getattr(process,'selectedPatTausBoosted').cut = cms.string("pt > {} && abs(eta) < 2.5 && tauID(\'decayModeFindingNewDMs\')> 0.5".format(tauPt))
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

getattr(process,'selectedPatTausElectronCleaned').cut = cms.string("pt > {} && abs(eta) < 2.5 && tauID(\'decayModeFindingNewDMs\')> 0.5".format(tauPt))
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

getattr(process,'selectedPatTausMuonCleaned').cut = cms.string("pt > {} && abs(eta) < 2.5 && tauID(\'decayModeFindingNewDMs\')> 0.5".format(tauPt))
process.ak4PFJetsLegacyHPSPiZerosMuonCleaned.minJetPt = jetPt
process.combinatoricRecoTausMuonCleaned.minJetPt = jetPt
process.recoTauAK4Jets08RegionPATMuonCleaned.minJetPt = jetPt
process.ak4PFJetsRecoTauChargedHadronsMuonCleaned.minJetPt = jetPt

#############################################
#### Lower Pt LowPtElectronCleaned Taus #####

print ('Step : 8 - Lower Pt LowPtElectronCleaned Taus')

getattr(process,'selectedPatTausLowPtElectronCleaned').cut = cms.string("pt > {} && abs(eta) < 2.5 && tauID(\'decayModeFindingNewDMs\')> 0.5".format(tauPt))
process.ak4PFJetsLegacyHPSPiZerosLowPtElectronCleaned.minJetPt = jetPt
process.combinatoricRecoTausLowPtElectronCleaned.minJetPt = jetPt
process.recoTauAK4Jets08RegionPATLowPtElectronCleaned.minJetPt = jetPt
process.ak4PFJetsRecoTauChargedHadronsLowPtElectronCleaned.minJetPt = jetPt

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

process.Timing = cms.Service("Timing",
    summaryOnly = cms.untracked.bool(True),
    useJobReport = cms.untracked.bool(True)
)

SimpleMemoryCheck = cms.Service("SimpleMemoryCheck",ignoreTotal = cms.untracked.int32(1) )
