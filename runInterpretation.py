import sys
import os
sys.path.append('cfgs/')
import argparse
import subprocess


def main():

        parser = argparse.ArgumentParser(description='Steering tool for Zprime -> ll analysis interpretation in combine')
        parser.add_argument("-r", "--redo", action="store_true", default=False, help="recreate datacards and workspaces for this configuration")
        parser.add_argument("-s", "--submit", action="store_true", default=False, help="submit jobs to cluster/GRID")
        parser.add_argument("-c", "--config", dest = "config", required=True, help="name of the congiguration to use")
        parser.add_argument("-m", "--mass", dest = "mass", default = -1,type=int, help="mass point")

        args = parser.parse_args()
	
	
        configName = "scanConfiguration_%s"%args.config

        config =  __import__(configName)

	if args.redo:
		for channel in config.channels:
			if args.mass > 0:	
				subprocess.call(["python", "writeDataCards.py", "-c","%s"%channel,"-o","%s"%args.config,"-m","%d"%args.mass])
			else:	
				subprocess.call(["python", "writeDataCards.py", "-c","%s"%channel,g])

		if len(config.channels) > 1:
			print "writing combined channel datacards"
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
			print "significance calculation requested. Not implemented yet, sorry! "
			sys.exit()	
	        if args.mass > 0:
        	        masses = [[5,args.mass,args.mass]]
        	else:
                	masses = config.masses
	        for massRange in masses:
	                mass = massRange[1]
	                while mass <= massRange[2]:
			
				if not config.significance:
					print "calculate limit for mass %d"%mass
					if len(config.channels) == 1:
						cardName = config.cardDir + "/" + config.channels[0] + "_%d"%mass + ".txt"
					else:
						cardName = config.cardDir + "/" + args.config + "_combined" + "_%d"%mass + ".txt"
					subprocess.call(["combine","-M","MarkovChainMC","%s"%cardName, "-n" "%s"%args.config , "-m","%d"%mass, "-i", "%d"%config.numInt, "--tries", "%d"%config.numToys ,  "--prior","flat","--LoadLibrary","userfuncs/ZPrimeMuonBkgPdf_cxx.so","--LoadLibrary","userfuncs/Pol2_cxx.so"])
					
					resultFile = "higgsCombine%s.MarkovChainMC.mH%d.root"%(args.config,mass)
					subprocess.call(["mv","%s"%resultFile,"%s"%outDir])		
	                        mass += massRange[0]
main()
