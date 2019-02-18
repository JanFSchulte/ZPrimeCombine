import ROOT,sys
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = 1 
from ROOT import *
from math import sqrt
#nBkg = -1
nBkg = 9444.1 

dataFile = "input/diEleEBEB_2016_promptRECOICHEP.txt"

def provideSignalScaling(mass):
	nz   =  1900930                      
	nsig_scale = 10.91       
	eff = signalEff(mass)
	result = (nsig_scale*nz*eff)

	return result

def signalEff(mass):

	eff_a     = 0.713
	eff_b     = -940.1
	eff_c     = 1578 
	eff_d     = 0
	eff_e	  = 0
	return (eff_a+eff_b/(mass+eff_c)+eff_d/(mass*mass+eff_e))
		

def provideUncertainties(mass):

	result = {}

	result["sigEff"] = [1.08]
	result["massScale"] = 0.01
	result ["bkgUncert"] = 1.4
	
	return result



def getResolution(mass):

	res_scale = 1
	res_s = 11.6
	res_n = 10.0
	res_c = 0.64
	res_slope = 7.1E-5
	return res_scale*0.01*(sqrt(res_s*res_s/mass+res_n*res_n/mass/mass+res_c*res_c)+res_slope*mass)	

def loadBackgroundShape(ws):

	bkg_a = RooRealVar('bkg_a_dielectron_EBEB','bkg_a_dielectron_EBEB',-0.000706351)
	bkg_b = RooRealVar('bkg_b_dielectron_EBEB','bkg_b_dielectron_EBEB',-4.3829e-08)
	bkg_c = RooRealVar('bkg_c_dielectron_EBEB','bkg_c_dielectron_EBEB',-7.22726e-12)
	bkg_d = RooRealVar('bkg_d_dielectron_EBEB','bkg_d_dielectron_EBEB',-4.15683)
	bkg_a.setConstant()
	bkg_b.setConstant()
	bkg_c.setConstant()
	bkg_d.setConstant()
	getattr(ws,'import')(bkg_a,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_b,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_c,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_d,ROOT.RooCmdArg())
	
	# background systematics
	bkg_syst_a = RooRealVar('bkg_syst_a_dielectron_EBEB','bkg_syst_a_dielectron_EBEB',1.0)
	bkg_syst_b = RooRealVar('bkg_syst_b_dielectron_EBEB','bkg_syst_b_dielectron_EBEB',0.000)
	#bkg_syst_b = RooRealVar('bkg_syst_b','bkg_syst_b',-0.000017)
	bkg_syst_a.setConstant()
	bkg_syst_b.setConstant()
	getattr(ws,'import')(bkg_syst_a,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_syst_b,ROOT.RooCmdArg())
	
	# background shape
	ws.factory("ZPrimeBkgPdf::bkgpdf_dielectron_EBEB(mass_dielectron_EBEB, bkg_a_dielectron_EBEB, bkg_b_dielectron_EBEB, bkg_c_dielectron_EBEB,bkg_d_dielectron_EBEB,bkg_syst_a_dielectron_EBEB,bkg_syst_b_dielectron_EBEB)")		
	ws.factory("ZPrimeBkgPdf::bkgpdf_fullRange(massFullRange, bkg_a_dielectron_EBEB, bkg_b_dielectron_EBEB, bkg_c_dielectron_EBEB,bkg_d_dielectron_EBEB,bkg_syst_a_dielectron_EBEB,bkg_syst_b_dielectron_EBEB)")		

	return ws
