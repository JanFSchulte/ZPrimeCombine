import argparse
import subprocess
import time
import os
import sys
sys.path.append('cfgs/')
sys.path.append('input/')

def get_git_revision_hash():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'])


cardTemplate='''
##Data card for Zprime -> ll analysis, created on %(date)s at %(time)s using revision %(hash)s of the package
imax 1  number of channels
jmax %(nBkgs)d  number of backgrounds
kmax *  number of nuisance parameters (sources of systematical uncertainties)
------------
#for background shapes
%(bkgShapes)s
#for signal shape
%(sigShape)s
#for data
%(data)s
------------
# we have just one channel, in which we observe 0 events
bin %(bin)s
observation -1.
------------
# now we list the expected events for signal and all backgrounds in that bin
# the second 'process' line must have a positive number for backgrounds, and 0 for signal
# then we list the independent sources of uncertainties, and give their effect (syst. error)
# on each process and bin
%(channels)s  
------------
%(systs)s
'''


def getChannelBlock(nBkgs,bkgYields,chan):

	result = "bin %s"%chan
	for i in range(0,nBkgs):
		result += " %s "%chan
	result+="\n"
	result += "process      sig"
	if nBkgs == 1:
		result+= "  bkg  "
	else:
		for i in range(0,nBkgs):
			result+= "  bkg_%d  "%i
	result +="\n"
	result +="process       0 "
	for i in range(0,nBkgs):
		result+=" %d"%(i+1)
	result +="\n"
	result += "rate         1.000 "
	for i in range (0, nBkgs):
		result+= " %.2f"%bkgYields[i]
	return result
 


def getUncert(uncert, value, nBkgs, mass):

	if uncert == "sigEff":
	        if len(value) == 1:
	                result = "sig_effUnc  lnN  %.2f"%value[0]
	        else:
	                result = "sig_effUnc  lnN  %.2f/%.2f"%( value[0], value[1] )

		for i in range(0,nBkgs):
	                result += "  -  "

	if uncert == "bkgUncert":
		if value != 0:
			print "non-standard background uncertainties not supported yet"
			sys.exit()
		result = "bkg_shapeUnc    lnU     -  "    
		for i in range(0, nBkgs):
			result += "  1.4  "

	if uncert == "massScale":

		result = "peak param %d %.2f" % ( mass, mass*value )
	result += "\n"		
        return result
		
	


def writeCard(card,fileName):

	text_file = open("%s.txt" % (fileName), "w")
	text_file.write(card)
	text_file.close()
	

def getDataset(binned,fileName, chan):

	if binned:
		return "bla"
	else:
		return "shapes data_obs %s %s %s:data_%s" % (chan, fileName, chan, chan)	

def getSignalShape(binned,fileName,chan):
	
	if binned:
		return "bla"
	else:
		return  "shapes sig %s %s %s:sig_pdf_%s" % (chan, fileName, chan, chan)

def getBackgroundShapes(binned,fileName,chan,nBkg=0):

	if binned:
		return "bla"
	else:
		if nBkg == 0:
			return "shapes bkg %s %s %s:bkgpdf_%s" % (chan, fileName, chan, chan)
		else:
			return "shapes bkg %s %s %s:bkgpdf_%s_%d" % (chan, fileName, chan, chan, nBkg)
def main():

	parser = argparse.ArgumentParser(description='Data writer for Zprime -> ll analysis interpretation in combine')
	parser.add_argument("-b", "--binned", action="store_true", default=False, help="use binned dataset")
	parser.add_argument("-c", "--chan", dest = "chan", default="", help="name of the channel to use")
	parser.add_argument("-o", "--options", dest = "options", default="", help="name of config file")
	parser.add_argument("-m", "--mass", dest = "mass", default=-1,type=int, help="mass point")
				
	args = parser.parse_args()	

	configName = "scanConfiguration_%s"%args.options
	config =  __import__(configName)

	moduleName = "createWS_%s"%args.chan
	module =  __import__(moduleName)

	if not os.path.exists(config.cardDir):
    		os.makedirs(config.cardDir)
	if args.mass > 0:
		masses = [[5,args.mass,args.mass]]
	else:
		masses = config.masses	
	for massRange in masses:
		mass = massRange[1]
		while mass <= massRange[2]:
			name = "%s/%s_%d" % (config.cardDir,args.chan, mass)
			bkgYields = [module.createWS(mass,100, name)]

			nBkg = module.nBkg 

						

			channelDict = {}

			channelDict["date"] = time.strftime("%d/%m/%Y")
			channelDict["time"] = time.strftime("%H:%M:%S")
			channelDict["hash"] = get_git_revision_hash()	
	
			channelDict["bin"] = args.chan

			channelDict["nBkgs"] = nBkg
			if nBkg == 1:
				channelDict["bkgShapes"] = getBackgroundShapes(args.binned,"%s.root"%name,args.chan,0)
			else:
				channelDict["bkgShapes"] = ""
				for i in range(1,nBkg+1):
                			channelDict["bkgShapes"] += getBackgroundShapes(args.binned,"%s.root"%nam,eargs.chan,i)
					if i < nBkg:
						channelDict["bkgShapes"] += "\n"
	
			channelDict["sigShape"] = getSignalShape(args.binned,"%s.root"%name,args.chan)
			channelDict["data"] = getDataset(args.binned,"%s.root"%name,args.chan)
			
			channelDict["channels"]	= getChannelBlock(nBkg,bkgYields,args.chan)		

			uncertBlock = ""
			uncerts = module.provideUncertainties(mass)
			for uncert in config.systematics:
				uncertBlock += getUncert(uncert,uncerts[uncert],nBkg,mass)
			
			channelDict["systs"] = uncertBlock

			writeCard(cardTemplate % channelDict, name)

			mass += massRange[0]
main()
