#include "BoostedDiTau/MiniAODSkimmer/plugins/fastMTTNtuples.h"

fastMTTNtuples::fastMTTNtuples(const edm::ParameterSet& iConfig) :
  MET_(consumes< vector<pat::MET> > (iConfig.getParameter<edm::InputTag>("METCollection"))),
  Jets_(consumes< vector<pat::Jet> > (iConfig.getParameter<edm::InputTag>("JetCollection"))),
  Muons_(consumes< vector<pat::Muon> > (iConfig.getParameter<edm::InputTag>("MuonCollection"))),
  Vertices_(consumes< vector<reco::Vertex> > (iConfig.getParameter<edm::InputTag>("VertexCollection"))),
  TausMCleaned_(consumes< vector<pat::Tau> > (iConfig.getParameter<edm::InputTag>("MCleanedTauCollection"))),
  TausBoosted_(consumes< vector<pat::Tau> > (iConfig.getParameter<edm::InputTag>("BoostedTauCollection"))) {
  usesResource(TFileService::kSharedResource);
}

void fastMTTNtuples::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

void fastMTTNtuples::beginJob() {
  
  edm::Service<TFileService> fs;
  //fs->mkdir( "analysis" );
  
  tree = fs->make<TTree>("analysisTree", "");
  
  tree->Branch("run", &run_, "run/I");
  tree->Branch("lumiblock", &lumiblock_, "lumiblock/I");
  tree->Branch("event", &event_, "event/I");
  
  tree->Branch("info", &evtInfo_, "mu_pt/F:tau_pt/F:mu_eta/F:tau_eta/F:mu_phi/F:tau_phi/F:mu_m/F:tau_m/F:pt/F:phi/F:ptUncor/F:phiUncor/F:ptJECUp/F:phiJECUp/F:ptJERUp/F:phiJERUp/F:ptUncUp/F:phiUncUp/F:ptJECDown/F:phiJECDown/F:ptJERDown/F:phiJERDown/F:ptUncDown/F:phiUncDown/F:covXX/F:covYY/F:covXY/F");
}

