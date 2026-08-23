#ifndef __TCPAnalysis_JetInfoDS_H__
#define __TCPAnalysis_JetInfoDS_H__

#include <vector>

struct JetInfo {
  float pt, eta, phi, mass;
  float ptuncor; 
  float deepcsv;
  float pNet; 
  float deepjet;
  int id; //jetID 1, jetID + lept-veto 2
  int puid; // fail 0, loose 1, medium 2, tight 3
  int jetflavour;

  bool operator<(const JetInfo& j) const { return pt < j.pt; }
  
};

typedef class std::vector<JetInfo> JetInfoDS;

#endif
