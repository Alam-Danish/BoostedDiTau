import os, sys, math
import ROOT
import argparse

parser = argparse.ArgumentParser(description="Normalize by cross-section. e.g. python3 -v v6 -f studySVFit --histo MuTau_OS_dRcut_lowMt_Mass --all")
parser.add_argument("-v", "--version", type=str, help="Version for doHadd")
parser.add_argument("-f", "--filename", type=str, help="filename from condor output")
parser.add_argument("-a", "--all", action="store_true", help="go through all samples")
parser.add_argument("--era", type=str, help="Era")
parser.add_argument("--tcp", action="store_true", help="go through tcp samples only")
parser.add_argument("--bkg", action="store_true", help="go through background samples only")
parser.add_argument("-r", "--region", type=str, help="regions to plot")
parser.add_argument("--histo", type=str, nargs="+")
parser.add_argument("--alpmodel", type=str)
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

pi = math.pi

era = args.era

c_t = 1
m_t = 1.77686 #Tau Mass
fa = 1000 #dimensional param
m_a = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65]
Br = {
    'M1':{'10':6.7, '15':4.01, '20':3.4, '25':2.9, '30':2.5, '35':2.2, '40':1.9, '45':1.7, '50':1.5, '55':1.3, '60':1.2, '65':1.05},
    'M2':{'10':9.7, '15':5.8, '20':4.8, '25':4.1, '30':3.6, '35':3.1, '40':2.7, '45':2.4, '50':2.1, '55':1.9, '60':1.7, '65':1.5},
    'M3':{'10':5.7, '15':3.4, '20':2.9, '25':2.6, '30':2.2, '35':1.98, '40':1.8, '45':1.6, '50':1.4, '55':1.2, '60':1.1, '65':1.01},
    'M4':{'10':6.2, '15':3.6, '20':2.6, '25':2.03, '30':1.6, '35':1.3, '40':1.1, '45':0.9, '50':0.79, '55':0.7, '60':0.6, '65':0.53},
    'M5':{'10':3.0, '15':1.8, '20':1.5, '25':1.28, '30':1.1, '35':0.96, '40':0.84, '45':0.74, '50':0.66, '55':0.6, '60':0.52, '65':0.47},
    'M6':{'10':3.0, '15':1.8, '20':1.5, '25':1.28, '30':1.1, '35':0.96, '40':0.84, '45':0.74, '50':0.66, '55':0.6, '60':0.52, '65':0.47},
    'M7':{'10':9.7, '15':5.8, '20':4.9, '25':4.1, '30':3.6, '35':3.1, '40':2.7, '45':2.4, '50':2.1, '55':1.9, '60':1.7, '65':1.5},
    'M8':{'10':0.88, '15':0.53, '20':0.5, '25':0.49, '30':0.48, '35':0.5, '40':0.46, '45':0.4, '50':0.43, '55':0.41, '60':0.4, '65':0.4},
    'M9':{'10':1.9, '15':1.1, '20':0.74, '25':0.54, '30':0.42, '35':0.33, '40':0.27, '45':0.2, '50':0.19, '55':0.17, '60':0.14, '65':0.13},
    'M10':{'10':1.8, '15':1.05, '20':0.73, '25':0.53, '30':0.41, '35':0.33, '40':0.27, '45':0.2, '50':0.19, '55':0.17, '60':0.14, '65':0.13},
    'M11':{'10':2.1, '15':1.2, '20':1.1, '25':1.02, '30':0.94, '35':0.86, '40':0.79, '45':0.7, '50':0.66, '55':0.6, '60':0.55, '65':0.51},
    'M12':{'10':2.9, '15':1.7, '20':1.5, '25':1.4, '30':1.3, '35':1.1, '40':1.0, '45':0.9, '50':0.85, '55':0.8, '60':0.70, '65':0.6}
}


xsec_M = {
    'M1':{},
    'M2':{},
    'M3':{},
    'M4':{},
    'M5':{},
    'M6':{},
    'M7':{},
    'M8':{},
    'M9':{},
    'M10':{},
    'M11':{},
    'M12':{}
}

