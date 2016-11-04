import ROOT,sys
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = 1 
from ROOT import *
sys.path.append('cfgs/')
sys.path.append('input/')


def createSignalDataset(massVal,name,channel,width,nEvents,CB):

	#ROOT.gSystem.Load("shapes/ZPrimeMuonBkgPdf_cxx.so")
#	ROOT.gSystem.AddIncludePath("-Ishapes"
	ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)

	import glob
	for f in glob.glob("userfuncs/*.cxx"):
		ROOT.gSystem.Load(f)
        configName ="channelConfig_%s"%channel
        config =  __import__(configName)
	
	dataFile = config.dataFile
	
	ws = RooWorkspace("tempWS")
        mass = RooRealVar('massFullRange','massFullRange',massVal, 200, 5000 )
        getattr(ws,'import')(mass,ROOT.RooCmdArg())


	peak = RooRealVar("peak","peak",massVal, 200,500)
	peak.setConstant()
	getattr(ws,'import')(peak,ROOT.RooCmdArg())


	### define signal shape
	if CB:

		ws.factory("BreitWigner::bw(massFullRange, peak, %.3f)"%(massVal*width))
		ws.factory("RooCBShape::cb(massFullRange, mean[0.0], %.3f, alpha[1.43], n[3])"%(massVal*config.getResolution(massVal)))
		
		bw = ws.pdf("bw")
		cb = ws.pdf("cb")
		
		mass.setBins(10000,"cache")
		mass.setMin("cache",0)
		mass.setMax("cache",6000); ## need to be adjusted to be higher than limit setting
		
		sigpdf = RooFFTConvPdf("sig_pdf","sig_pdf",mass,bw,cb)
		getattr(ws,'import')(sigpdf,ROOT.RooCmdArg())

	else:
		ws.factory("Voigtian::sig_pdf(massFullRange,peak,%.3f, %.3f)"%(massVal*width,massVal*config.getResolution(massVal)))

	ws = config.loadBackgroundShape(ws)

        with open(dataFile) as f:
                masses = f.readlines()
        nBkg = len(masses)
	dataSet = ws.pdf("bkgpdf_fullRange").generate(ROOT.RooArgSet(ws.var("massFullRange")),nBkg)
	nSignal = int(round(nEvents*config.signalEff(massVal)))
	dataSet.append(ws.pdf("sig_pdf").generate(ROOT.RooArgSet(ws.var("massFullRange")),nSignal))

	masses = []
	for i in range(0,dataSet.numEntries()):
		masses.append(dataSet.get(i).getRealValue("mass"))
 	if CB:
		f = open("%s_%d_%.3f_%d_CB.txt"%(name,massVal,width,nEvents), 'w')
	else:	
		f = open("%s_%d_%.3f_%d.txt"%(name,massVal,width,nEvents), 'w')
	for mass in masses:
		f.write("%.4f\n" % mass)
	f.close()

def createWS(massVal,minNrEv,name,channel,width,correlateMass,dataFile="",CB=True,write=True):
	ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)

	import glob
	for f in glob.glob("userfuncs/*.cxx"):
		ROOT.gSystem.Load(f)


        configName ="channelConfig_%s"%channel
        config =  __import__(configName)
	
	if dataFile == "":
		dataFile = config.dataFile

	if not correlateMass:
		peakName = "_%s"%channel 
	else:
		peakName = ""

	effWidth = width + config.getResolution(massVal)
	
	from tools import getMassRange
	massLow, massHigh = getMassRange(massVal,minNrEv,effWidth,dataFile)	
	ws = RooWorkspace(channel)

        massFullRange = RooRealVar('massFullRange','massFullRange',massVal, 200, 5000 )
        getattr(ws,'import')(massFullRange,ROOT.RooCmdArg())


	mass = RooRealVar('mass_%s'%channel,'mass_%s'%channel,massVal, massLow, massHigh )
	getattr(ws,'import')(mass,ROOT.RooCmdArg())
	
	peak = RooRealVar("peak%s"%peakName,"peak%s"%peakName,massVal, massLow, massHigh)
	peak.setConstant()
	getattr(ws,'import')(peak,ROOT.RooCmdArg())
	
	### define signal shape

	#ws.factory("Voigtian::sig_pdf_dimuon_BB(mass, peak, width, sigma)")
	if CB:

		ws.factory("BreitWigner::bw(mass_%s, peak%s, %.3f)"%(channel,peakName,massVal*config.getResolution(massVal)))
		ws.factory("RooCBShape::cb(mass_%s, mean[0.0], %.3f, alpha[1.43], n[3])"%(channel,massVal*config.getResolution(massVal)))
		
		bw = ws.pdf("bw")
		cb = ws.pdf("cb")
		
		mass.setBins(10000,"cache")
		mass.setMin("cache",0)
		mass.setMax("cache",6000); ## need to be adjusted to be higher than limit setting
		
		sigpdf = RooFFTConvPdf("sig_pdf_%s"%channel,"sig_pdf_%s"%channel,mass,bw,cb)
		getattr(ws,'import')(sigpdf,ROOT.RooCmdArg())

	else:
		ws.factory("Voigtian::sig_pdf_%s(mass_%s, %s,  %.3f, %.3f)"%(channel,peakName,massVal*width,massVal*config.getResolution(massVal)))

	ws = config.loadBackgroundShape(ws)

	ds = RooDataSet.read(dataFile,RooArgList(mass))
	ds.SetName('data_%s'%channel)
	ds.SetTitle('data_%s'%channel)
	getattr(ws,'import')(ds,ROOT.RooCmdArg())

	ws.addClassDeclImportDir("shapes/")	
	ws.importClassCode()	

	if write:
		ws.writeToFile("%s.root"%name,True)

        	from tools import getBkgEstInWindow
        	return getBkgEstInWindow(ws,massLow,massHigh,dataFile)
	else:
		return ws

