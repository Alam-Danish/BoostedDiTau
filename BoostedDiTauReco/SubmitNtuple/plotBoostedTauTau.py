import ROOT, sys, os
import numpy as np
import time
import correctionlib
from array import array
import BJetSF
import argparse

start_time = time.time()

# opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]

# sfDir = os.path.join('/cvmfs','cms.cern.ch','rsync','cms-nanoAOD','jsonpog-integration','POG','BTV','2017_UL')
# btvjson = correctionlib.CorrectionSet.from_file(os.path.join(sfDir, 'btagging.json.gz'))

parser = argparse.ArgumentParser(description="Main plotting script for the boosted AToTauTau analysis")
parser.add_argument("-i", "--inputfile", type=str, required=True, help="Text file with list of ntuple root files")
parser.add_argument("-s", "--sample", type=str, required=True, help="Type of sample. Accepted: MC, SingleMuon, SingleElectron, MuonEG, TCP")
parser.add_argument("--folder", type=str, help="Output folder. Default is /output/")
parser.add_argument("--year", type=str, required=True, help="Year. Accepted: 2016preVFP, 2016postVFP, 2017, 2018")
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

year = args.year

outputTitle = "h_plotBoostedTauTau_"+year

EGsffile = ROOT.TFile("egammaEffi_EGM2D_UL"+year+".root")
EGsfhist = EGsffile.Get("EGamma_SF2D")
mu50SF = correctionlib.CorrectionSet.from_file("Efficiencies_NUM_Mu50_DEN_LooseID_abseta_pt_UL"+year+"_schemaV2.json")
try:
    etauTrigSF = ROOT.TFile("Baseline1_MmuMiso_EleEta_ElePt_SF_"+year+".root")
    etauTrigHist = etauTrigSF.Get("SF")
    etauTrigUncert = etauTrigSF.Get("Uncert")
except FileNotFoundError:
    etauTrigSF = None
    etauTrigHist = None
    etauTrigUncert = None
#etauTrigSF = ROOT.TFile("Baseline1_MmuMiso_EleEta_ElePt_SF_"+year+".root")
#etauTrigHist = etauTrigSF.Get("SF")
#etauTrigUncert = etauTrigSF.Get("Uncert")

isData = 0

if args.sample == "MC":
    isData = 0
    isMuonEGData = False
    isSingleMuonData = False
    isSingleElectronData = False
    isJetHTSample = False
    isSignal = False

elif args.sample == "TCP":
    isData = 0
    isMuonEGData = False
    isSingleMuonData = False
    isSingleElectronData = False
    isJetHTSample = False
    isSignal = True

elif args.sample == "SingleMuon":
    isData = 1
    isMuonEGData = False
    isSingleMuonData = True
    isSingleElectronData = False
    isJetHTSample = False
    isSignal = False

elif args.sample == "MuonEG":
    isData = 1
    isMuonEGData = True    
    isSingleMuonData = False
    isSingleElectronData = False
    isJetHTSample = False
    isSignal = False

elif args.sample == "SingleElectron":
    isData = 1
    isMuonEGData = False
    isSingleMuonData = False
    isSingleElectronData = True
    isJetHTSample = False
    isSignal = False
else:
    print("Please choose one of the accepted samples.")
    exit()

ROOT.gInterpreter.Declare('#include "../../MiniAODSkimmer/interface/JetInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../../MiniAODSkimmer/interface/MuonInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../../MiniAODSkimmer/interface/ElectronInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../../MiniAODSkimmer/interface/TauInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../../MiniAODSkimmer/interface/TrigObjectInfoDS.h"')
ROOT.gInterpreter.ProcessLine('#include "../../../TauAnalysis/ClassicSVfit/test/testClassicSVfit.h"')

inputFileListName=args.inputfile
inputFileList=inputFileListName

if args.folder is not None:
    outputFileDir=args.folder
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
    'vismass' : 5.0,
    'mass' : 12.0
}

#define histograms here

