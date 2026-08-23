#!/bin/bash
# submit_xsec_condor.sh
# Submits one condor job per sample for GenXSecAnalyzer with 1M events

mkdir -p xsec_jobs/logs
mkdir -p xsec_jobs/cfgs
mkdir -p xsec_jobs/results

declare -A SAMPLES

# DY MLL-4to50:
SAMPLES["DYto2L-4Jets_MLL-4to50_HT-40to70"]="/DYto2L-4Jets_MLL-4to50_HT-40to70_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v3/MINIAODSIM"
SAMPLES["DYto2L-4Jets_MLL-4to50_HT-70to100"]="/DYto2L-4Jets_MLL-4to50_HT-70to100_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v3/MINIAODSIM"
SAMPLES["DYto2L-4Jets_MLL-4to50_HT-100to400"]="/DYto2L-4Jets_MLL-4to50_HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v4/MINIAODSIM"
SAMPLES["DYto2L-4Jets_MLL-4to50_HT-400to800"]="/DYto2L-4Jets_MLL-4to50_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v3/MINIAODSIM"
SAMPLES["DYto2L-4Jets_MLL-4to50_HT-800to1500"]="/DYto2L-4Jets_MLL-4to50_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v3/MINIAODSIM"
SAMPLES["DYto2L-4Jets_MLL-4to50_HT-1500to2500"]="/DYto2L-4Jets_MLL-4to50_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v3/MINIAODSIM"
SAMPLES["DYto2L-4Jets_MLL-4to50_HT-2500"]="/DYto2L-4Jets_MLL-4to50_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"

# DY MLL-50to120:
SAMPLES["DYto2L-4Jets_MLL-50to120_HT-40to70"]="/DYto2L-4Jets_MLL-50to120_HT-40to70_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["DYto2L-4Jets_MLL-50to120_HT-70to100"]="/DYto2L-4Jets_MLL-50to120_HT-70to100_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["DYto2L-4Jets_MLL-50to120_HT-100to400"]="/DYto2L-4Jets_MLL-50to120_HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["DYto2L-4Jets_MLL-50to120_HT-400to800"]="/DYto2L-4Jets_MLL-50to120_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["DYto2L-4Jets_MLL-50to120_HT-800to1500"]="/DYto2L-4Jets_MLL-50to120_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v3/MINIAODSIM"
SAMPLES["DYto2L-4Jets_MLL-50to120_HT-1500to2500"]="/DYto2L-4Jets_MLL-50to120_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v3/MINIAODSIM"
SAMPLES["DYto2L-4Jets_MLL-50to120_HT-2500"]="/DYto2L-4Jets_MLL-50to120_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v4/MINIAODSIM"

# DY MLL-120:
SAMPLES["DYto2L-4Jets_MLL-120_HT-40to70"]="/DYto2L-4Jets_MLL-120_HT-40to70_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v3/MINIAODSIM"
SAMPLES["DYto2L-4Jets_MLL-120_HT-70to100"]="/DYto2L-4Jets_MLL-120_HT-70to100_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v3/MINIAODSIM"
SAMPLES["DYto2L-4Jets_MLL-120_HT-100to400"]="/DYto2L-4Jets_MLL-120_HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v3/MINIAODSIM"
SAMPLES["DYto2L-4Jets_MLL-120_HT-400to800"]="/DYto2L-4Jets_MLL-120_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v3/MINIAODSIM"
SAMPLES["DYto2L-4Jets_MLL-120_HT-800to1500"]="/DYto2L-4Jets_MLL-120_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v3/MINIAODSIM"
SAMPLES["DYto2L-4Jets_MLL-120_HT-1500to2500"]="/DYto2L-4Jets_MLL-120_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v3/MINIAODSIM"
SAMPLES["DYto2L-4Jets_MLL-120_HT-2500"]="/DYto2L-4Jets_MLL-120_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v3/MINIAODSIM"

# WJets MLNu-0to120:
SAMPLES["WtoLNu-4Jets_MLNu-0to120_HT-40to100"]="/WtoLNu-4Jets_MLNu-0to120_HT-40to100_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v3/MINIAODSIM"
SAMPLES["WtoLNu-4Jets_MLNu-0to120_HT-100to400"]="/WtoLNu-4Jets_MLNu-0to120_HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v3/MINIAODSIM"
SAMPLES["WtoLNu-4Jets_MLNu-0to120_HT-400to800"]="/WtoLNu-4Jets_MLNu-0to120_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v1/MINIAODSIM"
SAMPLES["WtoLNu-4Jets_MLNu-0to120_HT-800to1500"]="/WtoLNu-4Jets_MLNu-0to120_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["WtoLNu-4Jets_MLNu-0to120_HT-1500to2500"]="/WtoLNu-4Jets_MLNu-0to120_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["WtoLNu-4Jets_MLNu-0to120_HT-2500"]="/WtoLNu-4Jets_MLNu-0to120_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"

