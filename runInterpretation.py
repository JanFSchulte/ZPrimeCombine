import sys
import os
sys.path.append('cfgs/')
import argparse
import subprocess


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
			if args.expected:
				subprocess.call(["combine","-M","MarkovChainMC","%s"%cardName, "-n" "%s"%args.config , "-m","%d"%mass, "-i", "%d"%config.numInt, "--tries", "%d"%config.numToys , "-t" , "%d"%config.exptToys ,  "--prior","flat","--LoadLibrary","userfuncs/ZPrimeMuonBkgPdf_cxx.so","--LoadLibrary","userfuncs/Pol2_cxx.so"])
			else:	
				subprocess.call(["combine","-M","MarkovChainMC","%s"%cardName, "-n" "%s"%args.config , "-m","%d"%mass, "-i", "%d"%config.numInt, "--tries", "%d"%config.numToys ,  "--prior","flat","--LoadLibrary","userfuncs/ZPrimeMuonBkgPdf_cxx.so","--LoadLibrary","userfuncs/Pol2_cxx.so"])
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
			if args.expected:
				subprocess.call(["combine","-M","MarkovChainMC","%s"%cardName, "-n" "%s"%args.config , "-m","%d"%mass, "-i", "%d"%config.numInt, "--tries", "%d"%config.numToys , "-t" , "%d"%config.exptToys ,  "--prior","flat","--LoadLibrary","userfuncs/ZPrimeMuonBkgPdf_cxx.so","--LoadLibrary","userfuncs/Pol2_cxx.so"])
			else:	
				subprocess.call(["combine","-M","ProfileLikelihood","%s"%cardName, "-n" "%s"%args.config , "-m","%d"%mass, "--signif","--LoadLibrary","userfuncs/ZPrimeMuonBkgPdf_cxx.so","--LoadLibrary","userfuncs/Pol2_cxx.so"])
			if args.expected:	
				resultFile = "higgsCombine%s.ProfileLikelihood.mH%d.123456.root"%(args.config,mass)
			else:
				resultFile = "higgsCombine%s.ProfileLikelihood.mH%d.root"%(args.config,mass)
			subprocess.call(["mv","%s"%resultFile,"%s"%outDir])
			mass += massRange[0]





def summarizeConfig(config,args):
	print "      "
	print "Z' -> ll statistics tool based on Higgs Combine"
	print "               "
	print "------- Configuration Summary --------"
	if config.significance:
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
        parser.add_argument("-s", "--submit", action="store_true", default=False, help="submit jobs to cluster/GRID")
        parser.add_argument("-e", "--expected", action="store_true", default=False, help="expected limits")
        parser.add_argument("-c", "--config", dest = "config", required=True, help="name of the congiguration to use")
        parser.add_argument("-m", "--mass", dest = "mass", default = -1,type=int, help="mass point")

        args = parser.parse_args()
	
	
        configName = "scanConfiguration_%s"%args.config

        config =  __import__(configName)
	summarizeConfig(config,args)
	if args.redo:
		for channel in config.channels:
			print "writing datacards and workspaces for channel %s ...."%channel
			if args.mass > 0:	
				subprocess.call(["python", "writeDataCards.py", "-c","%s"%channel,"-o","%s"%args.config,"-m","%d"%args.mass])
			else:	
				subprocess.call(["python", "writeDataCards.py", "-c","%s"%channel,g])
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
	outDir = "results_%s"%args.config
        if not os.path.exists(outDir):
                os.makedirs(outDir)
	
	if args.submit:
		print "implement some submission tools"


	else:
		print "no submisson requested - running locally"
		if config.significance:
			runLocalSignificance(args,config,outDir)
		else:
			runLocalLimits(args,config,outDir)	
main()
