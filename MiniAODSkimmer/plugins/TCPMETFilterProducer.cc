
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

#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"

#include "TTree.h"

using namespace edm;
using namespace std;

class TCPMETFilter : public edm::one::EDAnalyzer<edm::one::WatchRuns,edm::one::SharedResources> {
public:

  explicit TCPMETFilter(const edm::ParameterSet&);
  ~TCPMETFilter() override {}

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:

  virtual void beginJob() override;
  virtual void endJob() override {}
  virtual void beginRun(edm::Run const&, edm::EventSetup const&) override {}
  virtual void endRun(edm::Run const&, edm::EventSetup const&) override {}
  virtual void analyze(edm::Event const&, edm::EventSetup const&) override;


  // bool doprints_;		

  edm::EDGetTokenT<edm::TriggerResults> metFiltersToken_;

  // std::string beamHaloFilter_;
  // std::string hbheFilter_;
  // std::string hbheIsoFilter_;
  // std::string ecalTPFilter_;
  // std::string badPFMuonFilter_;
  // std::string badChargedCandFilter_;
  // std::string eeBadScFilter_;

  bool beamHaloFilter_;
  bool primaryVertexFilter_;
  //bool hbheFilter_;
  //bool hbheIsoFilter_;
  bool ecalTPFilter_;
  bool badPFMuonFilter_;
  bool badPFMuonDzFilter_;
  bool hfNoisyHitsFilter_;
  //bool badChargedCandFilter_;
  bool eeBadScFilter_;
  bool ecalBadCalFilter_;

  std::string beamHaloFilterSt_;
  std::string primaryVertexFilterSt_;
  //std::string hbheFilterSt_;
  //std::string hbheIsoFilterSt_;
  std::string ecalTPFilterSt_;
  std::string badPFMuonFilterSt_;
  std::string badPFMuonDzFilterSt_;
  std::string hfNoisyHitsFilterSt_;
  //std::string badChargedCandFilterSt_;
  std::string eeBadScFilterSt_;
  std::string ecalBadCalFilterSt_;

  TTree *tree;

  int event_;

};

TCPMETFilter::TCPMETFilter(const edm::ParameterSet& iConfig):
  //doprints_(iConfig.getParameter<bool>("doprints")),
  metFiltersToken_(consumes< edm::TriggerResults >(iConfig.getParameter<edm::InputTag>("metFilters"))){
  usesResource(TFileService::kSharedResource);
  beamHaloFilterSt_       = iConfig.getParameter<std::string>("beamHaloFilterSel");
  primaryVertexFilterSt_  = iConfig.getParameter<std::string>("primaryVertexFilterSel");
  //hbheFilterSt_           = iConfig.getParameter<std::string>("hbheFilterSel");
  //hbheIsoFilterSt_        = iConfig.getParameter<std::string>("hbheIsoFilterSel");
  ecalTPFilterSt_         = iConfig.getParameter<std::string>("ecalTPFilterSel");
  badPFMuonFilterSt_      = iConfig.getParameter<std::string>("badPFMuonFilterSel");
  badPFMuonDzFilterSt_    = iConfig.getParameter<std::string>("badPFMuonDzFilterSel");
  hfNoisyHitsFilterSt_    = iConfig.getParameter<std::string>("HFnoisyhitsFilterSel");
  //badChargedCandFilterSt_ = iConfig.getParameter<std::string>("badChargedCandFilterSel");
  eeBadScFilterSt_        = iConfig.getParameter<std::string>("eeBadScFilterSel");
  ecalBadCalFilterSt_     = iConfig.getParameter<std::string>("ecalBadCalFilterSel");
}

void TCPMETFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

void TCPMETFilter::beginJob(){

  edm::Service<TFileService> fs;

  tree = fs->make<TTree>("metfilterTree", "");

  tree->Branch("event", &event_, "event/I");

  tree->Branch("primaryvertexfilter", &primaryVertexFilter_, "primaryvertexfilter/O");
  tree->Branch("beamhalofilter", &beamHaloFilter_, "beamhalofilter/O");
  //tree->Branch("hbhefilter", &hbheFilter_, "hbhefilter/O");
  //tree->Branch("hbheisofilter", &hbheIsoFilter_, "hbheisofilter/O");
  tree->Branch("ecaltpfilter", &ecalTPFilter_, "ecaltpfilter/O");
  tree->Branch("badpfmuonfilter", &badPFMuonFilter_, "badpfmuonfilter/O");
  tree->Branch("badpfmuonDzfilter", &badPFMuonDzFilter_, "badpfmuonDzfilter/O");
  tree->Branch("hfnoisyhitsfilter", &hfNoisyHitsFilter_, "hfnoisyhitsfilter/O");
  //tree->Branch("badchangedcandfilter", &badChargedCandFilter_,"badchangedcandfilter/O");
  tree->Branch("eebadscfilter", &eeBadScFilter_, "eebadscfilter/O");
  tree->Branch("ecalbadcalfilter", &ecalBadCalFilter_, "ecalbadcalfilter/O");

}

