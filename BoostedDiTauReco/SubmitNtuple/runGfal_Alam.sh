#!/bin/tcsh

setenv ERA $1
setenv SAMPLENAME $2
setenv SAMPLE $3
setenv MSAMPLENAME $4

set BASE = "root://cmsio3.rc.ufl.edu:1094"
set STOREPATH = "/store/user/dalam/TCPNtuple/Run3/2022EE/${SAMPLE}"
#set STOREPATH = "/store/user/dalam/TCPNtuple/Run3/2022preEE/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8"

@ j = -1

foreach part (`xrdfs $BASE ls $STOREPATH`)
    echo "found part: $part"
    setenv PART `basename $part`
    if ($PART =~ *2022EE* || $PART =~ *v1*) then
        echo "Found: $PART"
        @ i = 0
        foreach date (`xrdfs $BASE ls ${STOREPATH}/${PART}`)
            setenv DATE `basename $date`
            foreach num (`xrdfs $BASE ls ${STOREPATH}/${PART}/${DATE}`)
                setenv NUM `basename $num`
                set namestr = "${BASE}/${STOREPATH}/${PART}/${DATE}/${NUM}/"
                foreach file (`xrdfs $BASE ls ${STOREPATH}/${PART}/${DATE}/${NUM}`)
                    set fname = `basename $file`
                    if ($i % 100 == 0) then
                        @ j += 1
                        if (! -d filelists/${SAMPLENAME}/${ERA}/${MSAMPLENAME}) then
                            mkdir -p filelists/${SAMPLENAME}/${ERA}/${MSAMPLENAME}
                        endif
                        echo ${namestr}${fname} > filelists/${SAMPLENAME}/${ERA}/${MSAMPLENAME}/${MSAMPLENAME}_${j}.txt
                        @ i += 1
                    else
                        echo ${namestr}${fname} >> filelists/${SAMPLENAME}/${ERA}/${MSAMPLENAME}/${MSAMPLENAME}_${j}.txt
                        @ i += 1
                    endif
                end  # foreach file
            end  # foreach num
        end  # foreach date
    endif
end
