import sys
import os
sys.path.append('cfgs/')
import argparse
import subprocess

supportedResources = ["Purdue"]


def getRange(mass):
	
	if 400 <= mass <= 500:
		return 400
	elif 500 < mass <= 600:
		return 200
	elif 600 < mass <= 700:
		return 100
	elif 700 < mass <= 800:
		return 90
	elif 800 < mass <= 1000:
		return 50
	elif 1000 < mass <= 2000:
		return 50
	else:
		return 40

def runLocalLimits(args,config,outDir,cardDir,binned):
	if args.mass > 0:
      		masses = [[5,args.mass,args.mass]]
        else:
                masses = config.masses
	for massRange in masses:
		mass = massRange[1]
		while mass <= massRange[2]:
			print "calculate limit for mass %d"%mass
			if len(config.channels) == 1:
				cardName = cardDir + "/" + config.channels[0] + "_%d"%mass + ".txt"
			else:
				cardName = cardDir + "/" + args.config + "_combined" + "_%d"%mass + ".txt"
		
			if binned:
				cardName = cardName.split(".")[0] + "_binned.txt"
			numToys = config.numToys
			if args.expected:
				numToys = 1
	
			subCommand = ["combine","-M","MarkovChainMC","%s"%cardName, "-n" "%s"%args.config , "-m","%d"%mass, "-i", "%d"%config.numInt, "--tries", "%d"%numToys ,  "--prior","flat","--rMax","%d"%getRange(mass)]
			if args.expected: 
				subCommand.append("-t")
				subCommand.append("%d"%config.exptToys)
			
			for library in config.libraries:		
				subCommand.append("--LoadLibrary")
				subCommand.append("userfuncs/%s"%library)
			subprocess.call(subCommand)

			if args.expected:	
				resultFile = "higgsCombine%s.MarkovChainMC.mH%d.123456.root"%(args.config,mass)
			else:
				resultFile = "higgsCombine%s.MarkovChainMC.mH%d.root"%(args.config,mass)
				
			subprocess.call(["mv","%s"%resultFile,"%s"%outDir])
			mass += massRange[0]

def runLocalSignificance(args,config,outDir,cardDir,binned):
	if args.mass > 0:
      		masses = [[5,args.mass,args.mass]]
        else:
                masses = config.masses
	for massRange in masses:
		mass = massRange[1]
		while mass <= massRange[2]:
			print "calculate significance for mass %d"%mass
                        if len(config.channels) == 1:
                                cardName = cardDir + "/" + config.channels[0] + "_%d"%mass + ".txt"
                        else:
                                cardName = cardDir + "/" + args.config + "_combined" + "_%d"%mass + ".txt"
                        if binned:
				cardName = cardName.split(".")[0]+"_binned.txt"
                        subCommand = ["combine","-M","ProfileLikelihood","%s"%cardName, "-n" "%s"%(args.config) , "-m","%d"%mass, "--signif" , "--pvalue"]
			for library in config.libraries:
                                subCommand.append("--LoadLibrary")
                                subCommand.append("userfuncs/%s"%library)


			subprocess.call(subCommand)
                        if args.expected:
                                resultFile = "higgsCombine%s.ProfileLikelihood.mH%d.123456.root"%(args.config,mass)
                        else:
                                resultFile = "higgsCombine%s.ProfileLikelihood.mH%d.root"%(args.config,mass)
                        subprocess.call(["mv","%s"%resultFile,"%s"%outDir])
                        mass += massRange[0]


