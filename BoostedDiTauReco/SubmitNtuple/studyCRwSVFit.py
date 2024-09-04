import ROOT, sys, os
import numpy as np
import time
import correctionlib
from array import array
import BJetSF

start_time = time.time()

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]

# sfDir = os.path.join('/cvmfs','cms.cern.ch','rsync','cms-nanoAOD','jsonpog-integration','POG','BTV','2017_UL')
# btvjson = correctionlib.CorrectionSet.from_file(os.path.join(sfDir, 'btagging.json.gz'))

outputTitle = "h_studyCRwSVFit"

isData = 0

doDM = False

if "-b" in opts:
    isData = 0
    isMuonEGData = False
    isSingleMuonData = False
    isSingleElectronData = False
    isJetHTSample = False
    isSignal = False

if "-s" in opts:
    isData = 0
    isMuonEGData = False
    isSingleMuonData = False
    isSingleElectronData = False
    isJetHTSample = False
    isSignal = True

if "-dm" in opts:
    isData = 1
    isMuonEGData = False
    isSingleMuonData = True
    isSingleElectronData = False
    isJetHTSample = False
    isSignal = False

if "-dg" in opts:
    isData = 1
    isMuonEGData = True    
    isSingleMuonData = False
    isSingleElectronData = False
    isJetHTSample = False
    isSignal = False

if "-de" in opts:
    isData = 1
    isMuonEGData = False
    isSingleMuonData = False
    isSingleElectronData = True
    isJetHTSample = False
    isSignal = False


ROOT.gInterpreter.Declare('#include "../../MiniAODSkimmer/interface/JetInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../../MiniAODSkimmer/interface/MuonInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../../MiniAODSkimmer/interface/ElectronInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../../MiniAODSkimmer/interface/TauInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../../MiniAODSkimmer/interface/TrigObjectInfoDS.h"')
ROOT.gInterpreter.ProcessLine('#include "../../../TauAnalysis/ClassicSVfit/test/testClassicSVfit.h"')

inputFileListName=sys.argv[1]
inputFileList=inputFileListName

if len(sys.argv)>2 and not sys.argv[2].startswith("-"):
    outputFileDir=sys.argv[2]
else:
    outputFileDir = "./output/"

outputFileName = outputFileDir+outputTitle+"_"+inputFileListName.split("/")[-1].replace(".txt",".root")

out=ROOT.TFile.Open(outputFileName,'recreate')
print(outputFileName)

fchain = ROOT.TChain('tcpNtuples/analysisTree')
chain2 = ROOT.TChain('tcpTrigNtuples/triggerTree')
if isData == 0:
#    chain3 = ROOT.TChain('lumiSummary/lumiTree')
    chain4 = ROOT.TChain('tcpGenNtuples/genTree')
    chain5 = ROOT.TChain('tcpPrefiring/prefiringTree')
chain6 = ROOT.TChain('tcpMetfilter/metfilterTree')
chain7 = ROOT.TChain('testTrigObj/TriggerObjectTree')

pi = np.pi

h = {}

event_cut = {
    'jetpt': 100.0,
    'dRl': 0.4,
    'dRltau': 0.05,
    'dRlj': 0.8,
    'metcut': 100.0,
    'mtcut': 50.0,
    'dPhiml': 1.0,
    'dPhimj': 2.0,
    'mass' : 5.0
}


#define histograms here