xsec_M_unscaled = {
    'M1':{},
    'M2':{},
    'M3':{},
    'M4':{},
    'M5':{},
    'M6':{},
    'M7':{},
    'M8':{},
    'M9':{},
    'M10':{},
    'M11':{},
    'M12':{}
}

for mass in m_a:
    Gamma_tt = ((c_t**2*mass/(8*pi))*m_t**2*math.sqrt(1-4*m_t**2/mass**2))/fa**2
    xsec_g_TCP = 1/Gamma_tt #cross section of gg fusion to tcp
    for model in Br.keys():
        xsec_M_list = xsec_g_TCP * Br[model][str(mass)]
        xsec_M_unscaled[model][str(mass)] = xsec_g_TCP
        xsec_M[model][str(mass)] = xsec_M_list

TCP_xsec = {
    'M1':{},
    'M2':{},
    'M3':{},
    'M4':{},
    'M5':{},
    'M6':{},
    'M7':{},
    'M8':{},
    'M9':{},
    'M10':{},
    'M11':{},
    'M12':{}
}

TCP_xsec_unscaled = {
    'M1':{},
    'M2':{},
    'M3':{},
    'M4':{},
    'M5':{},
    'M6':{},
    'M7':{},
    'M8':{},
    'M9':{},
    'M10':{},
    'M11':{},
    'M12':{}
}


norm = {
    '10': 3.163e-06 + 3.160e-06,
    '15': 4.712e-06 + 4.721e-06,
    '20': 6.164e-06 + 6.175e-06,
    '25': 7.530e-06 + 7.532e-06,
    '30': 8.808e-06 + 8.815e-06,
    '35': 9.970e-06 + 9.966e-06,
    '40': 1.104e-05 + 1.102e-05,
    '45': 1.203e-05 + 1.200e-05,
    '50': 1.290e-05 + 1.290e-05,
    '55': 1.370e-05 + 1.369e-05,
    '60': 1.439e-05 + 1.438e-05,
    '65': 1.501e-05 + 1.498e-05,
}

for model in Br.keys():
    for mass in range(10,70,5):
        TCP_xsec[model][str(mass)] = xsec_M[model][str(mass)] * norm[str(mass)]
        TCP_xsec_unscaled[model][str(mass)] = xsec_M_unscaled[model][str(mass)] * norm[str(mass)]


if args.alpmodel is not None:
    model = args.alpmodel
else : model = "M1"

#----------------------------------

