#ifndef __TCPAnalysis_TauInfoDS_H__
#define __TCPAnalysis_TauInfoDS_H__

#include <vector>

struct TauInfo {
  float pt, eta, phi, mass, charge;
  int decaymode;
  float mvaidraw;
  int mvaid; // VVLoose 1, VLoose 2, Loose 3, Medium 4, Tight 5, VTight 6, VVTight 7
  float deepidraw;
  int deepid; // VVVLoose 0, VVLoose 1, VLoose 2, Loose 3, Medium 4, Tight 5, VTight 6, VVTight 7
  //float dxy, dz;
  
  float vsjetraw;   // byDeepTau2018v2p5VSjetraw
  int   vsjet;      // VVVLoose=0, VVLoose=1, VLoose=2, Loose=3, Medium=4, Tight=5, VTight=6, VVTight=7
  
  float vseraw;     // byDeepTau2018v2p5VSeraw
  int   vse;        // VVVLoose=0, VVLoose=1, VLoose=2, Loose=3, Medium=4, Tight=5, VTight=6, VVTight=7

  float vsmuraw;    // byDeepTau2018v2p5VSmuraw
  int   vsmu;       // VLoose=0, Loose=1, Medium=2, Tight=3

  bool operator<(const TauInfo& t) const { return pt < t.pt; }
  
};

typedef class std::vector<TauInfo> TauInfoDS;

#endif
