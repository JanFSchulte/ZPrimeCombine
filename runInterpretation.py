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
		return 20
	else:
		return 10

def runLocalLimits(args,config,outDir):
	if args.mass > 0:
      		masses = [[5,args.mass,args.mass]]
        else:
                masses = config.masses
	for massRange in masses:
		mass = massRange[1]
		while mass <= massRange[2]:
			print "calculate limit for mass %d"%mass
			if len(config.channels) == 1:
				cardName = config.cardDir + "/" + config.channels[0] + "_%d"%mass + ".txt"
			else:
				cardName = config.cardDir + "/" + args.config + "_combined" + "_%d"%mass + ".txt"
		
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

def runLocalSignificance(args,config,outDir):
	if args.mass > 0:
      		masses = [[5,args.mass,args.mass]]
        else:
                masses = config.masses
	for massRange in masses:
		mass = massRange[1]
		while mass <= massRange[2]:
			print "calculate significance for mass %d"%mass
                        if len(config.channels) == 1:
                                cardName = config.cardDir + "/" + config.channels[0] + "_%d"%mass + ".txt"
                        else:
                                cardName = config.cardDir + "/" + args.config + "_combined" + "_%d"%mass + ".txt"
                       
                        subCommand = ["combine","-M","ProfileLikelihood","%s"%cardName, "-n" "%s"%args.config , "-m","%d"%mass, "--signif"]
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


def submitLimits(args,config,outDir):

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

	srcDir = os.getcwd()
	os.chdir(srcDir+"/logFiles_%s"%args.config)
	
	Libs = ""
	for library in config.libraries:
        	Libs += "%s/userfuncs/%s "%(srcDir,library)



        for massRange in masses:
                mass = massRange[1]
                while mass <= massRange[2]:

                        print "submit limit for mass %d"%mass
                        if len(config.channels) == 1:
                                cardName = config.channels[0] + "_%d"%mass + ".txt"
                        else:
                                cardName = args.config + "_combined" + "_%d"%mass + ".txt"
                       
			if config.submitTo == "Purdue":
				if args.expected:
					subCommand = "qsub -l walltime=48:00:00 -q cms-express %s/submission/zPrimeLimits_PURDUE.job -F '%s %s %s %d %d %d %d %d %s'"%(srcDir,args.config,srcDir,cardName,config.numInt,config.numToys,config.exptToys,mass,getRange(mass),Libs)
				else:
					subCommand = "qsub -l walltime=48:00:00 -q cms-express %s/submission/zPrimeLimits_PURDUE.job -F '%s %s %s %d %d %d %d %d %s'"%(srcDir,args.config,srcDir,cardName,config.numInt,config.numToys,0,mass,getRange(mass),Libs)
				subprocess.call(subCommand,shell=True)			
			
			mass += massRange[0]



def summarizeConfig(config,args):
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
	print "data cards and workspaces are saved in %s"%config.cardDir	
	print "--------------------------------------"
	print "                                      "
def main():

        parser = argparse.ArgumentParser(description='Steering tool for Zprime -> ll analysis interpretation in combine')
        parser.add_argument("-r", "--redo", action="store_true", default=False, help="recreate datacards and workspaces for this configuration")
        parser.add_argument("-w", "--write", action="store_true", default=False, help="create datacards and workspaces for this configuration")
        parser.add_argument("-s", "--submit", action="store_true", default=False, help="submit jobs to cluster/GRID")
        parser.add_argument("--signif", action="store_true", default=False, help="run significance instead of limits")
        parser.add_argument("-e", "--expected", action="store_true", default=False, help="expected limits")
        parser.add_argument("-c", "--config", dest = "config", required=True, help="name of the congiguration to use")
        parser.add_argument("-m", "--mass", dest = "mass", default = -1,type=int, help="mass point")

        args = parser.parse_args()
	
	
        configName = "scanConfiguration_%s"%args.config

        config =  __import__(configName)
	summarizeConfig(config,args)
	if args.redo or args.write:
		for channel in config.channels:
			print "writing datacards and workspaces for channel %s ...."%channel
			if args.mass > 0:	
				subprocess.call(["python", "writeDataCards.py", "-c","%s"%channel,"-o","%s"%args.config,"-m","%d"%args.mass])
			else:	
				subprocess.call(["python", "writeDataCards.py", "-c","%s"%channel,"-o","%s"%args.config])
		print "done!"
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
						command.append( "%s=%s_%d.txt"%(channel,channel,mass))			
					
					outName = "%s/%s_combined_%d.txt"%(config.cardDir,args.config,mass)
					with open('%s'%outName, "w") as outfile:
    						subprocess.call(command, stdout=outfile,cwd=config.cardDir)
					mass += massRange[0]			

			print "done!"
	if args.write:
		sys.exit()
	outDir = "results_%s"%args.config
        if not os.path.exists(outDir):
                os.makedirs(outDir)
	
	if args.submit:
		if args.signif:
			print "Significance calculation supported only for local running"
			sys.exit()
		else:
			submitLimits(args,config,outDir)
	else:
		print "no submisson requested - running locally"
		if args.signif:
			runLocalSignificance(args,config,outDir)
		else:
			runLocalLimits(args,config,outDir)	
main()
