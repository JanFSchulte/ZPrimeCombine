import sys
import os
sys.path.append('cfgs/')
import ROOT

if __name__ == "__main__":
        import argparse
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument("-c","--config", dest="config",default="", required=True, help='configuration name')
        parser.add_argument("--input",dest="input", default='', help='folder with input root files')
        parser.add_argument("-t","--tag",dest="tag", default='', help='tag')
    	parser.add_argument("--exp",dest="exp", action="store_true", default=False, help='write expected limits')
    	parser.add_argument("--signif",dest="signif", action="store_true", default=False, help='write pValues')
    	parser.add_argument("--injected",dest="injected", action="store_true", default=False, help='injected')
    	parser.add_argument("--binned",dest="binned", action="store_true", default=False, help='binned')
        args = parser.parse_args()

	tag = ""
	if not args.tag == "":
		tag = "_"  + args.tag

        configName = "scanConfiguration_%s"%args.config

        config =  __import__(configName)


       	if args.input == "":
		dirs=sorted([d for d in os.listdir(os.getcwd()+"/results_%s"%args.config + tag) if os.path.isdir(os.getcwd()+"/results_%s"%args.config+tag+"/"+d)])
		inputDir = "results_%s/"%(args.config+tag)+dirs[-1]

        else:
                inputDir = args.input

        print "Taking inputs from %s"%inputDir

	
	if args.exp:
		outFileName = "limitCard_%s_Exp"%(args.config)
	elif args.signif:
		outFileName = "limitCard_%s_Signif"%(args.config)
	else:
		outFileName = "limitCard_%s_Obs"%(args.config)
	if not args.tag =='':
		outFileName = outFileName + "_" + args.tag 	
	if args.binned:
		outFileName += "_binned"
	outFile = open("%s.txt"%outFileName, "w")
#	if args.signif: 
#		tag = ""	
	if args.injected:
		name = "%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]) + tag
	else:
		name=args.config + tag

        for massRange in config.masses:
                mass = massRange[1]
                while mass < massRange[2]:
			if  args.exp:
                        	fileName = inputDir + "/higgsCombine%s.MarkovChainMC.mH%d.123456.root"%(name,mass)
			elif args.signif:	
                        	fileName = inputDir + "/higgsCombine%s.ProfileLikelihood.mH%d.root"%(name,mass)
			else:
                        	fileName = inputDir + "/higgsCombine%s.MarkovChainMC.mH%d.root"%(name,mass)
			if os.path.isfile(fileName):
                                limitTree = ROOT.TChain()
                                limitTree.Add(fileName+"/limit")
                                for entry in limitTree:
					if args.signif:
                                		outFile.write("%d %.15f\n"%(mass,entry.limit))        
                                	else:	
						outFile.write("%d %.15f\n"%(mass,entry.limit*1e-7))        
                        mass += massRange[0]
	outFile.close()