# WJets MLNu-120:
SAMPLES["WtoLNu-4Jets_MLNu-120_HT-40to100"]="/WtoLNu-4Jets_MLNu-120_HT-40to100_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["WtoLNu-4Jets_MLNu-120_HT-100to400"]="/WtoLNu-4Jets_MLNu-120_HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["WtoLNu-4Jets_MLNu-120_HT-400to800"]="/WtoLNu-4Jets_MLNu-120_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["WtoLNu-4Jets_MLNu-120_HT-800to1500"]="/WtoLNu-4Jets_MLNu-120_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["WtoLNu-4Jets_MLNu-120_HT-1500to2500"]="/WtoLNu-4Jets_MLNu-120_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["WtoLNu-4Jets_MLNu-120_HT-2500"]="/WtoLNu-4Jets_MLNu-120_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"

# TT:
SAMPLES["TTto2L2Nu"]="/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["TTtoLNu2Q"]="/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["TTto4Q"]="/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"

# ST:
SAMPLES["ST_s_top"]="/TBbartoLplusNuBbar-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["ST_s_antitop"]="/TbarBtoLminusNuB-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["ST_t_top"]="/TBbarQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["ST_t_antitop"]="/TbarBQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["ST_tW_top"]="/TWminus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["ST_tW_antitop"]="/TbarWplus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"

# Diboson:
SAMPLES["WWto2L2Nu"]="/WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["WWtoLNu2Q"]="/WWtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["WWto4Q"]="/WWto4Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["WZto3LNu"]="/WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["WZtoLNu2Q"]="/WZtoLNu2Q-1Jets-4FS_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["WZto2L2Q"]="/WZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["WZto4Q"]="/WZto4Q-1Jets-4FS_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["ZZto2L2Nu"]="/ZZto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["ZZto2L2Q"]="/ZZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["ZZto2Nu2Q"]="/ZZto2Nu2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"
SAMPLES["ZZto4L"]="/ZZto4L_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM"

# ── Create and submit one condor job per sample ───────────────────
for name in "${!SAMPLES[@]}"; do
    dataset="${SAMPLES[$name]}"

    # Get one file:
    fname=$(dasgoclient --query="file dataset=$dataset" --limit 1 2>/dev/null)
    if [ -z "$fname" ]; then
        echo "ERROR: no file found for $name"
        continue
    fi

    # Write CMSSW cfg:
    cat > xsec_jobs/cfgs/xsec_${name}.py << EOF
import FWCore.ParameterSet.Config as cms
process = cms.Process("XSEC")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000000))
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring("root://cms-xrd-global.cern.ch/$fname")
)
process.genxsec = cms.EDAnalyzer("GenXSecAnalyzer")
process.p = cms.Path(process.genxsec)
EOF

# Write executable — use absolute paths:
    CMSSW_BASE_DIR=$(pwd)
    RESULTS_DIR=$(pwd)/xsec_jobs/results
    CFG_FILE=$(pwd)/xsec_jobs/cfgs/xsec_${name}.py

    cat > xsec_jobs/cfgs/run_${name}.sh << EOF
#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=el8_amd64_gcc11
cd ${CMSSW_BASE_DIR}
eval \$(scramv1 runtime -sh)
mkdir -p ${RESULTS_DIR}
cmsRun ${CFG_FILE} 2>&1 | grep "After filter: final cross section" | awk '{print "${name}, "\$7", "\$9}' > ${RESULTS_DIR}/${name}.txt
echo "Done: ${name}" >> ${RESULTS_DIR}/${name}.txt
EOF
    chmod +x xsec_jobs/cfgs/run_${name}.sh

    # Write condor submit file:
cat > xsec_jobs/cfgs/condor_${name}.sub << EOF
Universe     = vanilla
Executable   = xsec_jobs/cfgs/run_${name}.sh
Output       = xsec_jobs/logs/${name}.out
Error        = xsec_jobs/logs/${name}.err
Log          = xsec_jobs/logs/${name}.log
+ApptainerImage = "/cvmfs/singularity.opensciencegrid.org/cmssw/cms:rhel8"
request_cpus   = 1
request_memory = 2GB
request_disk   = 2GB
should_transfer_files   = NO
queue 1
EOF

    condor_submit xsec_jobs/cfgs/condor_${name}.sub
    echo "Submitted: $name"
done

echo ""
echo "All jobs submitted. Monitor with: condor_q"
echo "Collect results with: cat xsec_jobs/results/*.txt | tee xsec_results_1M.txt"
