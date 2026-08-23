import ROOT, sys, os
import correctionlib

sfDir = os.path.join('/cvmfs','cms.cern.ch','rsync','cms-nanoAOD','jsonpog-integration','POG','BTV','2022_Summer22')
btvjson = correctionlib.CorrectionSet.from_file(os.path.join(sfDir, 'btagging.json.gz'))

WP = 'T'
h = {}

effMapFileName = "EMu_OS_BTag_Efficiency.root"
effMapFile = ROOT.TFile(effMapFileName)

h['lowMET_BFlavour'] = effMapFile.Get("TT_EMu_OS_dRcut_lowMET_BFlavour_BTagged_Eff")
h['highMET_BFlavour'] = effMapFile.Get("TT_EMu_OS_dRcut_highMET_BFlavour_BTagged_Eff")
h['lowMET_CFlavour'] = effMapFile.Get("TT_EMu_OS_dRcut_lowMET_CFlavour_BTagged_Eff")
h['highMET_CFlavour'] = effMapFile.Get("TT_EMu_OS_dRcut_highMET_CFlavour_BTagged_Eff")
h['lowMET_LFlavour'] = effMapFile.Get("TT_EMu_OS_dRcut_lowMET_LFlavour_BTagged_Eff")
h['highMET_LFlavour'] = effMapFile.Get("TT_EMu_OS_dRcut_highMET_LFlavour_BTagged_Eff")

#print(h)


def find_sf(js):

    if js.jetflavour != 5 or js.jetflavour != 4 or js.jetflavour != 0 : return 1

    if js.jetflavour == 0 :
        deepjet_col = 'deepJet_incl'

    else:
        deepjet_col = 'deepJet_comb'

    jet_sf = btvjson[deepjet_col].evaluate("central", WP, js.jetflavour, abs(js.eta), js.pt)

    return jet_sf


def get_efficiency(region, jet):

    if jet.jetflavour != 5 and jet.jetflavour != 4 and jet.jetflavour != 0 : 
        return 1

    if jet.jetflavour == 5 : flavour = "BFlavour"
    if jet.jetflavour == 4 : flavour = "CFlavour"
    if jet.jetflavour == 0 : flavour = "LFlavour"

    binPt = h[region+"_"+flavour].GetXaxis().FindBin(jet.pt)
    binEta = h[region+"_"+flavour].GetYaxis().FindBin(jet.eta)
    eff = h[region+"_"+flavour].GetBinContent(binPt, binEta)

    # binPt = h[region+"_"+flavour].GetXaxis().FindBin(2)
    # binEta = h[region+"_"+flavour].GetYaxis().FindBin(2)
    # eff = h[region+"_"+flavour].GetBinContent(binPt, binEta)
    
    # print(eff)

    return eff


def get_weight(region, jets):

    pMC = 1.0
    pData = 1.0
    bweight = 1.0

    for js in jets:

        eff = get_efficiency(region, js)
        sf = find_sf(js)

        if js.deepjet >= 0.7476 :
            pMC = pMC*eff
            pData = pData*sf*eff

        else :
            pMC = pMC*(1.0-eff)
            pData = pData*sf*(1.0-eff)

    if pMC != 0.0 :
        bweight = pData/pMC

    return bweight
