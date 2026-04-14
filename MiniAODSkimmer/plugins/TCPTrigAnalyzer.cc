// system include files
#include <memory>
#include <iostream>
#include <regex>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"

#include "TTree.h"

using namespace edm;
using namespace std;

class TCPTrigNtuples : public edm::one::EDAnalyzer<edm::one::WatchRuns,edm::one::SharedResources> {
public:

  explicit TCPTrigNtuples(const edm::ParameterSet&);
  ~TCPTrigNtuples() override {}

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:

  virtual void beginJob() override;
  virtual void endJob() override {}
  virtual void beginRun(edm::Run const&, edm::EventSetup const&) override {}
  virtual void endRun(edm::Run const&, edm::EventSetup const&) override {}
  virtual void analyze(edm::Event const&, edm::EventSetup const&) override;

  //  edm::EDGetTokenT< edm::TriggerResults > triggerBits_;
  edm::EDGetTokenT< edm::TriggerResults > TriggerResults_;
  
  TTree *tree;
  int event_;

  // --- Jets -------------------------------------------------
  bool isSingleJet450_;
  bool isSingleJet500_;
  bool isSingleJet550_;
  bool isHT_;
  
  // --- MET --------------------------------------------------
  bool isMET_;
  bool isPFMET120_;
  bool isPFHT60_;
  bool isPFHT500_;
  bool isPFHT700_;
  bool isPFHT800_;
  //bool isHBHECleaned_;
  //bool isPFMET200_;
  //bool isPFMETOne200_;
  
  // --- Single Muon -------------------------------------------
  bool isIsoMu_;           // HLT_IsoMu27_v
  bool isIsoMu24_;         // HLT_IsoMu24_v
  bool isMu_;              // HLT_Mu50_v

  // --- Mu-Tau -------------------------------------------------
  bool isIsoMuTau_;        // HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27 (Run 3)

  // --- Single Electron -------------------------------------------------
  bool isIsoEle_;          // HLT_Ele35 + Ele32_L1DoubleEG
  bool isEle_;             // HLT_Ele115_CaloIdVT_GsfTrkIdT
  bool isEleJet_;          // HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165

  // --- ETau -------------------------------------------------
  bool isEleTau_;          // HLT_Ele24_eta2p1_WPTight_Gsf_LooseDeepTauPFTauHPS30 (Run 3)

  // --- Di-Mu -------------------------------------------------
  bool isDoubleMu_;        // Mu17_Mu8 Mass8 + Mass3p8

  // --- Di-Electron -------------------------------------------------
  bool isDoubleIsoEG_;     // HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL
  bool isDoubleEG_;        // HLT_DoubleEle33_CaloIdL_MW

  // --- MuonEG -------------------------------------------------
  bool isMuonEG_;
  bool isMu8Ele23_;
  bool isMu23Ele12_;
  bool isMuonEGnoDZ_;
  bool isMu8Ele23noDZ_;
  bool isMu23Ele12noDZ_;

  // --- Tau -------------------------------------------------
  bool isDoubleTauMedium_; // Run 3 DeepTau di-tau
  bool isDoubleTauTight_;  // Run 3 DeepTau di-tau + jet
  bool isSingleTauMET_;    // HLT_LooseDeepTauPFTauHPS180 (Run 3)
  bool isDisplacedDiTau_;  // NEW Run 3

  // --- Photon -------------------------------------------------
  bool isPhoton200_;
  bool isPhoton175_;
};

TCPTrigNtuples::TCPTrigNtuples(const edm::ParameterSet& iConfig) :
  //triggerBits_(consumes< edm::TriggerResults >(iConfig.getParameter<edm::InputTag>("bits"))),
  TriggerResults_(consumes< edm::TriggerResults >(iConfig.getParameter<edm::InputTag>("TriggerResults"))) {
  usesResource(TFileService::kSharedResource);
  //std::cout << "debug0" << "\n";
}

void TCPTrigNtuples::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

