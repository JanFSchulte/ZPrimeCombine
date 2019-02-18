import ROOT,sys
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = 1 
from ROOT import *

nBkg = -1

def provideSignalScaling(mass):
        nz   = 14980                      #From Alexander (80X prompt)
        nsig_scale = 1392.85843240991  # prescale/eff_z (123.685828798/0.0887) -->derives th
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
	uncertNeg = 1. + ( effPart**2 + trigPart**2 )**0.5
	uncertNeg = 1./uncertNeg
	if uncertNeg < 0.01:
		uncertNeg = 0.01
	return [uncertNeg,1.01]


def provideUncertainties(mass):

	result = {}

	result["sigEff"] = signalEffUncert(mass)
	result["massScale"] = 0.01
	result ["bkgUncert"] = 1.4
	
	return result
def getResolution(mass):
	return 2.6E-02 + 3.2E-05*mass - 1.6E-09*mass*mass

dataFile = "input/dimuon_13TeV_2016_ICHEPDataset_BEneg.txt"

def loadBackgroundShape(ws):
	bkg_a = RooRealVar('bkg_a_dimuon_BEneg','bkg_a_dimuon_BEneg',21.24)
	bkg_b = RooRealVar('bkg_b_dimuon_BEneg','bkg_b_dimuon_BEneg',-3.521E-3)
	bkg_c = RooRealVar('bkg_c_dimuon_BEneg','bkg_c_dimuon_BEneg',5.025E-7)
	bkg_d = RooRealVar('bkg_d_dimuon_BEneg','bkg_d_dimuon_BEneg',-4.365E-11)
	bkg_e = RooRealVar('bkg_e_dimuon_BEneg','bkg_e_dimuon_BEneg',-2.768)
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
	ws.factory("ZPrimeMuonBkgPdf::bkgpdf_dimuon_BEneg(mass_dimuon_BEneg, bkg_a_dimuon_BEneg, bkg_b_dimuon_BEneg, bkg_c_dimuon_BEneg,bkg_d_dimuon_BEneg,bkg_e_dimuon_BEneg,bkg_syst_a,bkg_syst_b)")		
	ws.factory("ZPrimeMuonBkgPdf::bkgpdf_fullRange(massFullRange, bkg_a_dimuon_BEneg, bkg_b_dimuon_BEneg, bkg_c_dimuon_BEneg,bkg_d_dimuon_BEneg,bkg_e_dimuon_BEneg,bkg_syst_a,bkg_syst_b)")		
	
	return ws

