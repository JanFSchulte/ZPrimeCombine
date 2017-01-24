def getCardDir(args,config):

	if args.inject:
		cardDir = "dataCards_" + args.config + "_%d_%.4f_%d"%(config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]) + args.tag
	else:
		cardDir = "dataCards_" + args.config +  args.tag

	if args.DM:
		cardDir = cardDir + "_DM"
	
	if args.binned:
		cardDir = cardDir + "_binned"

	return cardDir
def getOutDir(args,config):

	if args.inject:
		outDir = "results_" + args.config + "_%d_%.4f_%d"%(config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]) + args.tag
	else:
		outDir = "results_" + args.config +  args.tag
	if args.DM:
		outDir = outDir + "_DM"

	if args.binned:
		outDir = outDir + "_binned"

	return outDir

def getMassRange(massVal,minNrEv,effWidth,dataFile):
	with open(dataFile) as f:
		masses = f.readlines()
	massDiffs = []
	for evMass in masses:
		massDiffs.append(abs(float(evMass)-massVal)) 
	massDiffs = sorted(massDiffs)
	
	if minNrEv <= len(massDiffs):
		massDiff = massDiffs[minNrEv]
	massLow = massVal - massDiff
	massHigh = massVal + massDiff
	
	if (massVal-6*effWidth*massVal) < massLow:
		massLow = massVal - 6*effWidth*massVal
	if (massVal+6*effWidth*massVal) > massHigh:
		massHigh = massVal + 6*effWidth*massVal
	massLow= max(massLow,120)
	return massLow, massHigh


def getBkgEstInWindow(ws,massLow,massHigh,nBkgTotal):
	import ROOT
	ws.var("massFullRange").setRange("window",massLow,massHigh)
	argSet = ROOT.RooArgSet(ws.var("massFullRange"))
	integral = ws.pdf("bkgpdf_fullRange").createIntegral(argSet,ROOT.RooFit.NormSet(argSet), ROOT.RooFit.Range("window"))
	return nBkgTotal*integral.getVal()



def createGridPack():

	import subprocess
	args = ['tar', '-cvf', 'gridPack.tar','cfgs/',"input/",'writeDataCards.py','runInterpretation.py','createInputs.py']
	subprocess.call(args)