def createHistograms(massVal,minNrEv,name,channel,width,correlateMass,binWidth,dataFile="",CB=True):
	ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)

	print massVal
	configName ="channelConfig_%s"%channel
        config =  __import__(configName)
	
	if dataFile == "":
		dataFile = config.dataFile
	effWidth = width + config.getResolution(massVal)
	
	from tools import getMassRange
	massLow, massHigh = getMassRange(massVal,minNrEv,effWidth,dataFile)	
	if not correlateMass:
		peakName = "_%s"%channel 
	else:
		peakName = ""


	ws = createWS(massVal,minNrEv,name,channel,width,correlateMass,dataFile=dataFile,CB=CB,write=False)
        
	from tools import getBkgEstInWindow
	nBackground = getBkgEstInWindow(ws,massLow,massHigh,dataFile)
	
	nBins = int((massHigh - massLow)/binWidth) 
	ws.var("mass_%s"%channel).setBins(nBins)
	print name
	histFile = ROOT.TFile("%s.root"%name, "RECREATE")	

        scaleName = "scale"
        if not correlateMass:
                scaleName +="_%s"%channel

	scaleUncert = config.provideUncertainties(massVal)["massScale"]
	print ws.var("peak%s"%peakName).getVal()
        sigShape = ws.pdf("sig_pdf_%s"%channel).generate(ROOT.RooArgSet(ws.var("mass_%s"%channel)),1000000)
	ws.var("peak%s"%peakName).setVal(massVal*(1+scaleUncert))
        sigShapeUp = ws.pdf("sig_pdf_%s"%channel).generate(ROOT.RooArgSet(ws.var("mass_%s"%channel)),1000000)
	ws.var("peak%s"%peakName).setVal(massVal*(1-scaleUncert))
        sigShapeDown = ws.pdf("sig_pdf_%s"%channel).generate(ROOT.RooArgSet(ws.var("mass_%s"%channel)),1000000)

	sigHistRooFit = ROOT.RooDataHist("sigHist_%s"%channel, "sigHist_%s"%channel, ROOT.RooArgSet(ws.var('mass_%s'%channel)), sigShape)	
	sigHist = sigHistRooFit.createHistogram("sigHist_%s"%channel,ws.var("mass_%s"%channel))
	sigHist.SetName("sigHist_%s"%channel)

	sigHistRooFitUp = ROOT.RooDataHist("sigHist_%s_%sUp"%(channel,scaleName), "sigHist_%s_%sUp"%(channel,scaleName), ROOT.RooArgSet(ws.var('mass_%s'%channel)), sigShapeUp)	
	sigHistUp = sigHistRooFitUp.createHistogram("sigHist_%s_%sUp"%(channel,scaleName),ws.var("mass_%s"%channel))
	sigHistUp.SetName("sigHist_%s_%sUp"%(channel,scaleName))

	sigHistRooFitDown = ROOT.RooDataHist("sigHist_%s_%sDown"%(channel,scaleName), "sigHist_%s_%sDown"%(channel,scaleName), ROOT.RooArgSet(ws.var('mass_%s'%channel)), sigShapeDown)	
	sigHistDown = sigHistRooFitDown.createHistogram("sigHist_%s_%sDown"%(channel,scaleName),ws.var("mass_%s"%channel))
	sigHistDown.SetName("sigHist_%s_%sDown"%(channel,scaleName))
	
	sigHist.Scale(1./(sigHist.Integral())*config.provideSignalScaling(massVal)*1e-7)
	sigHistUp.Scale(1./(sigHistUp.Integral())*config.provideSignalScaling(massVal)*1e-7)
	sigHistDown.Scale(1./(sigHistDown.Integral())*config.provideSignalScaling(massVal)*1e-7)

	bkgShape = ws.pdf("bkgpdf_%s"%channel).generate(ROOT.RooArgSet(ws.var("mass_%s"%channel)),1000000)
	bkgHistRooFit = ROOT.RooDataHist("bkgHist_%s"%channel, "bkgHist_%s"%channel, ROOT.RooArgSet(ws.var('mass_%s'%channel)), bkgShape)	
	bkgHist = bkgHistRooFit.createHistogram("bkgHist_%s"%channel,ws.var("mass_%s"%channel))
	bkgHist.SetName("bkgHist_%s"%channel)

	bkgHist.Scale(1./(bkgHist.Integral())*nBackground)

	dataHist = ROOT.TH1F("data_%s"%channel,"data_%s"%channel,nBins,massLow,massHigh)
	
	
        with open(dataFile) as f:
                masses = f.readlines()
	for mass in masses:
		mass = float(mass)
		if (mass >= massLow and mass <= massHigh):
			dataHist.Fill(mass)
	histFile.Write()
	histFile.Close()


        return nBackground
	