void TCPTrigNtuples::beginJob() {
  
  edm::Service<TFileService> fs;
  fs->mkdir( "trigger" );
  
  tree = fs->make<TTree>("triggerTree", "");
  
  tree->Branch("event", &event_, "event/I");
  
  // Jets
  tree->Branch("isSingleJet450", &isSingleJet450_, "isSingleJet450/O");
  tree->Branch("isSingleJet500", &isSingleJet500_, "isSingleJet500/O");
  tree->Branch("isSingleJet550", &isSingleJet550_, "isSingleJet550/O");
  tree->Branch("isHT", &isHT_, "isHT/O");
  // MET
  tree->Branch("isMET", &isMET_, "isMET/O");
  tree->Branch("isPFMET120", &isPFMET120_, "isPFMET120/O");
  tree->Branch("isPFHT60", &isPFHT60_, "isPFHT60/O");
  tree->Branch("isPFHT500", &isPFHT500_, "isPFHT500/O");
  tree->Branch("isPFHT700", &isPFHT700_, "isPFHT700/O");
  tree->Branch("isPFHT800", &isPFHT800_, "isPFHT800/O");
  //tree->Branch("isHBHECleaned", &isHBHECleaned_, "isHBHECleaned/O");
  //tree->Branch("isPFMET200", &isPFMET200_, "isPFMET200/O");
  //tree->Branch("isPFMETOne200", &isPFMETOne200_, "isPFMETOne200/O");

  // Single Muon
  tree->Branch("isIsoMu", &isIsoMu_, "isIsoMu/O");
  tree->Branch("isIsoMu24", &isIsoMu24_, "isIsoMu24/O");
  tree->Branch("isMu", &isMu_, "isMu/O");
  // MuTau
  tree->Branch("isIsoMuTau", &isIsoMuTau_, "isIsoMuTau/O");
  // Single Electron
  tree->Branch("isIsoEle", &isIsoEle_, "isIsoEle/O");
  tree->Branch("isEle", &isEle_, "isEle/O");
  tree->Branch("isEleJet", &isEleJet_, "isEleJet/O");
  // ETau
  tree->Branch("isEleTau", &isEleTau_, "isEleTau/O");
  // Di-Muon
  tree->Branch("isDoubleMu", &isDoubleMu_, "isDoubleMu/O");
  // Di-Electron
  tree->Branch("isDoubleIsoEG", &isDoubleIsoEG_, "isDoubleIsoEG/O");
  tree->Branch("isDoubleEG", &isDoubleEG_, "isDoubleEG/O");
  // MuonEG
  tree->Branch("isMuonEG", &isMuonEG_, "isMuonEG/O");
  tree->Branch("isMu8Ele23", &isMu8Ele23_, "isMu8Ele23/O");
  tree->Branch("isMu23Ele12", &isMu23Ele12_, "isMu23Ele12/O");
  tree->Branch("isMuonEGnoDZ", &isMuonEGnoDZ_, "isMuonEGnoDZ/O");
  tree->Branch("isMu8Ele23noDZ", &isMu8Ele23noDZ_, "isMu8Ele23noDZ/O");
  tree->Branch("isMu23Ele12noDZ", &isMu23Ele12noDZ_, "isMu23Ele12noDZ/O");
  // Tau
  tree->Branch("isDoubleTauMedium", &isDoubleTauMedium_, "isDoubleTauMedium/O");
  tree->Branch("isDoubleTauTight", &isDoubleTauTight_, "isDoubleTauTight/O");
  tree->Branch("isSingleTauMET", &isSingleTauMET_, "isSingleTauMET/O");
  tree->Branch("isDisplacedDiTau",   &isDisplacedDiTau_,   "isDisplacedDiTau/O");
  // Photon
  tree->Branch("isPhoton175", &isPhoton175_, "isPhoton175/O");
  tree->Branch("isPhoton200", &isPhoton200_, "isPhoton200/O");
    
}

