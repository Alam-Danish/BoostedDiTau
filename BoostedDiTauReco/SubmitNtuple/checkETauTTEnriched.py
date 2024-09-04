import ROOT, sys, os
import numpy as np
import time
import correctionlib
from array import array
# import BJetSF
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

idjson = correctionlib.CorrectionSet.from_file("Efficiencies_ID_TRK_UL"+year+"_schemaV2.json")
trigjson = correctionlib.CorrectionSet.from_file("Efficiencies_muon_generalTracks_Z_Run"+year+"_UL_SingleMuonTriggers_schemaV2.json")

EGsffile = ROOT.TFile("egammaEffi_EGM2D_UL"+year+".root")

EGsfhist = EGsffile.Get("EGamma_SF2D")

outputTitle = "h_checkETauTTEnriched_"+year

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
# ROOT.gInterpreter.ProcessLine('#include "../../../TauAnalysis/ClassicSVfit/test/testClassicSVfit.h"')

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

    h['ETau_Altered_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("ETau_Altered_OS_dRcut_highMET_lowMt_mSVFitTauPt", "ETau mSVFIt,tauPt ; mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_Altered_OS_dRcut_highMET_lowMt_DM0_mSVFitTauPt'] = ROOT.TH2F ("ETau_Altered_OS_dRcut_highMET_lowMt_DM0_mSVFitTauPt", "ETau mSVFIt,tauPt (DM0) ; mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_Altered_OS_dRcut_highMET_lowMt_DM1_mSVFitTauPt'] = ROOT.TH2F ("ETau_Altered_OS_dRcut_highMET_lowMt_DM1_mSVFitTauPt", "ETau mSVFIt,tauPt (DM1); mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_Altered_OS_dRcut_highMET_lowMt_DM10_mSVFitTauPt'] = ROOT.TH2F ("ETau_Altered_OS_dRcut_highMET_lowMt_DM10_mSVFitTauPt", "ETau mSVFIt,tauPt (DM10); mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)

    h['ETau_ttEnriched_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("ETau_ttEnriched_OS_dRcut_highMET_lowMt_mSVFitTauPt", "ETau mSVFIt,tauPt ; mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_ttEnriched_OS_dRcut_highMET_lowMt_DM0_mSVFitTauPt'] = ROOT.TH2F ("ETau_ttEnriched_OS_dRcut_highMET_lowMt_DM0_mSVFitTauPt", "ETau mSVFIt,tauPt (DM0) ; mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_ttEnriched_OS_dRcut_highMET_lowMt_DM1_mSVFitTauPt'] = ROOT.TH2F ("ETau_ttEnriched_OS_dRcut_highMET_lowMt_DM1_mSVFitTauPt", "ETau mSVFIt,tauPt (DM1); mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_ttEnriched_OS_dRcut_highMET_lowMt_DM10_mSVFitTauPt'] = ROOT.TH2F ("ETau_ttEnriched_OS_dRcut_highMET_lowMt_DM10_mSVFitTauPt", "ETau mSVFIt,tauPt (DM10); mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)

    h['ETau_Loose_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("ETau_Loose_OS_dRcut_highMET_lowMt_mSVFitTauPt", "ETau mSVFIt,tauPt ; mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_VLoose_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("ETau_VLoose_OS_dRcut_highMET_lowMt_mSVFitTauPt", "ETau mSVFIt,tauPt ; mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)
    h['ETau_noID_OS_dRcut_highMET_lowMt_mSVFitTauPt'] = ROOT.TH2F ("ETau_noID_OS_dRcut_highMET_lowMt_mSVFitTauPt", "ETau mSVFIt,tauPt ; mSVFit (GeV) ; tauPt (GeV)", 150, 0, 150, 500, 0, 500)


def book_trigObj_histogram(baseSel):

    h[baseSel+"_trigObj_Count"] = ROOT.TH1F (baseSel+"_trigObj_Count", baseSel+"_trigObj_Count ; Events ; Events", 1, 0, 1)
    h[baseSel+"_trigObj_Pt"] = ROOT.TH1F (baseSel+"_trigObj_Pt", baseSel+"_trigObj_Pt ; P_{T} (GeV) ; Events", 500, 0, 500)

    h[baseSel+"_trigObj_dRl"] = ROOT.TH1F (baseSel+"_trigObj_dRl", baseSel+"_trigObj_dRl ; dR(lepton, trigO) ; Events", 100, 0, 5)
    h[baseSel+"_trigObj_dRj"] = ROOT.TH1F (baseSel+"_trigObj_dRj", baseSel+"_trigObj_dRj ; dR(jet, trigO) ; Events", 100, 0, 5)

    h[baseSel+"_trigObj_dRo"] = ROOT.TH2F (baseSel+"_trigObj_dRo", baseSel+"_trigObj_dRo ; dR(lepton, trigO) ; dR(jet, trigO)", 100, 0, 5, 100, 0, 5)

def book_event_histogram(region):

    h[region+"_Count"] = ROOT.TH1F (region+"_Count", region+"_Count ; Events ; Events ", 1, 0, 1)

    h[region+"_VisMass"] = ROOT.TH1F (region+"_VisMass", region+"_VisMass ; M_{vis.} (GeV) ; Events ", 150, 0, 150)
    h[region+"_Lepton1Pt"] = ROOT.TH1F (region+"_Lepton1Pt", region+"_Lepton1Pt ; P_{T} (GeV) ; Events ", 500, 0, 500)
    h[region+"_Lepton2Pt"] = ROOT.TH1F (region+"_Lepton2Pt", region+"_Lepton2Pt ; P_{T} (GeV) ; Events ", 500, 0, 500)
    h[region+"_LeadingJetPt"] = ROOT.TH1F (region+"_LeadingJetPt", region+"_LeadingJetPt ; LedingJetP_{T} (GeV) ; Events ", 2000, 0, 2000)
    h[region+"_MetPt"] = ROOT.TH1F (region+"_MetPt", region+"_MetPt ; MET (GeV) ; Events ", 500, 0, 500)
    h[region+"_Mt"] = ROOT.TH1F (region+"_Mt", region+"_Mt ; M_{T} (GeV) ; Events ", 150, 0, 150)
    h[region+"_Nj"] = ROOT.TH1F (region+"_Nj", region+"_Nj ; N_{j} ; Events ", 10, 0, 10)
    h[region+"_Nbjet"] = ROOT.TH1F (region+"_Nbjet", region+"_Nbjet ; N_{bjet} ; Events ", 10, 0, 10)
    h[region+"_dRl"] = ROOT.TH1F (region+"_dRl", region+"_dRl ; dR(leptons) ; Events", 100, 0, 5)
    h[region+"_dRl1j"] = ROOT.TH1F (region+"_dRl1j", region+"_dRl1j ; dR(jet, l1) ; Events", 100, 0, 5)
    h[region+"_dRl2j"] = ROOT.TH1F (region+"_dRl2j", region+"_dRl2j ; dR(jet, l2) ; Events", 100, 0, 5)
    h[region+"_HT"] = ROOT.TH1F (region+"_HT", region+"_HT ; HT ; Events", 2000, 0, 2000)
    h[region+"_Lepton1Eta"] = ROOT.TH1F (region+"_Lepton1Eta", region+"_Lepton1Eta ; Eta ; Events", 100, -3.0, 3.0)
    h[region+"_Lepton1Phi"] = ROOT.TH1F (region+"_Lepton1Phi", region+"_Lepton1Phi ; Phi ; Events", 100, -pi, pi)
    h[region+"_LeadingJetEta"] = ROOT.TH1F (region+"_LeadingJetEta", region+"_LeadingJetEta ; LeadingJet Eta ; Events", 100, -3.0, 3.0)
    h[region+"_LeadingJetPhi"] = ROOT.TH1F (region+"_LeadingJetPhi", region+"_LeadingJetPhi ; LeadingJet Phi ; Events", 100, -pi, pi)


def define_eff_histogram(region):

    h[region+"_BFlavour_JetPtEta_"+year] = ROOT.TH2F (region+"_BFlavour_JetPtEta_"+year, region+"_BFlavour_JetPtEta ; P_{T} (GeV) ; Eta", 100, 0, 1000, 10, 0, 2.5)
    h[region+"_BFlavour_BTagged_JetPtEta_"+year] = ROOT.TH2F (region+"_BFlavour_BTagged_JetPtEta_"+year, region+"_BFlavour_BTagged_JetPtEta ; P_{T} (GeV) ; Eta", 100, 0, 1000, 10, 0, 2.5)

    h[region+"_CFlavour_JetPtEta_"+year] = ROOT.TH2F (region+"_CFlavour_JetPtEta_"+year, region+"_CFlavour_JetPtEta ; P_{T} (GeV) ; Eta", 100, 0, 1000, 10, 0, 2.5)
    h[region+"_CFlavour_BTagged_JetPtEta_"+year] = ROOT.TH2F (region+"_CFlavour_BTagged_JetPtEta_"+year, region+"_CFlavour_BTagged_JetPtEta ; P_{T} (GeV) ; Eta", 100, 0, 1000, 10, 0, 2.5)

    h[region+"_LFlavour_JetPtEta_"+year] = ROOT.TH2F (region+"_LFlavour_JetPtEta_"+year, region+"_LFlavour_JetPtEta ; P_{T} (GeV) ; Eta", 100, 0, 1000, 10, 0, 2.5)
    h[region+"_LFlavour_BTagged_JetPtEta_"+year] = ROOT.TH2F (region+"_LFlavour_BTagged_JetPtEta_"+year, region+"_LFlavour_BTagged_JetPtEta ; P_{T} (GeV) ; Eta", 100, 0, 1000, 10, 0, 2.5)

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

    return egsf


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
    h[region+"_Nbjet"].Fill(len(s_bjet), weight*sf)
    h[region+"_dRl"].Fill(l1.DeltaR(l2), weight*sf)
    h[region+"_dRl1j"].Fill(j.DeltaR(l1), weight*sf)
    h[region+"_dRl2j"].Fill(j.DeltaR(l2), weight*sf)
    h[region+"_HT"].Fill(iht, weight*sf)
    h[region+"_Lepton1Eta"].Fill(l1.Eta(), weight*sf)
    h[region+"_Lepton1Phi"].Fill(l1.Phi(), weight*sf)
    h[region+"_LeadingJetEta"].Fill(j.Eta(), weight*sf)
    h[region+"_LeadingJetPhi"].Fill(j.Phi(), weight*sf)



def hist_for_sf(baselineSel):
    for i in range(1,6):
        h['ETau_'+baselineSel+'_Eta_ept'+str(i)] = ROOT.TH1F('ETau_'+baselineSel+'_Eta_ept'+str(i), 'ETau_'+baselineSel+'_Eta_ept'+str(i)+' ; Eta ; N', 100, -2.5, 2.5)
        h['ETau_'+baselineSel+'_Eta_pass_ept'+str(i)] = ROOT.TH1F('ETau_'+baselineSel+'_Eta_pass_ept'+str(i), 'ETau_'+baselineSel+'_Eta_pass_ept'+str(i)+' ; Eta ; N', 100, -2.5, 2.5)

        h['ETau_'+baselineSel+'_EPt_eta'+str(i)] = ROOT.TH1F('ETau_'+baselineSel+'_EPt_eta'+str(i), 'ETau_'+baselineSel+'_EPt_eta'+str(i)+' ; Electron Pt (GeV) ; Efficiency', 500, 0, 500)
        h['ETau_'+baselineSel+'_EPt_pass_eta'+str(i)] = ROOT.TH1F('ETau_'+baselineSel+'_EPt_pass_eta'+str(i), 'ETau_'+baselineSel+'_EPt_pass_eta'+str(i)+' ; Electron Pt ; Efficiency', 500, 0, 500)
        
        h['ETau_'+baselineSel+'_Jet_ept'+str(i)] = ROOT.TH1F('ETau_'+baselineSel+'_Jet_ept'+str(i), 'ETau_'+baselineSel+'_Jet_ept'+str(i)+' ; LeadingJet P_{T} (GeV) ; N', 2000, 0, 2000)
        h['ETau_'+baselineSel+'_Jet_pass_ept'+str(i)] = ROOT.TH1F('ETau_'+baselineSel+'_Jet_pass_ept'+str(i), 'ETau_'+baselineSel+'_Jet_pass_ept'+str(i)+' ; Leading P_{T} (GeV) ; N', 2000, 0, 2000)

        h['ETau_'+baselineSel+'_JetEta_jetpt'+str(i)] = ROOT.TH1F('ETau_'+baselineSel+'_JetEta_jetpt'+str(i), 'ETau_'+baselineSel+'_JetEta_jetpt'+str(i)+' ; JetEta ; N', 100, -2.5, 2.5)
        h['ETau_'+baselineSel+'_JetEta_pass_jetpt'+str(i)] = ROOT.TH1F('ETau_'+baselineSel+'_JetEta_pass_jetpt'+str(i), 'ETau_'+baselineSel+'_JetEta_pass_jetpt'+str(i)+' ; JetEta ; N', 100, -2.5, 2.5)


def select_Nm1(l1, l2, ljet, ms, channel):

    plot_variable(channel+'_OS', l1, l2, ljet, ms)

    if channel == 'EMu' or channel == 'MuMu' or channel == 'EE':

        if ms.Pt() >= 100 :
            plot_variable(channel+'_OS_highMET', l1, l2, ljet , ms)
        if pass_deltaR(l1, l2, ljet, channel) == 1 :
            plot_variable(channel+'_OS_dRcut', l1, l2, ljet , ms)

    else:

        if ms.Pt() >= 100 :
            if pass_deltaR(l1, l2, ljet, channel) == 1 :
                plot_variable(channel+'_OS_dRcut_highMET', l1, l2, ljet , ms)
        if Mt(l1,ms) <= 50.0 :
            if pass_deltaR(l1, l2, ljet, channel) == 1 :
                plot_variable(channel+'_OS_dRcut_lowMt', l1, l2, ljet , ms)
            if ms.Pt() >= 100 :
                plot_variable(channel+'_OS_highMET_lowMt', l1, l2, ljet , ms)



def baseline_selection(l1, l2, ljet, ms, channel):

    if ljet.Pt() < 100.0 : return -9999
    if pass_deltaR(l1, l2, ljet, channel) != 1 : return -9999
    if ms.Pt() < 100.0: return -9999

    return 1


def plot_trigger_object(l1, j, trigO, baseSel):

    if baseSel not in region_trigObj_list:
        book_trigObj_histogram(baseSel)
        region_trigObj_list.append(baseSel)

    h[baseSel+"_trigObj_Count"].Fill(1)

    h[baseSel+"_trigObj_Pt"].Fill(trigO.Pt())

    h[baseSel+"_trigObj_dRl"].Fill(l1.DeltaR(trigO))
    h[baseSel+"_trigObj_dRj"].Fill(j.DeltaR(trigO))

    h[baseSel+"_trigObj_dRo"].Fill(l1.DeltaR(trigO), j.DeltaR(trigO))


def control(theJet, theMu):

    isSingleMuonEvent = False
    isIsoMuonEvent = False

    jet = get_TLorentzVector(theJet[0])
    mu1 = get_TLorentzVector(theMu[0])
    mu2 = get_TLorentzVector(theMu[1])

    if jet.Pt() < 100.0 : return

    isMatchedMu = False
    for ito in tOisMu:
        if isMatchedMu == True: break
        trigObject = get_TLorentzVector(ito)
        if trigObject.DeltaR(mu1) < 0.1 :
            isMatchedMu = True

    isMatchedIsoMu = False
    for ito in tOisIsoMu:
        if isMatchedIsoMu == True: break
        trigObject = get_TLorentzVector(ito)
        if trigObject.DeltaR(mu1) < 0.1 :
            isMatchedIsoMu = True

    if isMatchedMu == True and mu1.Pt() >= 52 : isSingleMuonEvent = True
    if isMatchedIsoMu == True and mu1.Pt() >= 29 : isIsoMuonEvent = True

    if ( isData == 0 or isSingleMuonData == True ) and ( isSingleMuonEvent == True or isIsoMuonEvent == True ) :

        if theMu[0].charge*theMu[1].charge < 0 :
            if met.Pt() <= 100.0 :
                plot_variable("MuMu_Control", mu1, mu2, jet, met)



def measure_btag_eff(region, theJet, sf=1):

    if region not in btag_list:
        define_eff_histogram(region)
        btag_list.append(region)

    for js in theJet:
        if js.jetflavour == 5 : #bjet
            h[region+"_BFlavour_JetPtEta_"+year].Fill(js.pt, abs(js.eta))
            if js.deepjet >= 0.7476 : #btagged
                h[region+'_BFlavour_BTagged_JetPtEta_'+year].Fill(js.pt, abs(js.eta))

        if js.jetflavour == 4 : #cjet
            h[region+"_CFlavour_JetPtEta_"+year].Fill(js.pt, abs(js.eta))
            if js.deepjet >= 0.7476 : #btagged
                h[region+'_CFlavour_BTagged_JetPtEta_'+year].Fill(js.pt, abs(js.eta))

        if js.jetflavour == 0 : #ljet
            h[region+'_LFlavour_JetPtEta_'+year].Fill(js.pt, abs(js.eta))
            if js.deepjet >= 0.7476 : #btagged
                h[region+'_LFlavour_BTagged_JetPtEta_'+year].Fill(js.pt, abs(js.eta))
    

def measure_eff(baselineSel, theEle, theJet, theMu):

    isSingleMuonEvent = False
    isIsoMuonEvent = False

    e = get_TLorentzVector(theEle[0])
    if len(s_tauEcleanNom) > 0:
        tau = get_TLorentzVector(s_tauEcleanNom[0])
    jet = get_TLorentzVector(theJet[0])
    mu = get_TLorentzVector(theMu[0])

    if jet.Pt() < 100.0 : return

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

        plot_trigger_object(e, jet, trigObject, baselineSel)

        if isEleLeg == True and isMatchedE == False:
            if trigObject.DeltaR(e) < 0.1 :
                isMatchedE = True

        if isJetLeg == True and isMatchedJet == False:
            if trigObject.DeltaR(jet) < 0.1 : 
                isMatchedJet = True

    if ( isMatchedE == True and isMatchedJet == True ) or isMatchedPhoton == True: 
        isMatchedEleJet = True

    isMatchedMu = False
    for ito in tOisMu:
        if isMatchedMu == True: break
        trigObject = get_TLorentzVector(ito)
        if trigObject.DeltaR(mu) < 0.1 :
            isMatchedMu = True

    isMatchedIsoMu = False
    for ito in tOisIsoMu:
        if isMatchedIsoMu == True: break
        trigObject = get_TLorentzVector(ito)
        if trigObject.DeltaR(mu) < 0.1 :
            isMatchedIsoMu = True

    muTrigThresh = 26.0        
            
    if year == '2018' : 
        if ( jet.Phi() > -1.57 and jet.Phi() < -0.87 and jet.Eta() > -3.0 and jet.Eta() < -1.3 ) : return
        if ( e.Phi() > -1.57 and e.Phi() < -0.87 and e.Eta() > -3.0 and e.Eta() < -1.3 ) : return

    if year == '2017' : muTrigThresh = 29.0

    if isMatchedMu == True and mu.Pt() >= 52 : isSingleMuonEvent = True
    if isMatchedIsoMu == True and mu.Pt() >= muTrigThresh : isIsoMuonEvent = True

    etauOS = False
    
    if baselineSel == "Baseline6" or baselineSel == "Baseline5" :
        if theEle[0].charge*s_tauEcleanNom[0].charge < 0 : 
            etauOS = True
    else:
        etauOS = True

    if ( isData == 0 or isSingleMuonData == True ) and ( isIsoMuonEvent == True ) :

        if theMu[0].charge*theEle[0].charge < 0 and etauOS == True :

            muon_id_sf = 1
            muon_track_sf = 1
            muon_trig_sf = 1
            ele_id_sf = 1

            if isData == 0:
                if abs(e.Eta()) < 2.5 and e.Pt() < 500:
                    ele_id_sf = get_EGsf(e.Eta(), e.Pt())
                if abs(mu.Eta()) <= 2.4:
                    muon_id_sf = idjson["NUM_MediumID_DEN_TrackerMuons"].evaluate(abs(mu.Eta()), mu.Pt(), "nominal")
                    if mu.Pt() >= 40.0 :
                        if year == "2017" or year == "2018":
                            muon_track_sf = idjson["NUM_TrackerMuons_DEN_genTracks"].evaluate(abs(mu.Eta()), mu.Pt(), "nominal")
                    if mu.Pt() <= 200.0 :
                        if year == "2016preVFP" or year == "2016postVFP":
                            muon_trig_sf = trigjson["NUM_IsoMu24_or_IsoTkMu24_DEN_CutBasedIdMedium_and_PFIsoMedium"].evaluate(abs(mu.Eta()), mu.Pt(), "nominal")
                        elif year == "2017":
                            muon_trig_sf = trigjson["NUM_IsoMu27_DEN_CutBasedIdMedium_and_PFIsoMedium"].evaluate(abs(mu.Eta()), mu.Pt(), "nominal")
                        elif year == "2018":
                            muon_trig_sf = trigjson["NUM_IsoMu24_DEN_CutBasedIdMedium_and_PFIsoMedium"].evaluate(abs(mu.Eta()), mu.Pt(), "nominal")

            muon_sf = muon_id_sf*muon_track_sf*muon_trig_sf
            ele_sf = ele_id_sf
            sfTot = muon_sf*ele_sf

            if jet.Pt() >= 200.0 and e.Pt() >= 60.0:
                plot_variable('ETau_'+baselineSel+"_jetPtcut_ePtcut", e, mu, jet, met, sfTot)
                if isEleJet == 1 :
                    plot_variable('ETau_'+baselineSel+"_jetPtcut_ePtcut_isEleJet", e, mu, jet, met, sfTot)

                if e.DeltaR(jet) >= 0.8 :
                    plot_variable('ETau_'+baselineSel+'_jetPtcut_ePtcut_dRj', e, mu, jet, met, sfTot)
                    if isEleJet == 1:
                        plot_variable('ETau_'+baselineSel+'_jetPtcut_ePtcut_dRj_isEleJet', e, mu, jet, met, sfTot)

                    if met.Pt() >= 100.0 :
                        plot_variable('ETau_'+baselineSel+'_jetPtcut_ePtcut_dRj_highMET', e, mu, jet, met, sfTot)
                        # measure_btag_eff('ETau_'+baselineSel+'_jetPtcut_ePtcut_dRj_highMET', theJet, sfTot)
                        if isEleJet == 1:
                            plot_variable('ETau_'+baselineSel+'_jetPtcut_ePtcut_dRj_highMET_isEleJet', e, mu, jet, met, sfTot)
                            # h['ETau_'+baselineSel+'_jetPtcut_ePtcut_dRj_highMET_isEleJet_Lepton1PtLeadingJetPt'].Fill(e.Pt(), j.Pt(),  weight*sfTot)
                            # h['ETau_'+baselineSel+'_jetPtcut_ePtcut_dRj_highMET_isEleJet_Lepton1PtLepton1Eta'].Fill(e.Pt(), e.Eta(), weight*sfTot)
                            # h['ETau_'+baselineSel+'_jetPtcut_ePtcut_dRj_highMET_isEleJet_LeadingJetPtLeadingJetEta'].Fill(j.Pt(), j.Eta(), weight*sfTot)

                            # measure_btag_eff('ETau_'+baselineSel+'_jetPtcut_ePtcut_dRj_highMET_isEleJet', theJet, sfTot)
                            
                        if abs(e.Eta()) >= abseta[0] and abs(e.Eta()) < abseta[1] :
                            h['ETau_'+baselineSel+'_EPt_eta1'].Fill(e.Pt(), weight*sfTot)
                            if isEleJet == 1 :
                                h['ETau_'+baselineSel+'_EPt_pass_eta1'].Fill(e.Pt(), weight*sfTot)
                            
                        if abs(e.Eta()) >= abseta[1] and abs(e.Eta()) < abseta[2] :
                            h['ETau_'+baselineSel+'_EPt_eta2'].Fill(e.Pt(), weight*sfTot)
                            if isEleJet == 1 :
                                h['ETau_'+baselineSel+'_EPt_pass_eta2'].Fill(e.Pt(), weight*sfTot)

                        if abs(e.Eta()) >= abseta[2] and abs(e.Eta()) < abseta[3] :
                            h['ETau_'+baselineSel+'_EPt_eta3'].Fill(e.Pt(), weight*sfTot)
                            if isEleJet == 1 :
                                h['ETau_'+baselineSel+'_EPt_pass_eta3'].Fill(e.Pt(), weight*sfTot)

                        if abs(e.Eta()) >= abseta[3] and abs(e.Eta()) < abseta[4] :
                            h['ETau_'+baselineSel+'_EPt_eta4'].Fill(e.Pt(), weight*sfTot)
                            if isEleJet == 1 :
                                h['ETau_'+baselineSel+'_EPt_pass_eta4'].Fill(e.Pt(), weight*sfTot)

                        if abs(e.Eta()) >= abseta[4] and abs(e.Eta()) <= abseta[5] :
                            h['ETau_'+baselineSel+'_EPt_eta5'].Fill(e.Pt(), weight*sfTot)
                            if isEleJet == 1 :
                                h['ETau_'+baselineSel+'_EPt_pass_eta5'].Fill(e.Pt(), weight*sfTot)

                                
                        if e.Pt() >= Ept[0] and e.Pt() < Ept[1] :
                            h['ETau_'+baselineSel+'_Eta_ept1'].Fill(e.Eta(), weight*sfTot)
                            h['ETau_'+baselineSel+'_Jet_ept1'].Fill(jet.Pt(), weight*sfTot)
                            if isEleJet == 1:
                                h['ETau_'+baselineSel+'_Eta_pass_ept1'].Fill(e.Eta(), weight*sfTot)
                                h['ETau_'+baselineSel+'_Jet_pass_ept1'].Fill(jet.Pt(), weight*sfTot)

                        if e.Pt() >= Ept[1] and e.Pt() < Ept[2] :
                            h['ETau_'+baselineSel+'_Eta_ept2'].Fill(e.Eta(), weight*sfTot)
                            h['ETau_'+baselineSel+'_Jet_ept2'].Fill(jet.Pt(), weight*sfTot)
                            if isEleJet == 1:
                                h['ETau_'+baselineSel+'_Eta_pass_ept2'].Fill(e.Eta(), weight*sfTot)
                                h['ETau_'+baselineSel+'_Jet_pass_ept2'].Fill(jet.Pt(), weight*sfTot)

                        if e.Pt() >= Ept[2] and e.Pt() < Ept[3] :
                            h['ETau_'+baselineSel+'_Eta_ept3'].Fill(e.Eta(), weight*sfTot)
                            h['ETau_'+baselineSel+'_Jet_ept3'].Fill(jet.Pt(), weight*sfTot)
                            if isEleJet == 1:
                                h['ETau_'+baselineSel+'_Eta_pass_ept3'].Fill(e.Eta(), weight*sfTot)
                                h['ETau_'+baselineSel+'_Jet_pass_ept3'].Fill(jet.Pt(), weight*sfTot)

                        if e.Pt() >= Ept[3] and e.Pt() <= Ept[4] :
                            h['ETau_'+baselineSel+'_Eta_ept4'].Fill(e.Eta(), weight*sfTot)
                            h['ETau_'+baselineSel+'_Jet_ept4'].Fill(jet.Pt(), weight*sfTot)
                            if isEleJet == 1:
                                h['ETau_'+baselineSel+'_Eta_pass_ept4'].Fill(e.Eta(), weight*sfTot)
                                h['ETau_'+baselineSel+'_Jet_pass_ept4'].Fill(jet.Pt(), weight*sfTot)

                        if jet.Pt() >= Jetpt[0] and jet.Pt() < Jetpt[1]:
                            h['ETau_'+baselineSel+'_JetEta_jetpt1'].Fill(jet.Eta(), weight*sfTot)
                            if isEleJet == 1:
                                h['ETau_'+baselineSel+'_JetEta_pass_jetpt1'].Fill(jet.Eta(), weight*sfTot)

                        if jet.Pt() >= Jetpt[1] and jet.Pt() < Jetpt[2]:
                            h['ETau_'+baselineSel+'_JetEta_jetpt2'].Fill(jet.Eta(), weight*sfTot)
                            if isEleJet == 1:
                                h['ETau_'+baselineSel+'_JetEta_pass_jetpt2'].Fill(jet.Eta(), weight*sfTot)

                        if jet.Pt() >= Jetpt[2] and jet.Pt() < Jetpt[3]:
                            h['ETau_'+baselineSel+'_JetEta_jetpt3'].Fill(jet.Eta(), weight*sfTot)
                            if isEleJet == 1:
                                h['ETau_'+baselineSel+'_JetEta_pass_jetpt3'].Fill(jet.Eta(), weight*sfTot)

                        if jet.Pt() >= Jetpt[3] and jet.Pt() <= Jetpt[4]:
                            h['ETau_'+baselineSel+'_JetEta_jetpt4'].Fill(jet.Eta(), weight*sfTot)
                            if isEleJet == 1:
                                h['ETau_'+baselineSel+'_JetEta_pass_jetpt4'].Fill(jet.Eta(), weight*sfTot)


book_histogram()
region_list = []
btag_list = []
svfit_plot = []
region_trigObj_list = []
trigObj_list = []

hist_for_sf("Baseline1_MmuMiso")
hist_for_sf("Baseline1_Iso_MmuMiso")
hist_for_sf("Baseline1_nonIso_MmuMiso")
hist_for_sf("Baseline1_TmuTiso")
hist_for_sf("Baseline1_Iso_TmuTiso")
hist_for_sf("Baseline1_nonIso_TmuTiso")

for key in h.keys():
    h[key].Sumw2()


Ept = [60.0, 100.0, 150.0, 300.0, 500.0]
Jetpt = [200.0,400.0,600.0,1000.0,2000.0]
Eta = [-3.0, -2.5, -2.0, -1.566, -1.444, -0.8, 0.0, 0.8, 1.444, 1.566, 2.0, 2.5, 3.0]
abseta = [0, 0.8, 1.444, 1.566, 2.0, 2.5]

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
    # print('total weight', weight)
    # print('genweight', genweight)
    # print('puweight', puweight)
    # print('prweight', prweight)
    # print('tauidsf', tauidsf)

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
    s_notbjet = []

    iht = 0

    if jets.size() > 0:
        for i in range(jets.size()):
            ijet = jets.at(i)
            if abs(ijet.eta) < 2.5 :
                if ijet.id >= 2:
                    h['hJetPt'].Fill(ijet.pt, weight)
                    h['hDeepjet'].Fill(ijet.deepjet, weight)
                    iht = iht + ijet.pt
                    s_jet+=[ijet]
                    if isData == 0 :
                        if ijet.deepjet >= 0.7476:
                            h['hBJetPt'].Fill(ijet.pt, weight) 
                            s_bjet+=[ijet]
                        elif ijet.jetflavour != 5:
                            s_notbjet+=[ijet]
                    else:
                        if ijet.deepjet >= 0.7476:
                            h['hBJetPt'].Fill(ijet.pt, weight)
                            s_bjet+=[ijet]
                        else:
                            s_notbjet+=[ijet]
                        

    s_TmuLiso = []
    s_MmuTiso = []
    s_muon = []
    s_MmuMiso = []
    s_TmuTiso = []

    if muons.size() > 0:
        for i in range(muons.size()):
            imuon = muons.at(i)
            if abs(imuon.eta) < 2.4 :
                if imuon.id >= 3: #Tight Muons
                    if imuon.iso <= 0.15: #TightIso
                        s_TmuTiso+=[imuon]
                    if imuon.iso <= 0.25: #LooseIso
                        s_TmuLiso+=[imuon]
                if imuon.id >= 2: #Medium Muons
                    s_muon+=[imuon]
                    if imuon.iso <= 0.2: #MediumIso
                        s_MmuMiso+=[imuon]
                    if imuon.iso <= 0.15: #TightIso
                        s_MmuTiso+=[imuon]

    s_electron = []
    s_isoelectron = []
    s_nonIsoElectron = []
    s_nonLooseIsoElectron = []

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
                        s_nonIsoElectron+=[ielectron]
                    if ielectron.iso <= 1 :
                        s_nonLooseIsoElectron+=[ielectron]

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
                if itau.mvaid >= 4: #Medium
                    h['hTauECleanedPt'].Fill(itau.pt, weight)
                    s_tauEcleanNom+=[itau]
                if itau.mvaid >= 1 : s_tauEcleanAlt+=[itau] #VVLoose
                if itau.mvaid >= 2 : s_tauEcleanAltVLoose+=[itau]
                if itau.mvaid >= 3 : s_tauEcleanAltLoose+=[itau]
                # if itau.mvaid < 4 :
                #     s_tauEcleanAltnoID+=[itau]
                #     if itau.mvaid >= 1 : s_tauEcleanAlt+=[itau] #VVLoose

                                            
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

    if len(s_TmuLiso) >= 2 and len(s_jet) >= 1 and len(s_bjet) == 0 :
        control(s_jet,s_TmuLiso)

    # if len(s_electron) >= 1 and len(s_muon) >= 1 and len(s_jet) >= 1 and len(s_bjet) >= 1 :
    #     measure_eff("Baseline1", s_electron, s_jet, s_muon)

    if len(s_electron) >= 1 and len(s_MmuMiso) >= 1 and len(s_jet) >= 1 and len(s_bjet) >= 1 :
        measure_eff("Baseline1_MmuMiso", s_electron, s_jet, s_MmuMiso)

    # if len(s_electron) >= 1 and len(s_TmuTiso) >= 1 and len(s_jet) >= 1 and len(s_bjet) >= 1 :
    #     measure_eff("Baseline1_TmuTiso", s_electron, s_jet, s_TmuTiso)

    # if len(s_electron) >= 1 and len(s_muon) >= 1 and len(s_notbjet) >= 1 and len(s_bjet) >= 1 :
    #     measure_eff("Baseline2", s_electron, s_notbjet)

    # if len(s_nonIsoElectron) >= 1 and len(s_muon) >= 1 and len(s_jet) >= 1 and len(s_bjet) >= 1 :
    #     measure_eff("Baseline1_nonIso", s_nonIsoElectron, s_jet, s_muon)

    if len(s_nonIsoElectron) >= 1 and len(s_MmuMiso) >= 1 and len(s_jet) >= 1 and len(s_bjet) >= 1 :
        measure_eff("Baseline1_nonIso_MmuMiso", s_nonIsoElectron, s_jet, s_MmuMiso)

    # if len(s_nonIsoElectron) >= 1 and len(s_TmuTiso) >= 1 and len(s_jet) >= 1 and len(s_bjet) >= 1 :
    #     measure_eff("Baseline1_nonIso_TmuTiso", s_nonIsoElectron, s_jet, s_TmuTiso)

    # if len(s_nonIsoElectron) >= 1 and len(s_muon) >= 1 and len(s_notbjet) >= 1 and len(s_bjet) >= 1 :
    #     measure_eff("Baseline2_nonIso", s_nonIsoElectron, s_notbjet)

    # if len(s_isoelectron) >= 1 and len(s_muon) >= 1 and len(s_jet) >= 1 and len(s_bjet) >= 1 :
    #     measure_eff("Baseline1_Iso", s_isoelectron, s_jet, s_muon)

    if len(s_isoelectron) >= 1 and len(s_MmuMiso) >= 1 and len(s_jet) >= 1 and len(s_bjet) >= 1 :
        measure_eff("Baseline1_Iso_MmuMiso", s_isoelectron, s_jet, s_MmuMiso)    

    # if len(s_isoelectron) >= 1 and len(s_TmuTiso) >= 1 and len(s_jet) >= 1 and len(s_bjet) >= 1 :
    #     measure_eff("Baseline1_Iso_TmuTiso", s_isoelectron, s_jet, s_TmuTiso)

    # if len(s_isoelectron) >= 1 and len(s_muon) >= 1 and len(s_notbjet) >= 1 and len(s_bjet) >= 1 :
    #     measure_eff("Baseline2_Iso", s_isoelectron, s_notbjet)

    # if len(s_electron) >= 1 and len(s_muon) >= 1 and len(s_jet) >= 1 and len(s_bjet) >= 2 :
    #     measure_eff("Baseline3", s_electron, s_jet)

    # if len(s_electron) >= 1 and len(s_muon) >= 1 and len(s_notbjet) >= 1 and len(s_bjet) >= 2 :
    #     measure_eff("Baseline4", s_electron, s_notbjet)

    # if len(s_electron) >= 1 and len(s_muon) >= 1 and len(s_jet) >= 1 and len(s_bjet) >= 1 and len(s_tauEcleanNom) >= 1 :
    #     measure_eff("Baseline5", s_electron, s_jet)

    # if len(s_electron) >= 1 and len(s_muon) >= 1 and len(s_notbjet) >= 1 and len(s_bjet) >= 1 and len(s_tauEcleanNom) >= 1 :
    #     measure_eff("Baseline6", s_electron, s_notbjet)


out.cd()

for key in h.keys():
    # print(key)
    h[key].Write()

out.Close()

print("--- %s seconds ---" % (time.time() - start_time))
