#!/usr/bin/env python3
# convert_central_mu50_SF_to_histogram.py

import ROOT
import correctionlib
import numpy as np

# -------------------------------------------------
# Style options
# -------------------------------------------------
ROOT.gStyle.SetOptStat(0)   # Remove statistics box

# -------------------------------------------------
# Bin definitions
# -------------------------------------------------
abseta_bins = [0.0, 0.9, 1.2, 2.1, 2.4]
pt_bins     = [50.0, 55.0, 60.0, 80.0, 120.0, 200.0, 1200.0]

n_abseta = len(abseta_bins) - 1
n_pt     = len(pt_bins) - 1

abseta_arr = np.array(abseta_bins, dtype='d')
pt_arr     = np.array(pt_bins,     dtype='d')

# -------------------------------------------------
# Load correction set
# -------------------------------------------------
cset = correctionlib.CorrectionSet.from_file(
    '/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/MUO/2022_Summer22/muon_Z.json.gz'
)

# Central key uses GlobalHighPt + TkIsoLoose denominator
sf_key = 'NUM_Mu50_or_CascadeMu100_or_HighPtTkMu100_DEN_CutBasedIdGlobalHighPt_and_TkIsoLoose'
sf_corr = cset[sf_key]

print('Central SF key:', sf_key)
print('Available keys:', list(cset.keys()))

# -------------------------------------------------
# Create histograms
# -------------------------------------------------
h_central = ROOT.TH2F(
    'central_SF',
    'NUM_Mu50_or_CascadeMu100_or_HighPtTkMu100_DEN_CutBasedIdGlobalHighPt_and_TkIsoLoose;|#eta|;p_{T} (GeV)',
    n_abseta, abseta_arr,
    n_pt, pt_arr
)

h_central_up = ROOT.TH2F(
    'central_SF_up',
    'Central SF systup;|#eta|;p_{T} (GeV)',
    n_abseta, abseta_arr,
    n_pt, pt_arr
)

h_central_down = ROOT.TH2F(
    'central_SF_down',
    'Central SF systdown;|#eta|;p_{T} (GeV)',
    n_abseta, abseta_arr,
    n_pt, pt_arr
)

# Remove stats boxes
for h in [h_central, h_central_up, h_central_down]:
    h.SetStats(0)

# -------------------------------------------------
# Fill histograms
# -------------------------------------------------
print(f'\n{"abseta bin":<20} {"pT bin":<18} {"nominal":>10} {"systup":>10} {"systdown":>10}')
print('-' * 65)

for ieta in range(n_abseta):

    abseta_center = 0.5 * (abseta_bins[ieta] + abseta_bins[ieta + 1])

    for ipt in range(n_pt):

        pt_center = 0.5 * (pt_bins[ipt] + pt_bins[ipt + 1])

        # Clamp to last valid bin
        pt_eval = min(pt_center, 1199.0)

        try:
            nom  = sf_corr.evaluate(abseta_center, pt_eval, 'nominal')
            up   = sf_corr.evaluate(abseta_center, pt_eval, 'systup')
            down = sf_corr.evaluate(abseta_center, pt_eval, 'systdown')

        except Exception as e:
            print(f'Warning eta={abseta_center:.2f} pt={pt_eval:.0f}: {e}')
            nom, up, down = 1.0, 1.0, 1.0

        h_central.SetBinContent(ieta + 1, ipt + 1, nom)
        h_central_up.SetBinContent(ieta + 1, ipt + 1, up)
        h_central_down.SetBinContent(ieta + 1, ipt + 1, down)

        h_central.SetBinError(
            ieta + 1,
            ipt + 1,
            (up - down) / 2.0
        )

        print(
            f'|eta|=[{abseta_bins[ieta]:.1f},{abseta_bins[ieta+1]:.1f}]  '
            f'pT=[{pt_bins[ipt]:5.0f},{pt_bins[ipt+1]:6.0f}]  '
            f'{nom:10.4f}  {up:10.4f}  {down:10.4f}'
        )

# -------------------------------------------------
# Save ROOT file
# -------------------------------------------------
fout = ROOT.TFile('central_MuPOG_Mu50_SF_2022preEE.root', 'RECREATE')

h_central.Write()
h_central_up.Write()
h_central_down.Write()

fout.Close()

print('\nSaved: central_MuPOG_Mu50_SF_2022preEE.root')

# -------------------------------------------------
# Draw histogram with log-scale pT axis
# -------------------------------------------------
canvas = ROOT.TCanvas("c1", "Central SF", 900, 700)

canvas.SetLogy()   # Log scale on Y-axis (pT axis)

h_central.Draw("COLZ TEXT")

canvas.SaveAs("central_MuPOG_Mu50_SF_2022preEE.png")

print('Saved: central_MuPOG_Mu50_SF_2022preEE.png')