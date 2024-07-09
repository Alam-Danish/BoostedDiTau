#!/bin/tcsh                                                                                                                                

setenv VER vAN

foreach Signal (`ls AToTauTau/UL2017`)
    echo h_plotBoostedTauTau_${Signal}.root
    xrdcp root://cmseos.fnal.gov//store/user/mwulansa/UL2017/h_plotBoostedTauTau_2017_${Signal}_0.root ../h_plotBoostedTauTau_2017_${Signal}__${VER}.root
end
