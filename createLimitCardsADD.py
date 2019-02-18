import sys
import os
sys.path.append('cfgs/')
import ROOT
import subprocess

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
    	parser.add_argument("--frequentist",dest="frequentist", action="store_true", default=False, help='use results from frequentist limits')
    	parser.add_argument("--hybrid",dest="hybrid", action="store_true", default=False, help='use results from hybrid significance calculations')
    	parser.add_argument("--merge",dest="merge", action="store_true", default=False, help='merge expected limits first')
    	parser.add_argument("--CI",dest="CI", action="store_true", default=False, help='is CI')
	parser.add_argument("--ADD",dest="ADD",action="store_true",default=False, help="is ADD")
     	parser.add_argument("--bias",dest="bias", action="store_true", default=False, help='is for bias study')
     	parser.add_argument("--mu1",dest="mu1", action="store_true", default=False, help='bias study for mu = 1')

        args = parser.parse_args()

	tag = ""
	if not args.tag == "":
		tag = "_"  + args.tag

	if args.hybrid:
		args.signif = True
	

        configName = "scanConfiguration_%s"%args.config

        config =  __import__(configName)


       	if args.input == "":
		dirs=sorted([d for d in os.listdir(os.getcwd()+"/results_%s"%args.config + tag) if os.path.isdir(os.getcwd()+"/results_%s"%args.config+tag+"/"+d)])
		inputDir = "results_%s/"%(args.config+tag)+dirs[-1]

        else:
                inputDir = args.input

        print "Taking inputs from %s"%inputDir

	algo = "MarkovChainMC"
	if args.signif:
		algo = "ProfileLikelihood"
		if args.hybrid:
			algo = "HybridNew"
	if args.frequentist:
		algo = "HybridNew"	
	if args.bias:
 		algo = "FitDiagnostics"	
	if args.exp:
		outFileName = "limitCard_%s_Exp"%(args.config)
	elif args.signif:
		outFileName = "limitCard_%s_Signif"%(args.config)
 	elif args.bias:
 		outFileName = "limitCard_%s_Bias"%(args.config)
	else:
		outFileName = "limitCard_%s_Obs"%(args.config)
	if args.ADD: outFileName = "ADD" + outFileName
	if args.hybrid:
		outFileName += "_hybrid"
	if args.frequentist:
		outFileName += "_frequentist"
	if not args.tag =='':
		outFileName = outFileName + "_" + args.tag	
	
	if args.binned:
		outFileName += "_binned"

	if not os.path.exists("cards"):
		os.mkdir("cards")	


   	if args.merge:
		if args.CI or args.ADD:	
        		for Lambda in config.lambdas:
				for interference in config.interferences:
					nJobs = int(config.exptToys/10)
					fileList = []
					for i in range(0,nJobs):
                        			fileName = inputDir + "/higgsCombine%s_%s.MarkovChainMC.mH%d.%d.root"%(args.config+tag,interference,Lambda,i)
						if os.path.isfile(fileName):
							fileList.append(fileName)
						i+=1
					print "merging Lambda point %d TeV, model %s %d/%d files present"%(Lambda,interference,len(fileList),nJobs)	
					command = ["hadd","-f","%s/higgsCombine%s_%s.MarkovChainMC.mH%d.123456.root"%(inputDir,args.config+tag,interference,Lambda)]
					command += fileList
					subprocess.call(command,stdout=open(os.devnull, 'wb'))
		else:
			print "not implemented yet"

	else: 
		if args.CI or args.ADD:
			if args.exp:
				outFileName = "limitCard_%s_Exp"%(args.config)
			elif args.signif:
				outFileName = "limitCard_%s_Signif"%(args.config)
		 	elif args.bias:
 				outFileName = "limitCard_%s_Bias"%(args.config)
 				if args.mu1:
 					outFileName = "limitCard_%s_Bias_mu1"%(args.config)
			else:
				outFileName = "limitCard_%s_Obs"%(args.config)
			if args.hybrid:
				outFileName += "_hybrid"
			if args.frequentist:
				outFileName += "_frequentist"
			if not args.tag =='':
				outFileName = outFileName + "_" + args.tag	
			if args.ADD: outFileName = "ADD" + outFileName

		#	if args.signif: 
		#		tag = ""	
			if args.injected:
				name = "%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]) + tag
			else:
				name=args.config + "_" + args.tag
		#name=args.config

	
			Lambdas = config.lambdas
			missingFiles = []
			outName = outFileName
			for interference in config.interferences:
				outFileName = outName + "_" + interference
				outFile = open("cards/%s.txt"%outFileName, "w")
	        		for Lambda in Lambdas:
					if  args.exp:
                        			fileName = inputDir + "/higgsCombine%s_%s.%s.mH%d.root"%(name,interference,algo,Lambda)
					elif args.signif:	
                        			fileName = inputDir + "/higgsCombine%s_%s.%s.mH%d.root"%(name,interference,algo,Lambda)
 					elif  args.bias:
                         			fileName = inputDir + "/higgsCombine%s_%s.%s.mH%d_mu0.root"%(name,interference,algo,Lambda)
                         			if args.mu1:	
 							fileName = inputDir + "/higgsCombine%s_%s.%s.mH%d_mu1.root"%(name,interference,algo,Lambda)
					else:
                        			fileName = inputDir + "/higgsCombine%s_%s.%s.mH%d.root"%(name,interference,algo,Lambda)
					print fileName
					if os.path.isfile(fileName):
                                		limitTree = ROOT.TChain()
                                		limitTree.Add(fileName+"/limit")
                                		for entry in limitTree:
							if not entry.limit == 10:
								outFile.write("%d %.15f\n"%(Lambda,entry.limit))        
                			else:
						missingFiles.append(fileName)	
			if len(missingFiles) == 0:
				print "all files present"
			else:
				print "missing files:"
				for fileN in missingFiles:
					print fileN


		else:	
			outFile = open("cards/%s.txt"%outFileName, "w")
			if args.injected:
				name = "%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]) + tag
			else:
				name=args.config + "_" + args.tag
				#name=args.config

	
			masses = config.masses
			if args.exp:
				masses = config.massesExp
			missingFiles = []
        		for massRange in masses:
                		mass = massRange[1]
                		while mass <= massRange[2]:
					if  args.exp:
                        			fileName = inputDir + "/higgsCombine%s.%s.mH%d.root"%(name,algo,mass)
					elif args.signif:	
                        			fileName = inputDir + "/higgsCombine%s.%s.mH%d.root"%(name,algo,mass)
					else:
                        			fileName = inputDir + "/higgsCombine%s.%s.mH%d.root"%(name,algo,mass)
					if os.path.isfile(fileName):
                                		limitTree = ROOT.TChain()
                                		limitTree.Add(fileName+"/limit")
                                		for entry in limitTree:
							if args.signif:
                                				outFile.write("%d %.15f\n"%(mass,entry.limit))        
                                			else:	
								outFile.write("%d %.15f\n"%(mass,entry.limit*1e-7))        
	                		else:
						missingFiles.append(fileName)	
			       		mass += massRange[0]
			if len(missingFiles) == 0:
				print "all files present"
			else:
				print "missing files:"
				for fileN in missingFiles:
					print fileN
			outFile.close()
