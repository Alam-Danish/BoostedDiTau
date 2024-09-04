import ROOT, sys, os
import numpy as np
import time
import correctionlib
from array import array
# import BJetSF
import argparse

start_time = time.time()

parser = argparse.ArgumentParser(description="Main plotting script for the boosted AToTauTau analysis")
parser.add_argument("-i", "--inputfile", type=str, required=True, help="Text file with list of ntuple root files")
parser.add_argument("-s", "--sample", type=str, required=True, help="Type of sample. Accepted: MC, data")
parser.add_argument("--folder", type=str, help="Output folder. Default is /output/")
parser.add_argument("--year", type=str, required=True, help="Year. Accepted: 2016preVFP, 2016postVFP, 2017, 2018")
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

year = args.year

idjson = correctionlib.CorrectionSet.from_file("Efficiencies_ID_TRK_UL"+year+"_schemaV2.json")
trigjson = correctionlib.CorrectionSet.from_file("Efficiencies_muon_generalTracks_Z_Run"+year+"_UL_SingleMuonTriggers_schemaV2.json")

outputTitle = "h_checkEMuTTEnriched_"+year

isData = 0

if args.sample == "MC":
    isData = 0

if args.sample == "data":
    isData = 1

if args.sample == "TCP":
    isData = 0
    
ROOT.gInterpreter.Declare('#include "../../MiniAODSkimmer/interface/JetInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../../MiniAODSkimmer/interface/MuonInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../../MiniAODSkimmer/interface/ElectronInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../../MiniAODSkimmer/interface/TrigObjectInfoDS.h"')

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

def book_histogram():

    h['hEvents'] = ROOT.TH1F ("NEvents", "Number of Events; ;N", 2, 0, 2)
    h['hWeights'] = ROOT.TH1F ("hWeights", "Weights per events; weight; N", 100, 0, 2)
    
    h['Baseline1_dRMu50'] = ROOT.TH1F ("Baseline1_dRMu50", "dRMu50; dR; N", 100, 0, 5)
    h['Baseline1_dRMu8'] = ROOT.TH1F ("Baseline1_dRMu8", "dRMu8; dR; N", 100, 0, 5)
    h['Baseline1_dRMu23'] = ROOT.TH1F ("Baseline1_dRMu23", "dRMu23; dR; N", 100, 0, 5)
    h['Baseline1_dREle23'] = ROOT.TH1F ("Baseline1_dREle23", "dREle23; dR; N", 100, 0, 5)
    h['Baseline1_dREle12'] = ROOT.TH1F ("Baseline1_dREle12", "dREle12; dR; N", 100, 0, 5)

    h['Baseline2_dRMu50'] = ROOT.TH1F ("Baseline2_dRMu50", "dRMu50; dR; N", 100, 0, 5)
    h['Baseline2_dRMu8'] = ROOT.TH1F ("Baseline2_dRMu8", "dRMu8; dR; N", 100, 0, 5)
    h['Baseline2_dRMu23'] = ROOT.TH1F ("Baseline2_dRMu23", "dRMu23; dR; N", 100, 0, 5)
    h['Baseline2_dREle23'] = ROOT.TH1F ("Baseline2_dREle23", "dREle23; dR; N", 100, 0, 5)
    h['Baseline2_dREle12'] = ROOT.TH1F ("Baseline2_dREle12", "dREle12; dR; N", 100, 0, 5)


def book_event_histogram(region):

    h[region+"_Count"] = ROOT.TH1F (region+"_Count", region+"_Count ; Events ; Events ", 1, 0, 1)

    h[region+"_Mass"] = ROOT.TH1F (region+"_Mass", region+"_Mass ; M_{vis.} (GeV) ; Events ", 150, 0, 150)
    h[region+"_Lepton1Pt"] = ROOT.TH1F (region+"_Lepton1Pt", region+"_Lepton1Pt ; P_{T} (GeV) ; Events ", 500, 0, 500)
    h[region+"_Lepton2Pt"] = ROOT.TH1F (region+"_Lepton2Pt", region+"_Lepton2Pt ; P_{T} (GeV) ; Events ", 500, 0, 500)

    h[region+"_Lepton1Eta"] = ROOT.TH1F (region+"_Lepton1Eta", region+"_Lepton1Eta ; Eta ; Events ", 100, -2.5, 2.5)
    h[region+"_Lepton2Eta"] = ROOT.TH1F (region+"_Lepton2Eta", region+"_Lepton2Eta ; Eta ; Events ", 100, -2.5, 2.5)
    
    h[region+"_LeadingJetPt"] = ROOT.TH1F (region+"_LeadingJetPt", region+"_LeadingJetPt ; LedingJetP_{T} (GeV) ; Events ", 2000, 0, 2000)
    h[region+"_LeadingJetEta"] = ROOT.TH1F (region+"_LeadingJetEta", region+"_LeadingJetEta ; Eta ; Events ", 100, -2.5, 2.5)
    
    h[region+"_MetPt"] = ROOT.TH1F (region+"_MetPt", region+"_MetPt ; MET (GeV) ; Events ", 500, 0, 500)
    h[region+"_Nj"] = ROOT.TH1F (region+"_Nj", region+"_Nj ; N_{j} ; Events ", 10, 0, 10)
    h[region+"_Nbjet"] = ROOT.TH1F (region+"_Nbjet", region+"_Nbjet ; N_{bjet} ; Events ", 10, 0, 10)
    h[region+"_dRl"] = ROOT.TH1F (region+"_dRl", region+"_dRl ; dR(leptons) ; Events", 100, 0, 5)
    h[region+"_dRl1j"] = ROOT.TH1F (region+"_dRl1j", region+"_dRl1j ; dR(jet, l1) ; Events", 100, 0, 5)
    h[region+"_dRl2j"] = ROOT.TH1F (region+"_dRl2j", region+"_dRl2j ; dR(jet, l2) ; Events", 100, 0, 5)
    h[region+"_HT"] = ROOT.TH1F (region+"_HT", region+"_HT ; HT ; Events", 2000, 0, 2000)