def book_histogram():

    h['hEvents'] = ROOT.TH1F ("NEvents", "Number of Events; ;N", 2, 0, 2)
    h['hWeights'] = ROOT.TH1F ("hWeights", "Weights per events; weight; N", 100, 0, 2)
    h['hGenWeights'] = ROOT.TH1F ("hGenWeights", "Genweights per events; genweight; N", 100, 0, 2)
    h['hPuWeights'] = ROOT.TH1F ("hPuWeights", "PUweights per events; PUweight; N", 100, 0, 2)
    h['hPrWeights'] = ROOT.TH1F ("hPrWeights", "PreFiringWeights per events; PRweight; N", 100, 0, 2)

    # ---------- ETau ID ---------- #

    h['MuMu_TauECleanID'] = ROOT.TH1F ("MuMu_TauECleanID", "TauID MuMu; ;N", 2, 0, 2)
    h['EMu_TauECleanID'] = ROOT.TH1F ("EMu_TauECleanID", "TauID EMu; ;N", 2, 0, 2)
    h['MuTau_TauECleanID'] = ROOT.TH1F ("MuTau_TauECleanID", "TauID MuTau; ;N", 2, 0, 2)
    h['EE_TauECleanID'] = ROOT.TH1F ("EE_TauECleanID", "TauID EE; ;N", 2, 0, 2)

    # ---------- Objects ---------- #

    h['hJetPt'] = ROOT.TH1F ("hJetPt", "Jet P_{T} ; P_{T} ; N", 1500, 0, 1500)
    h['hDeepjet'] = ROOT.TH1F ("hDeepjet", "deepjet score ; score ; N", 100, 0, 1)
    h['hBJetPt'] = ROOT.TH1F ("hBJetPt", "BJet P_{T} ; P_{T} ; N", 1500, 0, 1500)

    h['hMuonPt'] = ROOT.TH1F ("hMuPt", "Muon P_{T} ; P_{T} ; N", 500, 0, 500)
    h['hIsoMuonPt'] = ROOT.TH1F ("hIsoMuPt", "Isolated Muon P_{T} ; P_{T} ; N", 500, 0, 500)
    h['hNonIsoMuonPt'] = ROOT.TH1F ("hNonIsoMuPt", "Non-Isolated Muon P_{T} ; P_{T} ; N", 500, 0, 500)

    h['hElectronPt'] = ROOT.TH1F ("hEPt", "Electron P_{T} ; P_{T} ; N", 500, 0, 500)
    h['hIsoElectronPt'] = ROOT.TH1F ("hIsoEPt", "Isolated Electron P_{T} ; P_{T} ; N", 500, 0, 500)
    h['hNonIsoElectronPt'] = ROOT.TH1F ("hNonIsoEPt", "Non-Isolated Electron P_{T} ; P_{T} ; N", 500, 0, 500)

    h['hTauECleanedPt'] = ROOT.TH1F ("hTauECleanedPt", "Electron-Cleaned Tau P_{T} ; P_{T} ; N", 500, 0, 500)
    h['hTauECleanedAlteredPt'] = ROOT.TH1F ("hTauECleanedAlteredPt", "Electron-Cleaned Tau Altered ID P_{T} ; P_{T} ; N", 500, 0, 500)

    h['hTauMuCleanedPt'] = ROOT.TH1F ("hTauMuCleanedPt", "Muon-Cleaned Tau P_{T} ; P_{T} ; N", 500, 0, 500)

    # ---------------

    h['MuMu_OS_lowMET_deepjet'] = ROOT.TH1F ("MuMu_OS_lowMET_deepjet" , "MuMu lowMET - deepjet score ; deepjet ; N", 100, 0, 1)
    h['MuTau_Nominal_OS_dRcut_highMET_lowMt_mSVFit'] = ROOT.TH1F ("MuTau_Nominal_OS_dRcut_highMET_lowMt_mSVFit", "MuTau Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['MuTau_Altered_OS_dRcut_highMET_lowMt_mSVFit'] = ROOT.TH1F ("MuTau_Altered_OS_dRcut_highMET_lowMt_mSVFit", "MuTau Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)

    h['ETau_Nominal_OS_dRcut_highMET_lowMt_mSVFit'] = ROOT.TH1F ("ETau_Nominal_OS_dRcut_highMET_lowMt_mSVFit", "ETau Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['ETau_Altered_OS_dRcut_highMET_lowMt_mSVFit'] = ROOT.TH1F ("ETau_Altered_OS_dRcut_highMET_lowMt_mSVFit", "ETau Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['ETau_VLoose_OS_dRcut_highMET_lowMt_mSVFit'] = ROOT.TH1F ("ETau_VLoose_OS_dRcut_highMET_lowMt_mSVFit", "ETau Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['ETau_Loose_OS_dRcut_highMET_lowMt_mSVFit'] = ROOT.TH1F ("ETau_Loose_OS_dRcut_highMET_lowMt_mSVFit", "ETau Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['ETau_noID_OS_dRcut_highMET_lowMt_mSVFit'] = ROOT.TH1F ("ETau_noID_OS_dRcut_highMET_lowMt_mSVFit", "ETau Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)

    h['ETau_Nominal_OS_dRcut_lowMET_lowMt_mSVFit'] = ROOT.TH1F ("ETau_Nominal_OS_dRcut_lowMET_lowMt_mSVFit", "ETau Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['ETau_Altered_OS_dRcut_lowMET_lowMt_mSVFit'] = ROOT.TH1F ("ETau_Altered_OS_dRcut_lowMET_lowMt_mSVFit", "ETau Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['ETau_VLoose_OS_dRcut_lowMET_lowMt_mSVFit'] = ROOT.TH1F ("ETau_VLoose_OS_dRcut_lowMET_lowMt_mSVFit", "ETau Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['ETau_Loose_OS_dRcut_lowMET_lowMt_mSVFit'] = ROOT.TH1F ("ETau_Loose_OS_dRcut_lowMET_lowMt_mSVFit", "ETau Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['ETau_noID_OS_dRcut_lowMET_lowMt_mSVFit'] = ROOT.TH1F ("ETau_noID_OS_dRcut_lowMET_lowMt_mSVFit", "ETau Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)


    h['ETau_Nominal_genMatched_OS_dRcut_highMET_lowMt_mSVFit'] = ROOT.TH1F ("ETau_Nominal_genMatched_OS_dRcut_highMET_lowMt_mSVFit", "ETau Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['ETau_Altered_genMatched_OS_dRcut_highMET_lowMt_mSVFit'] = ROOT.TH1F ("ETau_Altered_genMatched_OS_dRcut_highMET_lowMt_mSVFit", "ETau Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)

    h['MuTau_SB_2017_OS_Boost_Mass'] = ROOT.TH1F ('MuTau_SB_2017_OS_Boost_Mass', "MuTau Mass - SVFit (SB) ; Mass (GeV) ; N", 150, 0, 150)

    h['MuTau_SR_2017_OS_Boost_Mass'] = ROOT.TH1F ('MuTau_SR_2017_OS_Boost_Mass', "MuTau Mass - SVFit (SR) ; Mass (GeV) ; N", 150, 0, 150)
    h['EMu_SR_2017_OS_Boost_Mass'] = ROOT.TH1F ("EMu_SR_2017_Boost_Mass", "EMu Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['ETau_SR_2017_OS_Boost_Mass'] = ROOT.TH1F ("ETau_SR_2017_Boost_Mass", "EMu Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)

    h['MuTau_OS_dRcut_highMET_lowMt_ptSVFit'] = ROOT.TH1F ("MuTau_OS_dRcut_highMET_lowMt_ptSVFit", "MuTau Pt - SVFit ; Pt (GeV) ; N", 500, 0, 500)

    h['MuTau_OS_dRcut_highMET_lowMt_mGenLevel'] = ROOT.TH1F ("MuTau_OS_dRcut_highMET_lowMt_mGenLevel", "ditau mass - genLevel ; Mass ; N", 150, 0, 150)
    h['MuTau_OS_dRcut_highMET_lowMt_ptGenLevel'] = ROOT.TH1F ("MuTau_OS_dRcut_highMET_lowMt_ptGenLevel", "ditau pt - genLevel ; Pt ; N", 500, 0, 500)

    h['MuTau_OS_dRcut_highMET_lowMt_mReco'] = ROOT.TH1F ("MuTau_OS_dRcut_highMET_lowMt_mReco", "MuTau Mass - Reco ; Mass (GeV) ; N", 150, 0, 150)
    h['MuTau_OS_dRcut_highMET_lowMt_ptReco'] = ROOT.TH1F ("MuTau_OS_dRcut_highMET_lowMt_ptReco", "MuTau Pt - Reco ; Pt (GeV) ; N", 500, 0, 500)

    h['ETau_OS_dRcut_highMET_lowMt_mGenLevel'] = ROOT.TH1F ("ETau_OS_dRcut_highMET_lowMt_mGenLevel", "ditau mass - genLevel ; Mass ; N", 150, 0, 150)
    h['ETau_OS_dRcut_highMET_lowMt_ptGenLevel'] = ROOT.TH1F ("ETau_OS_dRcut_highMET_lowMt_ptGenLevel", "ditau pt - genLevel ; Pt ; N", 500, 0, 500)

    h['ETau_OS_dRcut_highMET_lowMt_mReco'] = ROOT.TH1F ("ETau_OS_dRcut_highMET_lowMt_mReco", "ETau Mass - Reco ; Mass (GeV) ; N", 150, 0, 150)
    h['ETau_OS_dRcut_highMET_lowMt_ptReco'] = ROOT.TH1F ("ETau_OS_dRcut_highMET_lowMt_ptReco", "ETau Pt - Reco ; Pt (GeV) ; N", 500, 0, 500)

    h['EMu_OS_dRcut_highMET_mReco'] = ROOT.TH1F ("EMu_OS_dRcut_highMET_mReco", "EMu Mass - Reco ; Mass (GeV) ; N", 150, 0, 150)
    h['EMu_OS_dRcut_highMET_mSVFit'] = ROOT.TH1F ("EMu_OS_dRcut_highMET_mSVFit", "EMu Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)

    h['EMu_OS_dRcut_lowMET_bjetveto_mSVFit'] = ROOT.TH1F ("EMu_OS_dRcut_lowMET_bjetveto_mSVFit", "EMu Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['EMu_OS_dRcut_lowMET_bjet_mSVFit'] = ROOT.TH1F ("EMu_OS_dRcut_lowMET_bjet_mSVFit", "EMu Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['EMu_OS_dRcut_highMET_bjetveto_mSVFit'] = ROOT.TH1F ("EMu_OS_dRcut_highMET_bjetveto_mSVFit", "EMu Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['EMu_OS_dRcut_highMET_bjet_mSVFit'] = ROOT.TH1F ("EMu_OS_dRcut_highMET_bjet_mSVFit", "EMu Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)

    h['EMu_OS_SB_lowMET_bjetveto_mSVFit'] = ROOT.TH1F ("EMu_OS_SB_lowMET_bjetveto_mSVFit", "EMu Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['EMu_OS_SB_lowMET_bjet_mSVFit'] = ROOT.TH1F ("EMu_OS_SB_lowMET_bjet_mSVFit", "EMu Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['EMu_OS_SB_highMET_bjetveto_mSVFit'] = ROOT.TH1F ("EMu_OS_SB_highMET_bjetveto_mSVFit", "EMu Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['EMu_OS_SB_highMET_bjet_mSVFit'] = ROOT.TH1F ("EMu_OS_SB_highMET_bjet_mSVFit", "EMu Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)

    h['EMu_OS_dRcut_lowMET_bjetveto_lowMtLeptons_mSVFit'] = ROOT.TH1F ("EMu_OS_dRcut_lowMET_bjetveto_lowMtLeptons_mSVFit", "EMu Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['EMu_OS_dRcut_lowMET_bjet_lowMtLeptons_mSVFit'] = ROOT.TH1F ("EMu_OS_dRcut_lowMET_bjet_lowMtLeptons_mSVFit", "EMu Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['EMu_OS_dRcut_highMET_bjetveto_lowMtLeptons_mSVFit'] = ROOT.TH1F ("EMu_OS_dRcut_highMET_bjetveto_lowMtLeptons_mSVFit", "EMu Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['EMu_OS_dRcut_highMET_bjet_lowMtLeptons_mSVFit'] = ROOT.TH1F ("EMu_OS_dRcut_highMET_bjet_lowMtLeptons_mSVFit", "EMu Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)

    h['EMu_OS_dRcut_highMET_mGenLevel'] = ROOT.TH1F ("EMu_OS_dRcut_highMET_mGenLevel", "ditau Mass - genLevel ; Mass (GeV) ; N", 150, 0, 150)
    h['EMu_OS_dRcut_highMET_ratioSVFit'] = ROOT.TH1F ("EMu_OS_dRcut_highMET_ratioSVFit", " SVFit ratio; m_{reco}-m_{gen}/m_{gen}; N",100,-2,2)

    h['TauTau_OS_dRcut_highMET_mSVFit'] = ROOT.TH1F ("TauTau_OS_dRcut_highMET_mSVFit", "TauTau Mass - SVFit ; Mass (GeV) ; N", 150, 0, 150)
    h['TauTau_OS_dRcut_highMET_ratioSVFit'] = ROOT.TH1F ("TauTau_OS_dRcut_highMET_ratioSVFit", " SVFit ratio; m_{reco}-m_{gen}/m_{gen}; N",100,-2,2)

    h['MuTau_Nominal_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("MuTau_Nominal_OS_dRcut_highMET_lowMt_mSVFitTauPt", "MuTau mSVFIt,JetPt ; mSVFit (GeV) ; JetPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['MuTau_Altered_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("MuTau_Altered_OS_dRcut_highMET_lowMt_mSVFitTauPt", "MuTau mSVFIt,JetPt ; mSVFit (GeV) ; JetPt (GeV)", 150, 0, 150, 500, 0, 500)

    h['ETau_Nominal_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("ETau_Nominal_OS_dRcut_highMET_lowMt_mSVFitTauPt", "ETau mSVFIt,JetPt ; mSVFit (GeV) ; JetPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_Altered_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("ETau_Altered_OS_dRcut_highMET_lowMt_mSVFitTauPt", "ETau mSVFIt,JetPt ; mSVFit (GeV) ; JetPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_Loose_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("ETau_Loose_OS_dRcut_highMET_lowMt_mSVFitTauPt", "ETau mSVFIt,JetPt ; mSVFit (GeV) ; JetPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_VLoose_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("ETau_VLoose_OS_dRcut_highMET_lowMt_mSVFitTauPt", "ETau mSVFIt,JetPt ; mSVFit (GeV) ; JetPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_noID_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("ETau_noID_OS_dRcut_highMET_lowMt_mSVFitTauPt", "ETau mSVFIt,JetPt ; mSVFit (GeV) ; JetPt (GeV)", 150, 0, 150, 500, 0, 500)

def book_event_histogram(region):

    h[region+"_Count"] = ROOT.TH1F (region+"_Count", region+"_Count ; Events ; Events ", 1, 0, 1)

    h[region+"_VisMass"] = ROOT.TH1F (region+"_VisMass", region+"_VisMass ; M_{vis.} (GeV) ; Events ", 150, 0, 150)
    h[region+"_Lepton1Pt"] = ROOT.TH1F (region+"_Lepton1Pt", region+"_Lepton1Pt ; P_{T} (GeV) ; Events ", 500, 0, 500)
    h[region+"_Lepton2Pt"] = ROOT.TH1F (region+"_Lepton2Pt", region+"_Lepton2Pt ; P_{T} (GeV) ; Events ", 500, 0, 500)
    h[region+"_JetPt"] = ROOT.TH1F (region+"_JetPt", region+"_JetPt ; JetP_{T} (GeV) ; Events ", 2000, 0, 2000)
    h[region+"_MetPt"] = ROOT.TH1F (region+"_MetPt", region+"_MetPt ; MET (GeV) ; Events ", 500, 0, 500)
    h[region+"_Mt"] = ROOT.TH1F (region+"_Mt", region+"_Mt ; M_{T} (GeV) ; Events ", 150, 0, 150)
    h[region+"_MtBothLeptons"] = ROOT.TH1F (region+"_MtBothLeptons", region+"_MtBothLeptons ; M_{T} (GeV) ; Events ", 150, 0, 150)
    h[region+"_Nj"] = ROOT.TH1F (region+"_Nj", region+"_Nj ; N_{j} ; Events ", 10, 0, 10)
    h[region+"_dRl"] = ROOT.TH1F (region+"_dRl", region+"_dRl ; dR(leptons) ; Events", 100, 0, 5)
    h[region+"_dRj"] = ROOT.TH1F (region+"_dRj", region+"_dRj ; dR(jet, ditau) ; Events", 100, 0, 5)
    h[region+"_dPhil"] = ROOT.TH2F (region+"_dPhil", region+"_dPhil ; dPhi(met,lepton1) ; dPhi(met,lepton2)",  100, -pi, pi, 100, -pi, pi)
    h[region+"_dPhi"] = ROOT.TH2F (region+"_dPhi", region+"_dPhi ; dPhi(met,ditau) ; dPhi(met,jet)",  100, -pi, pi, 100, -pi, pi)


def define_eff_histogram(region):

    h[region+"_BFlavour_JetPtEta"] = ROOT.TH2F (region+"_BFlavour_JetPtEta", region+"_BFlavour_JetPtEta ; P_{T} (GeV) ; Eta", 100, 0, 1000, 10, 0, 2.5)
    h[region+"_BFlavour_BTagged_JetPtEta"] = ROOT.TH2F (region+"_BFlavour_BTagged_JetPtEta", region+"_BFlavour_BTagged_JetPtEta ; P_{T} (GeV) ; Eta", 100, 0, 1000, 10, 0, 2.5)

    h[region+"_CFlavour_JetPtEta"] = ROOT.TH2F (region+"_CFlavour_JetPtEta", region+"_CFlavour_JetPtEta ; P_{T} (GeV) ; Eta", 100, 0, 1000, 10, 0, 2.5)
    h[region+"_CFlavour_BTagged_JetPtEta"] = ROOT.TH2F (region+"_CFlavour_BTagged_JetPtEta", region+"_CFlavour_BTagged_JetPtEta ; P_{T} (GeV) ; Eta", 100, 0, 1000, 10, 0, 2.5)

    h[region+"_LFlavour_JetPtEta"] = ROOT.TH2F (region+"_LFlavour_JetPtEta", region+"_LFlavour_JetPtEta ; P_{T} (GeV) ; Eta", 100, 0, 1000, 10, 0, 2.5)
    h[region+"_LFlavour_BTagged_JetPtEta"] = ROOT.TH2F (region+"_LFlavour_BTagged_JetPtEta", region+"_LFlavour_BTagged_JetPtEta ; P_{T} (GeV) ; Eta", 100, 0, 1000, 10, 0, 2.5)

    h[region+'_BFlavour_BTagging_Efficiency'] = ROOT.TH2F (region+"_BFlavour_BTagging_Efficiency", region+"_BFlavour_BTagging_Efficiency ; P_{T} (GeV) ; Eta", 100, 0, 1000, 10, 0, 2.5)
    h[region+'_CFlavour_BTagging_Efficiency'] = ROOT.TH2F (region+"_CFlavour_BTagging_Efficiency", region+"_CFlavour_BTagging_Efficiency ; P_{T} (GeV) ; Eta", 100, 0, 1000, 10, 0, 2.5)
    h[region+'_LFlavour_BTagging_Efficiency'] = ROOT.TH2F (region+"_LFlavour_BTagging_Efficiency", region+"_LFlavour_BTagging_Efficiency ; P_{T} (GeV) ; Eta", 100, 0, 1000, 10, 0, 2.5)


def get_TLorentzVector(obj):
    
    v = ROOT.TLorentzVector()
    v.SetPtEtaPhiM(obj.pt, obj.eta, obj.phi, obj.mass)

    return v


def pass_deltaR(l1, l2, j, channel):

    if channel == "MuTau" or channel == "ETau":
        if l1.DeltaR(l2) <= event_cut["dRl"] and j.DeltaR(l1) >= event_cut["dRlj"] and j.DeltaR(l2) >= event_cut["dRlj"] and l1.DeltaR(l2) >= event_cut["dRltau"]:
            return 1
        else:
            return -9999
    if channel == "MuMu" or channel == "EMu" or channel == "EE":
        if l1.DeltaR(l2) <= event_cut["dRl"] and j.DeltaR(l1) >= event_cut["dRlj"] and j.DeltaR(l2) >= event_cut["dRlj"]:
            return 1
        else:
            return -9999

def Mt(lepton, met):

    cos = np.cos(met.DeltaPhi(lepton))
    Mt = np.sqrt(2*lepton.Pt()*met.Pt()*(1-cos))

    return Mt

def plot_variable(region, l1, l2, j, m, sf=1):

    h[region+"_Count"].Fill(0, weight*sf)

    h[region+"_VisMass"].Fill((l1+l2).M(), weight*sf)
    h[region+"_Lepton1Pt"].Fill(l1.Pt(), weight*sf)
    h[region+"_Lepton2Pt"].Fill(l2.Pt(), weight*sf)
    h[region+"_JetPt"].Fill(j.Pt(), weight*sf)
    h[region+"_MetPt"].Fill(m.Pt(), weight*sf)
    h[region+"_Mt"].Fill(Mt(l1, m), weight*sf)
    h[region+"_MtBothLeptons"].Fill(Mt(l1+l2, m), weight*sf)
    h[region+"_Nj"].Fill(len(s_jet), weight*sf)
    h[region+"_dRl"].Fill(l1.DeltaR(l2), weight*sf)
    h[region+"_dRj"].Fill(j.DeltaR(l1+l2), weight*sf)
    # h[region+"_dPhil"].Fill(m.DeltaPhi(l1), m.DeltaPhi(l2), weight*sf)
    # h[region+"_dPhi"].Fill(m.DeltaPhi(l1+l2), m.DeltaPhi(j), weight*sf)


def mumu_channel():

    isMuMu = 0

    isSingleMuonEvent = False

    if s_isomuon[0].charge*s_isomuon[1].charge < 0 :

        mu1 = get_TLorentzVector(s_isomuon[0])
        mu2 = get_TLorentzVector(s_isomuon[1])
        jet = get_TLorentzVector(s_jet[0])

        # isMatchedMu = False
        # for ito in tOisMu:
        #     if isMatchedMu == True: break
        #     trigObject = get_TLorentzVector(ito)
        #     if trigObject.DeltaR(mu1) < 0.1 or trigObject.DeltaR(mu2) < 0.1 :
        #         isMatchedMu = True

        if mu1.Pt() > 52 and isMu == 1 : isSingleMuonEvent = True

        if ( isData == 0 or isSingleMuonData == True ) and isSingleMuonEvent == True :
            if met.Pt() < event_cut['metcut'] :                
                if mu1.DeltaR(mu2) < 0.4 and jet.DeltaR(mu1+mu2) > 0.8 :
                    plot_variable('MuMu_OS_lowMET_Boosted', mu1, mu2, jet, met)
                if mu1.DeltaR(mu2) > 0.4 and jet.DeltaR(mu1+mu2) > 0.8 :
                    plot_variable('MuMu_OS_lowMET_Resolved', mu1, mu2, jet, met)

                if jet.Pt() > 100.0 :
                    h['MuMu_OS_lowMET_deepjet'].Fill(s_jet[0].deepjet, weight)
                    plot_variable('MuMu_OS_lowMET', mu1, mu2, jet, met)

                    if mu1.DeltaR(mu2) < 0.4 and jet.DeltaR(mu1+mu2) > 0.8 :
                        plot_variable('MuMu_OS_lowMET_Jetcut_Boosted', mu1, mu2, jet, met)
                    if mu1.DeltaR(mu2) > 0.4 and jet.DeltaR(mu1+mu2) > 0.8 :
                        plot_variable('MuMu_OS_lowMET_Jetcut_Resolved', mu1, mu2, jet, met)
    
        if isSingleMuonEvent == 1:
            if pass_deltaR(mu1, mu2, jet, 'MuMu') == 1 :
                if met.Pt() > event_cut['metcut'] :

                    if len(s_tauEclean) > 0 and len(s_electron) > 0 :
                        if len(s_tauEcleanNom) > 0 :
                            h['MuMu_TauECleanID'].Fill(0.5, weight)
                        if len(s_tauEcleanAlt) > 0 :
                            h['MuMu_TauECleanID'].Fill(1.5, weight)

                    isMuMu = 1

    return isMuMu


def mutau_channel(s_tauMuclean, tauid="Nominal"):

    isMuTau = 0

    mu = get_TLorentzVector(s_muon[0])
    tau = get_TLorentzVector(s_tauMuclean[0])
    jet = get_TLorentzVector(s_jet[0])

    isMatchedMu = False
    for ito in tOisMu:
        if isMatchedMu == True: break
        trigObject = get_TLorentzVector(ito)
        if trigObject.DeltaR(mu) < 0.1 :
            isMatchedMu = True

    if ( isData == 0 or isSingleMuonData == True ) and ( isMatchedMu == True and mu.Pt() >= 52 ) :

        if s_muon[0].charge*s_tauMuclean[0].charge < 0:
            if met.Pt() >= 100 :
                plot_variable('MuTau_OS_highMET', mu, tau, jet , met)                                           
            if pass_deltaR(mu, tau, jet, 'MuTau') == 1 :
                plot_variable('MuTau_OS_dRcut', mu, tau, jet , met)
            if Mt(mu,met) <= 50.0 :
                plot_variable('MuTau_OS_lowMt', mu, tau, jet , met)


        if s_muon[0].charge*s_tauMuclean[0].charge > 0: #SS
            if pass_deltaR(mu, tau, jet, 'MuTau') == 1 : #dRcut
                if met.Pt() < event_cut['metcut'] : #lowMET
                    if Mt(mu,met) < event_cut['mtcut'] : # lowMt
                        plot_variable('MuTau_'+tauid+'_SS_dRcut_lowMET_lowMt', mu, tau, jet, met)
                    if Mt(mu,met) > event_cut['mtcut'] : # highMt
                        plot_variable('MuTau_'+tauid+'_SS_dRcut_lowMET_highMt', mu, tau, jet, met)
                if met.Pt() > event_cut['metcut'] : #highMET
                    if Mt(mu,met) < event_cut['mtcut'] : # lowMt
                        plot_variable('MuTau_'+tauid+'_SS_dRcut_highMET_lowMt', mu, tau, jet, met)
                    if Mt(mu,met) > event_cut['mtcut'] : # highMt  
                        plot_variable('MuTau_'+tauid+'_SS_dRcut_highMET_highMt', mu, tau, jet, met)

        if s_muon[0].charge*s_tauMuclean[0].charge < 0: #OS
            plot_variable('MuTau_'+tauid+'_OS', mu, tau, jet, met)
            if pass_deltaR(mu, tau, jet, 'MuTau') == 1 : #dRcut
                plot_variable('MuTau_'+tauid+'_OS_dRcut', mu, tau, jet, met)
                if met.Pt() < event_cut['metcut'] : #lowMET
                    if Mt(mu,met) < event_cut['mtcut'] : # lowMt
                        plot_variable('MuTau_'+tauid+'_OS_dRcut_lowMET_lowMt', mu, tau, jet, met)
                    if Mt(mu,met) > event_cut['mtcut'] : # highMt
                        plot_variable('MuTau_'+tauid+'_OS_dRcut_lowMET_highMt', mu, tau, jet, met)
                if met.Pt() >= event_cut['metcut'] : #highMET
                    plot_variable('MuTau_'+tauid+'_OS_dRcut_highMET', mu, tau, jet, met)
                    if Mt(mu,met) < event_cut['mtcut'] : # lowMt SR!!!

                        a=None                                                                                                         
                        a = ROOT.svFit(met_x, met_y, mu.Pt(), mu.Eta(), mu.Phi(), mu.M(), tau.Pt(), tau.Eta(), tau.Phi(),  tau.M(), s_tauMuclean[0].decaymode, s_tauMuclean[0].decaymode, 2, met_covXX, met_covXY, met_covYY , 4.0)                                                                         
                        mSVFit = a.runSVFitMass()

                        if mSVFit >= 12.0 :

                            if tauid == "Altered" and isData == 1 : 
                                plot_variable('MuTau_'+tauid+'_OS_dRcut_highMET_lowMt', mu, tau, jet, met)
                                h['MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_mSVFit'].Fill(mSVFit, weight)
                                h['MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)
                                plot_variable('MuTau_SB_2017_OS_Boost', mu, tau, jet, met)
                                h['MuTau_SB_2017_OS_Boost_Mass'].Fill(mSVFit, weight)

                            if isData == 0 :
                                plot_variable('MuTau_'+tauid+'_OS_dRcut_highMET_lowMt', mu, tau, jet, met)
                                h['MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_mSVFit'].Fill(mSVFit, weight)
                                h['MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)
                                if tauid == "Altered":
                                    plot_variable('MuTau_SB_2017_OS_Boost', mu, tau, jet, met)
                                    h['MuTau_SB_2017_OS_Boost_Mass'].Fill(mSVFit, weight)
                                if tauid == "Nominal":
                                    plot_variable('MuTau_SR_2017_OS_Boost', mu, tau, jet, met)
                                    h['MuTau_SR_2017_OS_Boost_Mass'].Fill(mSVFit, weight)

                    if Mt(mu,met) > event_cut['mtcut'] : # highMt  
                        plot_variable('MuTau_'+tauid+'_OS_dRcut_highMET_highMt', mu, tau, jet, met)


    if ( isMatchedMu == True and mu.Pt() >= 52 ) :
        if s_muon[0].charge*s_tauMuclean[0].charge < 0: #OS                                                                                          
            if pass_deltaR(mu, tau, jet, 'MuTau') == 1 : #dRcut                                                                                             
                if met.Pt() >= event_cut['metcut'] :       
                    if Mt(mu,met) < event_cut['mtcut'] :
                        isMuTau = 1

                        if len(s_tauEclean) > 0 and len(s_electron) > 0 :
                            if len(s_tauEcleanNom) > 0 :
                                h['MuTau_TauECleanID'].Fill(0.5, weight)
                            if len(s_tauEcleanAlt) > 0 :
                                h['MuTau_TauECleanID'].Fill(1.5, weight)

    return isMuTau

def ee_channel():

    isEE = 0

    if s_isoelectron[0].charge*s_isoelectron[1].charge < 0 :
        
        e1 = get_TLorentzVector(s_isoelectron[0])
        e2 = get_TLorentzVector(s_isoelectron[1])
        jet = get_TLorentzVector(s_jet[0])

        isJetHTEvent = 0
        isSingleElectronEvent = 0

        # if ( isData == 0 and ( isJetHTEvent == 1 or isSingleElectronEvent == 1 ) ) \
        #    or ( isData == 1 and isJetHTSample == 1 and isJetHTEvent == 1 ) \
        #    or ( isData == 1 and ( isSingleElectronData == 1 and isJetHTSample == 0 and isSingleElectronEvent == 1 ) ) :

        if ( jet.Pt() > 510 and ( isHT == 1  or isSingleJet500 == 1 ) ) : isJetHTEvent = 1
        if ( e1.Pt() > 37 and isIsoEle == 1 ) : isSingleElectronEvent = 1

        if isJetHTEvent == 1 :             
            if pass_deltaR(e1, e2, jet, 'EE') == 1 :
                if met.Pt() > event_cut['metcut'] :
                    isEE = 1
                    
                    if len(s_tauEclean) > 0 and len(s_electron) > 0 :
                        if len(s_tauEcleanNom) > 0 :
                            h['EE_TauECleanID'].Fill(0.5, weight)
                        if len(s_tauEcleanAlt) > 0 :
                            h['EE_TauECleanID'].Fill(1.5, weight)


    return isEE

def emu_channel():

    isEMu = 0

    if s_isoelectron[0].charge*s_isomuon[0].charge < 0 :

        e = get_TLorentzVector(s_isoelectron[0])
        mu = get_TLorentzVector(s_isomuon[0])
        jet = get_TLorentzVector(s_jet[0])

        isMatchedMu = False
        for ito in tOisMu:
            if isMatchedMu == True: break
            trigObject = get_TLorentzVector(ito)
            if trigObject.DeltaR(mu) < 0.1 : 
                isMatchedMu = True

        isMatchedMuonEGe = False
        for ito in tOisMuonEGe:
            if isMatchedMuonEGe == True: break
            trigObject = get_TLorentzVector(ito)
            if trigObject.DeltaR(e) < 0.1 : 
                isMatchedMuonEGe = True

        isMatchedMuonEGmu = False
        for ito in tOisMuonEGmu:
            if isMatchedMuonEGmu == True: break
            trigObject = get_TLorentzVector(ito)
            if trigObject.DeltaR(mu) < 0.1 : 
                isMatchedMuonEGmu = True

        isMatchedMuonEG = False
        if isMatchedMuonEGe == True and isMatchedMuonEGmu == True: 
            isMatchedMuonEG == True

        SingleMuonHLT = False
        MuonEGHLT = False
            
        if mu.Pt() >= 52.0 and isMatchedMu == True : SingleMuonHLT = True
        if ( ( mu.Pt() >= 10.0 and e.Pt() >= 25.0 ) or ( mu.Pt() >= 25.0 and e.Pt() >= 15.0 ) ) and isMatchedMuonEG == True : MuonEGHLT = True

        if ( isSingleMuonData == True and SingleMuonHLT == True ) or \
           ( isMuonEGData == True and MuonEGHLT == True and SingleMuonHLT == False ) or \
           ( isData == 0 and ( SingleMuonHLT == True or MuonEGHLT == True ) ) :

            #For N-1 cuts:

            if met.Pt() >= 100 :
                plot_variable('EMu_OS_highMET', e, mu, jet , met)                                           
            if pass_deltaR(e, mu, jet, 'EMu') == 1 :
                plot_variable('EMu_OS_dRcut', e, mu, jet , met)

            #For closure test

            if e.DeltaR(mu) < 0.6 and e.DeltaR(mu) > 0.4 and jet.DeltaR(e+mu) > 0.8 :
                a=None
                a = ROOT.svFit(met_x, met_y, e.Pt(), e.Eta(), e.Phi(), 0.000511, mu.Pt(), mu.Eta(), mu.Phi(),  mu.M(), 0, 0, 1, met_covXX, met_covXY, met_covYY ,3.0)
                mSVFit = a.runSVFitMass()

                if mSVFit >= 12.0 :

                    if met.Pt() < event_cut['metcut'] : #lowMET
                        if len(s_bjet) == 0 :
                            h['EMu_OS_SB_lowMET_bjetveto_mSVFit'].Fill(mSVFit, weight)
                        else:
                            if isData == 0 :
                                if isSignal == False:
                                    bweight = BJetSF.get_weight("lowMET", s_jet)
                                else:
                                    bweight = 1
                            else:
                                bweight = 1

                            h['EMu_OS_SB_lowMET_bjet_mSVFit'].Fill(mSVFit, weight)
                    else:
                        if len(s_bjet) == 0 :
                            h['EMu_OS_SB_highMET_bjetveto_mSVFit'].Fill(mSVFit, weight)
                        else:
                            if isData == 0 :
                                if isSignal == False:
                                    bweight = BJetSF.get_weight("highMET", s_jet)
                                else:
                                    bweight = 1
                            else:
                                bweight = 1

                            h['EMu_OS_SB_highMET_bjet_mSVFit'].Fill(mSVFit, weight)


            if pass_deltaR(e, mu, jet, 'EMu') == 1 :

                if met.Pt() < event_cut['metcut'] : #lowMET

                    a=None
                    a = ROOT.svFit(met_x, met_y, e.Pt(), e.Eta(), e.Phi(), 0.000511, mu.Pt(), mu.Eta(), mu.Phi(),  mu.M(), 0, 0, 1, met_covXX, met_covXY, met_covYY , 3.0)
                    mSVFit = a.runSVFitMass()
                
                    if mSVFit >= 12.0 :

                        if len(s_bjet) == 0 :

                            if isData == 0 :
                                if isSignal == False:
                                    bweight = BJetSF.get_weight("lowMET", s_jet)
                                    print("bweight", bweight)
                                else:
                                    bweight = 1
                            else:
                                bweight = 1

                            print("bweight, 0bjet", bweight)
                            print("jetpt", jet.Pt())

                            plot_variable('EMu_OS_dRcut_lowMET_bjetveto', e, mu, jet , met, bweight)
                            h['EMu_OS_dRcut_lowMET_bjetveto_mSVFit'].Fill(mSVFit, weight*bweight) 

                        else:

                            if isData == 0 :
                                if isSignal == False:
                                    bweight = BJetSF.get_weight("lowMET", s_jet)
                                    print("bweight", bweight)
                                else:
                                    bweight = 1
                            else:
                                bweight = 1

                            print("bweight, 1bjet", bweight)
                            print("jetpt", jet.Pt())
                
                            plot_variable('EMu_OS_dRcut_lowMET_bjet', e, mu, jet , met, bweight)
                            h['EMu_OS_dRcut_lowMET_bjet_mSVFit'].Fill(mSVFit, weight*bweight)

                            if Mt(e+mu, met) < 70 :
                                plot_variable('EMu_OS_dRcut_lowMET_bjet_lowMtLeptons', e, mu, jet , met, bweight)
                                h['EMu_OS_dRcut_lowMET_bjet_lowMtLeptons_mSVFit'].Fill(mSVFit, weight*bweight)

                else: #highMET

                    a=None
                    a = ROOT.svFit(met_x, met_y, e.Pt(), e.Eta(), e.Phi(), 0.000511, mu.Pt(), mu.Eta(), mu.Phi(),  mu.M(), 0, 0, 1, met_covXX, met_covXY, met_covYY , 3.0)
                    mSVFit = a.runSVFitMass()

                    if mSVFit >= 12.0 :

                        if len(s_bjet) == 0: 
                            if isData == 0:

                                if isSignal == False:
                                    bweight = BJetSF.get_weight("highMET", s_jet)
                                    print("bweight", bweight)
                                else:
                                    bweight = 1
                            else:
                                bweight = 1

                            print("bweight, 0bjet", bweight)
                            print("jetpt", jet.Pt())

                            plot_variable('EMu_OS_dRcut_highMET_bjetveto', e, mu, jet , met, bweight)
                            h['EMu_OS_dRcut_highMET_bjetveto_mSVFit'].Fill(mSVFit, weight*bweight)
                            h['EMu_SR_2017_OS_Boost_Mass'].Fill(mSVFit, weight*bweight)

                            isEMu = 1

                        else:

                            if isData == 0 :
                                if isSignal == False:
                                    bweight = BJetSF.get_weight("highMET", s_jet)
                                    print("bweight", bweight)
                                else:
                                    bweight = 1
                            else:
                                bweight = 1

                            print("bweight, 1bjet", bweight)
                            print("jetpt", jet.Pt())

                            plot_variable('EMu_OS_dRcut_highMET_bjet', e, mu, jet , met, bweight)
                            h['EMu_OS_dRcut_highMET_bjet_mSVFit'].Fill(mSVFit, weight*bweight)

    return isEMu


def fill_efficiency(region, js):

    for i in range(len(js)) :

        if js[i].jetflavour == 5 :
            h[region+'_BFlavour_JetPtEta'].Fill(js[i].pt, abs(js[i].eta))
            if js[i].deepjet >= 0.7476 :
                h[region+'_BFlavour_BTagged_JetPtEta'].Fill(js[i].pt, abs(js[i].eta))

        if js[i].jetflavour == 4 :
            h[region+'_CFlavour_JetPtEta'].Fill(js[i].pt, abs(js[i].eta))
            if js[i].deepjet >= 0.7476:
                h[region+'_CFlavour_BTagged_JetPtEta'].Fill(js[i].pt, abs(js[i].eta))

        if js[i].jetflavour == 0 :
            h[region+'_LFlavour_JetPtEta'].Fill(js[i].pt, abs(js[i].eta))
            if js[i].deepjet >= 0.7476:
                h[region+'_LFlavour_BTagged_JetPtEta'].Fill(js[i].pt, abs(js[i].eta))


def etau_channel(s_tauEclean, tauid="Nominal"):

    isETau = 0

    e = get_TLorentzVector(s_electron[0])
    tau = get_TLorentzVector(s_tauEclean[0])
    jet = get_TLorentzVector(s_jet[0])

    isMatchedEleJet = False
    isMatchedE = False
    isMatchedJet = False
    isMatchedPhoton = False

    for itrigobj in tOisPhoton:
        if isMatchedPhoton == True : break
        trigObject = get_TLorentzVector(itrigobj)
        if trigObject.DeltaR(e) < 0.1:
            isMatchedPhoton = True

    for itrigobj in tOisEleJet:
        if isMatchedE == True and isMatchedJet == True: break
        isEleLeg = False
        isJetLeg = False
        if itrigobj.isEleLeg == 1 : isEleLeg = True
        if itrigobj.isJetLeg == 1 : isJetLeg = True

        trigObject = get_TLorentzVector(itrigobj)

        if isEleLeg == True and isMatchedE == False:
            if trigObject.DeltaR(e) < 0.1 :
                isMatchedE = True

        if isJetLeg == True and isMatchedJet == False:
            if trigObject.DeltaR(jet) < 0.1 : 
                isMatchedJet = True

    if isMatchedE == True and isMatchedJet == True : 
        isMatchedEleJet = True

    isEleJetEvent = False
    if jet.Pt() >= 200.0 and e.Pt() >= 60.0 and isMatchedEleJet == True : isEleJetEvent = True
    isPhotonEvent = False
    if e.Pt() >= 230.0 and isMatchedPhoton == True: isPhotonEvent = True

    if ( isData == 0 or isSingleElectronData == True ) and ( isEleJetEvent == True or isPhotonEvent == True ):

        if s_electron[0].charge*s_tauEclean[0].charge < 0:
            if met.Pt() >= 100 :
                plot_variable('ETau_OS_highMET', e, tau, jet , met)                                           
            if pass_deltaR(e, tau, jet, 'ETau') == 1 :
                plot_variable('ETau_OS_dRcut', e, tau, jet , met)
            if Mt(e,met) <= 50.0 :
                plot_variable('ETau_OS_lowMt', e, tau, jet , met)


#        Closure  studies        
        if s_electron[0].charge*s_tauEclean[0].charge < 0: #OS
            plot_variable('ETau_'+tauid+'_OS', e, tau, jet , met)
        if s_electron[0].charge*s_tauEclean[0].charge > 0: #SS
            plot_variable('ETau_'+tauid+'_SS', e, tau, jet , met)
            if Mt(e,met) <= 50.0 :
                plot_variable('ETau_'+tauid+'_SS_lowMt', e, tau, jet , met)
            if met.Pt() >= 100.0 : # highMET                                                                                                              
                plot_variable('ETau_'+tauid+'_SS_highMET', e, tau, jet , met)
            if met.Pt() < 100.0 : # lowMET                                                                                                               
                plot_variable('ETau_'+tauid+'_SS_lowMET', e, tau, jet , met)
            if pass_deltaR(e, tau, jet, 'ETau') == 1 : #dRcut                                                                                             
                plot_variable('ETau_'+tauid+'_SS_dRcut', e, tau, jet , met)
                if Mt(e,met) <= 50.0 :
                    plot_variable('ETau_'+tauid+'_SS_dRcut_lowMt', e, tau, jet , met)
                if met.Pt() >= 100.0 : # highMET
                    plot_variable('ETau_'+tauid+'_SS_dRcut_highMET', e, tau, jet , met)
                if met.Pt() < 100.0 : # lowMET
                    plot_variable('ETau_'+tauid+'_SS_dRcut_lowMET', e, tau, jet , met)
        

        if s_electron[0].charge*s_tauEclean[0].charge > 0: #SS
            if pass_deltaR(e, tau, jet, 'ETau') == 1 : #dRcut
                if met.Pt() >= 100.0 : # highMET
                    if Mt(e,met) <= 50.0 : #lowMt
                        plot_variable('ETau_'+tauid+'_SS_dRcut_highMET_lowMt', e, tau, jet , met)
                    else: #highMt
                        plot_variable('ETau_'+tauid+'_SS_dRcut_highMET_highMt', e, tau, jet , met)
                else: #lowMET
                    if Mt(e,met) <= 50.0 : #lowMt                                                                                                            
                        plot_variable('ETau_'+tauid+'_SS_dRcut_lowMET_lowMt', e, tau, jet , met)
                    else: #highMt                                                                                                            
                        plot_variable('ETau_'+tauid+'_SS_dRcut_lowMET_highMt', e, tau, jet , met)
        else: #OS
            if pass_deltaR(e, tau, jet, 'ETau') == 1 : #dRcut
                plot_variable('ETau_'+tauid+'_OS_dRcut', e, tau, jet, met)
                if met.Pt() >= 100.0 : # highMET       
                    plot_variable('ETau_'+tauid+'_OS_dRcut_highMET', e, tau, jet, met)                                                          
                    if Mt(e,met) <= 50.0 : #lowMt SR!!!!

                        a=None
                        a = ROOT.svFit(met_x, met_y, e.Pt(), e.Eta(), e.Phi(), 0.000511, tau.Pt(), tau.Eta(), tau.Phi(), tau.M(), s_tauEclean[0].decaymode, s_tauEclean[0].decaymode, 3, met_covXX, met_covXY, met_covYY , 4.0)
                        mSVFit = a.runSVFitMass()

                        if mSVFit >= 12.0 :

                            if ( tauid == "Altered" or tauid == "VLoose" or tauid == "VVLoose" or tauid == "noID") and isData == 1 :
                                plot_variable('ETau_'+tauid+'_OS_dRcut_highMET_lowMt', e, tau, jet, met)
                                h['ETau_'+tauid+'_OS_dRcut_highMET_lowMt_mSVFit'].Fill(mSVFit, weight)
                                h['ETau_'+tauid+'_OS_dRcut_highMET_lowMt_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)
                            if isData == 0 :
                                plot_variable('ETau_'+tauid+'_OS_dRcut_highMET_lowMt', e, tau, jet, met)
                                h['ETau_'+tauid+'_OS_dRcut_highMET_lowMt_mSVFit'].Fill(mSVFit, weight)
                                h['ETau_'+tauid+'_OS_dRcut_highMET_lowMt_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)
                                if tauid == "Nominal":
                                    h['ETau_SR_2017_OS_Boost_Mass'].Fill(mSVFit, weight)
                            
                    else: #highMt                                                                                                            
                        plot_variable('ETau_'+tauid+'_OS_dRcut_highMET_highMt', e, tau, jet , met)
                else: #lowMET                                                                                         
                    if Mt(e,met) <= 50.0 : #lowMt                                                                                                            
                        plot_variable('ETau_'+tauid+'_OS_dRcut_lowMET_lowMt', e, tau, jet , met)

                        a=None
                        a = ROOT.svFit(met_x, met_y, e.Pt(), e.Eta(), e.Phi(), 0.000511, tau.Pt(), tau.Eta(), tau.Phi(), tau.M(), s_tauEclean[0].decaymode, s_tauEclean[0].decaymode, 3, met_covXX, met_covXY, met_covYY , 4.0)
                        mSVFit = a.runSVFitMass()

                        if mSVFit >= 12.0:
 
                            h['ETau_'+tauid+'_OS_dRcut_lowMET_lowMt_mSVFit'].Fill(mSVFit, weight)

                    else: #highMt                                                                                                                            
                        plot_variable('ETau_'+tauid+'_OS_dRcut_lowMET_highMt', e, tau, jet , met)


    return isETau
        

def tautau_channel():

    tau1 = get_TLorentzVector(s_tauBoosted[0])
    tau2 = get_TLorentzVector(s_tauBoosted[1])
    jet = get_TLorentzVector(s_jet[0])

    if jet.Pt() >= 500 and ( isSingleJet500 == 1 or isHT == 1 ) :
        
        if s_tauBoosted[0].charge*s_tauBoosted[1].charge < 0 :

            if tau1.DeltaR(tau2) <= 0.4 and jet.DeltaR(tau1+tau2) >= 0.8 :
                
                plot_variable('TauTau_Triggered_OS_dRcut_isJet', tau1, tau2, jet , met)

                if met.Pt() >= 100.0 :

                    plot_variable('TauTau_Triggered_OS_dRcut_highMET_isJet', tau1, tau2, jet , met)

                    a=None
                    a = ROOT.svFit(met_x, met_y, tau1.Pt(), tau1.Eta(), tau1.Phi(), tau1.M(), tau2.Pt(), tau2.Eta(), tau2.Phi(), tau2.M(), s_tauBoosted[0].decaymode, s_tauBoosted[1].decaymode, 4, met_covXX, met_covXY, met_covYY, 5)

                    mSVFit = a.runSVFitMass()

                    h['TauTau_OS_dRcut_highMET_mSVFit'].Fill(mSVFit, weight)


book_histogram()

tauids = ['Altered', 'Nominal', 'Loose', 'VLoose', 'noID'] 

regions = [
'MuTau_Nominal_SS_dRcut_lowMET_lowMt',
'MuTau_Nominal_SS_dRcut_lowMET_highMt',
'MuTau_Nominal_SS_dRcut_highMET_lowMt',
'MuTau_Nominal_SS_dRcut_highMET_highMt',
'MuTau_Nominal_OS',
'MuTau_Nominal_OS_dRcut',
'MuTau_Nominal_OS_dRcut_highMET',
'MuTau_Altered_OS_dRcut',
'MuTau_Altered_OS_dRcut_highMET',
'MuTau_Nominal_OS_dRcut_lowMET_lowMt',
'MuTau_Nominal_OS_dRcut_lowMET_highMt',
'MuTau_Nominal_OS_dRcut_highMET_lowMt',
'MuTau_Nominal_OS_dRcut_highMET_highMt',
'MuTau_Altered_SS_dRcut_lowMET_lowMt',
'MuTau_Altered_SS_dRcut_lowMET_highMt',
'MuTau_Altered_SS_dRcut_highMET_lowMt',
'MuTau_Altered_SS_dRcut_highMET_highMt',
'MuTau_Altered_OS_dRcut_lowMET_lowMt',
'MuTau_Altered_OS_dRcut_lowMET_highMt',
'MuTau_Altered_OS_dRcut_highMET_lowMt',
'MuTau_Altered_OS_dRcut_highMET_highMt',
'MuMu_TrigMatched_OS_lowMET_Boosted',
'MuMu_TrigMatched_OS_lowMET_Resolved',
'MuMu_OS_lowMET_Boosted',
'MuMu_OS_lowMET_Resolved',
'MuMu_OS_lowMET_Jetcut_Boosted',
'MuMu_OS_lowMET_Jetcut_Resolved',
'MuMu_OS_lowMET',
'EMu_TriggerMatch_OS_dRcut_highMET_isMuisMuonEG',
'EMu_OS_dRcut_lowMET_bjetveto',
'EMu_OS_dRcut_lowMET_bjet',
'EMu_OS_dRcut_highMET_bjetveto',
'EMu_OS_dRcut_highMET_bjet',
'EMu_OS_dRcut_lowMET_bjetveto_lowMtLeptons',
'EMu_OS_dRcut_lowMET_bjet_lowMtLeptons',
'EMu_OS_dRcut_highMET_bjetveto_lowMtLeptons',
'EMu_OS_dRcut_highMET_bjet_lowMtLeptons',
'MuTau_SB_2017_OS_Boost',
'MuTau_SR_2017_OS_Boost',
'ETau_Altered_genMatched_OS_dRcut_highMET_lowMt',
'ETau_Nominal_genMatched_OS_dRcut_highMET_lowMt',
'EMu_OS_highMET',
'EMu_OS_dRcut',
'ETau_OS_highMET',
'ETau_OS_dRcut',
'ETau_OS_lowMt',
'MuTau_OS_highMET',
'MuTau_OS_dRcut',
'MuTau_OS_lowMt',
]    

for t in tauids:
    regions.append('ETau_'+t+'_OS')
    regions.append('ETau_'+t+'_OS_dRcut')
    regions.append('ETau_'+t+'_OS_dRcut_highMET')
    regions.append('ETau_'+t+'_SS')
    regions.append('ETau_'+t+'_SS_dRcut')
    regions.append('ETau_'+t+'_SS_lowMt')
    regions.append('ETau_'+t+'_SS_lowMET')
    regions.append('ETau_'+t+'_SS_highMET')
    regions.append('ETau_'+t+'_SS_dRcut_lowMET')
    regions.append('ETau_'+t+'_SS_dRcut_highMET')
    regions.append('ETau_'+t+'_SS_dRcut_lowMt')
    regions.append('ETau_'+t+'_SS_dRcut_lowMET_lowMt')
    regions.append('ETau_'+t+'_SS_dRcut_lowMET_highMt')
    regions.append('ETau_'+t+'_SS_dRcut_highMET_lowMt')
    regions.append('ETau_'+t+'_SS_dRcut_highMET_highMt')
    regions.append('ETau_'+t+'_OS_dRcut_lowMET_lowMt')
    regions.append('ETau_'+t+'_OS_dRcut_lowMET_highMt')
    regions.append('ETau_'+t+'_OS_dRcut_highMET_lowMt')
    regions.append('ETau_'+t+'_OS_dRcut_highMET_highMt')

for r in regions:
    book_event_histogram(r)

for key in h.keys():
    h[key].Sumw2()

# define_eff_histogram('EMu_OS_dRcut_lowMET')
# define_eff_histogram('EMu_OS_dRcut_highMET')
# define_eff_histogram('ETau_OS_dRcut_lowMET_lowMt')
# define_eff_histogram('ETau_OS_dRcut_highMET_lowMt')

#-------- File loop --------#

inputFileNames=open(inputFileList, 'r')
for inputFileName in inputFileNames:
    inputFileName=inputFileName.replace("\n","")
    print(inputFileName.replace("\n",""))

    fchain.Add(inputFileName)
    chain2.Add(inputFileName)
    if isData == 0:
#        chain3.Add(inputFileName)
        chain4.Add(inputFileName)
        chain5.Add(inputFileName)

    chain6.Add(inputFileName)
    chain7.Add(inputFileName)

#------- Adding friends to the main chain -------#


fchain.AddFriend(chain2)
if isData == 0:
#    fchain.AddFriend(chain3)
    fchain.AddFriend(chain4)
    fchain.AddFriend(chain5)
    
fchain.AddFriend(chain6)
fchain.AddFriend(chain7)

jets = ROOT.JetInfoDS()
muons = ROOT.MuonInfoDS()
electrons = ROOT.ElectronInfoDS()
tausUnCleaned = ROOT.TauInfoDS()
tausECleaned = ROOT.TauInfoDS()
tausMCleaned = ROOT.TauInfoDS()
tausBoosted = ROOT.TauInfoDS()
trigObj = ROOT.TrigObjectInfoDS()

fchain.SetBranchAddress("Jets", ROOT.AddressOf(jets))
fchain.SetBranchAddress("Muons", ROOT.AddressOf(muons))
fchain.SetBranchAddress("Electrons", ROOT.AddressOf(electrons))
fchain.SetBranchAddress("TausUnCleaned", ROOT.AddressOf(tausUnCleaned))
fchain.SetBranchAddress("TausECleaned", ROOT.AddressOf(tausECleaned))
fchain.SetBranchAddress("TausMCleaned", ROOT.AddressOf(tausMCleaned))
fchain.SetBranchAddress("TausBoosted", ROOT.AddressOf(tausBoosted))
fchain.SetBranchAddress("TriggerObjects", ROOT.AddressOf(trigObj))

if isData == 0:
    genParticle = ROOT.GenParticleInfoDS()
    fchain.SetBranchAddress("GenParticleInfo", ROOT.AddressOf(genParticle))

#----------- Event loop ----------#


for iev in range(fchain.GetEntries()): # Be careful!!!                                                               

    fchain.GetEntry(iev)

    mets = fchain.GetBranch("Mets")
    met_pt = mets.GetLeaf('pt').GetValue()
    met_phi = mets.GetLeaf('phi').GetValue()
    
    # ------- For SV fit

    met_covXX = mets.GetLeaf('covXX').GetValue()
    met_covXY = mets.GetLeaf('covXY').GetValue()
    met_covYY = mets.GetLeaf('covYY').GetValue()

    met_x = met_pt*np.cos(met_phi)
    met_y = met_pt*np.sin(met_phi)

    # -------------------- 

    met = ROOT.TLorentzVector()
    met.SetPtEtaPhiM(met_pt, 0, met_phi, 0)

    if isData == 0 :
        genweight = fchain.GetLeaf('genWeight').GetValue()
        puweight = fchain.GetLeaf('puWeight').GetValue()
        prweight = fchain.GetLeaf('prefiringWeight').GetValue()
        tauidsf = 0.97
    else :
        genweight = 1
        puweight = 1
        prweight = 1
        tauidsf = 1

    weight = genweight*puweight*prweight*tauidsf

    h['hEvents'].Fill(0.5, 1)
    h['hEvents'].Fill(1.5, genweight)

    h['hWeights'].Fill(weight)
    h['hPuWeights'].Fill(puweight)
    h['hGenWeights'].Fill(genweight)
    h['hPrWeights'].Fill(prweight)

    #-------------- Gen particles -----------#

    gen_mu = []
    gen_tau = []
    gen_e = []
    gen_tanu = []
    gen_enu = []

    if isData == 0 :
        if genParticle.size() > 0 :
            for i in range(genParticle.size()):
                igen = genParticle.at(i)
                if igen.isdirecthardprocesstaudecayproductfinalstate :
                    if abs(igen.pdgid) == 13 : gen_mu+=[igen]
                    if abs(igen.pdgid) == 11 : gen_e+=[igen]
                    if abs(igen.pdgid) == 12 : gen_enu+=[igen]
                    if abs(igen.pdgid) == 16 : gen_tanu+=[igen]
                if igen.ishardprocess and abs(igen.pdgid) == 15: gen_tau+=[igen]

    #-------------- Trigger Objects ---------------#

    tOisEleJet = []
    tOisIsoMu = []
    tOisMu = []
    tOisSingleJet = []
    tOisMuonEGe = []
    tOisMuonEGmu = []
    tOisPhoton = []

    if trigObj.size() > 0:
        for i in range(trigObj.size()):
            iobj = trigObj.at(i)
            if iobj.isEleLeg == 1 : tOisEleJet+=[iobj]
            if iobj.isJetLeg == 1 : tOisEleJet+=[iobj]
            if iobj.isMu == 1 : tOisMu+=[iobj]
            if iobj.isIsoMu == 1 : tOisIsoMu +=[iobj]
            if iobj.isSingleJet == 1 : tOisSingleJet+=[iobj]
            if iobj.isMuonEGmu == 1 : tOisMuonEGmu+=[iobj]
            if iobj.isMuonEGe == 1 : tOisMuonEGe+=[iobj]
            if iobj.isPhoton == 1 : tOisPhoton+=[iobj]
                
    tOisEleJet.sort(key=lambda x: x.pt, reverse=True)
    tOisIsoMu.sort(key=lambda x: x.pt, reverse=True)    
    tOisMu.sort(key=lambda x: x.pt, reverse=True)

    #-------------- Trigger definitions -----------#

    isSingleJet500 = fchain.GetLeaf('isSingleJet500').GetValue()
    isHT = fchain.GetLeaf('isHT').GetValue()
    isHTMHT = fchain.GetLeaf('isHTMHT').GetValue()
    isMu = fchain.GetLeaf('isMu').GetValue()
    isIsoMu = fchain.GetLeaf('isIsoMu').GetValue()
    isIsoMuTau = fchain.GetLeaf('isIsoMuTau').GetValue()
    isIsoEle = fchain.GetLeaf('isIsoEle').GetValue()
    isEleTau = fchain.GetLeaf('isEleTau').GetValue()
    isMuonEG = fchain.GetLeaf('isMuonEG').GetValue()
    isEle = fchain.GetLeaf('isEle').GetValue()
    isPhoton200 = fchain.GetLeaf('isPhoton200').GetValue()
    isEleJet = fchain.GetLeaf('isEleJet').GetValue()
    isSingleJet500 = fchain.GetLeaf('isSingleJet500').GetValue()
    isSingleJet450 = fchain.GetLeaf('isSingleJet450').GetValue()

    #------------ MET Filter --------------#

    pvFilter = fchain.GetLeaf('primaryvertexfilter').GetValue()
    haloFilter = fchain.GetLeaf('beamhalofilter').GetValue()
    hbheFilter = fchain.GetLeaf('hbhefilter').GetValue()
    hbheIsoFilter = fchain.GetLeaf('hbheisofilter').GetValue()
    eeBadSCFilter = fchain.GetLeaf('eebadscfilter').GetValue()
    ecalTPFilter = fchain.GetLeaf('ecaltpfilter').GetValue()
    badMuonFilter = fchain.GetLeaf('badpfmuonfilter').GetValue()
    ecalBadCalFilter = fchain.GetLeaf('ecalbadcalfilter').GetValue()

    #------------ Objects loop ------------#

    s_jet = []
    s_bjet = []

    iht = 0

    if jets.size() > 0:
        for i in range(jets.size()):
            ijet = jets.at(i)
            if abs(ijet.eta) < 2.5 :
                if ijet.id >= 2:
                    # h['hJetPt'].Fill(ijet.pt, weight)
                    # h['hDeepjet'].Fill(ijet.deepjet, weight)
                    s_jet+=[ijet]
                    iht = iht + ijet.pt
                    if ijet.deepjet >= 0.7476:
                        # h['hBJetPt'].Fill(ijet.pt, weight) 
                        s_bjet+=[ijet]

    s_muon = []
    s_isomuon = []
    s_nonisomuon = []

    if muons.size() > 0:
        for i in range(muons.size()):
            imuon = muons.at(i)
            if abs(imuon.eta) < 2.4 :
                if imuon.id >= 2: #loose Muons
                    # h['hMuonPt'].Fill(imuon.pt, weight) 
                    s_muon+=[imuon]
                    if imuon.iso <= 0.25:
                        # h['hIsoMuonPt'].Fill(imuon.pt, weight)
                        s_isomuon+=[imuon]
                    if imuon.iso > 0.2:
                        # h['hNonIsoMuonPt'].Fill(imuon.pt, weight)
                        s_nonisomuon+=[imuon]

    s_electron = []
    s_isoelectron = []
    s_nonisoelectron = []

    if electrons.size() > 0:
        for i in range(electrons.size()):
            ielectron = electrons.at(i)
            if abs(ielectron.eta) < 2.5 :
                if ielectron.id >= 1 :
                    h['hElectronPt'].Fill(ielectron.pt, weight)
                    s_electron+=[ielectron]
                    if ielectron.iso >= 1:
                        h['hIsoElectronPt'].Fill(ielectron.pt, weight)
                        s_isoelectron+=[ielectron]
                    if ielectron.iso == 0:
                        h['hNonIsoElectronPt'].Fill(ielectron.pt, weight)
                        s_nonisoelectron+=[ielectron]

    s_tauEcleanNom = []
    s_tauEcleanAlt = []
    s_tauEcleanAltVLoose = []
    s_tauEcleanAltLoose = []
    s_tauEcleanAltnoID = []
    s_tauEclean = []

    if tausECleaned.size()>0:
        for i in range(tausECleaned.size()):
            itau = tausECleaned.at(i)
            if abs(itau.eta) < 2.3 and itau.pt >= 20.0:
                if itau.mvaid >=1 :
                    s_tauEclean+=[itau]
                if itau.mvaid >= 4:
                    h['hTauECleanedPt'].Fill(itau.pt, weight)
                    s_tauEcleanNom+=[itau]
                if itau.mvaid < 4 :
                    s_tauEcleanAltnoID+=[itau]
                    if itau.mvaid >= 1 : s_tauEcleanAlt+=[itau]
                    if itau.mvaid >= 2 : s_tauEcleanAltVLoose+=[itau]
                    if itau.mvaid >= 3 : s_tauEcleanAltLoose+=[itau]
                                            

    s_tauMucleanNom = []
    s_tauMucleanAlt = []

    if tausMCleaned.size()>0:
        for i in range(tausMCleaned.size()):
            itau = tausMCleaned.at(i)
            if abs(itau.eta) < 2.3 and itau.pt >= 20.0:
                if itau.mvaid >= 4 :
                    # h['hTauMuCleanedPt'].Fill(itau.pt, weight)
                    s_tauMucleanNom+=[itau]
                if itau.mvaid >= 1 and itau.mvaid < 4 :
                    s_tauMucleanAlt+=[itau]

    s_tauBoosted = []
    if tausBoosted.size()>0:
        for i in range(tausBoosted.size()):
            itau = tausBoosted.at(i)
            if abs(itau.eta) < 2.3:
                if itau.mvaid >= 2 :
                    s_tauBoosted+=[itau]

    # ---------- Event Selections --------- #

    if len(s_isomuon) >= 2 and len(s_jet) >= 1 and len(s_bjet) == 0: 
        if mumu_channel() == 1 : continue

    if len(s_isomuon) >= 1 and len(s_isoelectron) >= 1 and len(s_jet) >= 1 : 
        if emu_channel() == 1 : continue

    # if len(s_muon) >= 1 and len(s_jet) >= 1 and len(s_bjet) == 0 and len(s_tauMucleanAlt) >= 1: 
    #     mutau_channel(s_tauMucleanAlt, "Altered")

    if len(s_muon) >= 1 and len(s_jet) >= 1 and len(s_bjet) == 0 and len(s_tauMucleanNom) >= 1: 
        if mutau_channel(s_tauMucleanNom, "Nominal") == 1 : continue

    if len(s_isoelectron) >= 2 and len(s_jet) >= 1 and len(s_bjet) == 0 :
        if ee_channel() == 1 : continue

    # if len(s_electron) >= 1 and len(s_tauEcleanAlt) >= 1 and len(s_jet) >=1 and len(s_bjet) == 0 :
    #     etau_channel(s_tauEcleanAlt, "Altered")

    # if len(s_electron) >= 1 and len(s_tauEcleanAltVLoose) >= 1 and len(s_jet) >=1 and len(s_bjet) == 0 :
    #     etau_channel(s_tauEcleanAltVLoose, "VLoose")

    # if len(s_electron) >= 1 and len(s_tauEcleanAltLoose) >= 1 and len(s_jet) >=1 and len(s_bjet) == 0 :
    #     etau_channel(s_tauEcleanAltLoose, "Loose")

    # if len(s_electron) >= 1 and len(s_tauEcleanAltnoID) >= 1 and len(s_jet) >=1 and len(s_bjet) == 0 :
    #     etau_channel(s_tauEcleanAltnoID, "noID")

    if len(s_electron) >= 1 and len(s_tauEcleanNom) >= 1 and len(s_jet) >=1 and len(s_bjet) == 0 :
        etau_channel(s_tauEcleanNom, "Nominal")

    # if len(s_tauBoosted) >= 2 and len(s_jet) >= 1 and len(s_bjet) == 0 :
    #     tautau_channel()



out.cd()

for key in h.keys():
    # print(key)
    h[key].Write()

out.Close()

print("--- %s seconds ---" % (time.time() - start_time))

# result = np.array(regions)
# print(result)
# print(regions)
