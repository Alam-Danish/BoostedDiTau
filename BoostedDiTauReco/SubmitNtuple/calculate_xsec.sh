#!/bin/bash
# calculate_xsec.sh
# Runs GenXSecAnalyzer for all samples and saves results to xsec_results.txt
# Usage: bash calculate_xsec.sh

OUTPUT="tcp_xsec_results.txt"
echo "Sample, xsec_pb, uncertainty_pb" > $OUTPUT

START_TIME=$SECONDS
echo "Started at: $(date)"
# GenXSecAnalyzer cfg template
cat > xsec_cfg.py << 'PYCFG'
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
PYCFG

# Sample list
declare -A SAMPLES

# DY MLL-4to50:
SAMPLES["ALP_M-10_HT-100to400"]="/GluGluALPtoTauTau_Bin-HT-100to400_Par-M-10_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v3/MINIAODSIM"
SAMPLES["ALP_M-15_HT-100to400"]="/GluGluALPtoTauTau_Bin-HT-100to400_Par-M-15_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-20_HT-100to400"]="/GluGluALPtoTauTau_Bin-HT-100to400_Par-M-20_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-25_HT-100to400"]="/GluGluALPtoTauTau_Bin-HT-100to400_Par-M-25_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-30_HT-100to400"]="/GluGluALPtoTauTau_Bin-HT-100to400_Par-M-30_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-35_HT-100to400"]="/GluGluALPtoTauTau_Bin-HT-100to400_Par-M-35_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-40_HT-100to400"]="/GluGluALPtoTauTau_Bin-HT-100to400_Par-M-40_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-45_HT-100to400"]="/GluGluALPtoTauTau_Bin-HT-100to400_Par-M-45_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-50_HT-100to400"]="/GluGluALPtoTauTau_Bin-HT-100to400_Par-M-50_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-55_HT-100to400"]="/GluGluALPtoTauTau_Bin-HT-100to400_Par-M-55_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-60_HT-100to400"]="/GluGluALPtoTauTau_Bin-HT-100to400_Par-M-60_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-65_HT-100to400"]="/GluGluALPtoTauTau_Bin-HT-100to400_Par-M-65_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"

# ── 2024 HT-400toInf ─────────────────────────────────────────────
SAMPLES["ALP_M-10_HT-400toInf"]="/GluGluALPtoTauTau_Bin-HT-400toInf_Par-M-10_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-15_HT-400toInf"]="/GluGluALPtoTauTau_Bin-HT-400toInf_Par-M-15_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-20_HT-400toInf"]="/GluGluALPtoTauTau_Bin-HT-400toInf_Par-M-20_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-25_HT-400toInf"]="/GluGluALPtoTauTau_Bin-HT-400toInf_Par-M-25_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-30_HT-400toInf"]="/GluGluALPtoTauTau_Bin-HT-400toInf_Par-M-30_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-35_HT-400toInf"]="/GluGluALPtoTauTau_Bin-HT-400toInf_Par-M-35_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-40_HT-400toInf"]="/GluGluALPtoTauTau_Bin-HT-400toInf_Par-M-40_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-45_HT-400toInf"]="/GluGluALPtoTauTau_Bin-HT-400toInf_Par-M-45_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-50_HT-400toInf"]="/GluGluALPtoTauTau_Bin-HT-400toInf_Par-M-50_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-55_HT-400toInf"]="/GluGluALPtoTauTau_Bin-HT-400toInf_Par-M-55_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-60_HT-400toInf"]="/GluGluALPtoTauTau_Bin-HT-400toInf_Par-M-60_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
SAMPLES["ALP_M-65_HT-400toInf"]="/GluGluALPtoTauTau_Bin-HT-400toInf_Par-M-65_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM"
# Main loop
# Replace the Main loop section with this:
for name in "${!SAMPLES[@]}"; do
    dataset="${SAMPLES[$name]}"
    echo "=============================="
    echo "Processing: $name"

    fname=$(dasgoclient --query="file dataset=$dataset" --limit 1 2>/dev/null)

    if [ -z "$fname" ]; then
        echo "  ERROR: no file found for $dataset"
        echo "$name, ERROR, ERROR" >> $OUTPUT
        continue
    fi

    echo "  file: $fname"

    sed "s|FILENAME_PLACEHOLDER|root://cms-xrd-global.cern.ch/$fname|" xsec_cfg.py > xsec_cfg_tmp.py

    # ── Save full output to log file first ──────────────────────
    LOGFILE="xsec_log_${name}.txt"
    cmsRun xsec_cfg_tmp.py > $LOGFILE 2>&1

    # ── Then extract from log ────────────────────────────────────
    result=$(grep "After filter: final cross section" $LOGFILE)
    echo "  raw result: $result"

    xsec=$(echo "$result" | grep -oP '[\d.e+-]+(?= \+-)' | head -1)
    unc=$(echo  "$result" | grep -oP '(?<=\+- )[\d.e+-]+' | head -1)

    if [ -z "$xsec" ]; then
        echo "  ERROR: could not extract xsec — check $LOGFILE"
        echo "$name, ERROR, ERROR" >> $OUTPUT
    else
        echo "  xsec = $xsec +- $unc pb"
        echo "$name, $xsec, $unc" >> $OUTPUT
    fi

    # ── Clean up log after successful extraction ─────────────────
    rm -f $LOGFILE
done

TOTAL_TIME=$((SECONDS-START_TIME))
MINUTES=$((TOTAL_TIME/60))
SECS=$((TOTAL_TIME%60))

echo ""
echo "=============================="
echo "Done at: $(date)"
echo "Total time: ${MINUTES}m ${SECS}s for $TOTAL samples"
echo "=============================="
cat $OUTPUT
