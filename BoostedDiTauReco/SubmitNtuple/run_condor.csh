#!/bin/tcsh

echo "Starting job on " `date` #Date/time of start of job                                                                                                     
echo "Running on: `uname -a`" #Condor job is running on this node                                                                                             
echo "System software: `cat /etc/redhat-release`" #Operating System on that node

source /cvmfs/cms.cern.ch/cmsset_default.csh  ## if a bash script, use .sh instead of .csh

xrdcp root://cmseos.fnal.gov//store/user/dalam/DIS/TCPAnalysis/CMSSW_12X.tgz CMSSW_12X.tgz

tar -xf CMSSW_12X.tgz
rm CMSSW_12X.tgz

setenv SCRAM_ARCH slc7_amd64_gcc900
cd CMSSW_12_1_0_pre3/src
scramv1 b ProjectRename
eval `scramv1 runtime -csh`

cd BoostedDiTau/BoostedDiTauReco/SubmitNtuple

echo "Arguments passed to this script are: "
echo "  script: $1"
echo "  input files: $2"
echo "  output dir: $3"
echo "  mode: $4"
echo "  year: $5"

python3 ${1} -i ${2} --folder ${3} -s ${4} --year ${5}

cd ${_CONDOR_SCRATCH_DIR}
rm -rf CMSSW_12_1_0_pre3
