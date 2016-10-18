import ROOT,sys
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = 1 
from ROOT import *

nBkg = 1

def provideSignalScaling(mass):
        nz   = 14767                      #From Alexander (80X prompt)
        nsig_scale = 1394.4287350394588  # prescale/eff_z (123.685828798/0.0887) -->derives the lumi 
        eff = signalEff(mass)
        result =(nsig_scale*nz*eff)
	return result	

def signalEff(mass):

        trig_a = 0.9712
        trig_b = 3.1063E-07
        trig_c = 0.

        eff_a     = 0.215
        eff_b     = -6.65E05
        eff_c     = 0.
        eff_d     = -5.617977528089888e-09

	return (eff_a+eff_b/(mass+eff_c)**3+(mass)**2*eff_d)*(trig_a + trig_b*mass + trig_c*mass*mass)	

def signalEffUncert(mass):


	effDown =  1. + (0.04**2 + ((0.971242305389  + 3.10628148131e-07*mass ) / (0.987369135229 + -3.75634851186e-05*mass + 2.48504956152e-09*mass*mass) -1.)**2)**0.5

	return [1./effDown,1.01]



def provideUncertainties(mass):

	result = {}

	result["sigEff"] = signalEffUncert(mass)
	result["massScale"] = 0.01
	result ["bkgUncert"] = 0
	
	return result


def getResolution(mass):
	return 2.7E-02 + 3.3E-05*mass  - 1.9E-09*mass*mass

def createSignalDataset(massVal,name,width,nEvents):

	#ROOT.gSystem.Load("shapes/ZPrimeMuonBkgPdf_cxx.so")
#	ROOT.gSystem.AddIncludePath("-Ishapes"
	ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)

	import glob
	for f in glob.glob("userfuncs/*.cxx"):
		ROOT.gSystem.Load(f)

	dataFile = "input/dimuon_13TeV_2016_ICHEPDataset_BEpos.txt"
	
	ws = RooWorkspace("dimuon_BEpos")
        mass = RooRealVar('mass','mass',massVal, 200, 5000 )
        getattr(ws,'import')(mass,ROOT.RooCmdArg())


	peak = RooRealVar("peak","peak",massVal, 200,500)
	peak.setConstant()
	getattr(ws,'import')(peak,ROOT.RooCmdArg())
	### configure instrinsic width

	width_p0 = RooRealVar('width_p0','width_p0',0.0)
	width_p1 = RooRealVar('width_p1','width_p1',0.006)
	width_p0.setConstant()
	width_p1.setConstant()
	getattr(ws,'import')(width_p0,ROOT.RooCmdArg())
	getattr(ws,'import')(width_p1,ROOT.RooCmdArg())

	ws.factory("sum::width(width_p0, prod(width_p1,peak))")

	### define signal shape

	#ws.factory("Voigtian::sig_pdf_dimuon_BB(mass, peak, width, sigma)")
	ws.factory("Voigtian::sig_pdf(mass, peak, width, %.3f)"%(massVal*getResolution(massVal)))

        bkg_a = RooRealVar('bkg_a','bkg_a',23.86)
        bkg_b = RooRealVar('bkg_b','bkg_b',-2.616E-3)
        bkg_c = RooRealVar('bkg_c','bkg_c',2.743E-7)
        bkg_d = RooRealVar('bkg_d','bkg_d',-2.527E-11)
        bkg_e = RooRealVar('bkg_e','bkg_e',-3.286)


	bkg_a.setConstant()
	bkg_b.setConstant()
	bkg_c.setConstant()
	bkg_d.setConstant()
	bkg_e.setConstant()
	getattr(ws,'import')(bkg_a,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_b,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_c,ROOT.RooCmdArg())
        getattr(ws,'import')(bkg_d,ROOT.RooCmdArg())
        getattr(ws,'import')(bkg_e,ROOT.RooCmdArg())

        # background systematics
        bkg_syst_a = RooRealVar('bkg_syst_a','bkg_syst_a',1.0)
        bkg_syst_b = RooRealVar('bkg_syst_b','bkg_syst_b',0.000)
        bkg_syst_a.setConstant()
        bkg_syst_b.setConstant()
        getattr(ws,'import')(bkg_syst_a,ROOT.RooCmdArg())
        getattr(ws,'import')(bkg_syst_b,ROOT.RooCmdArg())

        # background shape
        ws.factory("ZPrimeMuonBkgPdf::bkgpdf(mass, bkg_a, bkg_b, bkg_c,bkg_d,bkg_e,bkg_syst_a,bkg_syst_b)")


        with open(dataFile) as f:
                masses = f.readlines()
        nBkg = len(masses)

        dataSet = ws.pdf("bkgpdf").generate(ROOT.RooArgSet(ws.var("mass")),nBkg)
        nSignal = int(round(nEvents*signalEff(massVal)))
        dataSet.append(ws.pdf("sig_pdf").generate(ROOT.RooArgSet(ws.var("mass")),nSignal))
        dataSet.SetName("dimuon_BB")

        masses = []
        for i in range(0,dataSet.numEntries()):
                masses.append(dataSet.get(i).getRealValue("mass"))

        f = open("%s_%d_%.3f_%d.txt"%(name,massVal,width,nEvents), 'w')
        for mass in masses:
                f.write("%.4f\n" % mass)
        f.close()

