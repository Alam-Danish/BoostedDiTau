# checkLowPtEle.py
import ROOT
ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.gSystem.Load("libDataFormatsFWLite.so")
ROOT.FWLiteEnabler.enable()

from DataFormats.FWLite import Events, Handle

events = Events('../../../../../../test_TCP/CMSSW_13_0_13/src/AToTauTau/ALP/ALP_M-30_HT-400toInf_2022preEE_MiniAODv4_1162346_1.root')
handle = Handle('vector<pat::Electron>')
label  = ('slimmedLowPtElectrons', '', 'PAT')

for event in events:
    event.getByLabel(label, handle)
    electrons = handle.product()
    if electrons.size() > 0:
        ele = electrons[0]
        print("=== Available low-pT electron IDs ===")
        for id_pair in ele.electronIDs():
            print(f"  {id_pair.first} : {id_pair.second:.4f}")
        break
