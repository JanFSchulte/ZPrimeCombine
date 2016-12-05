

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
	massLow= max(massLow,200)
	return massLow, massHigh


def getBkgEstInWindow(ws,massLow,massHigh,nBkgTotal):
	import ROOT
	ws.var("massFullRange").setRange("window",massLow,massHigh)
	argSet = ROOT.RooArgSet(ws.var("massFullRange"))
	integral = ws.pdf("bkgpdf_fullRange").createIntegral(argSet,ROOT.RooFit.NormSet(argSet), ROOT.RooFit.Range("window"))
	return nBkgTotal*integral.getVal()