def createWS(massVal,minNrEv,name,width,correlateMass,dataFile=""):

	#ROOT.gSystem.Load("shapes/ZPrimeMuonBkgPdf_cxx.so")
#	ROOT.gSystem.AddIncludePath("-Ishapes"
	ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)

	import glob
	for f in glob.glob("userfuncs/*.cxx"):
		gSystem.Load(f)


        if not correlateMass:
                peakName = "_dimuon_BEpos"
        else:
                peakName = ""
	
	if dataFile == "":
		dataFile = "input/dimuon_13TeV_2016_ICHEPDataset_BEpos.txt"

        effWidth = width + getResolution(massVal)

        from tools import getMassRange
        massLow, massHigh = getMassRange(massVal,minNrEv,effWidth,dataFile)

	ws = RooWorkspace("dimuon_BEpos")
	
	massFullRange = RooRealVar('massFullRange','massFullRange',massVal, 200 , 5000 )
	getattr(ws,'import')(massFullRange,ROOT.RooCmdArg())

	mass = RooRealVar('mass_dimuon_BEpos','mass_dimuon_BEpos',massVal, massLow, massHigh )
	getattr(ws,'import')(mass,ROOT.RooCmdArg())
	
	peak = RooRealVar("peak%s"%peakName,"peak%s"%peakName,massVal, massLow, massHigh)
	peak.setConstant()
	getattr(ws,'import')(peak,ROOT.RooCmdArg())
	
	### configure resolution	

	res_p0 = RooRealVar('res_p0','res_p0',2.7E-02)
	res_p1 = RooRealVar('res_p1','res_p1',3.3E-05)
	res_p2 = RooRealVar('res_p2','res_p2',-1.9E-09)
 
        res_p0.setConstant()
        res_p1.setConstant()
        res_p2.setConstant()
        getattr(ws,'import')(res_p0,ROOT.RooCmdArg())
        getattr(ws,'import')(res_p1,ROOT.RooCmdArg())
        getattr(ws,'import')(res_p2,ROOT.RooCmdArg())

        ws.factory("Pol2::sigma_rel(peak%s,res_p0,res_p1,res_p2)"%peakName)
        ws.factory("prod::sigma(sigma_rel, peak%s)"%peakName)

	### configure instrinsic width

	width_p0 = RooRealVar('width_p0','width_p0',0.0)
	width_p1 = RooRealVar('width_p1','width_p1',0.006)
	width_p0.setConstant()
	width_p1.setConstant()
	getattr(ws,'import')(width_p0,ROOT.RooCmdArg())
	getattr(ws,'import')(width_p1,ROOT.RooCmdArg())

	ws.factory("sum::width_dimuon_BB(width_p0, prod(width_p1,peak%s))"%peakName)

	### define signal shape

	#ws.factory("Voigtian::sig_pdf_dimuon_BEpos(mass, peak, width, sigma)")
	ws.factory("Voigtian::sig_pdf_dimuon_BEpos(mass_dimuon_BEpos, peak%s, width_dimuon_BB, %.3f)"%(peakName,massVal*getResolution(massVal)))

	bkg_a_dimuon_BEpos = RooRealVar('bkg_a_dimuon_BEpos','bkg_a_dimuon_BEpos',23.86)
	bkg_b_dimuon_BEpos = RooRealVar('bkg_b_dimuon_BEpos','bkg_b_dimuon_BEpos',-2.616E-3)
	bkg_c_dimuon_BEpos = RooRealVar('bkg_c_dimuon_BEpos','bkg_c_dimuon_BEpos',2.743E-7)
	bkg_d_dimuon_BEpos = RooRealVar('bkg_d_dimuon_BEpos','bkg_d_dimuon_BEpos',-2.527E-11)
	bkg_e_dimuon_BEpos = RooRealVar('bkg_e_dimuon_BEpos','bkg_e_dimuon_BEpos',-3.286)

	bkg_a_dimuon_BEpos.setConstant()
	bkg_b_dimuon_BEpos.setConstant()
	bkg_c_dimuon_BEpos.setConstant()
	bkg_d_dimuon_BEpos.setConstant()
	bkg_e_dimuon_BEpos.setConstant()
	getattr(ws,'import')(bkg_a_dimuon_BEpos,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_b_dimuon_BEpos,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_c_dimuon_BEpos,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_d_dimuon_BEpos,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_e_dimuon_BEpos,ROOT.RooCmdArg())
	
	# background systematics
	bkg_syst_a = RooRealVar('bkg_syst_a','bkg_syst_a',1.0)
	bkg_syst_b = RooRealVar('bkg_syst_b','bkg_syst_b',0.000)
	bkg_syst_a.setConstant()
	bkg_syst_b.setConstant()
	getattr(ws,'import')(bkg_syst_a,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_syst_b,ROOT.RooCmdArg())
	
	# background shape
	ws.factory("ZPrimeMuonBkgPdf::bkgpdf_dimuon_BEpos(mass_dimuon_BEpos, bkg_a_dimuon_BEpos, bkg_b_dimuon_BEpos, bkg_c_dimuon_BEpos,bkg_d_dimuon_BEpos,bkg_e_dimuon_BEpos,bkg_syst_a,bkg_syst_b)")		
	ws.factory("ZPrimeMuonBkgPdf::bkgpdf_fullRange(massFullRange, bkg_a_dimuon_BEpos, bkg_b_dimuon_BEpos, bkg_c_dimuon_BEpos,bkg_d_dimuon_BEpos,bkg_e_dimuon_BEpos,bkg_syst_a,bkg_syst_b)")		

	ds = RooDataSet.read(dataFile,RooArgList(mass))
	ds.SetName('data_dimuon_BEpos')
	ds.SetTitle('data_dimuon_BEpos')
	getattr(ws,'import')(ds,ROOT.RooCmdArg())