xsecs={
     'ALP_M-10_HT-100to400_'+era: {'': xsec_M[model]['10'] * 3.163e-06},
     'ALP_M-10_HT-400toInf_'+era: {'': xsec_M[model]['10'] * 3.160e-06},
     'ALP_M-15_HT-100to400_'+era: {'': xsec_M[model]['15'] * 4.712e-06},
     'ALP_M-15_HT-400toInf_'+era: {'': xsec_M[model]['15'] * 4.721e-06},
     'ALP_M-20_HT-100to400_'+era: {'': xsec_M[model]['20'] * 6.164e-06},
     'ALP_M-20_HT-400toInf_'+era: {'': xsec_M[model]['20'] * 6.175e-06},
     'ALP_M-25_HT-100to400_'+era: {'': xsec_M[model]['25'] * 7.530e-06},
     'ALP_M-25_HT-400toInf_'+era: {'': xsec_M[model]['25'] * 7.532e-06},
     'ALP_M-30_HT-100to400_'+era: {'': xsec_M[model]['30'] * 8.808e-06},
     'ALP_M-30_HT-400toInf_'+era: {'': xsec_M[model]['30'] * 8.815e-06},
     'ALP_M-35_HT-100to400_'+era: {'': xsec_M[model]['35'] * 9.970e-06},
     'ALP_M-35_HT-400toInf_'+era: {'': xsec_M[model]['35'] * 9.966e-06},
     'ALP_M-40_HT-100to400_'+era: {'': xsec_M[model]['40'] * 1.104e-05},
     'ALP_M-40_HT-400toInf_'+era: {'': xsec_M[model]['40'] * 1.102e-05},
     'ALP_M-45_HT-100to400_'+era: {'': xsec_M[model]['45'] * 1.203e-05},
     'ALP_M-45_HT-400toInf_'+era: {'': xsec_M[model]['45'] * 1.200e-05},
     'ALP_M-50_HT-100to400_'+era: {'': xsec_M[model]['50'] * 1.290e-05},
     'ALP_M-50_HT-400toInf_'+era: {'': xsec_M[model]['50'] * 1.290e-05},
     'ALP_M-55_HT-100to400_'+era: {'': xsec_M[model]['55'] * 1.370e-05},
     'ALP_M-55_HT-400toInf_'+era: {'': xsec_M[model]['55'] * 1.369e-05},
     'ALP_M-60_HT-100to400_'+era: {'': xsec_M[model]['60'] * 1.439e-05},
     'ALP_M-60_HT-400toInf_'+era: {'': xsec_M[model]['60'] * 1.438e-05},
     'ALP_M-65_HT-100to400_'+era: {'': xsec_M[model]['65'] * 1.501e-05},
     'ALP_M-65_HT-400toInf_'+era: {'': xsec_M[model]['65'] * 1.498e-05},        
    # 'DYJetsToLL':{
    #     'M-50_HT-70to100':140.0,
    #     'M-50_HT-100to200':139.2, 
    #     'M-50_HT-200to400':38.4, 
    #     'M-50_HT-400to600':5.174,
    #     'M-50_HT-600to800':1.258, 
    #     'M-50_HT-800to1200':0.5598, 
    #     'M-50_HT-1200to2500':0.1305, 
    #     'M-50_HT-2500toInf':0.002997},
    # 'DYJetsToLL_M-4to50':{
    #     'HT-70to100':321.2,
    #     'HT-100to200':190.6,
    #     'HT-200to400':42.27,
    #     'HT-400to600':4.05,
    #     'HT-600toInf':1.216},
    # 'TT':{
    #     'TTTo2L2Nu_TuneCP5':88.2497,
    #     'TTToSemiLeptonic_TuneCP5':365.30899,
    #     'TTToHadronic_TuneCP5':377.9517},
    # 'ST':{
    #     's-channel':3.549,
    #     # 't-channel_antitop':26.2278,
    #     # 't-channel_top':44.07048,
    #     't_antitop':71.75,
    #     't_top':119.7,
    #     'tW_antitop':32.51,
    #     'tW_top':32.45},
    # 'Diboson':{
    #     'WW':76.25,
    #     'WZ':27.55,
    #     'ZZ':12.23},
    #  'WJetsToLNu_flat':{
    #      'TuneCP5':52940.0},
    #  'WJetsToLNu':{
    #      'HT-70to100':1264.0,
    #      'HT-100to200':1343.0,
    #      'HT-200to400':359.6,
    #      'HT-400to600':48.85,
    #      'HT-600to800':12.05,
    #      'HT-800to1200':5.501,
    #      'HT-1200to2500':1.329},
    #  'QCD':{
    #      'HT-50to100':185300000.0,
    #      'HT-100to200':23590000.0,
    #      'HT-200to300':1551000.0,
    #      'HT-300to500':323400.0,
    #      'HT-500to700':30140.0,
    #      'HT-700to1000':6344.0,
    #      'HT-1000to1500':1092.0,
    #      'HT-1500to2000':99.76,
    #      'HT-2000toInf':20.35},
    # 'Y':{
    #     'pth400':0.0504*0.01*0.00945495019497735,
    #     'pth100':47.980*0.01*0.00945495019497735},
    
    # 'DYJetsToLL_M-10to50':{
    #     'DYto2L-2Jets_MLL-10to50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8':20950},
    # 'DYJetsToLL_M-50':{
    #     'DYto2L-2Jets_MLL-50_0J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8':4969.83,
    #     'DYto2L-2Jets_MLL-50_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8':948.04,
    #     'DYto2L-2Jets_MLL-50_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8':365.61},
     'DYto2L-4Jets_MLL-4to50':{
        'HT-40to70_TuneCP5_13p6TeV_madgraphMLM-pythia8':911.4,
        'HT-70to100_TuneCP5_13p6TeV_madgraphMLM-pythia8':346.6,
        'HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8':316.8,
        'HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8':5.649,
        'HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8':0.4204,
        'HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8':0.02079,
        'HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8':0.00107},
     'DYto2L-4Jets_MLL-50to120':{
        'HT-40to70_TuneCP5_13p6TeV_madgraphMLM-pythia8':316.7,
        'HT-70to100_TuneCP5_13p6TeV_madgraphMLM-pythia8':140.6,
        'HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8':179.6,
        'HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8':6.742,
        'HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8':0.693,
        'HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8':0.05047,
        'HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8':0.00346},
     'DYto2L-4Jets_MLL-120':{
        'HT-40to70_TuneCP5_13p6TeV_madgraphMLM-pythia8':4.6,
        'HT-70to100_TuneCP5_13p6TeV_madgraphMLM-pythia8':2.205,
        'HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8':3.352,
        'HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8':0.1757,
        'HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8':0.02089,
        'HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8':0.001697,
        'HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8':0.0001247},
     'TT':{
         'TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8':97.74,
         'TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8':420.31,
         'TTto4Q_TuneCP5_13p6TeV_powheg-pythia8':404.95},
     'ST':{
         'TBbartoLplusNuBbar-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8':2.278,
         'TbarBtoLminusNuB-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8':1.430,
         'TBbarQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8':123.8,
         'TbarBQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8':75.47,
         'TWminus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8':35.99,
         'TbarWplus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8':36.5},
    # 'WJetsToLNu':{
    #     'WtoLNu-4Jets_1J_TuneCP5_13p6TeV_madgraphMLM-pythia8':9139.0,
    #     'WtoLNu-4Jets_2J_TuneCP5_13p6TeV_madgraphMLM-pythia8':2927.0,
    #     'WtoLNu-4Jets_3J_TuneCP5_13p6TeV_madgraphMLM-pythia8':863.1,
    #     'WtoLNu-4Jets_4J_TuneCP5_13p6TeV_madgraphMLM-pythia8':415.4},
     'WtoLNu-4Jets_MLNu-0to120':{
        'HT-40to100_TuneCP5_13p6TeV_madgraphMLM-pythia8':4254.0,
        'HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8':1626.0,
        'HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8':59.99,
        'HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8':6.23,
        'HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8':0.4477,
        'HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8':0.03075},
     'WtoLNu-4Jets_MLNu-120':{
        'HT-40to100_TuneCP5_13p6TeV_madgraphMLM-pythia8':20.56,
        'HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8':10.19,
        'HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8':0.5239,
        'HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8':0.06255,
        'HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8':0.005066,
        'HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8':0.0003788},
     'Diboson':{
         'WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8':11.79,
         'WWtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8':48.94,
         'WWto4Q_TuneCP5_13p6TeV_powheg-pythia8':50.79,
         'WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8':4.924,
         'WZtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8':15.87,
         'WZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8':7.568,
         'WZto4Q-1Jets-4FS_TuneCP5_13p6TeV_amcatnloFXFX-pythia8':24.83,
         'ZZto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8':1.031,
         'ZZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8':6.788,
         'ZZto2Nu2Q_TuneCP5_13p6TeV_powheg-pythia8':4.826,
         'ZZto4L_TuneCP5_13p6TeV_powheg-pythia8':1.39},
}


