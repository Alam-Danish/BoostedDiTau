import itertools
import subprocess

# Lists of arguments for the bash script
era = ["UL16pre"]
samplename = ["WJetsToLNu"]
sample = ["WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8"]
msamplename = ["WJetsToLNu_HT-2500toInf_postVFPUL16"]

# The bash script
script_to_run = "./runGfal_Alam.sh"

# Mass and PT values
#mass = ["50"]
#value1 = ["70To100", "100To200", "200To400", "400To600", "600To800", "800To1200", "1200To2500", "2500ToInf"]
#value2 = ["70to100", "100to200", "200to400", "400to600", "600to800", "800to1200", "1200to2500", "2500toInf"]


# Combinations of arguments
#combinations = itertools.product(era, samplename, sample, msamplename, mass, value)
combinations = itertools.product(era, samplename, sample, msamplename)

# Loop through each combination and execute the script
for combo in combinations:

    # Unpacking the combo tuple
    #era_val, samplename_val, sample_val, msamplename_val, m, v = combo
    era_val, samplename_val, sample_val, msamplename_val = combo

    # Replace ${1} and ${2} in sample_val and msamplename_val with actual values of mass and PT
    #sample_val = sample_val.replace("${1}", m).replace("${2}", v)
    #sample_val = sample_val.replace("${1}", v1)
    #msamplename_val = msamplename_val.replace("${1}", m).replace("${2}", v)
    #msamplename_val = msamplename_val.replace("${2}", v2)

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