#	ws.addClassDeclImportDir("shapes/")	
	ws.importClassCode()	


	ws.writeToFile("%s.root"%name,True)
        from tools import getBkgEstInWindow
        return getBkgEstInWindow(ws,massLow,massHigh,dataFile)


def createHistograms(massVal,minNrEv,name,width,correlateMass,binWidth,dataFile=""):
	#ROOT.gSystem.Load("shapes/ZPrimeMuonBkgPdf_cxx.so")
#	ROOT.gSystem.AddIncludePath("-Ishapes"
	ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)

	import glob
	for f in glob.glob("userfuncs/*.cxx"):
		ROOT.gSystem.Load(f)
	if dataFile == "":
		dataFile = "input/dimuon_13TeV_2016_ICHEPDataset_BEpos.txt"

	effWidth = width + getResolution(massVal)
	
	from tools import getMassRange
	massLow, massHigh = getMassRange(massVal,minNrEv,effWidth,dataFile)	

	massLow = int(round(massLow))
	massHigh = int(round(massHigh))

        if not correlateMass:
                peakName = "_dimuon_BEpos"
        else:
                peakName = ""


	ws = RooWorkspace("dimuon_BEpos")

        massFullRange = RooRealVar('massFullRange','massFullRange',massVal, 200, 5000 )
        getattr(ws,'import')(massFullRange,ROOT.RooCmdArg())


	mass = RooRealVar('mass_dimuon_BEpos','mass_dimuon_BEpos',massVal, massLow, massHigh )
	getattr(ws,'import')(mass,ROOT.RooCmdArg())
	
	peak = RooRealVar("peak%s"%peakName,"peak%s"%peakName,massVal, massLow, massHigh)
	peak.setConstant()
	getattr(ws,'import')(peak,ROOT.RooCmdArg())
	
	### configure resolution	

        res_p0 = RooRealVar('res_p0','res_p0',1.9E-02)
        res_p1 = RooRealVar('res_p1','res_p1',2.4E-05)
        res_p2 = RooRealVar('res_p2','res_p2',-2.4E-09)

        res_p0.setConstant()
        res_p1.setConstant()
        res_p2.setConstant()
        getattr(ws,'import')(res_p0,ROOT.RooCmdArg())
        getattr(ws,'import')(res_p1,ROOT.RooCmdArg())
        getattr(ws,'import')(res_p2,ROOT.RooCmdArg())

        ws.factory("Pol2::sigma_rel(peak%s,res_p0,res_p1,res_p2)"%peakName)
        ws.factory("prod::sigma(sigma_rel, peak%s)"%peakName)

	### configure instrinsic width

	width_p0 = RooRealVar('width_p0','width_p0',0.0)
	width_p1 = RooRealVar('width_p1','width_p1',0.006)
	width_p0.setConstant()
	width_p1.setConstant()
	getattr(ws,'import')(width_p0,ROOT.RooCmdArg())
	getattr(ws,'import')(width_p1,ROOT.RooCmdArg())

	ws.factory("sum::width_dimuon_BEpos(width_p0, prod(width_p1,peak%s))"%peakName)

	### define signal shape

	#ws.factory("Voigtian::sig_pdf_dimuon_BEpos(mass, peak, width, sigma)")
	ws.factory("Voigtian::sig_pdf_dimuon_BEpos(mass_dimuon_BEpos, peak%s, width_dimuon_BEpos, %.3f)"%(peakName,massVal*getResolution(massVal)))


	bkg_a = RooRealVar('bkg_a_dimuon_BEpos','bkg_a_dimuon_BEpos',28.51)
	bkg_b = RooRealVar('bkg_b_dimuon_BEpos','bkg_b_dimuon_BEpos',-3.614E-4)
	bkg_c = RooRealVar('bkg_c_dimuon_BEpos','bkg_c_dimuon_BEpos',-1.470E-7)
	bkg_d = RooRealVar('bkg_d_dimuon_BEpos','bkg_d_dimuon_BEpos',6.885E-12)
	bkg_e = RooRealVar('bkg_e_dimuon_BEpos','bkg_e_dimuon_BEpos',-4.196)
	bkg_a.setConstant()
	bkg_b.setConstant()
	bkg_c.setConstant()
	bkg_d.setConstant()
	bkg_e.setConstant()
	getattr(ws,'import')(bkg_a,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_b,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_c,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_d,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_e,ROOT.RooCmdArg())
	
	# background systematics
	bkg_syst_a = RooRealVar('bkg_syst_a','bkg_syst_a',1.0)
	bkg_syst_b = RooRealVar('bkg_syst_b','bkg_syst_b',0.000)
	bkg_syst_a.setConstant()
	bkg_syst_b.setConstant()
	getattr(ws,'import')(bkg_syst_a,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_syst_b,ROOT.RooCmdArg())
	
	# background shape
	ws.factory("ZPrimeMuonBkgPdf::bkgpdf_dimuon_BEpos(mass_dimuon_BEpos, bkg_a_dimuon_BEpos, bkg_b_dimuon_BEpos, bkg_c_dimuon_BEpos,bkg_d_dimuon_BEpos,bkg_e_dimuon_BEpos,bkg_syst_a,bkg_syst_b)")		
	ws.factory("ZPrimeMuonBkgPdf::bkgpdf_fullRange(massFullRange, bkg_a_dimuon_BEpos, bkg_b_dimuon_BEpos, bkg_c_dimuon_BEpos,bkg_d_dimuon_BEpos,bkg_e_dimuon_BEpos,bkg_syst_a,bkg_syst_b)")		

	ws.addClassDeclImportDir("shapes/")	
	ws.importClassCode()	


	
        
	from tools import getBkgEstInWindow
	nBackground = getBkgEstInWindow(ws,massLow,massHigh,dataFile)
	
	nBins = (massHigh - massLow)/binWidth 
	ws.var("mass_dimuon_BEpos").setBins(nBins)

	histFile = ROOT.TFile("%s.root"%name, "RECREATE")	

	scaleName = "scale"
	if not correlateMass:
		scaleName +="_dimuon_BEpos"

	sigShape = ws.pdf("sig_pdf_dimuon_BEpos").generate(ROOT.RooArgSet(ws.var("mass_dimuon_BEpos")),100000)
	sigHist = ROOT.TH1F("sigHist_dimuon_BEpos","sigHist_dimuon_BEpos",nBins,massLow,massHigh)
	sigHistUp = ROOT.TH1F("sigHist_dimuon_BEpos_%sUp"%scaleName,"sigHist_dimuon_BEpos_%sUp"%scaleName,nBins,massLow,massHigh)
	sigHistDown = ROOT.TH1F("sigHist_dimuon_BEpos_%sDown"%scaleName,"sigHist_dimuon_BEpos_%sDown"%scaleName,nBins,massLow,massHigh)
        for i in range(0,sigShape.numEntries()):
                sigHist.Fill(sigShape.get(i).getRealValue("mass_dimuon_BEpos"))
                sigHistUp.Fill(sigShape.get(i).getRealValue("mass_dimuon_BEpos")*1.01)
                sigHistDown.Fill(sigShape.get(i).getRealValue("mass_dimuon_BEpos")*0.99)
	sigHist.Scale(1./(sigHist.GetEntries())*provideSignalScaling(massVal)*1e-7)
	sigHistUp.Scale(1./(sigHistUp.GetEntries())*provideSignalScaling(massVal)*1e-7)
	sigHistDown.Scale(1./(sigHistDown.GetEntries())*provideSignalScaling(massVal)*1e-7)

	bkgShape = ws.pdf("bkgpdf_dimuon_BEpos").generate(ROOT.RooArgSet(ws.var("mass_dimuon_BEpos")),100000)
	bkgHist = ROOT.TH1F("bkgHist_dimuon_BEpos","bkgHist_dimuon_BEpos",nBins,massLow,massHigh)
        for i in range(0,bkgShape.numEntries()):
                bkgHist.Fill(bkgShape.get(i).getRealValue("mass_dimuon_BEpos"))
	bkgHist.Scale(1./(bkgHist.GetEntries())*nBackground)

	dataHist = ROOT.TH1F("data_dimuon_BEpos","data_dimuon_BEpos",nBins,massLow,massHigh)
	
	
        with open(dataFile) as f:
                masses = f.readlines()
	for mass in masses:
		mass = float(mass)
		if (mass >= massLow and mass <= massHigh):
			dataHist.Fill(mass)
	histFile.Write()
	histFile.Close()


        return nBackground
	
