#!/bin/tcsh                                                                                                                                

setenv VER v6

foreach Signal (`ls AToTauTau`)
    echo h_studySVFit_${Signal}.root
    xrdcp root://cmseos.fnal.gov//store/user/mwulansa/UL2017/h_studySVFit_${Signal}_0.root ../h_studySVFit_${Signal}__${VER}.root
end
