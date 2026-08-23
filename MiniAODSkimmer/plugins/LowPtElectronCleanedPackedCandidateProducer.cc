// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/AssociationMap.h"
#include "DataFormats/Common/interface/Ref.h"
#include "DataFormats/Common/interface/RefProd.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "TLorentzVector.h"
#include "TMath.h"
#include "DataFormats/Math/interface/deltaR.h"

//
// class declaration
//

class LowPtElectronCleanedPackedCandidateProducer : public edm::stream::EDProducer<> {
   public:
      explicit LowPtElectronCleanedPackedCandidateProducer(const edm::ParameterSet&);
      ~LowPtElectronCleanedPackedCandidateProducer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginStream(edm::StreamID) override;
      virtual void produce(edm::Event&, const edm::EventSetup&) override;
      virtual void endStream() override;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
  edm::EDGetTokenT<pat::ElectronRefVector> electronSrc_;
  edm::EDGetTokenT<pat::PackedCandidateCollection> packedCandSrc_;
  
  edm::ParameterSet* cfg_;

};

//
// constants, enums and typedefs
//


//
// static data member definitions
//

//
// constructors and destructor
//
LowPtElectronCleanedPackedCandidateProducer::LowPtElectronCleanedPackedCandidateProducer(const edm::ParameterSet& iConfig):
  electronSrc_(consumes<pat::ElectronRefVector>(iConfig.getParameter<edm::InputTag>("electronSrc"))),
  packedCandSrc_(consumes<pat::PackedCandidateCollection>(iConfig.getParameter<edm::InputTag>("packedCandSrc")))
{
  //register your products
  cfg_ = const_cast<edm::ParameterSet*>(&iConfig);
  
  produces<pat::PackedCandidateCollection >("packedPFCandidatesLowPtElectronCleaned");
  //now do what ever other initialization is needed
  
}


LowPtElectronCleanedPackedCandidateProducer::~LowPtElectronCleanedPackedCandidateProducer()
{
 
   // do anything here that needs to be done at destruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
LowPtElectronCleanedPackedCandidateProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   

   
   edm::Handle<pat::ElectronRefVector> electrons;
   iEvent.getByToken(electronSrc_, electrons);

   edm::Handle<pat::PackedCandidateCollection> packedCands;
   iEvent.getByToken(packedCandSrc_, packedCands);
   std::unique_ptr<pat::PackedCandidateCollection> packedCandsExcludingElectrons(new pat::PackedCandidateCollection);
   //Get the PFCandidates being pointed to by pat::Electrons
   std::vector<int> electronIds;
  for(unsigned int iElec = 0; iElec<electrons->size(); iElec++){
    pat::Electron ele(*((*electrons)[iElec].get()));
    int eraseId = -1;
    float drMin=9999;
    for(size_t i = 0; i < packedCands->size(); ++i){
      pat::PackedCandidate cand = (*packedCands)[i];
      if (abs(cand.pdgId())==11){
        //float dPhi=ele.phi()-cand.phi();
	float dPhi = reco::deltaPhi(ele.phi(), cand.phi());
        float dEta=ele.eta()-cand.eta();
        float dr = sqrt((dPhi*dPhi+dEta*dEta));
        if (dr<drMin&& dr<.1){
          drMin=dr;
          eraseId=i;
        }
      }
    }
    if (eraseId!=-1){
      electronIds.push_back(eraseId);
      //std::cout<<"Erased Electron with dr="<<drMin;
    }
  }

	for(size_t i = 0; i < packedCands->size(); ++i){
    if (std::find(electronIds.begin(), electronIds.end(), i) == electronIds.end()) {
      packedCandsExcludingElectrons->push_back((*packedCands)[i]);


    }
  }
   


   iEvent.put(std::move(packedCandsExcludingElectrons),"packedPFCandidatesLowPtElectronCleaned");

}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void
LowPtElectronCleanedPackedCandidateProducer::beginStream(edm::StreamID)
{
}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void
LowPtElectronCleanedPackedCandidateProducer::endStream() {
}

// ------------ method called when starting to processes a run  ------------
/*
void
ElectronCleanedPackedCandidateProducer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a run  ------------
/*
void
ElectronCleanedPackedCandidateProducer::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when starting to processes a luminosity block  ------------
/*
void
ElectronCleanedPackedCandidateProducer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
ElectronCleanedPackedCandidateProducer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
LowPtElectronCleanedPackedCandidateProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(LowPtElectronCleanedPackedCandidateProducer);
