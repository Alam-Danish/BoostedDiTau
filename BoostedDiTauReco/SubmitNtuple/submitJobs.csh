#!/bin/tcsh

setenv SAMPLE $1
setenv YEAR $2
setenv MODE $3

setenv CMSSW_BASE /uscms/home/dalam/nobackup/TCPNtuple/CMSSW_12_1_0_pre3

setenv OutputPrefix root://cmseos.fnal.gov//store/user/dalam/UL2016pre_updated/


setenv offset 0

foreach Mass (`ls filelists/$SAMPLE/UL$YEAR/`)
    setenv MASS $Mass
    setenv NQueue `ls filelists/$SAMPLE/UL${YEAR}/${MASS} | wc -l`
    # setenv NQueue 68
    # setenv NQueue 1
    echo $MASS
    setenv filelist ./filelists/${SAMPLE}/UL${YEAR}/${MASS}/${MASS}
    setenv logFile ${SAMPLE}_UL${YEAR}_${MASS}
    echo $filelist
    condor_submit condor.jdl                                                                                                        
end

# setenv MASS ALP_Ntuple_m_30_htj_400toInf_UL2018
# setenv MASS Ntuple_SingleMuon_Run2017E-UL2017_MiniAODv2-v1
# setenv MASS Ntuple_SingleMuon_Run2018A-UL2018_MiniAODv2
# setenv MASS Ntuple_WJetsToLNu_HT-2500toInf_Summer20UL18
# setenv MASS Ntuple_DYJetsToLL_M-50_HT-2500toInf_Summer20UL18
# setenv MASS DYJetsToLL_M-4to50_HT-70to100_preVFPUL16
# setenv MASS DYJetsToLL_M-4to50_HT-600toInf_preVFPUL16
# setenv NQueue `ls filelists/DYJetsToLL_M-4to50/UL16pre/${MASS} | wc -l`
# setenv NQueue `ls filelists/SingleMuon/UL2018/${MASS} | wc -l`
# setenv NQueue `ls singleMuonToResubmit/${MASS}* | wc -l`
# setenv NQueue 1
# echo ${NQueue}
# echo $MASS
# setenv filelist ./filelists/${SAMPLE}/UL${YEAR}/${MASS}/${MASS}
# setenv logFile ${SAMPLE}_UL${YEAR}_${MASS}
# echo $filelist
# condor_submit condor.jdl