def book_histogram():

    h['hEvents'] = ROOT.TH1F ("NEvents", "Number of Events; ;N", 2, 0, 2)
    h['hWeights'] = ROOT.TH1F ("hWeights", "Weights per events; weight; N", 100, 0, 2)
    h['hGenWeights'] = ROOT.TH1F ("hGenWeights", "Genweights per events; genweight; N", 100, 0, 2)
    h['hPuWeights'] = ROOT.TH1F ("hPuWeights", "PUweights per events; PUweight; N", 100, 0, 2)
    h['hPrWeights'] = ROOT.TH1F ("hPrWeights", "PreFiringWeights per events; PRweight; N", 100, 0, 2)

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

    # --------------- 2D plots for FF -----------

    h['MuTau_Nominal_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("MuTau_Nominal_OS_dRcut_highMET_lowMt_mSVFitTauPt", "MuTau mSVFIt,tauPt ; mSVFit (GeV); tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['MuTau_Nominal_OS_dRcut_highMET_lowMt_DM0_mSVFitTauPt'] = ROOT.TH2F ("MuTau_Nominal_OS_dRcut_highMET_lowMt_DM0_mSVFitTauPt", "MuTau mSVFIt,tauPt (DM0) ; mSVFit (GeV); tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['MuTau_Nominal_OS_dRcut_highMET_lowMt_DM1_mSVFitTauPt'] = ROOT.TH2F ("MuTau_Nominal_OS_dRcut_highMET_lowMt_DM1_mSVFitTauPt", "MuTau mSVFIt,tauPt (DM1); mSVFit (GeV); tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['MuTau_Nominal_OS_dRcut_highMET_lowMt_DM10_mSVFitTauPt'] = ROOT.TH2F ("MuTau_Nominal_OS_dRcut_highMET_lowMt_DM10_mSVFitTauPt", "MuTau mSVFIt,tauPt (DM10); mSVFit (GeV); tauPt (GeV)", 150, 0, 150, 500, 0, 500)

    h['MuTau_Altered_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("MuTau_Altered_OS_dRcut_highMET_lowMt_mSVFitTauPt", "MuTau mSVFIt,tauPt ; mSVFit (GeV); tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['MuTau_Altered_OS_dRcut_highMET_lowMt_DM0_mSVFitTauPt'] = ROOT.TH2F ("MuTau_Altered_OS_dRcut_highMET_lowMt_DM0_mSVFitTauPt", "MuTau mSVFIt,tauPt (DM0) ; mSVFit (GeV); tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['MuTau_Altered_OS_dRcut_highMET_lowMt_DM1_mSVFitTauPt'] = ROOT.TH2F ("MuTau_Altered_OS_dRcut_highMET_lowMt_DM1_mSVFitTauPt", "MuTau mSVFIt,tauPt (DM1); mSVFit (GeV); tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['MuTau_Altered_OS_dRcut_highMET_lowMt_DM10_mSVFitTauPt'] = ROOT.TH2F ("MuTau_Altered_OS_dRcut_highMET_lowMt_DM10_mSVFitTauPt", "MuTau mSVFIt,tauPt (DM10); mSVFit (GeV); tauPt (GeV)", 150, 0, 150, 500, 0, 500)

    h['ETau_Nominal_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("ETau_Nominal_OS_dRcut_highMET_lowMt_mSVFitTauPt", "ETau mSVFIt,tauPt ; mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_Nominal_OS_dRcut_highMET_lowMt_DM0_mSVFitTauPt'] = ROOT.TH2F ("ETau_Nominal_OS_dRcut_highMET_lowMt_DM0_mSVFitTauPt", "ETau mSVFIt,tauPt (DM0); mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_Nominal_OS_dRcut_highMET_lowMt_DM1_mSVFitTauPt'] = ROOT.TH2F ("ETau_Nominal_OS_dRcut_highMET_lowMt_DM1_mSVFitTauPt", "ETau mSVFIt,tauPt (DM1); mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_Nominal_OS_dRcut_highMET_lowMt_DM10_mSVFitTauPt'] = ROOT.TH2F ("ETau_Nominal_OS_dRcut_highMET_lowMt_DM10_mSVFitTauPt", "ETau mSVFIt,tauPt (DM10); mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)

    h['ETau_ttEnriched_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("ETau_ttEnriched_OS_dRcut_highMET_lowMt_mSVFitTauPt", "ETau mSVFIt,tauPt ; mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_ttEnriched_OS_dRcut_highMET_lowMt_DM0_mSVFitTauPt'] = ROOT.TH2F ("ETau_ttEnriched_OS_dRcut_highMET_lowMt_DM0_mSVFitTauPt", "ETau mSVFIt,tauPt (DM0); mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_ttEnriched_OS_dRcut_highMET_lowMt_DM1_mSVFitTauPt'] = ROOT.TH2F ("ETau_ttEnriched_OS_dRcut_highMET_lowMt_DM1_mSVFitTauPt", "ETau mSVFIt,tauPt (DM1); mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_ttEnriched_OS_dRcut_highMET_lowMt_DM10_mSVFitTauPt'] = ROOT.TH2F ("ETau_ttEnriched_OS_dRcut_highMET_lowMt_DM10_mSVFitTauPt", "ETau mSVFIt,tauPt (DM10); mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)

    h['ETau_Altered_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("ETau_Altered_OS_dRcut_highMET_lowMt_mSVFitTauPt", "ETau mSVFIt,tauPt ; mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_Altered_OS_dRcut_highMET_lowMt_DM0_mSVFitTauPt'] = ROOT.TH2F ("ETau_Altered_OS_dRcut_highMET_lowMt_DM0_mSVFitTauPt", "ETau mSVFIt,tauPt (DM0) ; mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_Altered_OS_dRcut_highMET_lowMt_DM1_mSVFitTauPt'] = ROOT.TH2F ("ETau_Altered_OS_dRcut_highMET_lowMt_DM1_mSVFitTauPt", "ETau mSVFIt,tauPt (DM1); mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_Altered_OS_dRcut_highMET_lowMt_DM10_mSVFitTauPt'] = ROOT.TH2F ("ETau_Altered_OS_dRcut_highMET_lowMt_DM10_mSVFitTauPt", "ETau mSVFIt,tauPt (DM10); mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)

    h['ETau_Loose_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("ETau_Loose_OS_dRcut_highMET_lowMt_mSVFitTauPt", "ETau mSVFIt,tauPt ; mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_VLoose_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("ETau_VLoose_OS_dRcut_highMET_lowMt_mSVFitTauPt", "ETau mSVFIt,tauPt ; mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_noID_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("ETau_noID_OS_dRcut_highMET_lowMt_mSVFitTauPt", "ETau mSVFIt,tauPt ; mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)

    h['MuTau_Nbjet_T'] = ROOT.TH1F ("MuTau_Nbjet_T", "MuTau_Nbjet_T : N_{bjet} : Events", 10, 0, 10)
    h['MuTau_Nbjet_M'] = ROOT.TH1F ("MuTau_Nbjet_M", "MuTau_Nbjet_M : N_{bjet} : Events", 10, 0, 10)
    h['MuTau_Nbjet_L'] = ROOT.TH1F ("MuTau_Nbjet_L", "MuTau_Nbjet_L : N_{bjet} : Events", 10, 0, 10)

    h['ETau_Nbjet_T'] = ROOT.TH1F ("ETau_Nbjet_T", "ETau_Nbjet_T : N_{bjet} : Events", 10, 0, 10)
    h['ETau_Nbjet_M'] = ROOT.TH1F ("ETau_Nbjet_M", "ETau_Nbjet_M : N_{bjet} : Events", 10, 0, 10)
    h['ETau_Nbjet_L'] = ROOT.TH1F ("ETau_Nbjet_L", "ETau_Nbjet_L : N_{bjet} : Events", 10, 0, 10)

    h['EMu_Nbjet_T'] = ROOT.TH1F ("EMu_Nbjet_T", "EMu_Nbjet_T : N_{bjet} : Events", 10, 0, 10)
    h['EMu_Nbjet_M'] = ROOT.TH1F ("EMu_Nbjet_M", "EMu_Nbjet_M : N_{bjet} : Events", 10, 0, 10)
    h['EMu_Nbjet_L'] = ROOT.TH1F ("EMu_Nbjet_L", "EMu_Nbjet_L : N_{bjet} : Events", 10, 0, 10)

    
def book_event_histogram(region):

    h[region+"_Count"] = ROOT.TH1F (region+"_Count", region+"_Count ; Events ; Events ", 1, 0, 1)

    h[region+"_VisMass"] = ROOT.TH1F (region+"_VisMass", region+"_VisMass ; M_{vis.} (GeV) ; Events ", 150, 0, 150)
    h[region+"_Lepton1Pt"] = ROOT.TH1F (region+"_Lepton1Pt", region+"_Lepton1Pt ; P_{T} (GeV) ; Events ", 500, 0, 500)
    h[region+"_Lepton2Pt"] = ROOT.TH1F (region+"_Lepton2Pt", region+"_Lepton2Pt ; P_{T} (GeV) ; Events ", 500, 0, 500)
    h[region+"_LeadingJetPt"] = ROOT.TH1F (region+"_LeadingJetPt", region+"_LeadingJetPt ; LedingJetP_{T} (GeV) ; Events ", 2000, 0, 2000)
    h[region+"_MetPt"] = ROOT.TH1F (region+"_MetPt", region+"_MetPt ; MET (GeV) ; Events ", 500, 0, 500)
    h[region+"_Mt"] = ROOT.TH1F (region+"_Mt", region+"_Mt ; M_{T} (GeV) ; Events ", 150, 0, 150)
    h[region+"_Nj"] = ROOT.TH1F (region+"_Nj", region+"_Nj ; N_{j} ; Events ", 10, 0, 10)
    h[region+"_Nbj"] = ROOT.TH1F (region+"_Nbj", region+"_Nbj ; N_{bjet} ; Events ", 10, 0, 10)
    h[region+"_dRl"] = ROOT.TH1F (region+"_dRl", region+"_dRl ; dR(leptons) ; Events", 100, 0, 5)
    h[region+"_dRj"] = ROOT.TH1F (region+"_dRj", region+"_dRj ; dR(jet, ditau) ; Events", 100, 0, 5)
    h[region+"_Lepton1EtaPhi"] = ROOT.TH2F (region+"_Lepton1EtaPhi", region+"_Lepton1EtaPhi ; Eta ; Phi", 100, -3.0, 3.0, 100, -pi, pi)
    h[region+"_Lepton1Eta"] = ROOT.TH1F (region+"_Lepton1Eta", region+"_Lepton1Eta ; Eta ; Events", 100, -3.0, 3.0)
    h[region+"_Lepton1Phi"] = ROOT.TH1F (region+"_Lepton1Phi", region+"_Lepton1Phi ; Phi ; Events", 100, -pi, pi)
    h[region+"_Lepton2Eta"] = ROOT.TH1F (region+"_Lepton2Eta", region+"_Lepton2Eta ; Eta ; Events", 100, -3.0, 3.0)
    h[region+"_Lepton2Phi"] = ROOT.TH1F (region+"_Lepton2Phi", region+"_Lepton2Phi ; Phi ; Events", 100, -pi, pi)
    h[region+"_JetEtaPhi"] = ROOT.TH2F (region+"_JetEtaPhi", region+"_JetEtaPhi ; Eta ; Phi", 100, -3.0, 3.0, 100, -pi, pi)
    h[region+"_JetEta"] = ROOT.TH1F (region+"_JetEta", region+"_JetEta ; LeadingJet Eta ; Events", 100, -3.0, 3.0)
    h[region+"_JetPhi"] = ROOT.TH1F (region+"_JetPhi", region+"_JetPhi ; LeadingJet Phi ; Events", 100, -pi, pi)


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


def get_EGsf(eta, pt):

    binPt = EGsfhist.GetYaxis().FindBin(pt)
    binEta = EGsfhist.GetXaxis().FindBin(eta)
    egsf = EGsfhist.GetBinContent(binEta, binPt)
    uncert = EGsfhist.GetBinError(binEta, binPt)
    egsf_up = egsf+uncert
    egdf_down = egsf-uncert

    return egsf, egsf_up, egdf_down


def get_etauTrigsf(eta, pt):

    binPt = etauTrigHist.GetYaxis().FindBin(pt)
    binEta = etauTrigHist.GetXaxis().FindBin(eta)
    trigSF = etauTrigHist.GetBinContent(binEta, binPt)
    uncert = etauTrigUncert.GetBinContent(binEta, binPt)
    trigSF_up = trigSF+uncert
    trigSF_down = trigSF-uncert

    return trigSF, trigSF_up, trigSF_down
    

def plot_variable(region, l1, l2, j, m, sf=1):

    if region not in region_list:
        book_event_histogram(region)
        region_list.append(region)

    h[region+"_Count"].Fill(0, weight*sf)

    h[region+"_VisMass"].Fill((l1+l2).M(), weight*sf)
    h[region+"_Lepton1Pt"].Fill(l1.Pt(), weight*sf)
    h[region+"_Lepton2Pt"].Fill(l2.Pt(), weight*sf)
    h[region+"_LeadingJetPt"].Fill(j.Pt(), weight*sf)
    h[region+"_MetPt"].Fill(m.Pt(), weight*sf)
    h[region+"_Mt"].Fill(Mt(l1, m), weight*sf)
    h[region+"_Nj"].Fill(len(s_jet), weight*sf)
    h[region+"_Nbj"].Fill(len(s_bjet), weight*sf)
    h[region+"_dRl"].Fill(l1.DeltaR(l2), weight*sf)
    h[region+"_dRj"].Fill(j.DeltaR(l1+l2), weight*sf)
    h[region+"_Lepton1Eta"].Fill(l1.Eta(), weight*sf)
    h[region+"_Lepton1Phi"].Fill(l1.Phi(), weight*sf)
    h[region+"_Lepton2Eta"].Fill(l2.Eta(), weight*sf)
    h[region+"_Lepton2Phi"].Fill(l2.Phi(), weight*sf)
    h[region+"_JetEta"].Fill(j.Eta(), weight*sf)
    h[region+"_JetPhi"].Fill(j.Phi(), weight*sf)
    h[region+"_Lepton1EtaPhi"].Fill(l1.Eta(), l1.Phi(), weight*sf)
    h[region+"_JetEtaPhi"].Fill(j.Eta(), j.Phi(), weight*sf)


def select_Nm1(l1, l2, ljet, ms, l2dm, channel):

    plot_variable(channel+'_OS', l1, l2, ljet, ms)

    if channel == 'EMu' or channel == 'MuMu' or channel == 'EE':

        if ms.Pt() >= 100 :
            if ljet.Pt() > event_cut['jetpt'] :
                if pass_deltaR(l1, l2, ljet, channel) == 1 :
                    mSVFit = get_svfit(l1, l2, 0, channel)
                    if mSVFit >= event_cut['mass'] :
                        plot_variable(channel+'_NmBjetcut', l1, l2, ljet , ms) #Nmbjetveto

        if len(s_bjet) == 0:
            if ms.Pt() >= 100 :
                mSVFit = get_svfit(l1, l2, 0, channel)
                if mSVFit >= event_cut['mass'] :
                    if pass_deltaR(l1, l2, ljet, channel) == 1 :
                        plot_variable(channel+'_NmJetcut', l1, l2, ljet , ms) #Nmjet
                    if ljet.Pt() > event_cut['jetpt'] :
                        plot_variable(channel+'_NmdRcut', l1, l2, ljet , ms) #NmDRcut
                        if l1.DeltaR(l2) <= event_cut["dRl"] :
                            plot_variable(channel+'_NmdRjcut', l1, l2, ljet , ms) #NmDRjcut
                        if ljet.DeltaR(l1+l2) >= event_cut["dRlj"]  :
                            plot_variable(channel+'_NmdRlcut', l1, l2, ljet , ms) #NmDRlcut
            if pass_deltaR(l1, l2, ljet, channel) == 1 :
                mSVFit = get_svfit(l1, l2, 0, channel)
                if mSVFit >= event_cut['mass'] :
                    if ljet.Pt() > event_cut['jetpt'] : 
                        plot_variable(channel+'_NmMETcut', l1, l2, ljet , ms) #NmMET

    else:

        if ms.Pt() >= 100 :
            if pass_deltaR(l1, l2, ljet, channel) == 1 :
                if ljet.Pt() > event_cut['jetpt'] :
                    if Mt(l1,ms) <= 50.0 :
                        mSVFit = get_svfit(l1, l2, l2dm, channel)
                        if mSVFit >= event_cut['mass'] :
                            plot_variable(channel+'_NmBjetcut', l1, l2, ljet , ms) #Nmbjetveto

        if len(s_bjet) == 0:
            if ms.Pt() >= 100 :
                if pass_deltaR(l1, l2, ljet, channel) == 1 :
                    mSVFit = get_svfit(l1, l2, l2dm, channel)
                    if mSVFit >= event_cut['mass'] :
                        if Mt(l1,ms) <= 50.0 :
                            plot_variable(channel+'_NmJetcut', l1, l2, ljet , ms) #Nmjetcut
                        if ljet.Pt() > event_cut['jetpt'] :
                            plot_variable(channel+'_NmMtcut', l1, l2, ljet , ms) #NmMt
            if Mt(l1,ms) <= 50.0 :
                if pass_deltaR(l1, l2, ljet, channel) == 1 :
                    mSVFit = get_svfit(l1, l2, l2dm, channel)
                    if mSVFit >= event_cut['mass'] :
                        if ljet.Pt() > event_cut['jetpt'] :
                            plot_variable(channel+'_NmMETcut', l1, l2, ljet , ms) #NmMET
                if ms.Pt() >= 100 :
                    mSVFit = get_svfit(l1, l2, l2dm, channel)
                    if mSVFit >= event_cut['mass'] :
                        if ljet.Pt() > event_cut['jetpt'] :
                            plot_variable(channel+'_NmdRcut', l1, l2, ljet , ms) #NmDRcut
                            if l1.DeltaR(l2) >= event_cut["dRltau"]:
                                if l1.DeltaR(l2) <= event_cut["dRl"]:
                                    plot_variable(channel+'_NmdRjcut', l1, l2, ljet , ms) #NmDRlcut
                                if ljet.DeltaR(l1+l2) >= event_cut["dRlj"]:
                                    plot_variable(channel+'_NmdRlcut', l1, l2, ljet , ms) #NmDRjcut



def baseline_selection(l1, l2, ljet, ms, channel):

    if ljet.Pt() < 100.0 : return -9999
    if pass_deltaR(l1, l2, ljet, channel) != 1 : return -9999
    if ms.Pt() < 100.0: return -9999

    return 1


def get_svfit(l1, l2, dm, channel):

    svfitParam = {
        'EMu':{
            'decaymode' : 0,
            'massl1' : 0.51100e-3,
            'channel' : 1,
            'kappa' : 3.0
        },
        'MuTau': {
            'decaymode' : dm,
            'massl1' : 105.658e-3,
            'channel': 2,
            'kappa' : 4.0
        },
        'ETau': {
            'decaymode' : dm,
            'massl1' :  0.51100e-3,
            'channel' : 3,
            'kappa' : 4.0
        }
    }

    a=None
    
    a = ROOT.svFit(met_x, met_y, l1.Pt(), l1.Eta(), l1.Phi(), svfitParam[channel]['massl1'], l2.Pt(), l2.Eta(), l2.Phi(), l2.M(), 0, svfitParam[channel]['decaymode'], svfitParam[channel]['channel'], met_covXX, met_covXY, met_covYY, svfitParam[channel]['kappa'])

    msvfit = a.runSVFitMass()

    return msvfit


def plot_svfit(region, msvfit, sf=1):

    if region not in svfit_plot:
        h[region+"_Mass"] = ROOT.TH1F (region+"_Mass", region+"_Mass ; M_{#tau#tau} (GeV) ; Events ", 150, 0, 150)
        svfit_plot.append(region)

    h[region+"_Mass"].Fill(msvfit, weight*sf)



def mumu_channel():

    isMuMu = 0

    isSingleMuonEvent = False

    if s_isomuon[0].charge*s_isomuon[1].charge < 0 :

        mu1 = get_TLorentzVector(s_isomuon[0])
        mu2 = get_TLorentzVector(s_isomuon[1])
        jet = get_TLorentzVector(s_jet[0])

        isMatchedMu = False
        for ito in tOisMu:
            if isMatchedMu == True: break
            trigObject = get_TLorentzVector(ito)
            if trigObject.DeltaR(mu1) < 0.1 or trigObject.DeltaR(mu2) < 0.1 :
                isMatchedMu = True

        if mu1.Pt() > 52 and isMatchedMu == True : isSingleMuonEvent = True

        if ( isData == 0 or isSingleMuonData == True ) and isSingleMuonEvent == True :

            if pass_deltaR(mu1, mu2, jet, 'MuMu') == 1 :
                if met.Pt() < event_cut['metcut']:
                    if jet.Pt() >= 100.0 :
                        plot_variable('MuMu_CR_'+year+'_OS_Boost', mu1, mu2, jet, met)

            if baseline_selection(mu1, mu2, jet, met, 'MuMu') == 1 :
                plot_variable('MuMu_Baseline', mu1, mu2, jet, met)

        if isSingleMuonEvent == 1:
            if baseline_selection(mu1, mu2, jet, met, 'MuMu') == 1 :
                isMuMu = 1

    return isMuMu



def mutau_channel(s_tauMuclean, tauid="Nominal"):

    isMuTau = 0
    isSingleMuonEvent = False

    mu = get_TLorentzVector(s_muon[0])
    tau = get_TLorentzVector(s_tauMuclean[0])
    jet = get_TLorentzVector(s_jet[0])

    plot_variable('MuTau_'+tauid+'_Baseline', mu, tau, jet, met)

    isMatchedMu = False
    for ito in tOisMu:
        if isMatchedMu == True: break
        trigObject = get_TLorentzVector(ito)
        if trigObject.DeltaR(mu) < 0.1 :
            isMatchedMu = True

    if isMatchedMu == True and mu.Pt() >= 52 : isSingleMuonEvent = True

    if ( isData == 0 or isSingleMuonData == True ) and isSingleMuonEvent == True :

        plot_variable('MuTau_'+tauid+'_Trigger', mu, tau, jet, met)

        # -------- Validation regions ----------

        if s_muon[0].charge*s_tauMuclean[0].charge > 0: #SS

            if jet.Pt() < event_cut['jetpt'] : return isMuTau
            if len(s_bjet) > 0 : return isMuTau

            if pass_deltaR(mu, tau, jet, 'MuTau') == 1 : #dRcut
                if met.Pt() < event_cut['metcut'] : #lowMET
                    if Mt(mu,met) < event_cut['mtcut'] : # lowMt
                        plot_variable('MuTau_'+tauid+'_SS_dRcut_lowMET_lowMt', mu, tau, jet, met)
                if met.Pt() > event_cut['metcut'] : #highMET
                    if Mt(mu,met) < event_cut['mtcut'] : # lowMt
                        plot_variable('MuTau_'+tauid+'_SS_dRcut_highMET_lowMt', mu, tau, jet, met)

        # --------------------------------------

        if s_muon[0].charge*s_tauMuclean[0].charge < 0: #OS
            
            plot_variable('MuTau_'+tauid+'_OS', mu, tau, jet, met)
            select_Nm1(mu, tau, jet, met, s_tauMuclean[0].decaymode,'MuTau')

            if len(s_bjet) > 0 : return isMuTau

            plot_variable('MuTau_'+tauid+'_OS_bjet0', mu, tau, jet, met)

            if jet.Pt() < event_cut['jetpt'] : return isMuTau

            plot_variable('MuTau_'+tauid+'_OS_bjet0_jetcut', mu, tau, jet, met)

            if pass_deltaR(mu, tau, jet, 'MuTau') == 1 : #dRcut
                plot_variable('MuTau_'+tauid+'_OS_dRcut', mu, tau, jet, met)
                if met.Pt() < event_cut['metcut'] : #lowMET
                    plot_variable('MuTau_'+tauid+'_OS_dRcut_lowMET', mu, tau, jet, met)
                    if Mt(mu,met) < event_cut['mtcut'] : # lowMt
                        plot_variable('MuTau_'+tauid+'_OS_dRcut_lowMET_lowMt', mu, tau, jet, met)

                if met.Pt() >= event_cut['metcut'] : #highMET
                    plot_variable('MuTau_'+tauid+'_OS_dRcut_highMET', mu, tau, jet, met)
                    if Mt(mu,met) < event_cut['mtcut'] : # lowMt SR!!!

                        if tauid == "Nominal" and isData == 0:
                            plot_variable('MuTau_'+tauid+'_OS_bjet0_jetcut_highMET_lowMt', mu, tau, jet, met)

                        mSVFit = get_svfit(mu, tau, s_tauMuclean[0].decaymode, 'MuTau')
                        
                        if mSVFit >= event_cut['mass'] :
                            
                            if tauid != "Nominal" and isData == 1 : 

                                plot_variable('MuTau_'+tauid+'_OS_dRcut_highMET_lowMt', mu, tau, jet, met)
                                plot_svfit('MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_DM0', mSVFit)
                                h['MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)

                                if s_tauMuclean[0].decaymode == 0 :
                                    plot_variable('MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_DM0', mu, tau, jet, met)
                                    plot_svfit('MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_DM0', mSVFit)
                                    h['MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_DM0_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)

                                if s_tauMuclean[0].decaymode == 1 :
                                    plot_variable('MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_DM1', mu, tau, jet, met)
                                    plot_svfit('MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_DM1', mSVFit)
                                    h['MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_DM1_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)

                                if s_tauMuclean[0].decaymode == 10 :
                                    plot_variable('MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_DM10', mu, tau, jet, met)
                                    plot_svfit('MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_DM10', mSVFit)
                                    h['MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_DM10_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)

                            if isData == 0 :

                                if tauid == "Nominal":

                                    h['MuTau_Nbjet_T'].Fill(len(s_bjet), weight)
                                    h['MuTau_Nbjet_M'].Fill(len(s_bjet_med), weight)
                                    h['MuTau_Nbjet_L'].Fill(len(s_bjet_loose), weight)

                                    plot_variable('MuTau_SR_'+year+'_OS_Boost', mu, tau, jet, met)

                                    musf = mu50SF["NUM_Mu50_DEN_LooseID"].evaluate(abs(mu.Eta()), mu.Pt(), "nominal")
                                    musf_up = mu50SF["NUM_Mu50_DEN_LooseID"].evaluate(abs(mu.Eta()), mu.Pt(), "systup")
                                    musf_down = mu50SF["NUM_Mu50_DEN_LooseID"].evaluate(abs(mu.Eta()), mu.Pt(), "systdown")
                                    
                                    plot_svfit('MuTau_SR_'+year+'_OS_Boost', mSVFit, musf)
                                    plot_svfit('MuTau_SR_'+year+'_OS_Boost_muUp', mSVFit, musf_up)
                                    plot_svfit('MuTau_SR_'+year+'_OS_Boost_muDown', mSVFit, musf_down)

                                plot_variable('MuTau_'+tauid+'_OS_dRcut_highMET_lowMt', mu, tau, jet, met)
                                plot_svfit('MuTau_'+tauid+'_OS_dRcut_highMET_lowMt', mSVFit)
                                h['MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)

                                if s_tauMuclean[0].decaymode == 0 :
                                    plot_variable('MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_DM0', mu, tau, jet, met)
                                    plot_svfit('MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_DM0', mSVFit)
                                    h['MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_DM0_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)

                                if s_tauMuclean[0].decaymode == 1 :
                                    plot_variable('MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_DM1', mu, tau, jet, met)
                                    plot_svfit('MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_DM1', mSVFit)
                                    h['MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_DM1_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)

                                if s_tauMuclean[0].decaymode == 10 :
                                    plot_variable('MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_DM10', mu, tau, jet, met)
                                    plot_svfit('MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_DM10', mSVFit)
                                    h['MuTau_'+tauid+'_OS_dRcut_highMET_lowMt_DM10_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)



    if isSingleMuonEvent == True :
        if s_muon[0].charge*s_tauMuclean[0].charge < 0: #OS
            if len(s_bjet) == 0 :
                if baseline_selection(mu, tau, jet, met, 'MuTau') == 1 :
                    if Mt(mu,met) < event_cut['mtcut'] :
                        isMuTau = 1

    return isMuTau

def ee_channel():

    isEE = 0

    if s_isoelectron[0].charge*s_isoelectron[1].charge < 0 :
        
        e1 = get_TLorentzVector(s_isoelectron[0])
        e2 = get_TLorentzVector(s_isoelectron[1])
        jet = get_TLorentzVector(s_jet[0])

        isJetHTEvent = 0
        isSingleElectronEvent = 0

        if ( jet.Pt() > 510 and ( isHT == 1  or isSingleJet500 == 1 ) ) : isJetHTEvent = 1
        if ( e1.Pt() > 37 and isIsoEle == 1 ) : isSingleElectronEvent = 1

        if isJetHTEvent == 1 :             
            if pass_deltaR(e1, e2, jet, 'EE') == 1 :
                if met.Pt() > event_cut['metcut'] :
                    plot_variable("EE_SR", e1, e2, jet, met)
                    isEE = 1

    return isEE

def emu_channel():

    isEMu = 0

    e = get_TLorentzVector(s_isoelectron[0])
    mu = get_TLorentzVector(s_isomuon[0])
    jet = get_TLorentzVector(s_jet[0])
    
    plot_variable('EMu_Baseline', e, mu, jet, met)

    if s_isoelectron[0].charge*s_isomuon[0].charge < 0 :

        plot_variable('EMu_Baseline_OS', e, mu, jet, met)

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
            isMatchedMuonEG = True

        SingleMuonHLT = False
        MuonEGHLT = False
            
        if mu.Pt() >= 52.0 and isMatchedMu == True : SingleMuonHLT = True
        if ( ( mu.Pt() >= 10.0 and e.Pt() >= 25.0 ) or ( mu.Pt() >= 25.0 and e.Pt() >= 15.0 ) ) and isMatchedMuonEG == True : MuonEGHLT = True

        if ( isSingleMuonData == True and SingleMuonHLT == True ) or \
           ( isMuonEGData == True and MuonEGHLT == True and SingleMuonHLT == False ) or \
           ( isData == 0 and ( SingleMuonHLT == True or MuonEGHLT == True ) ) :

            plot_variable('EMu_Baseline_OS_Trigger', e, mu, jet, met)
            select_Nm1(e, mu, jet, met, 0, 'EMu')

            if jet.Pt() < event_cut['jetpt'] : return isEMu

            plot_variable('EMu_Baseline_OS_Trigger_jetcut', e, mu, jet, met)

            # ------------- For closure test ------------

            if e.DeltaR(mu) < 0.6 and e.DeltaR(mu) > 0.4 and jet.DeltaR(e+mu) > 0.8 :

                if met.Pt() < event_cut['metcut'] : #lowMET

                    bweight = BJetSF.get_weight("lowMET", s_jet) if isData == 0 and isSignal == 0 else 1

                    if len(s_bjet) == 0 :
                        mSVFit = get_svfit(e, mu, 0, 'EMu')
                        if mSVFit >= event_cut['mass']:
                            plot_variable('EMu_OS_SB_lowMET_bjetveto', e, mu, jet, met, bweight)
                            plot_svfit('EMu_OS_SB_lowMET_bjetveto', mSVFit, bweight)

                    else:
                        mSVFit = get_svfit(e, mu, 0, 'EMu')
                        if mSVFit >= event_cut['mass'] :
                            plot_variable('EMu_OS_SB_lowMET_bjet', e, mu, jet, met, bweight)
                            plot_svfit('EMu_OS_SB_lowMET_bjet', mSVFit, bweight)

                else: #highMET

                    bweight = BJetSF.get_weight("highMET", s_jet) if isData == 0 and isSignal == 0 else 1

                    if len(s_bjet) == 0 :
                        mSVFit = get_svfit(e, mu, 0, 'EMu')
                        if mSVFit >= event_cut['mass']:
                            plot_variable('EMu_OS_SB_highMET_bjetveto', e, mu, jet, met, bweight)
                            plot_svfit('EMu_OS_SB_highMET_bjetveto', mSVFit, bweight)

                    else:
                        mSVFit = get_svfit(e, mu, 0, 'EMu')
                        if mSVFit >= event_cut['mass']:
                            plot_variable('EMu_OS_SB_highMET_bjet', e, mu, jet, met, bweight)
                            plot_svfit('EMu_OS_SB_highMET_bjet', mSVFit, bweight)


            # --------------------- Event selections -----------
            
            if pass_deltaR(e, mu, jet, 'EMu') == 1 :

                plot_variable('EMu_Baseline_OS_Trigger_jetcut_dRcut', e, mu, jet, met)

                if met.Pt() < event_cut['metcut'] : #lowMET

                    bweight = BJetSF.get_weight("lowMET", s_jet) if isData == 0 and isSignal == 0 else 1

                    if len(s_bjet) == 0 :
                        mSVFit = get_svfit(e, mu, 0, 'EMu')
                        if mSVFit >= event_cut['mass']:
                            plot_variable('EMu_OS_lowMET_bjetveto', e, mu, jet, met, bweight)
                            plot_svfit('EMu_OS_lowMET_bjetveto', mSVFit, bweight)

                    else:
                        mSVFit = get_svfit(e, mu, 0, 'EMu')
                        if mSVFit >= event_cut['mass'] :
                            plot_variable('EMu_OS_lowMET_bjet', e, mu, jet, met, bweight)
                            plot_svfit('EMu_OS_lowMET_bjet', mSVFit, bweight)

                else: #highMET

                    plot_variable('EMu_Baseline_OS_Trigger_jetcut_dRcut_highMET', e, mu, jet, met)

                    bweight = BJetSF.get_weight("highMET", s_jet) if isData == 0 and isSignal == 0 else 1

                    mSVFit = get_svfit(e, mu, 0, 'EMu')
                    if mSVFit >= event_cut['mass']:

                        plot_variable('EMu_Baseline_OS_Trigger_jetcut_dRcut_highMET_svfitcut', e, mu, jet, met)

                        h['EMu_Nbjet_T'].Fill(len(s_bjet), weight)
                        h['EMu_Nbjet_M'].Fill(len(s_bjet_med), weight)
                        h['EMu_Nbjet_L'].Fill(len(s_bjet_loose), weight)

                        if len(s_bjet) == 0 :
                            plot_variable('EMu_OS_highMET_bjetveto', e, mu, jet, met, bweight)
                            plot_svfit('EMu_OS_highMET_bjetveto', mSVFit, bweight)
                            plot_variable('EMu_SR_'+year+'_OS_Boost', e, mu, jet, met, bweight)
                            plot_svfit('EMu_SR_'+year+'_OS_Boost', mSVFit, bweight)
                            plot_variable('EMu_Baseline_OS_Trigger_jetcut_dRcut_highMET_svfitcut_bjet0', e, mu, jet, met)
                            isEMu = 1
                        else:
                            plot_variable('EMu_OS_highMET_bjet', e, mu, jet, met, bweight)
                            plot_svfit('EMu_OS_highMET_bjet', mSVFit, bweight)

                # --------------------------

    return isEMu



def etau_channel(s_tauEclean, tauid="Nominal"):

    isETau = 0

    e = get_TLorentzVector(s_electron[0])
    tau = get_TLorentzVector(s_tauEclean[0])
    jet = get_TLorentzVector(s_jet[0])

    plot_variable('ETau_'+tauid+'_Baseline', e, tau, jet, met)

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
                print("MatchedJet found")

    if isMatchedE == True and isMatchedJet == True :
        print("MatchEleJet found")
        isMatchedEleJet = True

    isEleJetEvent = False    
    if jet.Pt() >= 200.0 and e.Pt() >= 60.0 and isEleJet == 1 :
        isEleJetEvent = True

    if jet.Pt() >= 200.0 and e.Pt() >= 60.0 and isMatchedEleJet == True :
        isEleJetEvent = True

    isPhotonEvent = False
    if e.Pt() >= 230.0 and isMatchedPhoton == True :
        isPhotonEvent = True

    if ( isData == 0 or isSingleElectronData == True ) and ( isEleJetEvent == True or isPhotonEvent == True ):

        # print(isEleJetEvent, isPhotonEvent)

        plot_variable('ETau_'+tauid+'_Trigger', e, tau, jet, met)

        if s_electron[0].charge*s_tauEclean[0].charge > 0: #SS Validation Regions
            
            if len(s_bjet) > 0 : return isETau

            if jet.Pt() < event_cut['jetpt'] : return isETau
            
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
            select_Nm1(e, tau, jet, met, s_tauEclean[0].decaymode, 'ETau')

            plot_variable('ETau_'+tauid+'_OS', e, tau, jet, met)

            if len(s_bjet) > 0 : return isETau

            plot_variable('ETau_'+tauid+'_OS_bjet0', e, tau, jet, met)
            
            if jet.Pt() < event_cut['jetpt'] : return isETau

            plot_variable('ETau_'+tauid+'_OS_bjet0_jetcut', e, tau, jet, met)

            if pass_deltaR(e, tau, jet, 'ETau') == 1 : #dRcut
                plot_variable('ETau_'+tauid+'_OS_dRcut', e, tau, jet, met)
                if met.Pt() >= 100.0 : # highMET       
                    plot_variable('ETau_'+tauid+'_OS_dRcut_highMET', e, tau, jet, met)                                                          
                    if Mt(e,met) <= 50.0 : #lowMt SR!!!!

                        if tauid == "Nominal" and isData == 0:
                            plot_variable('ETau_'+tauid+'_OS_bjet0_jetcut_highMET_lowMt', e, tau, jet, met)

                        mSVFit = get_svfit(e,tau,s_tauEclean[0].decaymode,'ETau')

                        if mSVFit >= event_cut['mass'] :
                            
                            if tauid != "Nominal" and isData == 1 :

                                plot_variable('ETau_'+tauid+'_OS_dRcut_highMET_lowMt', e, tau, jet, met)
                                plot_svfit('ETau_'+tauid+'_OS_dRcut_highMET_lowMt', mSVFit)
                                h['ETau_'+tauid+'_OS_dRcut_highMET_lowMt_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)

                                if s_tauEclean[0].decaymode == 0 :
                                    plot_variable('ETau_'+tauid+'_OS_dRcut_highMET_lowMt_DM0', e, tau, jet, met)
                                    plot_svfit('ETau_'+tauid+'_OS_dRcut_highMET_lowMt_DM0', mSVFit)
                                    h['ETau_'+tauid+'_OS_dRcut_highMET_lowMt_DM0_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)

                                if s_tauEclean[0].decaymode == 1 :
                                    plot_variable('ETau_'+tauid+'_OS_dRcut_highMET_lowMt_DM1', e, tau, jet, met)
                                    plot_svfit('ETau_'+tauid+'_OS_dRcut_highMET_lowMt_DM1', mSVFit)
                                    h['ETau_'+tauid+'_OS_dRcut_highMET_lowMt_DM1_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)

                                if s_tauEclean[0].decaymode == 10 :
                                    plot_variable('ETau_'+tauid+'_OS_dRcut_highMET_lowMt_DM10', e, tau, jet, met)
                                    plot_svfit('ETau_'+tauid+'_OS_dRcut_highMET_lowMt_DM10', mSVFit)
                                    h['ETau_'+tauid+'_OS_dRcut_highMET_lowMt_DM10_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)

                            if isData == 0 :
                                plot_variable('ETau_'+tauid+'_OS_dRcut_highMET_lowMt', e, tau, jet, met)
                                plot_svfit('ETau_'+tauid+'_OS_dRcut_highMET_lowMt', mSVFit)
                                h['ETau_'+tauid+'_OS_dRcut_highMET_lowMt_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)

                                if s_tauEclean[0].decaymode == 0 :
                                    plot_variable('ETau_'+tauid+'_OS_dRcut_highMET_lowMt_DM0', e, tau, jet, met)
                                    plot_svfit('ETau_'+tauid+'_OS_dRcut_highMET_lowMt_DM0', mSVFit)
                                    h['ETau_'+tauid+'_OS_dRcut_highMET_lowMt_DM0_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)

                                if s_tauEclean[0].decaymode == 1 :
                                    plot_variable('ETau_'+tauid+'_OS_dRcut_highMET_lowMt_DM1', e, tau, jet, met)
                                    plot_svfit('ETau_'+tauid+'_OS_dRcut_highMET_lowMt_DM1', mSVFit)
                                    h['ETau_'+tauid+'_OS_dRcut_highMET_lowMt_DM1_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)

                                if s_tauEclean[0].decaymode == 10 :
                                    plot_variable('ETau_'+tauid+'_OS_dRcut_highMET_lowMt_DM10', e, tau, jet, met)
                                    plot_svfit('ETau_'+tauid+'_OS_dRcut_highMET_lowMt_DM10', mSVFit)
                                    h['ETau_'+tauid+'_OS_dRcut_highMET_lowMt_DM10_mSVFitTauPt'].Fill(mSVFit, tau.Pt(), weight)

                                if tauid == "Nominal":

                                    h['ETau_Nbjet_T'].Fill(len(s_bjet), weight)
                                    h['ETau_Nbjet_M'].Fill(len(s_bjet_med), weight)
                                    h['ETau_Nbjet_L'].Fill(len(s_bjet_loose), weight)

                                    
                                if year == "2016preVFP" or year == "2016postVFP":
                                    esf, esf_up, esf_down = 1, 1, 1
                                    trigsf, trigsf_up, trigsf_down = 1, 1, 1
                                else:
                                    esf, esf_up, esf_down = get_EGsf(e.Eta(), e.Pt())
                                    trigsf, trigsf_up, trigsf_down = get_etauTrigsf(e.Eta(), e.Pt())

                                    plot_variable('ETau_SR_'+year+'_OS_Boost', e, tau, jet, met)
                                    
                                    plot_svfit('ETau_SR_'+year+'_OS_Boost', mSVFit, esf*trigsf)
                                    
                                    plot_svfit('ETau_SR_'+year+'_OS_Boost_egup', mSVFit, esf_up)
                                    plot_svfit('ETau_SR_'+year+'_OS_Boost_egdown', mSVFit, esf_down)

                                    plot_svfit('ETau_SR_'+year+'_OS_Boost_trigup', mSVFit, trigsf_up)
                                    plot_svfit('ETau_SR_'+year+'_OS_Boost_trigdown', mSVFit, trigsf_down)
                                    
                                    
                else: #lowMET                                                                                         
                    if Mt(e,met) <= 50.0 : #lowMt                                                                                             
                        mSVFit = get_svfit(e,tau,s_tauEclean[0].decaymode,'ETau')

                        if mSVFit >= event_cut['mass']:

                            plot_variable('ETau_'+tauid+'_OS_dRcut_lowMET_lowMt', e, tau, jet, met)
                            plot_svfit('ETau_'+tauid+'_OS_dRcut_lowMET_lowMt', mSVFit)
 
    return isETau
        

def book_gen_hists(region):

    h[region+"_Mass"] = ROOT.TH1F(region+"_Mass", region+"_Mass ; Mass (GeV) ; Events", 100, 0, 100)
    h[region+"_Lepton1Pt"] = ROOT.TH1F(region+"_Lepton1Pt", region+"_Lepton1Pt ; Lepton1Pt (GeV) ; Events", 500, 0, 500)
    h[region+"_Lepton2Pt"] = ROOT.TH1F(region+"_Lepton2Pt", region+"_Lepton1Pt ; Lepton2Pt (GeV) ; Events", 500, 0, 500)
    h[region+"_dRl"] = ROOT.TH1F(region+"_dRl", region+"_dRl ; dR(l1,l2) ; Events", 100, 0, 5)
    h[region+"_dRj"] = ROOT.TH1F(region+"_dRj", region+"_dRl ; dR(jet,leptons) ; Events", 100, 0, 5)
    h[region+"_MET"] = ROOT.TH1F(region+"_MET", region+"_MET ; MET (GeV) ; Events", 1000, 0, 1000)
    h[region+"_JetPt"] = ROOT.TH1F(region+"_JetPt", region+"_JetPt ; JetPt (GeV) ; Events", 2000, 0, 2000)


def plot_for_gen(region, genl1, genl2, genjet):

    h[region+"_Mass"].Fill((genl1+genl2).M(), genweight)
    h[region+"_Lepton1Pt"].Fill(genl1.Pt(), genweight)
    h[region+"_Lepton2Pt"].Fill(genl2.Pt(), genweight)
    h[region+"_dRl"].Fill(genl1.DeltaR(genl2), genweight)
    h[region+"_dRj"].Fill(genjet.DeltaR(genl1+genl2), genweight)
    h[region+"_JetPt"].Fill(genjet.Pt(), genweight)

    met = (genjet-genl1+genl2).Pt()
    h[region+"_MET"].Fill(met, genweight)


def gen_tautau(gen_tau, genJet):

    genTau1 = get_TLorentzVector(gen_tau[0])
    genTau2 = get_TLorentzVector(gen_tau[1])

    plot_for_gen("Gen_TauTau", genTau1, genTau2, genJet)

def gen_emu(gen_e, gen_mu, genJet):

    genE = get_TLorentzVector(gen_e[0])
    genMu = get_TLorentzVector(gen_mu[0])
 
    plot_for_gen("Gen_EMu", genE, genMu, genJet)


def gen_mutau(gen_mu, gen_tau, gen_tanu, genJet):

    genMu = get_TLorentzVector(gen_mu[0])
    genTau = ROOT.TLorentzVector()
    genNu = ROOT.TLorentzVector()

    if gen_mu[0].pdgid == 13: 
        genTau.SetPtEtaPhiM(gen_tau[0].pt, gen_tau[0].eta, gen_tau[0].phi, gen_tau[0].mass) if gen_tau[0].pdgid==-15 else genTau.SetPtEtaPhiM(gen_tau[1].pt, gen_tau[1].eta, gen_tau[1].phi, gen_tau[1].mass)
        genNu.SetPtEtaPhiM(gen_tanu[0].pt, gen_tanu[0].eta, gen_tanu[0].phi, gen_tanu[0].mass) if gen_tanu[0].pdgid==-16 else genNu.SetPtEtaPhiM(gen_tanu[1].pt, gen_tanu[1].eta, gen_tanu[1].phi, gen_tanu[1].mass)
    else:
        genTau.SetPtEtaPhiM(gen_tau[0].pt, gen_tau[0].eta, gen_tau[0].phi, gen_tau[0].mass) if gen_tau[0].pdgid==15 else genTau.SetPtEtaPhiM(gen_tau[1].pt, gen_tau[1].eta, gen_tau[1].phi, gen_tau[1].mass)
        genNu.SetPtEtaPhiM(gen_tanu[0].pt, gen_tanu[0].eta, gen_tanu[0].phi, gen_tanu[0].mass) if gen_tanu[0].pdgid==16 else genNu.SetPtEtaPhiM(gen_tanu[1].pt, gen_tanu[1].eta, gen_tanu[1].phi, gen_tanu[1].mass)
        
    plot_for_gen("Gen_MuTau", genMu, genTau-genNu, genJet)


def gen_etau(gen_e, gen_tau, gen_tanu, genJet):        

    genE = get_TLorentzVector(gen_e[0])
    genTau = ROOT.TLorentzVector()
    genNu = ROOT.TLorentzVector()

    if gen_e[0].pdgid == 11: 
        genTau.SetPtEtaPhiM(gen_tau[0].pt, gen_tau[0].eta, gen_tau[0].phi, gen_tau[0].mass) if gen_tau[0].pdgid==-15 else genTau.SetPtEtaPhiM(gen_tau[1].pt, gen_tau[1].eta, gen_tau[1].phi, gen_tau[1].mass)
        genNu.SetPtEtaPhiM(gen_tanu[0].pt, gen_tanu[0].eta, gen_tanu[0].phi, gen_tanu[0].mass) if gen_tanu[0].pdgid==-16 else genNu.SetPtEtaPhiM(gen_tanu[1].pt, gen_tanu[1].eta, gen_tanu[1].phi, gen_tanu[1].mass)
    else:
        genTau.SetPtEtaPhiM(gen_tau[0].pt, gen_tau[0].eta, gen_tau[0].phi, gen_tau[0].mass) if gen_tau[0].pdgid==15 else genTau.SetPtEtaPhiM(gen_tau[1].pt, gen_tau[1].eta, gen_tau[1].phi, gen_tau[1].mass)
        genNu.SetPtEtaPhiM(gen_tanu[0].pt, gen_tanu[0].eta, gen_tanu[0].phi, gen_tanu[0].mass) if gen_tanu[0].pdgid==16 else genNu.SetPtEtaPhiM(gen_tanu[1].pt, gen_tanu[1].eta, gen_tanu[1].phi, gen_tanu[1].mass)
        
    plot_for_gen("Gen_ETau", genE, genTau-genNu, genJet)



book_histogram()
region_list = []
svfit_plot = []
book_gen_hists("Gen_EMu")
book_gen_hists("Gen_MuTau")
book_gen_hists("Gen_ETau")
book_gen_hists("Gen_TauTau")

for key in h.keys():
    h[key].Sumw2()


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
    gen_munu = []

    if isData == 0 :
        if genParticle.size() > 0 :
            for i in range(genParticle.size()):
                igen = genParticle.at(i)
                if igen.isdirecthardprocesstaudecayproductfinalstate :
                    if abs(igen.pdgid) == 13 : gen_mu+=[igen]
                    if abs(igen.pdgid) == 11 : gen_e+=[igen]
                    if abs(igen.pdgid) == 12 : gen_enu+=[igen]
                    if abs(igen.pdgid) == 16 : gen_tanu+=[igen]
                    if abs(igen.pdgid) == 14 : gen_munu+=[igen]
                if igen.ishardprocess and abs(igen.pdgid) == 15: gen_tau+=[igen]

        GenJets = fchain.GetBranch("genJetInfo")
        genjet_pt = GenJets.GetLeaf('pt').GetValue()
        genjet_eta = GenJets.GetLeaf('eta').GetValue()
        genjet_phi = GenJets.GetLeaf('phi').GetValue()
        genjet_mass = GenJets.GetLeaf('mass').GetValue()

        genJet= ROOT.TLorentzVector()
        genJet.SetPtEtaPhiM(genjet_pt, genjet_eta, genjet_phi, genjet_mass)

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
    s_bjet_loose = []
    s_bjet_med = []

    iht = 0

    if jets.size() > 0:
        for i in range(jets.size()):
            ijet = jets.at(i)
            if abs(ijet.eta) < 2.5 :
                if ijet.id >= 2:
                    h['hJetPt'].Fill(ijet.pt, weight)
                    h['hDeepjet'].Fill(ijet.deepjet, weight)
                    s_jet+=[ijet]
                    iht = iht + ijet.pt
                    if ijet.deepjet >= 0.7476:
                        h['hBJetPt'].Fill(ijet.pt, weight) 
                        s_bjet+=[ijet]
                    if ijet.deepjet > 0.3040:
                        s_bjet_med+=[ijet]
                    if ijet.deepjet > 0.0532:
                        s_bjet_loose+=[ijet]

    s_muon = []
    s_isomuon = []
    s_nonisomuon = []

    if muons.size() > 0:
        for i in range(muons.size()):
            imuon = muons.at(i)
            if abs(imuon.eta) < 2.4 :
                if imuon.id >= 1: #loose Muons
                    h['hMuonPt'].Fill(imuon.pt, weight) 
                    s_muon+=[imuon]
                    if imuon.iso <= 0.25:
                        h['hIsoMuonPt'].Fill(imuon.pt, weight)
                        s_isomuon+=[imuon]
                    if imuon.iso > 0.2:
                        h['hNonIsoMuonPt'].Fill(imuon.pt, weight)
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

    s_tauUncleanNom = []

    if tausUnCleaned.size() > 0 :
        for i in range(tausUnCleaned.size()):
            itau = tausUnCleaned.at(i)
            if abs(itau.eta) < 2.3 and itau.pt >= 20.0:
                if itau.mvaid >= 4:
                    s_tauUncleanNom+=[itau]
                        
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
                    h['hTauMuCleanedPt'].Fill(itau.pt, weight)
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

    # if len(gen_tau) == 2 :
    #     gen_tautau(gen_tau, genJet)

    # if len(gen_e) == 1 and len(gen_mu) == 0 and len(gen_tau) > 0:
    #     gen_etau(gen_e, gen_tau, gen_tanu, genJet)

    # if len(gen_e) == 1 and len(gen_mu) == 1:
    #     gen_emu(gen_e, gen_mu, genJet)

    # if len(gen_e) == 0 and len(gen_mu) == 1 and len(gen_tau) > 0:
    #     gen_mutau(gen_mu, gen_tau, gen_tanu, genJet)

    if len(s_isomuon) >= 2 and len(s_jet) >= 1 and len(s_bjet) == 0: 
        if mumu_channel() == 1 : continue

    if len(s_isomuon) >= 1 and len(s_isoelectron) >= 1 and len(s_jet) >= 1 : 
        if emu_channel() == 1 : continue

    if len(s_muon) >= 1 and len(s_jet) >= 1 and len(s_bjet) == 0 and len(s_tauMucleanAlt) >= 1: 
        mutau_channel(s_tauMucleanAlt, "Altered")

    # if len(s_muon) >= 1 and len(s_jet) >= 1 and len(s_bjet) == 0 and len(s_tauUncleanNom) >= 1: 
    #     mutau_channel(s_tauUncleanNom, "Uncleaned")
    
    if len(s_muon) >= 1 and len(s_jet) >= 1 and len(s_tauMucleanNom) >= 1: 
        if mutau_channel(s_tauMucleanNom, "Nominal") == 1 : continue

    if len(s_isoelectron) >= 2 and len(s_jet) >= 1 and len(s_bjet) == 0 :
        if ee_channel() == 1 : continue

    if len(s_electron) >= 1 and len(s_tauEcleanAlt) >= 1 and len(s_jet) >=1 and len(s_bjet) == 0:
        etau_channel(s_tauEcleanAlt, "Altered")

    if len(s_electron) >= 1 and len(s_tauEcleanNom) >= 1 and len(s_jet) >=1 :
        etau_channel(s_tauEcleanNom, "Nominal")
        
    # if len(s_electron) >= 1 and len(s_tauUncleanNom) >= 1 and len(s_jet) >=1 and len(s_bjet) == 0 :
    #     etau_channel(s_tauUncleanNom, "Uncleaned")



out.cd()

for key in h.keys():
    # print(key)
    h[key].Write()

out.Close()

print("--- %s seconds ---" % (time.time() - start_time))
