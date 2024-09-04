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

    for s in args.sample:

        smpl = s
        era = args.era
    
#        hist = "h_"+fname+"_"+era+"_Ntuple_"+smpl+"_"
        hist = "h_"+fname+"_"+era+"_"+smpl+"_"


        outputfiles = os.popen("eos root://cmseos.fnal.gov ls /store/user/dalam/UL2016pre/ | grep "+hist).read().split()

        print(outputfiles)
        print(len(outputfiles))

        plotDir = "./output/"+version

        n = 0

        for fil in outputfiles:
            print(fil)
            os.system("xrdcp root://cmseos.fnal.gov//store/user/dalam/UL2016pre/"+fil+" "+plotDir+"/"+fil)

        searchString = hist+"*"        

        print('ls '+plotDir+'/'+searchString)
        os.system('ls '+plotDir+'/'+searchString)
        if os.path.exists(searchString.replace("*",version+".root")):
            os.remove(searchString.replace("*",version+".root"))
