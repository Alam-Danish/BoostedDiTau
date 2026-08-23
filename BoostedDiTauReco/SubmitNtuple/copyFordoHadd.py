import subprocess
import sys,string,math,os
import glob
import numpy as np
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="To copy output histograms from eos space in preparation for hadd")
    parser.add_argument("--era", type=str, help="Era. e.g. 2016preVFP, 2016postVFP, 2017, 2018, 2022, 2022EE, 2023, 2023BPix, 2024")
    parser.add_argument("-v", "--version", type=str, help="version. User defined")
    parser.add_argument("--sample", nargs="+", type=str, help="sample. e.g. DYto2L-2Jets_MLL-4to10, DYJetsToLL_M-10to50, DYJetsToLL_M-50, TTTo2L2Nu, etc. Able take more than one")
    parser.add_argument("--fname", type=str, help="output name. e.g. plotBoostedTauTau")
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    version = args.version
    fname = args.fname
    era = args.era

    for s in args.sample:

        smpl = s

        if era == "2016preVFP" or era == "2016postVFP":
            hist = "h_"+fname+"_"+era+"_"+smpl
            outputfiles = os.popen("eos root://cmseos.fnal.gov ls /store/user/dalam/UL2016pre_updated/ | grep "+hist).read().split()
        elif era == "2017" or era == "2018":
            hist = "h_"+fname+"_"+era+"_Ntuple_"+smpl
            outputfiles = os.popen("eos root://cmseos.fnal.gov ls /store/user/mwulansa/UL2017/ | grep "+hist).read().split()
        else:
            hist = "h_"+fname+"_"+era+"_"+smpl
            outputfiles = os.popen("eos root://cmseos.fnal.gov ls /store/user/dalam/SubmitNtuple/plotBoostedTauTau_june26_2026/ | grep "+hist).read().split()

        print(outputfiles)
        print(len(outputfiles))

        plotDir = "./output/"+version

        n = 0

        for fil in outputfiles:
            print(fil)
            if era == "2016preVFP" or era == "2016postVFP":
                os.system("xrdcp root://cmseos.fnal.gov//store/user/dalam/UL2016pre_updated/"+fil+" "+plotDir+"/"+fil)                                 
            elif era == "2017" or era == "2018":
                os.system("xrdcp root://cmseos.fnal.gov//store/user/mwulansa/UL2017/"+fil+" "+plotDir+"/"+fil)
            else:
                 os.system("xrdcp root://cmseos.fnal.gov//store/user/dalam/SubmitNtuple/plotBoostedTauTau_june26_2026/"+fil+" "+plotDir+"/"+fil)               

        searchString = hist+"*"        

        print('ls '+plotDir+'/'+searchString)
        os.system('ls '+plotDir+'/'+searchString)
        if os.path.exists(searchString.replace("*",version+".root")):
            os.remove(searchString.replace("*",version+".root"))