def get_TLorentzVector(obj):
    
    v = ROOT.TLorentzVector()
    v.SetPtEtaPhiM(obj.pt, obj.eta, obj.phi, obj.mass)

    return v

def plot_variable(region, l1, l2, j, m, sf=1):

    if region not in region_list:
        book_event_histogram(region)
        region_list.append(region)

    h[region+"_Count"].Fill(0, weight*sf)

    h[region+"_Mass"].Fill((l1+l2).M(), weight*sf)
    h[region+"_Lepton1Pt"].Fill(l1.Pt(), weight*sf)
    h[region+"_Lepton2Pt"].Fill(l2.Pt(), weight*sf)
    
    h[region+"_Lepton1Eta"].Fill(l1.Eta(), weight*sf)
    h[region+"_Lepton2Eta"].Fill(l2.Eta(), weight*sf)

    h[region+"_LeadingJetPt"].Fill(j.Pt(), weight*sf)    
    h[region+"_LeadingJetEta"].Fill(j.Eta(), weight*sf)
                                 
    h[region+"_MetPt"].Fill(m.Pt(), weight*sf)
    h[region+"_Nj"].Fill(len(s_jet), weight*sf)
    h[region+"_Nbjet"].Fill(len(s_bjet), weight*sf)
    h[region+"_dRl"].Fill(l1.DeltaR(l2), weight*sf)
    h[region+"_dRl1j"].Fill(j.DeltaR(l1), weight*sf)
    h[region+"_dRl2j"].Fill(j.DeltaR(l2), weight*sf)
    h[region+"_HT"].Fill(ht, weight*sf)


