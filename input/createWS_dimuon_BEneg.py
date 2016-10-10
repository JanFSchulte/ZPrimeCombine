import ROOT,sys
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = 1 
from ROOT import *

nBkg = 1

def provideSignalScaling(mass):
        nz   = 7262                      #From Alexander (80X prompt)
        nsig_scale = 1394.4287350394588  # prescale/eff_z (123.685828798/0.0887) -->derives the lumi 
        eff = signalEff(mass)
        result = (nsig_scale*nz*eff)
	return result

def signalEff(mass):

        trig_a = 0.9724
        trig_b = -3.3403E-07
        trig_c = 1.6175E-10

        eff_a     = 0.248
        eff_b     = -1.44e6
        eff_c     = 0.
        eff_d     = -2.967359050445104e-09

        return (eff_a+eff_b/(mass+eff_c)**3+(mass)**2*eff_d)*(trig_a + trig_b*mass + trig_c*mass*mass)



def signalEffUncert(mass):

        effPart = max(0.,min(1.,1.003 -0.000132*mass-0.000000024*mass*mass)) -1.
        trigPart = (0.972352522752 + -3.34032692503e-06*mass + 1.61745590874e-10*mass*mass) / (0.981606029688 + -1.39766860383e-05*mass + -9.42079658943e-09*mass*mass) -1.
        uncertNeg = 1. - ( effPart**2 + trigPart**2 )**0.5
	if uncertNeg < 0.01:
		uncertNet = 0.01
	return [1. - uncertNeg,1.01]


def provideUncertainties(mass):

	result = {}

	result["sigEff"] = signalEffUncert(mass)
	result["massScale"] = 0.01
	result ["bkgUncert"] = 0
	
	return result


def createWS(massVal,minNrEv,name):

	#ROOT.gSystem.Load("shapes/ZPrimeMuonBkgPdf_cxx.so")
#	ROOT.gSystem.AddIncludePath("-Ishapes"
	ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)

	import glob
	for f in glob.glob("userfuncs/*.cxx"):
		gSystem.Load(f)
	
	
	with open("input/dimuon_13TeV_2016_ICHEPDataset_BEneg.txt") as f:
		masses = f.readlines()
	massDiffs = []
	for evMass in masses:
		massDiffs.append(abs(float(evMass)-massVal)) 
	massDiffs = sorted(massDiffs)
	
	if minNrEv < len(massDiffs):
		massDiff = massDiffs[minNrEv]
	massLow = massVal - massDiff
	massHigh = massVal + massDiff

	width = 0.006

	if (massVal-6*width*massVal) < massLow:
		massLow = massVal - 6*width*massVal
	if (massVal+6*width*massVal) > massHigh:
		massHigh = massVal + 6*width*massVal

	ws = RooWorkspace("dimuon_BEneg")
	
	mass = RooRealVar('mass','mass',massVal, massLow, massHigh )
	getattr(ws,'import')(mass,ROOT.RooCmdArg())
	
	peak = RooRealVar("peak","peak",massVal, massLow, massHigh)
	peak.setConstant()
	getattr(ws,'import')(peak,ROOT.RooCmdArg())
	
	### configure resolution	

	res_p0 = RooRealVar('res_p0','res_p0',2.6E-02)
	res_p1 = RooRealVar('res_p1','res_p1',3.2E-05)
	res_p2 = RooRealVar('res_p2','res_p2',-1.6E-09)
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

	ws.factory("Voigtian::sig_pdf_dimuon_BEneg(mass, peak, width, sigma)")

	bkg_a = RooRealVar('bkg_a','bkg_a',21.24)
	bkg_b = RooRealVar('bkg_b','bkg_b',-3.521E-3)
	bkg_c = RooRealVar('bkg_c','bkg_c',5.025E-7)
	bkg_d = RooRealVar('bkg_d','bkg_d',-4.365E-11)
	bkg_e = RooRealVar('bkg_e','bkg_e',-2.768)
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
	ws.factory("ZPrimeMuonBkgPdf::bkgpdf_dimuon_BEneg(mass, bkg_a, bkg_b, bkg_c,bkg_d,bkg_e,bkg_syst_a,bkg_syst_b)")		

	ds = RooDataSet.read("input/dimuon_13TeV_2016_ICHEPDataset_BB.txt",RooArgList(mass))
	ds.SetName('data_dimuon_BEneg')
	ds.SetTitle('data_dimuon_BEneg')
	getattr(ws,'import')(ds,ROOT.RooCmdArg())

#	ws.addClassDeclImportDir("shapes/")	
	ws.importClassCode()	


	ws.writeToFile("%s.root"%name,True)

	return ws.data("data_dimuon_BEneg").sumEntries()
