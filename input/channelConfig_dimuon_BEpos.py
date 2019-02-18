import ROOT,sys
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = 1 
from ROOT import *

nBkg = -1

def provideSignalScaling(mass):
        nz   = 14767                      #From Alexander (80X prompt)
        nsig_scale = 1394.4287350394588  # prescale/eff_z (123.685828798/0.0887) -->derives the lumi 
        eff = signalEff(mass)
	result = (nsig_scale*nz*eff)

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
	result ["bkgUncert"] = 1.4
	
	return result


def getResolution(mass):
	return 2.7E-02 + 3.3E-05*mass  - 1.9E-09*mass*mass

dataFile = "input/dimuon_13TeV_2016_ICHEPDataset_BEpos.txt"


def loadBackgroundShape(ws):
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

	return ws