void fastMTTNtuples::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

  Reset();

  int Event = iEvent.id().event();
  int Run = iEvent.id().run();
  int LumiBlock = iEvent.id().luminosityBlock();

  run_ = Run;
  lumiblock_ = LumiBlock;
  event_ = Event;

  edm::Handle< std::vector<pat::MET> > METHandle;
  iEvent.getByToken(MET_, METHandle);
  auto met = METHandle->front();

  evtInfo_.pt = met.pt();
  evtInfo_.phi = met.phi();
  evtInfo_.ptUncor = met.uncorPt();
  evtInfo_.phiUncor = met.uncorPhi();
  evtInfo_.ptJECUp = met.shiftedPt(pat::MET::JetEnUp);
  evtInfo_.phiJECUp = met.shiftedPhi(pat::MET::JetEnUp);
  evtInfo_.ptJERUp = met.shiftedPt(pat::MET::JetResUp);
  evtInfo_.phiJERUp = met.shiftedPhi(pat::MET::JetResUp);
  evtInfo_.ptUncUp = met.shiftedPt(pat::MET::UnclusteredEnUp);
  evtInfo_.phiUncUp = met.shiftedPhi(pat::MET::UnclusteredEnUp);
  evtInfo_.ptJECDown = met.shiftedPt(pat::MET::JetEnDown);
  evtInfo_.phiJECDown = met.shiftedPhi(pat::MET::JetEnDown);
  evtInfo_.ptJERDown = met.shiftedPt(pat::MET::JetResDown);
  evtInfo_.phiJERDown = met.shiftedPhi(pat::MET::JetResDown);
  evtInfo_.ptUncDown = met.shiftedPt(pat::MET::UnclusteredEnDown);
  evtInfo_.phiUncDown = met.shiftedPhi(pat::MET::UnclusteredEnDown);
  evtInfo_.covXX = met.getSignificanceMatrix().At(0,0);
  evtInfo_.covYY = met.getSignificanceMatrix().At(1,1);
  evtInfo_.covXY = met.getSignificanceMatrix().At(0,1);


  edm::Handle< std::vector<pat::Jet> > JetsHandle;
  iEvent.getByToken(Jets_, JetsHandle);
  auto Jets = *JetsHandle;

  std::vector<pat::Jet> selected_jets;
  if (Jets.size() > 0) {
    for (unsigned int i = 0; i < Jets.size(); ++i) {
      auto jet = Jets[i];
      if (jet.pt() < 100 || fabs(jet.eta()) > 2.5) continue;
      float NHF  = jet.neutralHadronEnergyFraction();
      float NEMF = jet.neutralEmEnergyFraction();
      float CHF  = jet.chargedHadronEnergyFraction();
      float MUF  = jet.muonEnergyFraction();
      float CEMF = jet.chargedEmEnergyFraction();
      auto NumConst = jet.chargedMultiplicity()+jet.neutralMultiplicity();
      //auto NumNeutralParticles = jet.neutralMultiplicity();
      auto CHM = jet.chargedMultiplicity();
      bool jetID = CHM>0 && CHF>0 && NumConst>1 && NEMF<0.9 && NHF < 0.9;
      bool jetIDLepVeto = CEMF<0.8 && CHM>0 && CHF>0 && NumConst>1 && NEMF<0.9 && MUF <0.8 && NHF < 0.9;
      if (jetID) {
        selected_jets.push_back(jet);
      }
    }
  }

  edm::Handle< std::vector<pat::Muon> > MuonsHandle;
  iEvent.getByToken(Muons_, MuonsHandle);
  auto Muons = *MuonsHandle;


  std::vector<pat::Muon> selected_muons;
  if (Muons.size() > 0) {
    for (unsigned int i = 0; i < Muons.size(); ++i) {
      auto muon = Muons[i];
      if (muon.pt() < 3 || fabs(muon.eta()) > 2.4 || !muon.isLooseMuon()) continue;
      selected_muons.push_back(muon);
    }
  }


  edm::Handle< std::vector<pat::Tau> > TausMCleanedHandle;
  iEvent.getByToken(TausMCleaned_, TausMCleanedHandle);
  auto Taus = *TausMCleanedHandle;

  std::vector<pat::Tau> selected_taus;
  if (Taus.size()>0) {
    for (unsigned int i = 0; i < Taus.size(); ++i) {
      auto tau = Taus[i];
      if (tau.pt() < 10 || fabs(tau.eta()) > 2.5) continue;
      if (!tau.tauID("byVLooseDeepTau2018v2p5VSjet")) continue;
      selected_taus.push_back(tau);
    }
  }
  

  // ── Boosted Tau selection ──────────────────────────────────────────
  edm::Handle< std::vector<pat::Tau> > TausBoostedHandle;
  iEvent.getByToken(TausBoosted_, TausBoostedHandle);
  auto TausBoosted = *TausBoostedHandle;

  std::vector<pat::Tau> selected_boosted_taus;
  if (TausBoosted.size() > 0) {
      for (unsigned int i = 0; i < TausBoosted.size(); ++i) {
          auto tau = TausBoosted[i];
          if (tau.pt() < 10 || fabs(tau.eta()) > 2.5) continue;
          if (!tau.tauID("byVLooseDeepTau2018v2p5VSjet")) continue;
          selected_boosted_taus.push_back(tau);
      }
  }

  edm::Handle< std::vector<reco::Vertex> > VerticesHandle;
  iEvent.getByToken(Vertices_, VerticesHandle);

  // Guard against empty vertex collection (pathological events)
  if (VerticesHandle->empty()) { tree->Fill(); return; }
  const reco::Vertex& primaryVertex = VerticesHandle->front();

  // Then use primaryVertex for muon dxy/dz cuts if desired:
  // e.g. fabs(muon.muonBestTrack()->dxy(primaryVertex.position())) < 0.2

  if (selected_jets.size()>0 && selected_muons.size()>0 && (selected_taus.size()>0 || selected_boosted_taus.size() > 0)) {
    
    pat::Tau bestTau;
    bool foundTau = false;
    if (selected_taus.size() > 0) {
        bestTau = selected_taus[0];
        foundTau = true;
    } else if (selected_boosted_taus.size() > 0) {
        bestTau = selected_boosted_taus[0];
        foundTau = true;
    }

    if (foundTau && deltaR(selected_jets[0].phi(), bestTau.phi(), selected_jets[0].eta(), bestTau.eta()) > 0.8  && \
    deltaR(selected_jets[0].phi(), selected_muons[0].phi(), selected_jets[0].eta(), selected_muons[0].eta()) > 0.8  && \
    deltaR(selected_muons[0].phi(), bestTau.phi(), selected_muons[0].eta(), bestTau.eta())< 0.4  && \
    deltaR(selected_muons[0].phi(), bestTau.phi(), selected_muons[0].eta(), bestTau.eta())> 0.01 ) {
      evtInfo_.mu_pt = selected_muons[0].pt();
      evtInfo_.tau_pt = bestTau.pt();
      evtInfo_.mu_eta = selected_muons[0].eta();
      evtInfo_.tau_eta = bestTau.eta();
      evtInfo_.mu_phi = selected_muons[0].phi();
      evtInfo_.tau_phi = bestTau.phi();
      evtInfo_.mu_m = selected_muons[0].mass();
      evtInfo_.tau_m = bestTau.mass();
    }													    
  }
  
  
  
  tree->Fill();

  selected_jets.clear();
  selected_muons.clear();
  selected_taus.clear();
  selected_boosted_taus.clear();
}

float fastMTTNtuples::deltaR(float phi1, float phi2, float eta1, float eta2) {
  
  const float dphi = reco::deltaPhi(phi1, phi2);
  const float deta = eta1 - eta2;
  const float dr = std::sqrt(deta*deta + dphi*dphi);
  return dr;
}


//#include "FWCore/Framework/interface/MakerMacros.h"
//define this as a plug-in
DEFINE_FWK_MODULE(fastMTTNtuples);
