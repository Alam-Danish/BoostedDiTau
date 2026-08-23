# checkBtag.py
import ROOT
ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.gSystem.Load("libDataFormatsFWLite.so")
ROOT.FWLiteEnabler.enable()

from DataFormats.FWLite import Events, Handle

events = Events('../../../../../../test_TCP/CMSSW_13_0_13/src/AToTauTau/ALP/ALP_M-30_HT-400toInf_2022preEE_MiniAODv4_1162346_1.root')
handle = Handle('vector<pat::Jet>')
label  = ('slimmedJetsPuppi', '', 'PAT')

for event in events:
    event.getByLabel(label, handle)
    jets = handle.product()
    if jets.size() > 0:
        jet = jets[0]
        print("=== Available b-tag discriminators ===")
        for name, val in jet.getPairDiscri():
            print(f"  {name} : {val:.4f}")
        break  # only need first event
