#ifndef __TCPAnalysis_TrigObjectInfoDS_H__
#define __TCPAnalysis_TrigObjectInfoDS_H__

#include <vector>

struct TrigObjectInfo {
  // Kinematics
  float pt, eta, phi, mass;

  // EleJet 
  int isEleJet;       // HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165 (combined)
  int isEleLeg;       // electron leg of EleJet
  int isJetLeg;       // jet leg of EleJet

  // Jets
  int isSingleJet450; // HLT_PFJet450_v
  int isSingleJet500;    // HLT_PFJet500_v
  int isSingleJet550; // HLT_PFJet550_v
  int isJetHTMET;     // HLT_PFHT500_PFMET100_PFMHT100_IDTight_v
  int isJetHT;        // HLT_PFHT1050_v

  //  MuTau cross triggers 
  int isMuTau;        // all HLT_IsoMu20/24_eta2p1 x DeepTau variants

  //  Single Muon 
  int isIsoMu24;      // HLT_IsoMu24_v
  int isIsoMu;        // HLT_IsoMu27_v
  int isMu;           // HLT_Mu50_v

  //  Di-Electron 
  int isDiEle;        // HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v (DZ + noDZ)

  //  ETau 
  int isEleTau;       // HLT_Ele24_eta2p1_WPTight_Gsf_LooseDeepTauPFTauHPS30

  //  Single Electron 
  int isSingleEle;    // HLT_Ele32/35_WPTight_Gsf variants

  //  Ele+HT/Jet 
  int isEleHTJet;     // HLT_Ele50_IsoVVVL_PFHT450 + HLT_Ele115

  //  DoubleEle33 
  int isDoubleEle33;  // HLT_DoubleEle33_CaloIdL_MW_v

  //  MuonEG noDZ 
  int isMuonEGnoDZmu; // muon leg of MuonEG noDZ
  int isMuonEGnoDZe;  // electron leg of MuonEG noDZ
  int isMuonEGnoDZ;   // combined MuonEG noDZ

  //  MuonEG DZ 
  int isMuonEGmu;     // muon leg of MuonEG DZ
  int isMuonEGe;      // electron leg of MuonEG DZ
  int isMuonEG;       // combined MuonEG DZ

  //  Di-Muon 
  int isDiMu;         // HLT_Mu17_Mu8_DZ_Mass8 + Mass3p8
  
  //  Tau 
  int isSingleTau;    // HLT_LooseDeepTauPFTauHPS180_L2NN_eta2p1_v
  int isDisplacedDiTau; // HLT_DoubleMediumChargedIsoDisplacedPFTauHPS32
  int isDiTau;        // HLT_DoubleMediumDeepTauPFTauHPS35/30+PFJet60/75

  //  Photon 
  int isPhoton175;    // HLT_Photon175_v
  int isPhoton;       // HLT_Photon200_v
};

typedef class std::vector<TrigObjectInfo> TrigObjectInfoDS;

#endif
