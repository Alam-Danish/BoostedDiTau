import itertools
import subprocess

# Lists of arguments for the bash script
era = ["UL16post"]
#samplename = ["AToTauTau"]
#sample = ["AToTauTau_ALP_M-${1}_HT-${2}_TuneCP5_13TeV-madgraphMLM-pythia8"]
#msamplename = ["ALP_M-${1}_HT-${2}_postVFPUL16"]

#samplename = ["DYJetsToLL_M-50"]
#sample = ["DYJetsToLL_M-${1}_HT-${2}_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8"]
#msamplename = ["DYJetsToLL_M-${1}_HT-${2}_postVFPUL16"]

samplename = ["YTauTau"]
sample = ["UpsilonToTauTau_pth${1}_TuneCP5_13TeV_pythia8"]
msamplename = ["UpsilonToTauTau_pth${1}_postVFPUL16"]

# The bash script
script_to_run = "./runGfal_Alam.sh"

# Mass and PT values
#m = ["50"]
value1 = ["80To200", "200To400",  "400ToInf"]
#value2 = ["100",  "200", "400", "600", "800", "1200", "2500", "Inf"]
#value1 = ["70to100", "100to200",  "200to400", "400to600",  "600to800", "800to1200", "1200to2500", "2500toInf"]
#value2 = ["70to100", "100to200", "200to400", "400to600", "600to800", "800to1200", "1200to2500", "2500toInf"]


# Combinations of arguments
combinations = itertools.product(era, samplename, sample, msamplename, value1)
#combinations = itertools.product(era, samplename, sample, msamplename)

# Loop through each combination and execute the script
for combo in combinations:

    # Unpacking the combo tuple
    era_val, samplename_val, sample_val, msamplename_val, v1 = combo
    #era_val, samplename_val, sample_val, msamplename_val = combo

    # Replace ${1} and ${2} in sample_val and msamplename_val with actual values of mass and PT
    #sample_val = sample_val.replace("${1}", v1).replace("${2}", v2)
    sample_val = sample_val.replace("${1}", v1)
    #msamplename_val = msamplename_val.replace("${1}", v1).replace("${2}", v2)
    msamplename_val = msamplename_val.replace("${1}", v1)

    # Construct the command to run the script with the combination as arguments
    command = [script_to_run, era_val, samplename_val, sample_val, msamplename_val]

    # Print the command (optional)
    print(f"Running {' '.join(command)}")

    # Run the script using subprocess
    result = subprocess.run(command)

    if result.returncode == 0:
        print(f"Script executed successfully with {' '.join(command)}")
    else:
        print(f"Error executing script with {' '.join(command)}")
