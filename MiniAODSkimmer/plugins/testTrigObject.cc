// system include files
#include <memory>
#include <iostream>
#include <regex>
#include <cmath>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
// #include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"
#include "BoostedDiTau/MiniAODSkimmer/interface/TrigObjectInfoDS.h"

#include "TTree.h"

using namespace edm;
using namespace std;

class TCPTrigObjectAnalyzer : public edm::one::EDAnalyzer<edm::one::WatchRuns,edm::one::SharedResources> {
public:

  explicit TCPTrigObjectAnalyzer (const edm::ParameterSet&);
  ~TCPTrigObjectAnalyzer() override {}

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  virtual void beginJob() override;
  virtual void endJob() override {}
  virtual void beginRun(edm::Run const&, edm::EventSetup const&) override {}
  virtual void endRun(edm::Run const&, edm::EventSetup const&) override {}
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;

  edm::EDGetTokenT<edm::TriggerResults> triggerBits_;
  edm::EDGetTokenT<std::vector<pat::TriggerObjectStandAlone> > triggerObjects_;
  edm::EDGetTokenT <pat::PackedTriggerPrescales> triggerPrescales_;

  TTree *tree;
  int event_;
  TrigObjectInfoDS *trigObjectInfoData;
};

TCPTrigObjectAnalyzer::TCPTrigObjectAnalyzer(const edm::ParameterSet& iConfig):
  triggerBits_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("bits"))),
  triggerObjects_(consumes<std::vector<pat::TriggerObjectStandAlone> >(iConfig.getParameter<edm::InputTag>("objects"))),
  triggerPrescales_(consumes<pat::PackedTriggerPrescales>(iConfig.getParameter<edm::InputTag>("prescales")))
{
  usesResource(TFileService::kSharedResource);
}

void TCPTrigObjectAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions){
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

void TCPTrigObjectAnalyzer::beginJob(){

  edm::Service<TFileService> fs;
  fs->mkdir( "triggerObject" );

  tree = fs->make<TTree>("TriggerObjectTree", "");

  tree->Branch("event", &event_, "event/I");

  trigObjectInfoData = new TrigObjectInfoDS();

  tree->Branch("TriggerObjects", "TrigObjectInfoDS", &trigObjectInfoData);
}


void TCPTrigObjectAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  
  trigObjectInfoData->clear();

  int Event = iEvent.id().event();
  event_ = Event;

  edm::Handle<edm::TriggerResults> triggerBits;
  iEvent.getByToken(triggerBits_, triggerBits);

  edm::Handle<std::vector<pat::TriggerObjectStandAlone> > triggerObjects;
  iEvent.getByToken(triggerObjects_, triggerObjects);

  edm::Handle<pat::PackedTriggerPrescales> triggerPrescales;
  iEvent.getByToken(triggerPrescales_, triggerPrescales);

  const edm::TriggerNames &names = iEvent.triggerNames(*triggerBits);

  bool muonLeg, eLeg, muonLegnoDZ, eLegnoDZ;
  muonLeg = false;
  eLeg = false;
  muonLegnoDZ = false;
  eLegnoDZ = false;

  for (pat::TriggerObjectStandAlone obj : *triggerObjects) { // note: not "const &" since we want to call unpackPathNames
    obj.unpackPathNames(names);

    std::vector pathNamesAll = obj.pathNames(false);
    std::vector pathNamesLast = obj.pathNames(true);

    TrigObjectInfo trigObj;
    bool acceptedPath = false;
        
    trigObj.pt = obj.pt();
    trigObj.eta = obj.eta();
    trigObj.mass = obj.mass();
    trigObj.phi = obj.phi();  
    
    trigObj.isEleJet         = 0;
    trigObj.isEleLeg         = 0;
    trigObj.isJetLeg         = 0;

    trigObj.isSingleJet450   = 0;
    trigObj.isSingleJet500   = 0;
    trigObj.isSingleJet550   = 0;
    trigObj.isJetHTMET       = 0;
    trigObj.isJetHT          = 0;

    trigObj.isMuTau          = 0;
    trigObj.isIsoMu24        = 0;
    trigObj.isIsoMu          = 0;
    trigObj.isMu             = 0;

    trigObj.isDiEle          = 0;
    trigObj.isEleTau         = 0;
    trigObj.isSingleEle      = 0;
    trigObj.isEleHTJet       = 0;
    trigObj.isDoubleEle33    = 0;

    trigObj.isMuonEGnoDZmu   = 0;
    trigObj.isMuonEGnoDZe    = 0;
    trigObj.isMuonEGnoDZ     = 0;
    trigObj.isMuonEGmu       = 0;
    trigObj.isMuonEGe        = 0;
    trigObj.isMuonEG         = 0;

    trigObj.isDiMu           = 0;

    trigObj.isSingleTau      = 0;
    trigObj.isDisplacedDiTau = 0;
    trigObj.isDiTau          = 0;

    trigObj.isPhoton175 = 0;
    trigObj.isPhoton = 0;

    for (unsigned h = 0, n = pathNamesAll.size(); h < n; ++h) {
      /*if ( pathNamesAll[h].find("HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v") == std::string::npos &&
    	   pathNamesAll[h].find("HLT_Ele35_WPTight_Gsf_v") == std::string::npos && 
    	   pathNamesAll[h].find("HLT_Ele115_CaloIdVT_GsfTrkIdT_v") == std::string::npos &&
    	   pathNamesAll[h].find("HLT_Ele32_WPTight_Gsf_L1DoubleEG_v") == std::string::npos &&
    	   pathNamesAll[h].find("HLT_PFHT1050_v") == std::string::npos &&
    	   pathNamesAll[h].find("HLT_PFJet500_v") == std::string::npos &&
           pathNamesAll[h].find("HLT_Mu50_v") == std::string::npos &&
	   pathNamesAll[h].find("HLT_IsoMu27_v") == std::string::npos &&
	   pathNamesAll[h].find("HLT_Photon200_v") == std::string::npos &&
	   pathNamesAll[h].find("HLT_Photon175_v") == std::string::npos &&
	   pathNamesAll[h].find("HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v") == std::string::npos &&
	   pathNamesAll[h].find("HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v") == std::string::npos &&
	   pathNamesAll[h].find("HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v") == std::string::npos &&
	   pathNamesAll[h].find("HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v") == std::string::npos
    	   ) continue;*/
      
      if (pathNamesAll[h].find("HLT_PFJet450_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_PFJet500_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_PFJet550_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_PFHT500_PFMET100_PFMHT100_IDTight_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_PFHT1050_v") == std::string::npos &&

      pathNamesAll[h].find("HLT_IsoMu24_eta2p1_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_IsoMu24_eta2p1_LooseDeepTauPFTauHPS180_eta2p1_v") == std::string::npos &&
      //pathNamesAll[h].find("HLT_IsoMu20_eta2p1_TightChargedIsoPFTauHPS27_eta2p1_TightID_CrossL1_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_IsoMu24_eta2p1_LooseDeepTauPFTauHPS30_eta2p1_CrossL1_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS35_L2NN_eta2p1_CrossL1_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS30_L2NN_eta2p1_CrossL1_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS30_L2NN_eta2p1_PFJet60_CrossL1_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS30_L2NN_eta2p1_PFJet75_CrossL1_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS20_eta2p1_SingleL1_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS45_eta2p1_SingleL1_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_IsoMu24_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_IsoMu27_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_Mu50_v") == std::string::npos &&

      pathNamesAll[h].find("HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v") == std::string::npos &&      //removed in run3
      pathNamesAll[h].find("HLT_Ele24_eta2p1_WPTight_Gsf_LooseDeepTauPFTauHPS30_eta2p1_CrossL1_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_Ele32_WPTight_Gsf_L1DoubleEG_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_Ele32_WPTight_Gsf_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_Ele35_WPTight_Gsf_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_Ele50_IsoVVVL_PFHT450_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_Ele115_CaloIdVT_GsfTrkIdT_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_DoubleEle33_CaloIdL_MW_v") == std::string::npos &&

      pathNamesAll[h].find("HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v") == std::string::npos &&


      pathNamesAll[h].find("HLT_LooseDeepTauPFTauHPS180_L2NN_eta2p1_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_DoubleMediumChargedIsoDisplacedPFTauHPS32_Trk1_eta2p1_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_DoubleMediumDeepTauPFTauHPS30_L2NN_eta2p1_PFJet60_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_DoubleMediumDeepTauPFTauHPS30_L2NN_eta2p1_PFJet75_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_DoubleMediumDeepTauPFTauHPS35_L2NN_eta2p1_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v") == std::string::npos &&     //removed in run3
      pathNamesAll[h].find("HLT_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr_MET90_v") == std::string::npos &&            //removed in run3
      pathNamesAll[h].find("HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v") == std::string::npos &&      //removed in run3
      pathNamesAll[h].find("HLT_DoubleTightChargedIsoPFTauHPS35_Trk1_eta2p1_v") == std::string::npos &&               //removed in run3
      pathNamesAll[h].find("HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v") == std::string::npos &&              //removed in run3

	    pathNamesAll[h].find("HLT_Photon175_v") == std::string::npos &&
      pathNamesAll[h].find("HLT_Photon200_v") == std::string::npos
      ) continue;

      bool isL3   = obj.hasPathName( pathNamesAll[h], false, true );

      if ( !isL3 ) continue;

      bool isBoth = obj.hasPathName( pathNamesAll[h], true, true );      

      if (pathNamesAll[h].find("HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v") != std::string::npos) {
        for (unsigned h = 0; h < obj.filterIds().size(); ++h){
          if (obj.filterIds()[h] == 81 || obj.filterIds()[h] == 92 || obj.filterIds()[h] == 82 ) trigObj.isEleLeg = 1;
          if (obj.hasPathName("HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v", true, true)){
            trigObj.isJetLeg = 1;
            trigObj.isEleJet = 1;
          }
        }
        acceptedPath = true;
      }

      if (!isBoth ) continue;

      //  JetHT, JetMET 
      if (pathNamesAll[h].find("HLT_PFJet450_v") != std::string::npos){
        trigObj.isSingleJet450 = 1; acceptedPath = true;
      }
      if (pathNamesAll[h].find("HLT_PFJet500_v") != std::string::npos){
        trigObj.isSingleJet500 = 1; acceptedPath = true;
      }
      if (pathNamesAll[h].find("HLT_PFJet550_v") != std::string::npos){
        trigObj.isSingleJet550 = 1; acceptedPath = true;
      }
      if (pathNamesAll[h].find("HLT_PFHT500_PFMET100_PFMHT100_IDTight_v") != std::string::npos){
        trigObj.isJetHTMET = 1; acceptedPath = true;
      }
      if (pathNamesAll[h].find("HLT_PFHT1050_v") != std::string::npos){
        trigObj.isJetHT = 1; acceptedPath = true;
      }

      //  MuTau cross triggers
      if (pathNamesAll[h].find("HLT_IsoMu24_eta2p1_v") != std::string::npos                                              ||
          pathNamesAll[h].find("HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1_v") != std::string::npos        ||
          pathNamesAll[h].find("HLT_IsoMu24_eta2p1_LooseDeepTauPFTauHPS180_eta2p1_v") != std::string::npos               ||
          //pathNamesAll[h].find("HLT_IsoMu20_eta2p1_TightChargedIsoPFTauHPS27_eta2p1_TightID_CrossL1_v") != std::string::npos ||
          pathNamesAll[h].find("HLT_IsoMu24_eta2p1_LooseDeepTauPFTauHPS30_eta2p1_CrossL1_v") != std::string::npos        ||
          pathNamesAll[h].find("HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS35_L2NN_eta2p1_CrossL1_v") != std::string::npos  ||
          pathNamesAll[h].find("HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS30_L2NN_eta2p1_CrossL1_v") != std::string::npos  ||
          pathNamesAll[h].find("HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS30_L2NN_eta2p1_PFJet60_CrossL1_v") != std::string::npos ||
          pathNamesAll[h].find("HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS30_L2NN_eta2p1_PFJet75_CrossL1_v") != std::string::npos ||
          pathNamesAll[h].find("HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS20_eta2p1_SingleL1_v") != std::string::npos      ||
          pathNamesAll[h].find("HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS45_eta2p1_SingleL1_v") != std::string::npos){
        trigObj.isMuTau = 1; acceptedPath = true;
      }

      //  Single Muon 
      if (pathNamesAll[h].find("HLT_IsoMu24_v") != std::string::npos){
        trigObj.isIsoMu24 = 1; acceptedPath = true;
      }
      if (pathNamesAll[h].find("HLT_IsoMu27_v") != std::string::npos){
        trigObj.isIsoMu = 1; acceptedPath = true;
      }
      if (pathNamesAll[h].find("HLT_Mu50_v") != std::string::npos){
        trigObj.isMu = 1; acceptedPath = true;
      }

      //  Di-Electron 
      if (pathNamesAll[h].find("HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v") != std::string::npos    ||
          pathNamesAll[h].find("HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v") != std::string::npos){
        trigObj.isDiEle = 1; acceptedPath = true;
      }

      //  ETau 
      if (pathNamesAll[h].find("HLT_Ele24_eta2p1_WPTight_Gsf_LooseDeepTauPFTauHPS30_eta2p1_CrossL1_v") != std::string::npos){
        trigObj.isEleTau = 1; acceptedPath = true;
      }

      //  Single Electron
      if (pathNamesAll[h].find("HLT_Ele32_WPTight_Gsf_L1DoubleEG_v") != std::string::npos ||
          pathNamesAll[h].find("HLT_Ele32_WPTight_Gsf_v") != std::string::npos             ||
          pathNamesAll[h].find("HLT_Ele35_WPTight_Gsf_v") != std::string::npos){
        trigObj.isSingleEle = 1; acceptedPath = true;
      }

      //  Ele+HT/Jet
      if (pathNamesAll[h].find("HLT_Ele50_IsoVVVL_PFHT450_v") != std::string::npos    ||
          pathNamesAll[h].find("HLT_Ele115_CaloIdVT_GsfTrkIdT_v") != std::string::npos){
        trigObj.isEleHTJet = 1; acceptedPath = true;
      }

      //  DoubleEle33 
      if (pathNamesAll[h].find("HLT_DoubleEle33_CaloIdL_MW_v") != std::string::npos){
        trigObj.isDoubleEle33 = 1; acceptedPath = true;
      }

      //  MuonEG noDZ 
      if (pathNamesAll[h].find("HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v") != std::string::npos ||
          pathNamesAll[h].find("HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v") != std::string::npos){
        for (unsigned h = 0; h < obj.filterIds().size(); ++h){
          if (obj.filterIds()[h] == 83){
            trigObj.isMuonEGnoDZmu = 1;
            muonLegnoDZ = true;
          }
          if (obj.filterIds()[h] == 81 || obj.filterIds()[h] == 82 || obj.filterIds()[h] == 92){
            trigObj.isMuonEGnoDZe = 1;
            eLegnoDZ = true;
          }
        }
        acceptedPath = true;
        if (muonLegnoDZ && eLegnoDZ) trigObj.isMuonEGnoDZ = 1;
      }

      //  MuonEG DZ 
      if (pathNamesAll[h].find("HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v") != std::string::npos ||
          pathNamesAll[h].find("HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v") != std::string::npos){
        for (unsigned h = 0; h < obj.filterIds().size(); ++h){
          if (obj.filterIds()[h] == 83){
            trigObj.isMuonEGmu = 1;
            muonLeg = true;
          }
          if (obj.filterIds()[h] == 81 || obj.filterIds()[h] == 82 || obj.filterIds()[h] == 92){
            trigObj.isMuonEGe = 1;
            eLeg = true;
          }
        }
        acceptedPath = true;
        if (muonLeg && eLeg) trigObj.isMuonEG = 1;
      }
      
      //  Di-Muon 
      if (pathNamesAll[h].find("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v") != std::string::npos   ||
          pathNamesAll[h].find("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v") != std::string::npos){
        trigObj.isDiMu = 1; acceptedPath = true;
      }

      //  Single Tau
      if (pathNamesAll[h].find("HLT_LooseDeepTauPFTauHPS180_L2NN_eta2p1_v") != std::string::npos){
        trigObj.isSingleTau = 1; acceptedPath = true;
      }

      //  Displaced Di-Tau 
      if (pathNamesAll[h].find("HLT_DoubleMediumChargedIsoDisplacedPFTauHPS32_Trk1_eta2p1_v") != std::string::npos){
        trigObj.isDisplacedDiTau = 1; acceptedPath = true;
      }
      
      //  Di-Tau 
      if (pathNamesAll[h].find("HLT_DoubleMediumDeepTauPFTauHPS30_L2NN_eta2p1_PFJet60_v") != std::string::npos  ||
          pathNamesAll[h].find("HLT_DoubleMediumDeepTauPFTauHPS30_L2NN_eta2p1_PFJet75_v") != std::string::npos  ||
          pathNamesAll[h].find("HLT_DoubleMediumDeepTauPFTauHPS35_L2NN_eta2p1_v") != std::string::npos){
        trigObj.isDiTau = 1; acceptedPath = true;
      }

      //  Photon 
      if (pathNamesAll[h].find("HLT_Photon175_v") != std::string::npos){
        trigObj.isPhoton175 = 1; acceptedPath = true;
      }
      if (pathNamesAll[h].find("HLT_Photon200_v") != std::string::npos){
        trigObj.isPhoton = 1; acceptedPath = true;
      }
    }

    if (acceptedPath == false) continue;

    trigObjectInfoData->push_back(trigObj);
  }
  tree->Fill();
}


//define this as a plug-in
DEFINE_FWK_MODULE(TCPTrigObjectAnalyzer);
