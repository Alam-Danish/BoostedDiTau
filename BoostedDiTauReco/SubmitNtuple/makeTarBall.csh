#!/bin/tcsh

setenv MAKETARBALL 1

setenv CMSSW_BASE /uscms/home/dalam/nobackup/TCPNtuple/CMSSW_12_1_0_pre3

if ($MAKETARBALL == 1) then

    cp EMu_OS_BTag_Efficiency.root $CMSSW_BASE/src

    cd $CMSSW_BASE/src

    tar --exclude="../../CMSSW_12_1_0_pre3/src/BoostedDiTau/BoostedDiTauReco/SubmitNtuple/output" --exclude="*.root" --exclude="*.pdf" --exclude="*.gif" --exclude=.git --exclude="*.Log" --exclude="*stderr" --exclude="*stdout" --exclude="*.log" --exclude="*.tar.gz" --exclude="../../CMSSW_12_1_0_pre3/src/BoostedDiTau/MiniAODSkimmer/test/crabConfig" --exclude="../../CMSSW_12_1_0_pre3/src/BoostedDiTau/BoostedDiTauReco/SubmitNtuple/filelists_bkp" --exclude="../../CMSSW_12_1_0_pre3/src/BoostedDiTau/BoostedDiTauReco/SubmitNtuple/filelists_old" --exclude="../../CMSSW_12_1_0_pre3/src/BoostedDiTau/BoostedDiTauReco/SubmitNtuple/sampleList" -zcvf ../../CMSSW_12X.tgz ../../CMSSW_12_1_0_pre3/

    mkdir ../../tarToUpdate

    cp ../../CMSSW_12X.tgz ../../tarToUpdate

    rm ../../CMSSW_12X.tgz

    cp EMu_OS_BTag_Efficiency.root ../../tarToUpdate
    cp egammaEffi_EGM2D_UL2018.root ../../tarToUpdate
    cp egammaEffi_EGM2D_UL2017.root ../../tarToUpdate
    cp egammaEffi_EGM2D_UL2016preVFP.root ../../tarToUpdate
    cp egammaEffi_EGM2D_UL2016postVFP.root ../../tarToUpdate

    cd ../../tarToUpdate
    
    ls -l

    tar -zxvf CMSSW_12X.tgz

    cp EMu_OS_BTag_Efficiency.root  CMSSW_12_1_0_pre3/src/BoostedDiTau/BoostedDiTauReco/SubmitNtuple/
    cp egammaEffi_EGM2D_UL2018.root CMSSW_12_1_0_pre3/src/BoostedDiTau/BoostedDiTauReco/SubmitNtuple/
    cp egammaEffi_EGM2D_UL2017.root CMSSW_12_1_0_pre3/src/BoostedDiTau/BoostedDiTauReco/SubmitNtuple/
    cp egammaEffi_EGM2D_UL2016preVFP.root CMSSW_12_1_0_pre3/src/BoostedDiTau/BoostedDiTauReco/SubmitNtuple/
    cp egammaEffi_EGM2D_UL2016postVFP.root CMSSW_12_1_0_pre3/src/BoostedDiTau/BoostedDiTauReco/SubmitNtuple/

    tar -zcvf ../CMSSW_12X.tgz CMSSW_12_1_0_pre3/

    eosrm /store/user/dalam/DIS/TCPAnalysis/CMSSW_12X.tgz

    xrdcp ../CMSSW_12X.tgz root://cmseos.fnal.gov//store/user/dalam/DIS/TCPAnalysis/CMSSW_12X.tgz

    cd ../

    rm -r tarToUpdate

    cd $CMSSW_BASE/src/BoostedDiTau/BoostedDiTauReco/SubmitNtuple

endif
