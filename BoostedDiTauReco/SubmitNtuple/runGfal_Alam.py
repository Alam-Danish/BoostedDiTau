import sys,os
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="To submit MC/data to condor. Example python3 submitAllJobs.py --mc DYJetsToLL_M-4to50")
    parser.add_argument("--complete", action="store_true", help="submit all MC samples and data (current default SingleE and JetHT)")
    parser.add_argument("--sim", action="store_true", help="submit all MC samples only")
    parser.add_argument("--mc", nargs="+", type=str, help="MC samples to submit")
    parser.add_argument("--data", nargs="+", type=str, help="submit dataset")
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    os.system("./makeTarBall.csh")

    if args.sim:
        SAMPLE = ['DYJetsToLL_M-50','DYJetsToLL_M-4to50','WJetsToLNu','QCD','YMuMu']
        
        SAMPLE += ['WZ', 'WW', 'ZZ', 'ST_tW_top','ST_tW_antitop','ST_s-channel','ST_t-channel_antitop', 'ST_t-channel_top', 'DYJetsToLL']
        #SAMPLE += ['WZ', 'WW', 'ZZ', 'ST_tW_top','ST_tW_antitop','ST_s-channel','ST_t-channel_antitop', 'ST_t-channel_top', 'TTTo2L2Nu', 'DYJetsToLL']

        #SAMPLE = ['TTJets', 'DYJetsToLL']

        for sample in SAMPLE:
            os.system("./submitJobs.csh "+sample+" -b")

    if args.complete:
        SAMPLE = ['DYJetsToLL_M-50','DYJetsToLL_M-4to50','WJetsToLNu','WW','WZ','ZZ','ST_tW_top','ST_tW_antitop','TTTo2L2Nu','TTToSemiLeptonic','ST_s-channel','ST_t-channel_antitop','ST_t-channel_top','TTToHadronic','QCD']

        DATASET = ["SingleElectron", "JetHT"]

        for sample in SAMPLE:
            os.system("./submitJobs.csh "+sample+" -b")

        # for dataset in DATASET:
        #     if dataset == "SingleElectron":
        #         os.system("./submitJobs.csh "+dataset+" -de")
        #         print("./submitJobs.csh "+dataset+" -de")

        #     if dataset == "JetHT":
        #         os.system("./submitJobs.csh "+dataset+" -dj")
        #         print("./submitJobs.csh "+dataset+" -dj")


    elif args.mc is not None:
        SAMPLE = args.mc

        for sample in SAMPLE:
            os.system("./submitJobs.csh "+sample+" -b")

    elif args.data is not None:
        DATASET = args.data

        for dataset in DATASET:
            if dataset == "SingleElectron":
                os.system("./submitJobs.csh "+dataset+" -de")
                print("./submitJobs.csh "+dataset+" -de")

            if dataset == "SingleMuon":
                os.system("./submitJobs.csh "+dataset+" -de")
                print("./submitJobs.csh "+dataset+" -de")

            if dataset == "JetHT":
                os.system("./submitJobs.csh "+dataset+" -dj")
                print("./submitJobs.csh "+dataset+" -dj")

        print("Submitted "+str(DATASET))

    #print("Submitted "+str(SAMPLE))