if args.filename :
    fileName = args.filename

def weightBackgroundHists(hists, files, version, study, var, Sample, era):
    for sample in Sample:
        h = None
        for mass in list(xsecs[sample]):
            #filename = "h_"+fileName+"_"+era+"_Ntuple_"+sample+"_"+mass+"_"+version+".root"
            #filename = "h_"+fileName+"_"+era+"_"+sample+"_"+mass+"_"+version+".root"
        
            plotDir = "./output/"+version+"/"
            if mass != '':
                filename = plotDir+"h_"+fileName+"_"+era+"_"+sample+"_"+mass+"_"+version+".root"
            else:
                filename = plotDir+"h_"+fileName+"_"+era+"_"+sample+"_"+version+".root"
            histname=var 
            print(filename, histname)
            fil=ROOT.TFile(filename, 'r')
            if fil.IsZombie(): continue
            files+=[fil]
            hist=fil.Get(histname)
            try:
                nEvt=fil.Get("NEvents").GetBinContent(2)
            except ReferenceError:
                print("ReferenceError")
                continue
            except AttributeError:
                print("AttributeError")
                continue
            xsec=xsecs[sample][mass]
            # if list(xsecs[sample]).index(mass)==0:  
            #     h = hist.Clone(sample+"_"+histname)                                                 
            #     h.Scale((xsec/nEvt)*L)
            #     hists[sample] = h                    
            # else: 
            #     hist.Scale((xsec/nEvt)*L)
            #     hists[sample].Add(hist)

            if h == None:
                try:
                    h = hist.Clone(sample+"_"+histname)                                                                      
                    h.Scale((xsec/nEvt)*L)                                                                           
                    hists[sample] = h
                except ReferenceError:
                    print("ReferenceError")
                    continue
                except AttributeError:
                    print("AttributeError")
                    continue
            else:
                try:
                    hist.Scale((xsec/nEvt)*L)                                                                                                  
                    hists[sample].Add(hist)
                except ReferenceError:
                    print("ReferenceError")
                    continue
                except AttributeError:
                    print("AttributeError")
                    continue



