import sys
import os
sys.path.append('cfgs/')
import ROOT

if __name__ == "__main__":
        import argparse
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument("-c","--config", dest="config",default="", required=True, help='configuration name')
        parser.add_argument("--input",dest="input", default='', help='folder with input root files')
    	parser.add_argument("--exp",dest="exp", action="store_true", default=False, help='write expected limits')
        args = parser.parse_args()


        configName = "scanConfiguration_%s"%args.config

        config =  __import__(configName)


       	if args.input == "":
		dirs=[d for d in os.listdir(os.getcwd()+"/results_%s"%args.config) if os.path.isdir(os.getcwd()+"/results_%s"%args.config+"/"+d)]
		inputDir = "results_%s/"%args.config+dirs[-1]

        else:
                inputDir = args.input

        print "Taking inputs from %s"%inputDir

	if not args.exp:
		outFile = open("limitCard_%s_Obs.txt"%(args.config), "w")
	else:
		outFile = open("limitCard_%s_Exp.txt"%(args.config), "w")
		

	

        for massRange in config.masses:
                mass = massRange[1]
                while mass <= massRange[2]:
			if not args.exp:
                        	fileName = inputDir + "/higgsCombine%s.MarkovChainMC.mH%d.root"%(args.config,mass)
			else:
                        	fileName = inputDir + "/higgsCombine%s.MarkovChainMC.mH%d.123456.root"%(args.config,mass)
                        if os.path.isfile(fileName):
                                limitTree = ROOT.TChain()
                                limitTree.Add(fileName+"/limit")
                                for entry in limitTree:
                                	outFile.write("%d %.10f\n"%(mass,entry.limit*1e-7))        
                        mass += massRange[0]
	outFile.close()
