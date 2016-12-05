import ROOT,sys
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = 1 
from ROOT import *

nBkg = -1

dataFile = "input/dimuon_13TeV_2016_ICHEPDataset_BB.txt"

def provideSignalScaling(mass):
	nz   =  21152                      #From Alexander (80X prompt)
	nsig_scale = 1017.9903604773663       # prescale/eff_z (123.685828798/0.1215) -->derives the lumi 
	eff = signalEff(mass)
	result = (nsig_scale*nz*eff)
	return result

def signalEff(mass):

	trig_a = 0.9878
	trig_b = -7.8162E-08
	trig_c = 0.	

	eff_a     = 1.54
	eff_b     = -6.72E3
	eff_c     = 4.69E3 
	eff_d     = -6.08E-5
	return	(eff_a+eff_b/(mass+eff_c)+mass*eff_d)*(trig_a + trig_b*mass + trig_c*mass*mass)

		

def signalEffUncert(mass):

	effDown = 1.+(0.03**2 + 0.01**2)**0.5
	
	return [1./effDown,1.01]



def provideUncertainties(mass):

	result = {}

	result["sigEff"] = signalEffUncert(mass)
	result["massScale"] = 0.01
	result ["bkgUncert"] = 1.4
	
	return result



def getResolution(mass):
	
	return 1.9E-02 + 2.4E-05*mass -2.4E-09*mass*mass


def loadBackgroundShape(ws):

	bkg_a = RooRealVar('bkg_a_dimuon_BB','bkg_a_dimuon_BB',28.51)
	bkg_b = RooRealVar('bkg_b_dimuon_BB','bkg_b_dimuon_BB',-3.614E-4)
	bkg_c = RooRealVar('bkg_c_dimuon_BB','bkg_c_dimuon_BB',-1.470E-7)
	bkg_d = RooRealVar('bkg_d_dimuon_BB','bkg_d_dimuon_BB',6.885E-12)
	bkg_e = RooRealVar('bkg_e_dimuon_BB','bkg_e_dimuon_BB',-4.196)
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
	bkg_syst_a = RooRealVar('bkg_syst_a_BB_PI','bkg_syst_a_BB_PI',1.0)
	#bkg_syst_a = RooRealVar('bkg_syst_a_BB_PI','bkg_syst_a_BB_PI',0.26/0.3)
	bkg_syst_b = RooRealVar('bkg_syst_b_BB_PI','bkg_syst_b_BB_PI',0.000)
	#bkg_syst_b = RooRealVar('bkg_syst_b','bkg_syst_b',-0.000017)
	bkg_syst_a.setConstant()
	bkg_syst_b.setConstant()
	getattr(ws,'import')(bkg_syst_a,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_syst_b,ROOT.RooCmdArg())
	
	# background shape
	ws.factory("ZPrimeMuonBkgPdfPI::bkgpdf_dimuon_BB_PI(mass_dimuon_BB_PI, bkg_a_dimuon_BB, bkg_b_dimuon_BB, bkg_c_dimuon_BB,bkg_d_dimuon_BB,bkg_e_dimuon_BB,bkg_syst_a_BB_PI,bkg_syst_b_BB_PI)")		
	ws.factory("ZPrimeMuonBkgPdfPI::bkgpdf_fullRange(massFullRange, bkg_a_dimuon_BB, bkg_b_dimuon_BB, bkg_c_dimuon_BB,bkg_d_dimuon_BB,bkg_e_dimuon_BB,bkg_syst_a_BB_PI,bkg_syst_b_BB_PI)")		

	return ws
