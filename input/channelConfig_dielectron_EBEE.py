import ROOT,sys
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = 1 
from ROOT import *
from math import sqrt
nBkg = 8446.2
#nBkg = -1

dataFile = "input/diEleEBEE_2016_promptRECOICHEP.txt"

def provideSignalScaling(mass):
	nz   =  688995                      
	nsig_scale = 29.85       
	eff = signalEff(mass)
	result = (nsig_scale*nz*eff)

	return result

def signalEff(mass):

	eff_a     = -0.04029
	eff_b     = 801.3
	eff_c     = 1386
	eff_d     = -8.511E4
	eff_e	  = 2.279E5
	return (eff_a+eff_b/(mass+eff_c)+eff_d/(mass*mass+eff_e))

		

def provideUncertainties(mass):

	result = {}

	result["sigEff"] = [1.10] # must be list in case the uncertainty is asymmetric
	result["massScale"] = 0.01
	result ["bkgUncert"] = 1.4
	
	return result



def getResolution(mass):

	res_scale = 1
	res_s = 15.0
	res_n = 10.0
	res_c = 1.56
	res_slope = 0
	return res_scale*0.01*(sqrt(res_s*res_s/mass+res_n*res_n/mass/mass+res_c*res_c)+res_slope*mass)	


def loadBackgroundShape(ws):

	bkg_a = RooRealVar('bkg_a_dielectron_EBEE','bkg_a_dielectron_EBEE',-0.00366637)
	bkg_b = RooRealVar('bkg_b_dielectron_EBEE','bkg_b_dielectron_EBEE',6.18691e-07)
	bkg_c = RooRealVar('bkg_c_dielectron_EBEE','bkg_c_dielectron_EBEE',-7.06263e-11)
	bkg_d = RooRealVar('bkg_d_dielectron_EBEE','bkg_d_dielectron_EBEE',-3.05822)
	bkg_a.setConstant()
	bkg_b.setConstant()
	bkg_c.setConstant()
	bkg_d.setConstant()
	getattr(ws,'import')(bkg_a,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_b,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_c,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_d,ROOT.RooCmdArg())
	
	# background systematics
	bkg_syst_a = RooRealVar('bkg_syst_a_dielectron_EBEE','bkg_syst_a_dielectron_EBEE',1.0)
	bkg_syst_b = RooRealVar('bkg_syst_b_dielectron_EBEE','bkg_syst_b_dielectron_EBEE',0.000)
	#bkg_syst_b = RooRealVar('bkg_syst_b','bkg_syst_b',-0.000017)
	bkg_syst_a.setConstant()
	bkg_syst_b.setConstant()
	getattr(ws,'import')(bkg_syst_a,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_syst_b,ROOT.RooCmdArg())
	
	# background shape
	ws.factory("ZPrimeBkgPdf::bkgpdf_dielectron_EBEE(mass_dielectron_EBEE, bkg_a_dielectron_EBEE, bkg_b_dielectron_EBEE, bkg_c_dielectron_EBEE,bkg_d_dielectron_EBEE,bkg_syst_a_dielectron_EBEE,bkg_syst_b_dielectron_EBEE)")		
	ws.factory("ZPrimeBkgPdf::bkgpdf_fullRange(massFullRange, bkg_a_dielectron_EBEE, bkg_b_dielectron_EBEE, bkg_c_dielectron_EBEE,bkg_d_dielectron_EBEE,bkg_syst_a_dielectron_EBEE,bkg_syst_b_dielectron_EBEE)")		

	return ws
