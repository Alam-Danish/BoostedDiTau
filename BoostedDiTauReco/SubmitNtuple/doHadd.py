import subprocess
import sys,string,math,os
#import ConfigParser
import glob
import numpy as np
#from makeFileLists import *

isCopy = True

if len(sys.argv)>1:
    Sample = sys.argv[1]
    version = sys.argv[2]
    fname = sys.argv[3]
    if len(sys.argv)>4:
        if sys.argv[4] == "--isCopyFalse":
            isCopy = False

#hist = 'h_studyEMuDataMC_Isolated_'
hist = "h_"+fname+"_"

outputfiles=os.popen("eos root://cmseos.fnal.gov ls /store/user/dalam/UL2017/ | grep "+hist+Sample+"_").read().split()
if 'SingleMuon' in Sample:
    outputfiles=os.popen("eos root://cmseos.fnal.gov ls /store/user/dalam/UL2017/ | grep "+hist+Sample).read().split()
print(outputfiles)

plotDir = "./output/"+version

print(isCopy)

if isCopy:
    for fil in outputfiles:
        print(fil)
        os.system("xrdcp -f root://cmseos.fnal.gov//store/user/dalam/UL2017/"+fil+" "+plotDir+"/"+fil)

searchString = hist+Sample+'_*'
if 'SingleMuon' in Sample:
    searchString = hist+Sample+'*'

print('ls '+plotDir+'/'+searchString)
os.system('ls '+plotDir+'/'+searchString)
if os.path.exists(searchString.replace("*",version+".root")):
    os.remove(searchString.replace("*",version+".root"))

if 'SingleMuon' in Sample:
    print('hadd -f '+searchString.replace("*","_"+version+".root")+' '+plotDir+'/'+searchString)
    os.system('hadd -f '+searchString.replace("*","_"+version+".root")+' '+plotDir+'/'+searchString)
else:
    print('hadd -f '+searchString.replace("*",version+".root")+' '+plotDir+'/'+searchString)
    os.system('hadd -f '+searchString.replace("*",version+".root")+' '+plotDir+'/'+searchString)

if Sample == "TTJets":
    os.system("cp "+hist+Sample+"_"+version+".root "+hist+Sample+"_TuneCP5_"+version+".root")

if Sample == "TTTo2L2Nu":
    os.system("cp "+hist+Sample+"_"+version+".root "+hist+"TT_"+Sample+"_TuneCP5_"+version+".root")

if Sample == "TTToSemiLeptonic":
    os.system("cp "+hist+Sample+"_"+version+".root "+hist+"TT_"+Sample+"_TuneCP5_"+version+".root")

if Sample == "TTToHadronic":
    os.system("cp "+hist+Sample+"_"+version+".root "+hist+"TT_"+Sample+"_TuneCP5_"+version+".root")

if Sample == "WW" or Sample == "WZ" or Sample == "ZZ":
    os.system("cp "+hist+Sample+"_"+version+".root "+hist+"Diboson_"+Sample+"_"+version+".root")