def emu_channel(baseline, muons, electrons, jets):

    mu = get_TLorentzVector(muons[0])
    e = get_TLorentzVector(electrons[0])
    j = get_TLorentzVector(jets[0])

    if j.Pt() < event_cut['jetpt'] : return
    if isMET == 0 : return

    isMatchedMu50 = False
    
    for ito in tOisMuon50:
        if isMatchedMu50 == True : break
        trigObject = get_TLorentzVector(ito)
        h[baseline+'_dRMu50'].Fill(trigObject.DeltaR(mu), weight)
        if trigObject.DeltaR(mu) < 0.1 :
            isMatchedMu50 = True

    isMatchedMu8 = False
    isMatchedEle23 = False

    for ito in tOisMu8:
        if isMatchedMu8 == True : break
        trigObject = get_TLorentzVector(ito)
        h[baseline+'_dRMu8'].Fill(trigObject.DeltaR(mu), weight)
        if trigObject.DeltaR(mu) < 0.1 :
            isMatchedMu8 = True

    for ito in tOisEle23:
        if isMatchedEle23 == True : break
        trigObject = get_TLorentzVector(ito)
        h[baseline+'_dREle23'].Fill(trigObject.DeltaR(e), weight)
        if trigObject.DeltaR(e) < 0.1 :
            isMatchedEle23 = True

    isMatchedMu8Ele23 = False
    if isMatchedMu8 == True and isMatchedEle23 == True : isMatchedMu8Ele23 = True
            
    isMatchedMu23 = False
    isMatchedEle12 = False

    for ito in tOisMu23:
        if isMatchedMu23 == True: break
        trigObject = get_TLorentzVector(ito)
        h[baseline+'_dRMu23'].Fill(trigObject.DeltaR(mu), weight)
        if trigObject.DeltaR(mu) < 0.1:
            isMatchedMu23 = True

    for ito in tOisEle12:
        if isMatchedEle12 == True: break
        trigObject = get_TLorentzVector(ito)
        h[baseline+'_dREle12'].Fill(trigObject.DeltaR(e), weight)
        if trigObject.DeltaR(e) < 0.1:
            isMatchedEle12 = True

    isMatchedMu23Ele12 = False
    if isMatchedMu23 == True and isMatchedEle12 == True : isMatchedMu23Ele12 = True
            
    plot_variable(baseline, e, mu, j, met)

    if e.DeltaR(mu) < 0.4 and j.DeltaR(e+mu) > 0.8 and met.Pt() > 100:
        
        plot_variable(baseline+"_nolepcut", e, mu, j, met)

        if e.Pt() > 15 :
            plot_variable(baseline+"_e15Ptcut", e, mu, j, met)
        if mu.Pt() > 25 :
            plot_variable(baseline+"_mu25Ptcut", e, mu, j, met)
        if e.Pt() > 15 and mu.Pt() > 25 :
            plot_variable(baseline+"_e15mu25Ptcut", e, mu, j, met)

        if e.Pt() > 25 :
            plot_variable(baseline+"_e25Ptcut", e, mu, j, met)
        if mu.Pt() > 10 :
            plot_variable(baseline+"_mu10Ptcut", e, mu, j, met)
        if e.Pt() > 25 and mu.Pt() > 10 :
            plot_variable(baseline+"_e25mu10Ptcut", e, mu, j, met)

        if ( e.Pt() > 15 and mu.Pt() > 25 ) or ( e.Pt() > 25 and mu.Pt() > 10 ):
            plot_variable(baseline+"_e15mu25PtcutORe25mu10Ptcut", e, mu, j, met)

        if isMatchedMu50 == True :
            plot_variable(baseline+"_isMatchedMu50", e, mu, j, met)

        if isMatchedMu23Ele12 == True :
            plot_variable(baseline+"_isMatchedMu23Ele12", e, mu, j, met)
            if e.Pt() > 15 :
                plot_variable(baseline+"_isMatchedMu23Ele12_ePtcut", e, mu, j, met)
            if mu.Pt() > 25 :
                plot_variable(baseline+"_isMatchedMu23Ele12_muPtcut", e, mu, j, met)
            if e.Pt() > 15 and mu.Pt() > 25 :
                plot_variable(baseline+"_isMatchedMu23Ele12_lepPtcut", e, mu, j, met)
            
        if isMatchedMu8Ele23 == True :
            plot_variable(baseline+"_isMatchedMu8Ele23", e, mu, j, met)
            if e.Pt() > 25 :
                plot_variable(baseline+"_isMatchedMu8Ele23_ePtcut", e, mu, j, met)
            if mu.Pt() > 10 :
                plot_variable(baseline+"_isMatchedMu8Ele23_muPtcut", e, mu, j, met)
            if e.Pt() > 25 and mu.Pt() > 10 :
                plot_variable(baseline+"_isMatchedMu8Ele23_lepPtcut", e, mu, j, met)

        if ( isMatchedMu23Ele12 == True and e.Pt() > 15 and mu.Pt() > 25 ) or ( isMatchedMu8Ele23 == True and e.Pt() > 25 and mu.Pt() > 10 ):
            plot_variable(baseline+"_isMatchedMu23Ele12ORisMatchedMu8Ele23_lepPtcut", e, mu, j, met)
            
        if isMu8Ele23 == 1 :
            plot_variable(baseline+"_isMu8Ele23", e, mu, j, met)
            if e.Pt() > 25 :
                plot_variable(baseline+"_isMu8Ele23_ePtcut", e, mu, j, met)
            if mu.Pt() > 10 :
                plot_variable(baseline+"_isMu8Ele23_muPtcut", e, mu, j, met)
            if e.Pt() > 25 and mu.Pt() > 10 :
                plot_variable(baseline+"_isMu8Ele23_lepPtcut", e, mu, j, met)

        if isMu23Ele12 == 1 :
            plot_variable(baseline+"_isMu23Ele12", e, mu, j, met)
            if e.Pt() > 15 :
                plot_variable(baseline+"_isMu23Ele12_ePtcut", e, mu, j, met)
            if mu.Pt() > 25 :
                plot_variable(baseline+"_isMu23Ele12_muPtcut", e, mu, j, met)
            if e.Pt() > 15 and mu.Pt() > 25 :
                plot_variable(baseline+"_isMu23Ele12_lepPtcut", e, mu, j, met)


            
book_histogram()
region_list = []

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
trigObj = ROOT.TrigObjectInfoDS()

