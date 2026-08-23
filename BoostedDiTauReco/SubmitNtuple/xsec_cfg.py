import FWCore.ParameterSet.Config as cms
import sys
process = cms.Process("XSEC")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000000))
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring("FILENAME_PLACEHOLDER")
)
process.genxsec = cms.EDAnalyzer("GenXSecAnalyzer")
process.p = cms.Path(process.genxsec)
