import subprocess
import sys,string,math,os
import glob
import numpy as np
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="To copy output histograms from eos space in preparation for hadd")
    parser.add_argument("--era", type=str, help="Era. e.g. 16preVFP, 16postVFP, 2017, 2018")
    parser.add_argument("-v", "--version", type=str, help="version. User defined")
    parser.add_argument("--sample", nargs="+", type=str, help="sample. e.g. DYJetsToLL_M-50, TTTo2L2Nu, etc. Able take more than one")
    parser.add_argument("--fname", type=str, help="output name. e.g. plotBoostedTauTau")
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    version = args.version
    fname = args.fname
    plotDir = "output/sept12"
    outDir = "output/sept12/merged"
    for s in args.sample:

        smpl = s
        era = args.era

        hist = "h_"+fname+"_"+era+"_"+smpl+"_"

       # outputfiles = os.popen("eos root://cmseos.fnal.gov ls /store/user/dalam/UL2016pre/ | grep "+hist).read().split()

        searchString = hist+"*"
    
        print('hadd '+searchString.replace("*",version+".root")+' '+plotDir+'/'+searchString)
        os.system('hadd '+outDir+'/'+searchString.replace("*",version+".root")+' '+plotDir+'/'+searchString)