hists = {}
files = []

#L = 19500.0 #2016pre
#L = 16800.0 #2016post
#L = 36700.0 #2017 ETau
#L = 41530.0 #2017
#L = 59740.0 #2018
L = 7990.0  #2022
#L = 26680.0 #2022EE
#L = 17960.0 #2023
#L = 9680.0 #2023BPix
#L = 109950.0 #2024

#L = 14000.0 #MET_2018_BC
#L = 137600.0 #Full RunII
#L = 1
#-------------

gen = False
scaling = 'xsection' #'xsection' else: 'unity'

if args.version :
    version = args.version
    iteration = args.version
    study = args.filename

#-------------

#Sample = ['TTJets']

signal_sample = []
signal_mass= []

if args.tcp :
#    signal_sample = ['ALP_M-30_HT-100to400','ALP_M-30_HT-400toInf', 'ALP_M-20_HT-100to400', 'ALP_M-20_HT-400toInf', 'ALP_M-50_HT-100to400', 'ALP_M-50_HT-400toInf','ALP_M-65_HT-100to400','ALP_M-65_HT-400toInf']
    # signal_sample = ['ALP_M-15_HT-100to400', 'ALP_M-15_HT-400toInf','ALP_M-20_HT-100to400', 'ALP_M-20_HT-400toInf','ALP_M-25_HT-100to400', 'ALP_M-25_HT-400toInf','ALP_M-30_HT-100to400','ALP_M-30_HT-400toInf','ALP_M-35_HT-100to400', 'ALP_M-35_HT-400toInf','ALP_M-40_HT-100to400', 'ALP_M-40_HT-400toInf','ALP_M-45_HT-100to400', 'ALP_M-45_HT-400toInf', 'ALP_M-60_HT-100to400', 'ALP_M-60_HT-400toInf','ALP_M-55_HT-100to400', 'ALP_M-55_HT-400toInf','ALP_M-50_HT-100to400', 'ALP_M-50_HT-400toInf']
    signal_sample = ['ALP_M-30_HT-100to400_'+era,'ALP_M-30_HT_400toInf'+era]
    signal_mass = [x.split("_")[0]+'_'+x.split("_")[1]+'_'+x.split("_")[2]+'_'+x.split("_")[3] for x in signal_sample]
    signal_mass = list(set(signal_mass))
    Sample = signal_sample