fchain.SetBranchAddress("Jets", ROOT.AddressOf(jets))
fchain.SetBranchAddress("Muons", ROOT.AddressOf(muons))
fchain.SetBranchAddress("Electrons", ROOT.AddressOf(electrons))
fchain.SetBranchAddress("TriggerObjects", ROOT.AddressOf(trigObj))

for iev in range(fchain.GetEntries()): # Be careful!!!                                                               

    fchain.GetEntry(iev)

    mets = fchain.GetBranch("Mets")
    met_pt = mets.GetLeaf('pt').GetValue()
    met_phi = mets.GetLeaf('phi').GetValue()

    met = ROOT.TLorentzVector()
    met.SetPtEtaPhiM(met_pt, 0, met_phi, 0)

    if isData == 0 :
        genweight = fchain.GetLeaf('genWeight').GetValue()
        puweight = fchain.GetLeaf('puWeight').GetValue()
        prweight = fchain.GetLeaf('prefiringWeight').GetValue()
    else :
        genweight = 1
        puweight = 1
        prweight = 1

    weight = genweight*puweight*prweight

    h['hEvents'].Fill(0.5, 1)
    h['hEvents'].Fill(1.5, genweight)
    h['hWeights'].Fill(weight)

    #-------------- Trigger Objects ---------------#
    
    tOisMuonEGe = []
    tOisMuonEGmu = []
    tOisMuon50 = []
    tOisMu8 = []
    tOisMu23 = []
    tOisEle23 = []
    tOisEle12 = []

    if trigObj.size() > 0:
        for i in range(trigObj.size()):
            iobj = trigObj.at(i)
            if iobj.isMuonEGmu == 1 : tOisMuonEGmu+=[iobj]
            if iobj.isMuonEGe == 1 : tOisMuonEGe+=[iobj]
            if iobj.isMu == 1 : tOisMuon50+=[iobj]
            if iobj.isMu8 == 1 : tOisMu8+=[iobj]
            if iobj.isMu23 == 1 : tOisMu23+=[iobj]
            if iobj.isEle23 == 1 : tOisEle23+=[iobj]
            if iobj.isEle12 == 1 : tOisEle12+=[iobj]
                
    tOisMuonEGmu.sort(key=lambda x: x.pt, reverse=True)
    tOisMuonEGe.sort(key=lambda x: x.pt, reverse=True)
    tOisMuon50.sort(key=lambda x: x.pt, reverse=True)
    tOisMu8.sort(key=lambda x: x.pt, reverse=True)
    tOisMu23.sort(key=lambda x: x.pt, reverse=True)
    tOisEle23.sort(key=lambda x: x.pt, reverse=True)
    tOisEle12.sort(key=lambda x: x.pt, reverse=True)

    #------------ HLT flags --------------#
    
    isMuonEG = fchain.GetLeaf('isMuonEG').GetValue()
    isMu = fchain.GetLeaf('isMu').GetValue()
    isMu8Ele23 = fchain.GetLeaf('isMu8Ele23').GetValue()
    isMu23Ele12 = fchain.GetLeaf('isMu23Ele12').GetValue()
    isMET = fchain.GetLeaf('isMET').GetValue()
    
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
    ht = 0

    if jets.size() > 0:
        for i in range(jets.size()):
            ijet = jets.at(i)
            if abs(ijet.eta) < 2.5 :
                if ijet.id >= 2:
                    ht = ht + ijet.pt
                    s_jet+=[ijet]
                    if ijet.deepjet >= 0.7476:
                        s_bjet+=[ijet]

    s_muon = []

    if muons.size() > 0:
        for i in range(muons.size()):
            imuon = muons.at(i)
            if abs(imuon.eta) < 2.4 :
                if imuon.id >= 1: 
                    if imuon.iso <= 0.25:
                        s_muon+=[imuon]

    s_electron = []

    if electrons.size() > 0:
        for i in range(electrons.size()):
            ielectron = electrons.at(i)
            if abs(ielectron.eta) < 2.5 :
                if ielectron.id >= 1 :
                    if ielectron.iso >= 1:
                        s_electron+=[ielectron]

                        
     # ---------- Event Selections --------- #

    if len(s_muon) > 0 and len(s_electron) > 0 and s_muon[0].charge*s_electron[0].charge < 0 and len(s_jet) > 0 and len(s_bjet) > 0 :
        emu_channel("Baseline1", s_muon, s_electron, s_jet)

    if isData == 0:
        if len(s_muon) > 0 and len(s_electron) > 0 and s_muon[0].charge*s_electron[0].charge < 0 and len(s_jet) > 0 and len(s_bjet) == 0 :
            emu_channel("Baseline2", s_muon, s_electron, s_jet)


         
out.cd()

for key in h.keys():
    h[key].Write()

out.Close()

print("--- %s seconds ---" % (time.time() - start_time))
