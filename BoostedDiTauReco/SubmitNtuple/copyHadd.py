import subprocess
import sys,string,math,os
import glob
import numpy as np
import argparse
import re
from collections import defaultdict

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="To copy output histograms from eos space and hadd per sample")
    parser.add_argument("--era", type=str, help="Era. e.g. 2016preVFP, 2016postVFP, 2017, 2018, 2022, 2022EE, 2023, 2023BPix, 2024")
    parser.add_argument("-v", "--version", type=str, help="version. User defined")
    parser.add_argument("--sample", nargs="+", type=str, help="sample. e.g. DYto2L-2Jets_MLL-4to10, DYto2L-2Jets_MLL-10to50, DYto2L-2Jets_MLL-50, TTTo2L2Nu, etc. Able take more than one. If not given, auto-discovers all samples from EOS.")
    parser.add_argument("--fname", type=str, help="output name. e.g. plotBoostedTauTau")
    parser.add_argument("--auto", action="store_true", help="Auto-discover all samples from EOS directory")
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    version = args.version
    fname = args.fname
    era = args.era
    plotDir = "./output/"+version

    if not os.path.exists(plotDir):
        os.makedirs(plotDir)

    # output directory and file prefix
    if era == "2016preVFP" or era == "2016postVFP":
        eosDir = "/store/user/dalam/UL2016pre_updated/"
        histPrefix = "h_"+fname+"_"+era+"_"
    elif era == "2017" or era == "2018":
        eosDir = "/store/user/mwulansa/UL2017/"
        histPrefix = "h_"+fname+"_"+era+"_Ntuple_"
    else:
        eosDir = "/store/user/dalam/SubmitNtuple/plotBoostedTauTau_july23_2026/"
        histPrefix = "h_"+fname+"_"+era+"_"

    # sample locator
    if args.auto or args.sample is None:
        print("==> Auto-discovering samples from EOS: "+eosDir)
        allfiles = os.popen("eos root://cmseos.fnal.gov ls "+eosDir+" | grep "+histPrefix).read().split()

        # Group files by sample name
        # File format: h_{fname}_{era}_{sample}_{jobnumber}.root
        # Job files end with numeric suffix e.g. _0.root _1.root
        # Skip already-hadded files which contain version string
        sample_files = defaultdict(list)
        for fil in allfiles:
            if version in fil:
                continue
            remainder = fil.replace(histPrefix, "")
            match = re.match(r"^(.+)_(\d+)\.root$", remainder)
            if match:
                sample_name = match.group(1)
                sample_files[sample_name].append(fil)

        print("==> Found "+str(len(sample_files))+" unique samples:")
        for s in sorted(sample_files.keys()):
            print("    "+s+" ("+str(len(sample_files[s]))+" files)")

        sample_list = sorted(sample_files.keys())
        auto_mode = True
    else:
        sample_list = args.sample
        sample_files = {}
        auto_mode = False

    # Copy from eos directory to local plotDir
    for s in sample_list:

        smpl = s
        hist = histPrefix+smpl

        if auto_mode:
            outputfiles = sample_files[smpl]
        else:
            outputfiles = os.popen("eos root://cmseos.fnal.gov ls "+eosDir+" | grep "+hist).read().split()

        print(outputfiles)
        print(len(outputfiles))

        n = 0

        for fil in outputfiles:
            print(fil)
            if os.path.exists(plotDir+"/"+fil):
                print("  already exists, skipping: "+fil)
                continue
            os.system("xrdcp root://cmseos.fnal.gov/"+eosDir+fil+" "+plotDir+"/"+fil)

        searchString = hist+"*"

        print('ls '+plotDir+'/'+searchString)
        os.system('ls '+plotDir+'/'+searchString)
        if os.path.exists(searchString.replace("*",version+".root")):
            os.remove(searchString.replace("*",version+".root"))

    # Do hadd
    for s in sample_list:

        smpl = s
        hist = histPrefix+smpl
        searchString = hist+"*"
        haddOut = plotDir+'/'+searchString.replace("*","_"+version+".root")

        if os.path.exists(haddOut):
            print("  already exists, skipping hadd: "+haddOut)
            continue

        if len(glob.glob(plotDir+'/'+searchString)) == 0:
            print("  no input files found, skipping hadd: "+searchString)
            continue

        print('hadd -f '+haddOut+' '+plotDir+'/'+searchString)
        os.system('hadd -f '+haddOut+' '+plotDir+'/'+searchString)

    # Delete the samples after hadd and keep only hadded
    for s in sample_list:

        smpl = s
        hist = histPrefix+smpl
        searchString = hist+"*"
        haddOut = plotDir+'/'+searchString.replace("*","_"+version+".root")

        # Check if the hadd output exists before attempting to delete input files
        if not os.path.exists(haddOut):
            print("  hadd output not found, skipping delete: "+haddOut)
            continue

        for fil in glob.glob(plotDir+'/'+searchString):
            # Do not delete the hadd output file itself
            if fil == haddOut:
                continue
            print("  deleting: "+fil)
            os.remove(fil)