if args.all :
    signal_sample = ['ALP_M-15_HT-100to400_'+era, 'ALP_M-15_HT-400toInf_'+era,'ALP_M-20_HT-100to400_'+era, 'ALP_M-20_HT-400toInf_'+era,'ALP_M-25_HT-100to400_'+era, 'ALP_M-25_HT-400toInf_'+era,'ALP_M-30_HT-100to400_'+era,'ALP_M-30_HT-400toInf_'+era,'ALP_M-35_HT-100to400_'+era, 'ALP_M-35_HT-400toInf_'+era,'ALP_M-40_HT-100to400_'+era, 'ALP_M-40_HT-400toInf_'+era, 'ALP_M-45_HT-100to400_'+era, 'ALP_M-45_HT-400toInf_'+era, 'ALP_M-50_HT-100to400_'+era, 'ALP_M-50_HT-400toInf_'+era, 'ALP_M-55_HT-100to400_'+era, 'ALP_M-55_HT-400toInf_'+era, 'ALP_M-60_HT-100to400_'+era, 'ALP_M-60_HT-400toInf_'+era, 'ALP_M-65_HT-100to400_'+era, 'ALP_M-65_HT-400toInf_'+era]
    signal_mass = [x.split("_")[0]+'_'+x.split("_")[1] for x in signal_sample]
    signal_mass = list(set(signal_mass))
    #bkg_sample = ['DYJetsToLL','DYJetsToLL_M-4to50','WJetsToLNu','Diboson','TT','ST']
    bkg_sample = ['DYto2L-4Jets_MLL-4to50','DYto2L-4Jets_MLL-50to120','DYto2L-4Jets_MLL-120','WtoLNu-4Jets_MLNu-0to120','WtoLNu-4Jets_MLNu-120','Diboson','TT','ST']
    Sample = signal_sample+bkg_sample
if args.bkg :
    Sample = ['TT','ST']


VARIABLE = ['Lepton1Pt', 'Lepton2Pt','dRl', 'MetPt', 'Mass', 'VisMass']

REGION = []

histlist = []

#for region in REGION:
if args.region is not None:
    for variable in VARIABLE:
        histlist.append(args.region+"_"+variable)

if args.histo is not None:
    histlist = args.histo
    
for var in histlist:
    weightBackgroundHists(hists, files, version, study, var, Sample, era)
    plotDir = "./output/"+version+"/"
    if scaling == 'xsection':
         out = ROOT.TFile(plotDir+"h_"+var+"_"+study+"_"+iteration+"_"+model+".root",'recreate')
         print(out)
    else: 
         out = ROOT.TFile(plotDir+"h_"+study+"_"+var+"_"+version+"_unity.root",'recreate')

    out.cd()

    print(hists)

    for name in Sample:
        try:
            if name=='DYJetsToLL_M-4to10':
                hists[name].SetFillColor(ROOT.kRed-6)
            elif name=='DYJetsToLL_M-10to50':
                hists[name].SetFillColor(ROOT.kRed-9)
            elif name=='DYJetsToLL_M-50':
                hists[name].SetFillColor(ROOT.kRed-7)
            elif name=='TTJets':
                hists[name].SetFillColor(ROOT.kOrange-4)
            elif name=='TTTo2L2Nu':
                hists[name].SetFillColor(ROOT.kOrange-4)
            elif name=='TTToSemiLeptonic':
                hists[name].SetFillColor(ROOT.kOrange-5)
            elif name=='TTToHadronic':
                hists[name].SetFillColor(ROOT.kOrange-6)
            elif name=='ST':
                hists[name].SetFillColor(ROOT.kMagenta-9)
            elif name == 'Diboson':
                hists[name].SetFillColor(ROOT.kAzure+7)
            elif name == 'QCD':
                hists[name].SetFillColor(ROOT.kGray)
            elif name=='WJetsToLNu':
                hists[name].SetFillColor(ROOT.kGreen-6)

            if name not in signal_sample:
                hists[name].Write()
                print(hists[name].GetName())
                print(name)
                
        except KeyError:
            continue

    for sig in signal_mass:
        print(sig)
        tmp = {}
        for key in hists.keys():
            if sig in key:
                if '100to400' in key:
                    tmp[sig] = hists[key]
                if '400toInf' in key:
                    if '100to400' not in key:
                        tmp[sig] = hists[key]
                    else:
                        tmp[sig].Add(hists[key])
                    print(sig+"_"+var)
                    tmp[sig].SetName(sig+"_"+var)
                    tmp[sig].Write(sig+"_"+var, ROOT.TObject.kWriteDelete)
                    # tmp[sig].SetName(sig+"_ETau_SR_2017_OS_Boost_Mass")
                    # tmp[sig].Write(sig+"_ETau_SR_2017_OS_Boost_Mass", ROOT.TObject.kWriteDelete)
                    

    out.Close()

print(VARIABLE)
print("Histlist")
print(*histlist, sep=", ")
print("Regions")
print(*REGION, sep=", ")
