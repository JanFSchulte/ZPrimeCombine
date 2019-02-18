import argparse
import subprocess
import time
import os
import sys
from copy import copy
sys.path.append('cfgs/')
sys.path.append('input/')

def get_git_revision_hash():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'])


def printProgress (iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = '%' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')
        sys.stdout.flush()


##Data card for Zprime -> ll analysis, created on %(date)s at %(time)s using revision %(hash)s of the package

cardTemplate='''
##Data card for CI interpretation of the Zprime -> ll analysis, created on %(date)s at %(time)s
imax 1  number of channels
jmax 4  number of backgrounds
kmax *  number of nuisance parameters (sources of systematical uncertainties)
------------
#for background shapes
%(bkgShapes)s
#for signal shape
%(sigShape)s
#for interference shape
%(intShape)s
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


def getChannelBlock(backgrounds,yields,signalScale,chan):

	result = "bin %s %s %s"%(chan,chan,chan)
	for i in range(0,len(backgrounds)):
		result += " %s "%chan
	result+="\n"
	result += "process      DY sig int"
	for background in backgrounds:
		result+= "  %s  "%background
	result +="\n"
	result +="process     -2 -1  0 "
	for i in range(0,len(backgrounds)):
		result+=" %d"%(i+1)
	result +="\n"
	result += "rate         %.2f %.2f %.2f "%(yields[0],yields[-2],yields[-1])
	#result += "rate         1 "
	for i in range (0, len(backgrounds)):
		result+= " %.2f"%yields[i+1]
	return result
 

# what uncertainties are correlated? 0 for none at all, 1 for within channels, 2 accross channels
correlations = {
"xSecOther":2,
"jets":2,
"zPeak":1,
"trig":1,
"massScale":0,
"stats":0,
"res":0,
"pdf":2,
"ID":0,
"lumi":2,
"PU":2
}



def getUncert(uncert, value, backgrounds, mass,channel,correlate,yields,signif):
	result = ""
	if correlate:
		if correlations[uncert] == 0:
			name = "%s_%s"%(uncert,channel)
		elif correlations[uncert] == 1:
			if "dimuon" in channel:
				name = "%s_dimuon"%uncert
			else:
				name = "%s_dielectron"%uncert
		elif correlations[uncert] == 2:
			name = uncert	
	else:
		name = "%s_%s"%(uncert,channel)



	if uncert == "xSecOther":
		result = "%s lnN - - - "%name
	        for background in backgrounds:
			if background == "Other":
        			result += "  %.3f  "%value
			else:
        			result += " - "
		result += "\n"		

	if uncert == "jets":
		result = "%s lnN - - - "%name
	        for background in backgrounds:
			if background == "Jets":
        			result += "  %.3f  "%value
			else:
        			result += " - "
		result += "\n"		



	if uncert == "zPeak":
		result = "%s lnN %.3f - %.3f"%(name,value,value)
	        for background in backgrounds:
			if background == "Jets":
        			result += "  -  "
			else:
        			result += "  %.3f"%value
		result += "\n"		



	if uncert == "trig":
		result = "%s lnN %.3f %.3f %.3f"%(name,value,value,value)
	        for background in backgrounds:
			if background == "Jets":
        			result += "  -  "
			else:
        			result += "  %.3f"%value
		result += "\n"		

	if uncert == "massScale":
		result = "%s shape 1 1 1"%name
	        for background in backgrounds:
			if background == "Jets":
        			result += "  -  "
			else:
        			result += "  1  "
	
		result += "\n"		

	if uncert == "stats":
		result = "%s shape 1 1 1"%name
	        for background in backgrounds:
			if background == "Jets":
        			result += "  -  "
       			else:
	 			result += "  1  "
	
		result += "\n"		


	if uncert == "res" and not "electron" in channel:
		result = "%s shape 1 1 1"%name
	        for background in backgrounds:
			if background == "Jets":
        			result += "  -  "
       			else:
	 			result += "  1  "
	
		result += "\n"		
	if uncert == "PU" and not "muon" in channel:
		result = "%s shape 1 1 1"%name
	        for background in backgrounds:
			if background == "Jets":
        			result += "  -  "	
        		else:
				result += "  1  "	
		result += "\n"		
	if uncert == "pdf":
		result = "%s shape 1 1 1"%name
	        for background in backgrounds:
			if background == "Jets":
        			result += "  -  "	
        		else:
				result += "  1  "	
		result += "\n"		
	if uncert == "ID" and not "electron" in channel:
		result = "%s shape 1 1 1"%name
	        for background in backgrounds:
			if background == "Jets":
        			result += "  -  "	
        		else:
				result += "  1  "	
		result += "\n"		

	if uncert == "lumi":
		result = "%s lnN - %.3f - "%(name,value)
	        for background in backgrounds:
        		result += "  -  "
		result += "\n"		

        return result
		
	


def writeCard(card,fileName):

	text_file = open("%s.txt" % (fileName), "w")
	text_file.write(card)
	text_file.close()
	

def getDataset(fileName, chan):

	return "shapes data_obs %s %s dataHist_%s" % (chan, fileName, chan )

def getSignalShape(fileName,chan,shape):
	
	result =  "shapes sig %s %s sigHist_%s" % (chan, fileName, chan)
	if shape:
		result += " sigHist_$SYSTEMATIC"  
	return result

def getIntShape(fileName,chan,shape):
	
	result =  "shapes int %s %s intHist_%s" % (chan, fileName, chan)
	if shape:
		result += " intHist_$SYSTEMATIC"  
	return result

def getBackgroundShapes(fileName,chan,name, shape):
	result =  "shapes %s %s %s bkgHist%s_%s" % (name, chan, fileName, name, chan)
	if shape:
		result += " bkgHist%s_$SYSTEMATIC"%name

	result += "\n"
	return result

def main():

	parser = argparse.ArgumentParser(description='Data writer for Zprime -> ll analysis interpretation in combine')
	parser.add_argument("--expected", action="store_true", default=False, help="write datacards for expected limit mass binning")
	parser.add_argument("-i", "--inject", action="store_true", default=False, help="inject signal")
	parser.add_argument("-c", "--chan", dest = "chan", default="", help="name of the channel to use")
	parser.add_argument("-o", "--options", dest = "config", default="", help="name of config file")
	parser.add_argument("-t", "--tag", dest = "tag", default="", help="tag")
	parser.add_argument("-s", "--signif", action="store_true", default=False, help="write card for significances")
        parser.add_argument( "--workDir", dest = "workDir", default = "", help="tells batch jobs where to put the datacards. Not for human use!")
				
	args = parser.parse_args()	
	tag = args.tag
	if not args.tag == "":
		tag = "_" + args.tag

        import glob
	from ROOT import gROOT
        for f in glob.glob("userfuncs/*.cxx"):
                gROOT.ProcessLine(".L "+f+"+")


	configName = "scanConfiguration_%s"%args.config
	config =  __import__(configName)

	moduleName = "channelConfig_%s"%args.chan
	module =  __import__(moduleName)

	from createInputs import createHistogramsIntCI
	from tools import getCardDir
	cardDir = getCardDir(args,config)	
	if not os.path.exists(cardDir):
    		os.makedirs(cardDir)

	lambdas = config.lambdas

	nPoints = len(config.lambdas)*len(config.interferences)
	

	index = 0
	for Lambda in config.lambdas:
		for interference in config.interferences:

			name = "%s/%s_%d_%s" % (cardDir,args.chan, Lambda, interference)
			if args.inject or "toy" in tag:	
				yields = createHistogramsIntCI(Lambda,interference, name,args.chan,args.config,dataFile=injectedFile)
			else:	
				yields = createHistogramsIntCI(Lambda,interference, name,args.chan,args.config)
			
			backgrounds = copy(config.backgrounds)
			nBkg = len(backgrounds) 
						
			
			shape = False
			if "massScale" in config.systematics:
				shape = True
			if "res" in config.systematics:
				shape = True
			if "pdf" in config.systematics:
				shape = True

		

			channelDict = {}

			channelDict["date"] = time.strftime("%d/%m/%Y")
			channelDict["time"] = time.strftime("%H:%M:%S")
			#channelDict["hash"] = get_git_revision_hash()	

			channelDict["bin"] = args.chan

			channelDict["nBkgs"] = nBkg
			channelDict["bkgShapes"] = ''
			for background in backgrounds:
				channelDict["bkgShapes"] += getBackgroundShapes("%s.root"%name,args.chan,background,shape)
			
			del backgrounds[0]	
	
			channelDict["sigShape"] = getSignalShape("%s.root"%name,args.chan,shape)
			channelDict["intShape"] = getIntShape("%s.root"%name,args.chan,shape)
			channelDict["data"] = getDataset("%s.root"%name,args.chan)
		
			channelDict["channels"]	= getChannelBlock(backgrounds,yields,1,args.chan)		

			uncertBlock = ""
			uncerts = module.provideUncertaintiesCI(Lambda)
			for uncert in config.systematics:
				uncertBlock += getUncert(uncert,uncerts[uncert],backgrounds,Lambda,args.chan,config.correlate,yields,args.signif)
		
			channelDict["systs"] = uncertBlock

			writeCard(cardTemplate % channelDict, name)
			printProgress(index+1, nPoints, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
			index += 1	
main()
