#!/bin/tcsh


setenv whichSample MuonEG

setenv nfiles 100

foreach sample (`gfal-ls root://cmsio2.rc.ufl.edu:1094//store/user/zhangj/$whichSample/`)
    setenv PART $sample
    if ($PART =~ *postVFPUL16* && $PART =~ *v5) then
        setenv SAMPLE $sample
        setenv SAMPLETXTT $sample:s/_MiniAODv2-v1_v5//
        setenv SAMPLETXT $SAMPLETXTT:s/Ntuple_${whichSample}//
        echo $SAMPLETXT
        @ j = -1
        foreach part (`gfal-ls root://cmsio2.rc.ufl.edu:1094//store/user/zhangj/$whichSample/$SAMPLE`)
    	setenv PART $part
    	echo $PART
    	@ i = 0
    	foreach num (`gfal-ls root://cmsio2.rc.ufl.edu:1094//store/user/zhangj/$whichSample/$SAMPLE/$PART`)
    	    setenv NUM $num
    	    set namestr = "root://cmsio2.rc.ufl.edu:1094//store/user/zhangj/$whichSample/$SAMPLE/$PART/$NUM/"
    	    echo $namestr
    	    foreach file (`gfal-ls root://cmsio2.rc.ufl.edu:1094//store/user/zhangj/$whichSample/$SAMPLE/$PART/$NUM/`)
    		if ($i % 100 == 0) then
    		    @ j += 1
    		    if (! -d filelists/$whichSample/$SAMPLETXT) then
    			mkdir -p filelists/$whichSample/$SAMPLETXT
    		    endif
    		    echo root://cmsio7.rc.ufl.edu:1094//store/user/zhangj/$whichSample/$SAMPLE/$PART/$NUM/$file > filelists/$whichSample/$SAMPLETXT/${SAMPLETXT}_$j.txt
    		    @ i += 1
    		else
    		    echo root://cmsio7.rc.ufl.edu:1094//store/user/zhangj/$whichSample/$SAMPLE/$PART/$NUM/$file >> filelists/$whichSample/$SAMPLETXT/${SAMPLETXT}_$j.txt
    		    @ i += 1
    		endif
    	    end
    	    echo $i
    	    echo $j
            end
        end
    endif
end
