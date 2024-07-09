#!/bin/tcsh

setenv ERA UL16pre
setenv SAMPLENAME AToTauTau

setenv SAMPLE AToTauTau_ALP_M-10_HT-100to400_TuneCP5_13TeV-madgraphMLM-pythia8
setenv MSAMPLENAME ALP_M-10_HT-100to400_preVFPUL16


@ j = -1

foreach part (`gfal-ls root://cmsio2.rc.ufl.edu:1094//store/user/zhangj/TCPNtuple/$SAMPLE`)
    setenv PART $part
    echo $PART
    if ($PART =~ *preVFPUL16* && $PART =~ *v5) then
	echo $PART
	@ i = 0
	setenv DATE `gfal-ls root://cmsio2.rc.ufl.edu:1094//store/user/zhangj/TCPNtuple/$SAMPLE/$PART`
	echo $DATE
	foreach num (`gfal-ls root://cmsio2.rc.ufl.edu:1094//store/user/zhangj/TCPNtuple/$SAMPLE/$PART/$DATE`)
	    setenv NUM $num
	    echo $NUM
	    setenv namestr root://cmsio2.rc.ufl.edu:1094//store/user/zhangj/TCPNtuple/$SAMPLE/$PART/$DATE/$NUM/
	    foreach file (`gfal-ls $namestr`)
		if ($i % 100 == 0) then
		    @ j += 1
		    if (! -d filelists/$SAMPLENAME/$ERA/$MSAMPLENAME) then
			mkdir -p filelists/$SAMPLENAME/$ERA/$MSAMPLENAME
		    endif
		    echo $namestr$file > filelists/$SAMPLENAME/$ERA/$MSAMPLENAME/${MSAMPLENAME}_${j}.txt
		    @ i += 1
		else
		    echo $namestr$file >> filelists/$SAMPLENAME/$ERA/$MSAMPLENAME/${MSAMPLENAME}_${j}.txt
		    @ i += 1
		endif
	    end
	end
    endif
end