void TCPMETFilter::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){

  int Event = iEvent.id().event();

  edm::Handle<edm::TriggerResults> metFilters;
  iEvent.getByToken(metFiltersToken_, metFilters);

  const edm::TriggerNames &names = iEvent.triggerNames(*metFilters);

  // TriggerResults triggerResults = *metFilters;
  // auto &names = iEvent.triggerNames(*metFilters);
  
  beamHaloFilter_ = 0;
  primaryVertexFilter_ = 0;
  //hbheFilter_ = 0;
  //hbheIsoFilter_ = 0;
  ecalTPFilter_ = 0;
  badPFMuonFilter_ = 0;
  badPFMuonDzFilter_ = 0;
  hfNoisyHitsFilter_ = 0;
  //badChargedCandFilter_ = 0;
  eeBadScFilter_ = 0;
  ecalBadCalFilter_ = 0;

  event_ = Event;

  for (unsigned i = 0, n = metFilters->size(); i < n; ++i){

    if ( names.triggerName(i) == beamHaloFilterSt_ && metFilters->accept(i) == 1 ) beamHaloFilter_ = 1;
    if ( names.triggerName(i) == primaryVertexFilterSt_ && metFilters->accept(i) == 1 ) primaryVertexFilter_ = 1;
    //if ( names.triggerName(i) == hbheFilterSt_ && metFilters->accept(i) == 1 ) hbheFilter_ = 1;
    //if ( names.triggerName(i) == hbheIsoFilterSt_ && metFilters->accept(i) == 1 ) hbheIsoFilter_= 1;
    if ( names.triggerName(i) == ecalTPFilterSt_ && metFilters->accept(i) == 1 ) ecalTPFilter_ = 1;
    if ( names.triggerName(i) == badPFMuonFilterSt_ && metFilters->accept(i) == 1 ) badPFMuonFilter_ = 1;
    if ( names.triggerName(i) == badPFMuonDzFilterSt_ && metFilters->accept(i) == 1 ) badPFMuonDzFilter_ = 1;
    if ( names.triggerName(i) == hfNoisyHitsFilterSt_ && metFilters->accept(i) == 1 ) hfNoisyHitsFilter_ = 1;
    //if ( names.triggerName(i) == badChargedCandFilterSt_ && metFilters->accept(i) == 1 ) badChargedCandFilter_ = 1;
    if ( names.triggerName(i) == eeBadScFilterSt_ && metFilters->accept(i) == 1 ) eeBadScFilter_ = 1;
    if ( names.triggerName(i) == ecalBadCalFilterSt_ && metFilters->accept(i) == 1 ) ecalBadCalFilter_ = 1;

    // if (names.triggerName(i) == primaryVertexFilterSt_) { std::cout << " Primary Vertex " << metFilters->accept(i) << "\n"; }
    // if (names.triggerName(i) == beamHaloFilterSt_) { std::cout << " Beam Halo = " << metFilters->accept(i) << "\n"; }
    // if (names.triggerName(i) == hbheFilterSt_) { std::cout << " HBHE = " << metFilters->accept(i) << "\n"; }
    // if (names.triggerName(i) == hbheIsoFilterSt_) { std::cout << " HBHE (Iso) = " << metFilters->accept(i) << "\n"; }
    // if (names.triggerName(i) == ecalTPFilterSt_) { std::cout << " Ecal TP = " << metFilters->accept(i) << "\n"; }
    // if (names.triggerName(i) == badPFMuonFilterSt_) { std::cout << " Bad PF Muon = " << metFilters->accept(i) << "\n"; }
    // if (names.triggerName(i) == badChargedCandFilterSt_) { std::cout << " Bad Charged Hadron = " << metFilters->accept(i) << "\n"; }
    // if (names.triggerName(i) == eeBadScFilterSt_) { std::cout << " EE SuperCluster = " << metFilters->accept(i) << "\n"; }
    // if (names.triggerName(i) == ecalBadCalFilterSt_) { std::cout << " ECAL Bad Calibration = " << metFilters->accept(i) << "\n"; }
  }


  tree->Fill();
}

DEFINE_FWK_MODULE(TCPMETFilter);