void TCPTrigNtuples::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

  int Event = iEvent.id().event();
  event_ = Event;

  //  edm::Handle<edm::TriggerResults> triggerBits;
  //  iEvent.getByToekn(triggerBits_, triggerBits);

  edm::Handle<edm::TriggerResults> triggerResultsHandle;
  iEvent.getByToken(TriggerResults_, triggerResultsHandle);

  TriggerResults triggerResults = *triggerResultsHandle;
  auto & names = iEvent.triggerNames(*triggerResultsHandle);

  //std::cout << "debug3" << "\n";

  isSingleJet450_ = 0;
  isSingleJet500_ = 0;
  isSingleJet550_ = 0;
  isHT_ = 0;

  isMET_ = 0;
  //isHBHECleaned_ = 0;
  //isPFMET200_ = 0;
  //isPFMETOne200_ = 0;
  isPFMET120_ = 0;
  isPFHT60_ = 0;
  isPFHT500_ = 0;
  isPFHT700_ = 0;
  isPFHT800_ = 0;

  isIsoMu_ = 0;
  isIsoMu24_ = 0;
  isMu_ = 0;
  isIsoMuTau_ = 0;

  isIsoEle_ = 0;
  isEle_ = 0;    // for 2018 data, non-iso electron trigger is available for all runs
  isEleJet_ = 0;

  isEleTau_ = 0;

  isDoubleMu_ = 0;

  isDoubleIsoEG_ = 0;
  isDoubleEG_ = 0;
  
  isMuonEG_ = 0;
  isMu8Ele23_ = 0;
  isMu23Ele12_ = 0;

  isMuonEGnoDZ_ = 0;
  isMu8Ele23noDZ_ = 0;
  isMu23Ele12noDZ_ = 0;

  isDoubleTauMedium_ = 0;
  isDoubleTauTight_ = 0;
  isSingleTauMET_ = 0;
  isDisplacedDiTau_ = 0;

  isPhoton200_ = 0;
  isPhoton175_ = 0;


  //std::cout << "debug4" << "\n";

  // Jets
  std::regex SingleJet450("(HLT_PFJet450_v)(.*)");
  std::regex SingleJet500("(HLT_PFJet500_v)(.*)");
  std::regex SingleJet550("(HLT_PFJet550_v)(.*)");
  std::regex HT("(HLT_PFHT1050_v)(.*)");
  // MET
  std::regex PFMET120("(HLT_PFMET120_PFMHT120_IDTight_v)(.*)");
  std::regex PFHT60("(HLT_PFMET120_PFMHT120_IDTight_PFHT60_v)(.*)");
  std::regex PFHT500("(HLT_PFHT500_PFMET100_PFMHT100_IDTight_v)(.*)");
  std::regex PFHT700("(HLT_PFHT700_PFMET85_PFMHT85_IDTight_v)(.*)");
  std::regex PFHT800("(HLT_PFHT800_PFMET75_PFMHT75_IDTight_v)(.*)");

  //std::regex HBHECleaned("(HLT_PFMET200_HBHECleaned_v)(.*)");
  //std::regex PFMET200("(HLT_PFMET200_HBHE_BeamHaloCleaned_v)(.*)");
  //std::regex PFMETOne200("(HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned_v)(.*)");

  // Single Muon
  std::regex IsoMu("(HLT_IsoMu27_v)(.*)");
  std::regex IsoMu24("(HLT_IsoMu24_v)(.*)");
  std::regex Mu("(HLT_Mu50_v)(.*)");
  // MuTau
  std::regex IsoMuTau("(HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1_v)(.*)");
  // Single Electron
  std::regex IsoEle35("(HLT_Ele35_WPTight_Gsf_v)(.*)");
  std::regex IsoEle32("(HLT_Ele32_WPTight_Gsf_L1DoubleEG_v)(.*)");
  std::regex Ele("(HLT_Ele115_CaloIdVT_GsfTrkIdT_v)(.*)");
  std::regex EleJet("(HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v)(.*)");
  //ETau
  std::regex EleTau("(HLT_Ele24_eta2p1_WPTight_Gsf_LooseDeepTauPFTauHPS30_eta2p1_CrossL1_v)(.*)");
  // Di-Muon
  std::regex DoubleMuMass8("(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v)(.*)");
  std::regex DoubleMuMass3p8("(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v)(.*)");
  // Di-Electron
  std::regex DoubleIsoEG("(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v)(.*)");
  std::regex DoubleEG("(HLT_DoubleEle33_CaloIdL_MW_v)(.*)");
  // MuonEG
  std::regex Muon8EG("(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v)(.*)");
  std::regex Muon23EG("(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v)(.*)");
  std::regex Muon8EGnoDZ("(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v)(.*)");
  std::regex Muon23EGnoDZ("(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v)(.*)");
  // Tau
  std::regex SingleTau("(HLT_LooseDeepTauPFTauHPS180_L2NN_eta2p1_v)(.*)");
  std::regex DoubleTau35("(HLT_DoubleMediumDeepTauPFTauHPS35_L2NN_eta2p1_v)(.*)");
  std::regex DoubleTauJet60("(HLT_DoubleMediumDeepTauPFTauHPS30_L2NN_eta2p1_PFJet60_v)(.*)");
  std::regex DoubleTauJet75("(HLT_DoubleMediumDeepTauPFTauHPS30_L2NN_eta2p1_PFJet75_v)(.*)");
  std::regex DisplacedDiTau("(HLT_DoubleMediumChargedIsoDisplacedPFTauHPS32_Trk1_eta2p1_v)(.*)");

  //std::regex DoubleTauMedium("(HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v)(.*)");
  //std::regex DoubleTauTight35("(HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v)(.*)");
  //std::regex DoubleTauTight40("(HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v)(.*)");
  //std::regex SingleTauMET("(HLT_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr_MET90_v)(.*)");
  // Photon
  
  std::regex Photon200("(HLT_Photon200_v)(.*)");
  std::regex Photon175("(HLT_Photon175_v)(.*)");

  for (unsigned i = 0, n = triggerResults.size(); i < n; ++i){
    std::string Trigger;
    Trigger = names.triggerName(i);

    // Jets
    if (std::regex_match(Trigger, SingleJet450) && triggerResults.accept(i)) isSingleJet450_ = 1;
    if (std::regex_match(Trigger, SingleJet500) && triggerResults.accept(i)) isSingleJet500_ = 1;
    if (std::regex_match(Trigger, SingleJet550) && triggerResults.accept(i)) isSingleJet550_ = 1;
    if (std::regex_match(Trigger, HT)           && triggerResults.accept(i)) isHT_ = 1;
    
    //MET
    //if ( std::regex_match(Trigger, HBHECleaned) && triggerResults.accept(i) == 1 ) isHBHECleaned_ = 1;
    //if ( std::regex_match(Trigger, PFMET200) && triggerResults.accept(i) == 1 ) isPFMET200_ = 1;
    //if ( std::regex_match(Trigger, PFMETOne200) && triggerResults.accept(i) == 1 ) isPFMETOne200_ = 1;
    if ( std::regex_match(Trigger, PFMET120) && triggerResults.accept(i) == 1 ) isPFMET120_ = 1;
    if ( std::regex_match(Trigger, PFHT60) && triggerResults.accept(i) == 1 ) isPFHT60_ = 1;
    if ( std::regex_match(Trigger, PFHT500) && triggerResults.accept(i) == 1 ) isPFHT500_ = 1;
    if ( std::regex_match(Trigger, PFHT700) && triggerResults.accept(i) == 1 ) isPFHT700_ = 1;
    if ( std::regex_match(Trigger, PFHT800) && triggerResults.accept(i) == 1 ) isPFHT800_ = 1;
    
    if (( std::regex_match(Trigger, PFMET120) && (triggerResults.accept(i) == 1 ) ) ||
    ( std::regex_match(Trigger, PFHT60) && (triggerResults.accept(i) == 1 ) ) || 
    ( std::regex_match(Trigger, PFHT500) && (triggerResults.accept(i) == 1 ) ) ||
    ( std::regex_match(Trigger, PFHT700) && (triggerResults.accept(i) == 1 ) ) ||
    ( std::regex_match(Trigger, PFHT800) && (triggerResults.accept(i) == 1 ) ) ) isMET_ = 1;
    // Single Muon
    if (std::regex_match(Trigger, IsoMu)   && triggerResults.accept(i)) isIsoMu_   = 1;
    if (std::regex_match(Trigger, IsoMu24) && triggerResults.accept(i)) isIsoMu24_ = 1;
    if (std::regex_match(Trigger, Mu)      && triggerResults.accept(i)) isMu_      = 1;
    // MuTau
    if (std::regex_match(Trigger, IsoMuTau) && triggerResults.accept(i)) isIsoMuTau_ = 1;
    // Single Electron
    if ((std::regex_match(Trigger, IsoEle35) || std::regex_match(Trigger, IsoEle32)) && triggerResults.accept(i)) isIsoEle_ = 1;
    if (std::regex_match(Trigger, Ele)    && triggerResults.accept(i)) isEle_    = 1;
    if (std::regex_match(Trigger, EleJet) && triggerResults.accept(i)) isEleJet_ = 1;
    // ETau
    if (std::regex_match(Trigger, EleTau) && triggerResults.accept(i)) isEleTau_ = 1;
    // Di-Muon
    if ((std::regex_match(Trigger, DoubleMuMass8) || std::regex_match(Trigger, DoubleMuMass3p8)) && triggerResults.accept(i)) isDoubleMu_ = 1;
    // Di-Electron
    if (std::regex_match(Trigger, DoubleIsoEG) && triggerResults.accept(i)) isDoubleIsoEG_ = 1;
    if (std::regex_match(Trigger, DoubleEG)    && triggerResults.accept(i)) isDoubleEG_    = 1;
    // MuonEG DZ
    if ( ( std::regex_match(Trigger, Muon8EG) && (triggerResults.accept(i) == 1)) ||
    ( std::regex_match(Trigger, Muon23EG) && (triggerResults.accept(i) == 1)) ) isMuonEG_ = 1;
    if ( std::regex_match(Trigger, Muon8EG) && (triggerResults.accept(i) == 1) ) isMu8Ele23_ = 1;
    if ( std::regex_match(Trigger, Muon23EG) && (triggerResults.accept(i) == 1) ) isMu23Ele12_ = 1;
    // MuonEG noDZ
    if ( ( std::regex_match(Trigger, Muon8EGnoDZ) && (triggerResults.accept(i) == 1 ) ) ||
	 ( std::regex_match(Trigger, Muon23EGnoDZ) && (triggerResults.accept(i) == 1 ) ) ) isMuonEGnoDZ_ = 1;
    if ( std::regex_match(Trigger, Muon8EGnoDZ) && (triggerResults.accept(i) == 1) ) isMu8Ele23noDZ_ = 1;
    if ( std::regex_match(Trigger, Muon23EGnoDZ) && (triggerResults.accept(i) == 1) ) isMu23Ele12noDZ_ = 1;
    // Tau
    if (std::regex_match(Trigger, SingleTau)     && triggerResults.accept(i)) isSingleTauMET_   = 1;
    if ((std::regex_match(Trigger, DoubleTau35)  ||
         std::regex_match(Trigger, DoubleTauJet60) ||
         std::regex_match(Trigger, DoubleTauJet75)) && triggerResults.accept(i)) isDoubleTauMedium_ = 1;
    if (std::regex_match(Trigger, DisplacedDiTau) && triggerResults.accept(i)) isDisplacedDiTau_ = 1;

    //if ( std::regex_match(Trigger, DoubleTauMedium) && (triggerResults.accept(i) == 1) ) isDoubleTauMedium_ = 1;
    //if ( ( std::regex_match(Trigger, DoubleTauTight35) && (triggerResults.accept(i) == 1)) ||
	 //( std::regex_match(Trigger, DoubleTauTight40) && (triggerResults.accept(i) == 1)) ) isDoubleTauTight_ = 1;
    //if ( std::regex_match (Trigger, SingleTauMET) && (triggerResults.accept(i) == 1) ) isSingleTauMET_ = 1;
    // Photon
    if ( std::regex_match(Trigger, Photon200) && (triggerResults.accept(i) == 1) ) isPhoton200_ = 1;
    if ( std::regex_match(Trigger, Photon175) && (triggerResults.accept(i) == 1) ) isPhoton175_ = 1;

  }  
  tree->Fill();
}

DEFINE_FWK_MODULE(TCPTrigNtuples);
