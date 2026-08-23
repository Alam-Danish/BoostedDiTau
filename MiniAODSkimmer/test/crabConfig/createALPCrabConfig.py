import os, sys, subprocess

mass    = [ str(x) for x in range(10,70,5) ]
HT      = ['100to400', '400toInf']
version = 'v1'
year    = '2023BPix'

eos_input_base  = '/store/user/dalam/signalMC/Run3/2023BPix/run3_2023BPix_miniAODv4_TCP'
eos_output_base = '/store/user/dalam/TCPNtuple/Run3/2023BPix'
eos_server      = 'root://cmseos.fnal.gov'

def list_eos_files(eos_dir):
    """List ROOT files in an EOS directory via xrdfs."""
    cmd = ['xrdfs', 'root://cmseos.fnal.gov', 'ls', eos_dir]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  WARNING: could not list {eos_dir}")
        return []
    files = [
        f'root://cmseos.fnal.gov/{line.strip()}'
        for line in result.stdout.strip().split('\n')
        if line.strip().endswith('.root')
    ]
    return files

print("Listing EOS directory...")
all_files = list_eos_files(eos_input_base)
print(f"Found {len(all_files)} total ROOT files\n")

for m in mass:
    for ht in HT:
        
        prefix = f'ALP_M-{m}_HT-{ht}_{year}_MiniAODv4_'

        sample_files = [
            f
            for f in all_files
            if os.path.basename(f).startswith(prefix)
        ]
        print(sample_files)

        if not sample_files:
            print(f"SKIP: no files matched prefix {prefix}")
            continue

        print(f"ALP_M-{m}_HT-{ht}: {len(sample_files)} files")

        fname = "crabConfig_ALP_M-"+m+"_HT-"+ht+"_"+year+".py"
        print(fname)
        f = open(fname, "w")
        f.writelines(f"""
from CRABClient.UserUtilities import config

config = config()
config.General.requestName = 'Ntuple_ALP_M-{m}_HT-{ht}_{year}_MiniAODv4_{version}'

config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 2500

config.JobType.psetName = '../rerunTauRecoOnMiniAOD_WithClean_Custom.py'

#config.JobType.pyCFGParams = [
#    'runType=signal',
#    'year={year}',
#]

#config.Data.inputDataset = '/AToTauTau_ALP_M-{m}_HT-{ht}_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM'
#config.Data.inputDataset = '/GluGluALPtoTauTau_Bin-HT-{ht}_Par-M-{m}_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM'
config.Data.userInputFiles = {sample_files}
config.Data.inputDBS = 'global'
#config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outputPrimaryDataset = 'ALP_M-{m}_HT-{ht}_{year}'

config.Data.outLFNDirBase = '{eos_output_base}'
#config.Data.outLFNDirBase = '/store/user/dalam/TCPNtuple/'
config.Data.publication = False
config.Data.outputDatasetTag = 'Ntuple_ALP_M-{m}_HT-{ht}_{year}_MiniAODv4_{version}'
#config.Data.outputDatasetTag = 'Ntuple_ALP_M-{m}_HT-{ht}_{year}_MiniAODv4_{version}'

#config.Site.storageSite = 'T3_US_FNALLPC'
config.Site.storageSite = 'T2_US_Florida'
#config.Site.whitelist = ['T2_US_Florida']      # only if you want to run the jobs on T2 Florida
config.Site.whitelist = ['T3_US_FNALLPC']       # only if you want to run the jobs on T3 FNAL

config.Site.ignoreGlobalBlacklist = True

#config.Data.ignoreLocality = True              # only if the running jobs and input files are on two different sites
""")
        f.close()

print("\nDone. To submit all:")
print("  for f in crabConfig_ALP_M-*.py; do crab submit $f; done")
