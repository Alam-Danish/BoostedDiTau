import ROOT

ROOT.gInterpreter.Declare('#include "../interface/JetInfoDS.h"')

#inputFile = 'TCPNtuple.root'
inputFile = 'TCPNtuple_v1.root'

jets = ROOT.JetInfoDS()

fchain = ROOT.TChain('tcpNtuples/analysisTree')
fchain.Add(inputFile)

fchain.SetBranchAddress("Jets", ROOT.AddressOf(jets))
met = fchain.GetBranch("Mets")
#fchain.SetBranchAddress("Mets")

print(fchain.GetEntries())

for iev in range(fchain.GetEntries()): # Be careful!!!
    fchain.GetEntry(iev)
    print(iev, met.GetLeaf('pt').GetValue(), jets.at(0).pt)