def submitLimits(args,config,outDir,binned,tag):

	print "Job submission requested"
	if config.submitTo in supportedResources:
		print "%s resources will be used"%config.submitTo
	else:
		print "Computing resource not supported at the moment. Supported resources are:"
		for resource in supportedResources:
			print resource
		sys.exit()	
        if args.mass > 0:
                masses = [[5,args.mass,args.mass]]
        else:
                masses = config.masses

	if not os.path.exists("logFiles_%s"%args.config):
    		os.makedirs("logFiles_%s"%args.config)

	if not args.inject:
		srcDir = os.getcwd()
		os.chdir(srcDir+"/logFiles_%s"%args.config)
	else:
		srcDir = os.getcwd()
		if not os.path.exists("logFiles_%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"])):
    			os.makedirs("logFiles_%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]))
		os.chdir(srcDir+"/logFiles_%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]))
	
	Libs = ""
	for library in config.libraries:
        	Libs += "%s/userfuncs/%s "%(srcDir,library)


	if args.inject:
		name = "%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]) + tag
	else:
		name = args.config + tag
	import time
	timestamp = time.strftime("%Y%m%d") + "_" + time.strftime("%H%M")
        for massRange in masses:
                mass = massRange[1]
                while mass <= massRange[2]:

                        print "submit limit for mass %d"%mass
                        if len(config.channels) == 1:
                                cardName = config.channels[0] + "_%d"%mass + ".txt"
                        else:
                                cardName = args.config + "_combined" + "_%d"%mass + ".txt"
                        if binned:
				cardName = cardName.split(".")[0] + "_binned.txt"
			if config.submitTo == "Purdue":
				if args.expected:
					subCommand = "qsub -l walltime=48:00:00 -q cms-express %s/submission/zPrimeLimits_PURDUE.job -F '%s %s %s %d %d %d %d %d %s %s'"%(srcDir,name,srcDir,cardName,config.numInt,config.numToys,config.exptToys,mass,getRange(mass),timestamp,Libs)
				else:
					subCommand = "qsub -l walltime=48:00:00 -q cms-express %s/submission/zPrimeLimits_PURDUE.job -F '%s %s %s %d %d %d %d %d %s %s'"%(srcDir,name,srcDir,cardName,config.numInt,config.numToys,0,mass,getRange(mass),timestamp,Libs)
				subprocess.call(subCommand,shell=True)			
			
			mass += massRange[0]

def submitPValues(args,config,outDir,binned,tag):

	if "toy" in tag:
		tag = "_"+tag

	print "Job submission requested"
	if config.submitTo in supportedResources:
		print "%s resources will be used"%config.submitTo
	else:
		print "Computing resource not supported at the moment. Supported resources are:"
		for resource in supportedResources:
			print resource
		sys.exit()	
        if args.mass > 0:
                masses = [[5,args.mass,args.mass]]
        else:
                masses = config.masses

	if not os.path.exists("logFiles_%s"%args.config):
    		os.makedirs("logFiles_%s"%args.config)

	if not args.inject:
		srcDir = os.getcwd()
		os.chdir(srcDir+"/logFiles_%s"%args.config)
	else:
		srcDir = os.getcwd()
		if not os.path.exists("logFiles_%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"])):
    			os.makedirs("logFiles_%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]))
		os.chdir(srcDir+"/logFiles_%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]))
	
	Libs = ""
	for library in config.libraries:
        	Libs += "%s/userfuncs/%s "%(srcDir,library)


	if args.inject:
		name = "%d_%.4f_%d"%(config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]) + tag
	else:
		name = tag
	import time
	timestamp = time.strftime("%Y%m%d") + "_" + time.strftime("%H%M")
        for massRange in masses:
		print "submit p-value for mass range %d - %d GeV in %d GeV steps"%(massRange[1],massRange[2],massRange[0])
		if len(config.channels) == 1:
			cardName = config.channels[0] + "_"
		else:
			cardName = args.config + "_combined" + "_"
		if binned:
			cardName = cardName + "binned.txt"
		if config.submitTo == "Purdue":
			subCommand = "qsub -l walltime=48:00:00 -q cms-express %s/submission/zPrimePValuesWS_PURDUE.job -F '%s %s %s %s %d %d %d %s %s'"%(srcDir,args.config,name,srcDir,cardName,massRange[1],massRange[2],massRange[0],timestamp,Libs)
			subprocess.call(subCommand,shell=True)			
	os.chdir(srcDir)	
def createInputs(args,config,cardDir):
	for channel in config.channels:
		print "writing datacards and workspaces for channel %s ...."%channel
		call = ["python","writeDataCards.py","-c","%s"%channel,"-o","%s"%args.config,"-t","%s"%args.tag]
		if args.mass > 0:
			call.append("-m")
			call.append("%d"%args.mass)
		if args.inject:
			call.append("-i")
		if args.binned:
			call.append("-b")
		if args.signif:
			call.append("-s")
		subprocess.call(call)

	print "done!"
	tag = args.tag
	if not args.tag == "":
		tag = "_" + args.tag

	if len(config.channels) > 1:
		print "writing combined channel datacards ...."
		if args.mass > 0:
			masses = [[5,args.mass,args.mass]]
		else:
			masses = config.masses
		for massRange in masses:
			mass = massRange[1]
			while mass <= massRange[2]:
				command = ["combineCards.py"]	
				for channel in config.channels:
					if args.binned:
						command.append( "%s=%s_%d_binned.txt"%(channel,channel,mass))			
					else:	
						command.append( "%s=%s_%d.txt"%(channel,channel,mass))			
				outName = "%s/%s_combined_%d.txt"%(cardDir,args.config,mass)
				if args.binned:
					outName = outName.split(".")[0]+"_binned.txt"
				with open('%s'%outName, "w") as outfile:
					subprocess.call(command, stdout=outfile,cwd=cardDir)
				mass += massRange[0]			
			
		print "done!"




def summarizeConfig(config,args,cardDir):
	print "      "
	print "Z' -> ll statistics tool based on Higgs Combine"
	print "               "
	print "------- Configuration Summary --------"
	if args.signif:
		print "Calculation of significances requested"
	else:
		print "Limit calculation requested"
		if args.expected:
			print "Calculating expected limits with %d toy datasets"%config.exptToys
		else:
			print "Calculating observed limits"
		print "MCMC configuration: iterations %d toys: %d"%(config.numInt,config.numToys)
	channelList = ""
	for channel in config.channels:
		channelList += " %s "%(channel)
	print "Consider channels: %s"%channelList
	systList = "" 
	for syst in config.systematics:
		systList += " %s "%(syst)
	print "Systematic uncertainties: %s"%systList
	if args.mass > 0:
		print "run for single mass point at %d GeV"%args.mass
	
	else:
		print "Mass scan configuration: "
		for massRange in config.masses:
			print "from %d to %d in %d GeV steps"%(massRange[1],massRange[2],massRange[0])
	print "data cards and workspaces are saved in %s"%cardDir	
	print "--------------------------------------"
	print "                                      "
def main():

        parser = argparse.ArgumentParser(description='Steering tool for Zprime -> ll analysis interpretation in combine')
        parser.add_argument("-r", "--redo", action="store_true", default=False, help="recreate datacards and workspaces for this configuration")
        parser.add_argument("-w", "--write", action="store_true", default=False, help="create datacards and workspaces for this configuration")
        parser.add_argument("-b", "--binned", action="store_true", default=False, help="use binned dataset")
        parser.add_argument("-s", "--submit", action="store_true", default=False, help="submit jobs to cluster/GRID")
        parser.add_argument("--signif", action="store_true", default=False, help="run significance instead of limits")
        parser.add_argument("--LEE", action="store_true", default=False, help="run significance on BG only toys to estimate LEE")
        parser.add_argument("-e", "--expected", action="store_true", default=False, help="expected limits")
        parser.add_argument("-i", "--inject", action="store_true", default=False, help="inject signal")
        parser.add_argument("-c", "--config", dest = "config", required=True, help="name of the congiguration to use")
        parser.add_argument("-t", "--tag", dest = "tag", default = "", help="tag to label output")
        parser.add_argument("-m", "--mass", dest = "mass", default = -1,type=int, help="mass point")

        args = parser.parse_args()
	
	if args.LEE:
		args.signif = True
		args.submit = True
        configName = "scanConfiguration_%s"%args.config

        config =  __import__(configName)
	tag = args.tag
	if not args.tag == "":
		args.tag = "_" + args.tag

	from tools import getCardDir, getOutDir
	cardDir = getCardDir(args,config)

	summarizeConfig(config,args,cardDir)
	if (args.redo or args.write) and not args.LEE:
		createInputs(args,config,cardDir)

	if args.write:
		sys.exit()

	outDir = getOutDir(args,config)
		
        if not os.path.exists(outDir):
                os.makedirs(outDir)
	
	if args.submit:
		if args.signif:
			if not args.LEE:
				submitPValues(args,config,outDir,args.binned,args.tag)
			else:
				for i in range(0,1000):
					args.tag = args.tag+"toy%d"%i
					if args.redo:
						createInputs(args,config,cardDir)
					submitPValues(args,config,outDir,args.binned,args.tag)						
					i += 1						
		else:
			submitLimits(args,config,outDir,args.binned,args.tag)
	else:
		print "no submisson requested - running locally"
		if args.signif:
			runLocalSignificance(args,config,outDir,cardDir,args.binned)
		else:
			runLocalLimits(args,config,outDir,cardDir,args.binned)	
main()
