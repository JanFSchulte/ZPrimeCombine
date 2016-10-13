import ROOT,sys
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = 1 
from ROOT import *

nBkg = 1

def provideSignalScaling(mass):
        nz   = 14980                      #From Alexander (80X prompt)
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


	effDown =  1. - (0.04**2 + ((0.971242305389  + 3.10628148131e-07*mass ) / (0.987369135229 + -3.75634851186e-05*mass + 2.48504956152e-09*mass*mass) -1.)**2)**0.5

	return [effDown,1.01]



def provideUncertainties(mass):

	result = {}

	result["sigEff"] = signalEffUncert(mass)
	result["massScale"] = 0.01
	result ["bkgUncert"] = 0
	
	return result


def getResolution(mass):
	return 2.7E-02 + 3.3E-05*mass  - 1.9E-09*mass*mass

def createWS(massVal,minNrEv,name,width):

	#ROOT.gSystem.Load("shapes/ZPrimeMuonBkgPdf_cxx.so")
#	ROOT.gSystem.AddIncludePath("-Ishapes"
	ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)

	import glob
	for f in glob.glob("userfuncs/*.cxx"):
		gSystem.Load(f)
	
	
	dataFile = "input/dimuon_13TeV_2016_ICHEPDataset_BEpos.txt"

        effWidth = width + getResolution(massVal)

        from tools import getMassRange
        massLow, massHigh = getMassRange(massVal,minNrEv,effWidth,dataFile)

	ws = RooWorkspace("dimuon_BEpos")
	
	massFullRange = RooRealVar('massFullRange','massFullRange',massVal, 200 , 5000 )
	getattr(ws,'import')(massFullRange,ROOT.RooCmdArg())

	mass = RooRealVar('mass','mass',massVal, massLow, massHigh )
	getattr(ws,'import')(mass,ROOT.RooCmdArg())
	
	peak = RooRealVar("peak","peak",massVal, massLow, massHigh)
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

        ws.factory("Pol2::sigma_rel(peak,res_p0,res_p1,res_p2)")
        ws.factory("prod::sigma(sigma_rel, peak)")

	### configure instrinsic width

	width_p0 = RooRealVar('width_p0','width_p0',0.0)
	width_p1 = RooRealVar('width_p1','width_p1',0.006)
	width_p0.setConstant()
	width_p1.setConstant()
	getattr(ws,'import')(width_p0,ROOT.RooCmdArg())
	getattr(ws,'import')(width_p1,ROOT.RooCmdArg())

	ws.factory("sum::width(width_p0, prod(width_p1,peak))")

	### define signal shape

	#ws.factory("Voigtian::sig_pdf_dimuon_BEpos(mass, peak, width, sigma)")
	ws.factory("Voigtian::sig_pdf_dimuon_BEpos(mass, peak, width, %.3f)"%(massVal*getResolution(massVal)))

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
	ws.factory("ZPrimeMuonBkgPdf::bkgpdf_dimuon_BEpos(mass, bkg_a, bkg_b, bkg_c,bkg_d,bkg_e,bkg_syst_a,bkg_syst_b)")		
	ws.factory("ZPrimeMuonBkgPdf::bkgpdf_fullRange(massFullRange, bkg_a, bkg_b, bkg_c,bkg_d,bkg_e,bkg_syst_a,bkg_syst_b)")		

	ds = RooDataSet.read(dataFile,RooArgList(mass))
	ds.SetName('data_dimuon_BEpos')
	ds.SetTitle('data_dimuon_BEpos')
	getattr(ws,'import')(ds,ROOT.RooCmdArg())

#	ws.addClassDeclImportDir("shapes/")	
	ws.importClassCode()	


	ws.writeToFile("%s.root"%name,True)
        from tools import getBkgEstInWindow
        return getBkgEstInWindow(ws,massLow,massHigh,dataFile)
