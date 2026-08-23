import subprocess

script_to_run = "./runGfal_Alam.sh"
era           = "2022EE"

signal_samples = []
mass_values = [str(x) for x in range(10, 70, 5)]
ht_values   = ["100to400", "400toInf"]
for m in mass_values:
    for ht in ht_values:
        signal_samples.append(f"ALP_M-{m}_HT-{ht}_2022EE")

background_samples = [
    ##"DYto2L-2Jets_MLL-4to10_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
    ##"DYto2L-2Jets_MLL-10to50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
    ##"DYto2L-2Jets_MLL-50_0J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
    ##"DYto2L-2Jets_MLL-50_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
    ##"DYto2L-2Jets_MLL-50_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
    #"DYto2L-4Jets_MLL-4to50_HT-40to70_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-4to50_HT-70to100_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-4to50_HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-4to50_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-4to50_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-4to50_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-4to50_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-50to120_HT-40to70_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-50to120_HT-70to100_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-50to120_HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-50to120_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-50to120_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-50to120_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-50to120_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-120_HT-40to70_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-120_HT-70to100_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-120_HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-120_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-120_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-120_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"DYto2L-4Jets_MLL-120_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8",
    "TTto4Q_TuneCP5_13p6TeV_powheg-pythia8",
    #"TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8",
    #"TBbartoLplusNuBbar-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8",
    #"TbarBtoLminusNuB-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8",
    #"TBbarQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8",
    #"TWminus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8",
    #"TbarBQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8",
    #"TbarWplus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8",
    ##"WtoLNu-4Jets_1J_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    ##"WtoLNu-4Jets_2J_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    ##"WtoLNu-4Jets_3J_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    ##"WtoLNu-4Jets_4J_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    "WtoLNu-4Jets_MLNu-0to120_HT-40to100_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"WtoLNu-4Jets_MLNu-0to120_HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"WtoLNu-4Jets_MLNu-0to120_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"WtoLNu-4Jets_MLNu-0to120_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"WtoLNu-4Jets_MLNu-0to120_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"WtoLNu-4Jets_MLNu-0to120_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"WtoLNu-4Jets_MLNu-120_HT-40to100_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"WtoLNu-4Jets_MLNu-120_HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"WtoLNu-4Jets_MLNu-120_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"WtoLNu-4Jets_MLNu-120_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"WtoLNu-4Jets_MLNu-120_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"WtoLNu-4Jets_MLNu-120_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8",
    #"WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8",
    #"WWto4Q_TuneCP5_13p6TeV_powheg-pythia8",
    #"WWtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8",
    #"WZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8",
    #"WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8",
    #"WZtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8",
    #"WZto4Q-1Jets-4FS_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
    #"ZZto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8",
    #"ZZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8",
    #"ZZto2Nu2Q_TuneCP5_13p6TeV_powheg-pythia8",
    #"ZZto4L_TuneCP5_13p6TeV_powheg-pythia8",
]
data_samples = [
    "EGamma",
    "MuonEG",
    "SingleMuon",
    "Muon",
]

# Map each sample to its samplename category
sample_to_samplename = {}
for s in signal_samples:
    sample_to_samplename[s] = "AToTauTau"
for s in background_samples:
    if s.startswith("DYto2L-2Jets_MLL-4to10"):
        sample_to_samplename[s] = "DYJetsToLL_M-4to10"
    elif s.startswith("DYto2L-2Jets_MLL-10to50"):
        sample_to_samplename[s] = "DYJetsToLL_M-10to50"
    elif s.startswith("DYto2L-2Jets_MLL-50"):
        sample_to_samplename[s] = "DYJetsToLL_M-50"
    elif s.startswith("DYto2L-4Jets_MLL-4to50"):
        sample_to_samplename[s] = "DYJetsToLL_M-4to50"
    elif s.startswith("DYto2L-4Jets_MLL-50to120"):
        sample_to_samplename[s] = "DYJetsToLL_M-50to120"
    elif s.startswith("DYto2L-4Jets_MLL-120"):
        sample_to_samplename[s] = "DYJetsToLL_M-120"
    elif s.startswith("TTto2L2Nu"):
        sample_to_samplename[s] = "TTTo2L2Nu"
    elif s.startswith("TTto4Q"):
        sample_to_samplename[s] = "TTToHadronic"
    elif s.startswith("TTtoLNu2Q"):
        sample_to_samplename[s] = "TTToSemiLeptonic"
    elif s.startswith("TBbartoLplusNuBbar-s-channel-4FS"):
        sample_to_samplename[s] = "ST_s_top"
    elif s.startswith("TbarBtoLminusNuB-s-channel-4FS"):
        sample_to_samplename[s] = "ST_s_antitop"
    elif s.startswith("TBbarQ_t-channel_4FS"):
        sample_to_samplename[s] = "ST_t_top"
    elif s.startswith("TWminus_DR_AtLeastOneLepton"):
        sample_to_samplename[s] = "ST_tW_top"
    elif s.startswith("TbarBQ_t-channel_4FS"):
        sample_to_samplename[s] = "ST_t_antitop"
    elif s.startswith("TbarWplus_DR_AtLeastOneLepton"):
        sample_to_samplename[s] = "ST_tW_antitop"
    #elif s.startswith("WtoLNu"):
    #    sample_to_samplename[s] = "WJetsToLNu"
    elif s.startswith("WtoLNu-4Jets_MLNu-0to120"):
        sample_to_samplename[s] = "WJetsToLNu_MLNu-0to120"
    elif s.startswith("WtoLNu-4Jets_MLNu-120"):
        sample_to_samplename[s] = "WJetsToLNu_MLNu-120"
    elif s.startswith("WW"):
        sample_to_samplename[s] = "WW"
    elif s.startswith("WZ"):
        sample_to_samplename[s] = "WZ"
    elif s.startswith("ZZ"):
        sample_to_samplename[s] = "ZZ"
    else:
        sample_to_samplename[s] = "Background"
for s in data_samples:
    if s.startswith("EGamma"):
        sample_to_samplename[s] = "EGamma"
    elif s.startswith("MuonEG"):
        sample_to_samplename[s] = "MuonEG"
    elif s.startswith("SingleMuon"):
        sample_to_samplename[s] = "SingleMuon"
    elif s.startswith("Muon"):
        sample_to_samplename[s] = "SingleMuon"


#all_samples = signal_samples + background_samples
#all_samples = background_samples
all_samples = data_samples
#all_samples = signal_samples

success = []
failed  = []

for sample in all_samples:
    samplename  = sample_to_samplename[sample]
    msamplename = sample
    #msamplename = sample.replace("2022EE", "2022EE")   # output subdir name = sample name

    command = [script_to_run, era, samplename, sample, msamplename]
    print(f"\nRunning: {' '.join(command)}")

    result = subprocess.run(command)

    if result.returncode == 0:
        print(f"Done: {sample}")
        success.append(sample)
    else:
        print(f"Error: {sample}")
        failed.append(sample)

# Summary
print(f"\n{'='*60}")
print(f"Done. {len(success)} succeeded, {len(failed)} failed.")
if failed:
    print("Failed samples:")
    for s in failed:
        print(f"{s}")
