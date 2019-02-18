import ROOT,sys
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = 1 
from ROOT import *
from math import sqrt
from resolution_dielectron2017_cfg import DCB_para
nBkg = -1
#nBkg = -1

dataFile = "input/data_rereco_2017_BE.txt"
def addBkgUncertPrior(ws,label,channel,uncert):

        beta_bkg = RooRealVar('beta_%s_%s'%(label,channel),'beta_%s_%s'%(label,channel),0,-5,5)
        getattr(ws,'import')(beta_bkg,ROOT.RooCmdArg())
        uncert = 1. + uncert
        bkg_kappa = RooRealVar('%s_%s_kappa'%(label,channel),'%s_%s_kappa'%(label,channel),uncert)
        bkg_kappa.setConstant()
        getattr(ws,'import')(bkg_kappa,ROOT.RooCmdArg())
        ws.factory("PowFunc::%s_%s_nuis(%s_%s_kappa, beta_%s_%s)"%(label,channel,label,channel,label,channel))
        ws.factory("prod::%s_%s_forUse(%s_%s, %s_%s_nuis)"%(label,channel,label,channel,label,channel))


def provideSignalScaling(mass,spin2=False):
	nz   =  2086010.3 
	nsig_scale = 1./0.0294 
	eff = signalEff(mass,spin2)
	result = (nsig_scale*nz*eff)

	return result

def signalEff(mass,spin2=False):
	eff_a     = 1.16132e-02
	eff_b     = 4.93560e+02
	eff_c     = 7.29289e+02
	eff_d     = -9.92777e+04
	eff_e	  = 7.29595e+04
	eff_f 	  = 1.39617e+07
	eff_g 	  = 2.15172e+07
	
	if spin2:
		eff_a = 0.06212
		eff_b = -7.192
		eff_c = 56.72
		eff_d = -43.69
		eff_e = 822.9
		eff_f = 3.579e08
		eff_g = 3.048e09
		
	return (eff_a+eff_b/(mass+eff_c)+eff_d/(mass*mass+eff_e))+eff_f/(mass**3+eff_g)

		

def provideUncertainties(mass):

	result = {}

	result["sigEff"] = [1.08] # must be list in case the uncertainty is asymmetric
	result["massScale"] = 0.01
	result ["bkgUncert"] = 1.4
	result ["res"] = 0.0

	result["bkgParams"] = {"bkg_a":0.25600139916050374,"bkg_b":0.057156914351919205,"bkg_c":0.0,"bkg_d":0.0,"bkg_e":0.022476664055819436,"bkg_a2":0.05148324153076286,"bkg_b2":0.07180284546858498,"bkg_c2":0.33612018781230835,"bkg_d2":0.5113617584805714,"bkg_e2":0.015269527416692675}
	#result["bkgParams"] = {"bkg_a":0.23843520903507034,"bkg_b":0.042557205520631004,"bkg_c":0.4772108713152145,"bkg_d":0.20039400197000984,"bkg_e":0.02121430756489364,"bkg_a2":0.21935669378841924,"bkg_b2":0.05489687902965316,"bkg_c2":0.11981929926738805,"bkg_d2":0.15078950936605048,"bkg_e2":0.023322536781016343}
	return result



def getResolution(mass):
	CBObject = DCB_para("dcb")
	CBObject.get_value(mass,False)

	result = {}

	result["res"] = CBObject.sigma
	result["mean"] = CBObject.mean
	result["powerR"] = CBObject.PowerR
	result["powerL"] = CBObject.PowerL
	result["cutL"] = CBObject.CutL
	result["cutR"] = CBObject.CutR
	if result["powerR"] < 0:
		result["powerR"] = 0.
	return result

def loadBackgroundShape(ws,useShapeUncert=False):
	bkg_a = RooRealVar('bkg_a_dielectron_2017_EBEE','bkg_a_dielectron_2017_EBEE',1.00060e+00)
	bkg_b = RooRealVar('bkg_b_dielectron_2017_EBEE','bkg_b_dielectron_2017_EBEE',-3.78047e-03)
	bkg_c = RooRealVar('bkg_c_dielectron_2017_EBEE','bkg_c_dielectron_2017_EBEE',0)
	bkg_d = RooRealVar('bkg_d_dielectron_2017_EBEE','bkg_d_dielectron_2017_EBEE',0)
	bkg_e = RooRealVar('bkg_e_dielectron_2017_EBEE','bkg_e_dielectron_2017_EBEE',-2.78326e+00)
	bkg_a2 = RooRealVar('bkg_a2_dielectron_2017_EBEE','bkg_a2_dielectron_2017_EBEE',4.99986e+00)
	bkg_b2 = RooRealVar('bkg_b2_dielectron_2017_EBEE','bkg_b2_dielectron_2017_EBEE',-2.37641e-03)
	bkg_c2 = RooRealVar('bkg_c2_dielectron_2017_EBEE','bkg_c2_dielectron_2017_EBEE',1.98922e-07)
	bkg_d2 = RooRealVar('bkg_d2_dielectron_2017_EBEE','bkg_d2_dielectron_2017_EBEE',-1.76698e-11)
	bkg_e2 = RooRealVar('bkg_e2_dielectron_2017_EBEE','bkg_e2_dielectron_2017_EBEE',-3.55641e+00)


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
	
        
	bkg_a2.setConstant()
	bkg_b2.setConstant()
	bkg_c2.setConstant()
	bkg_d2.setConstant()
	bkg_e2.setConstant()
	getattr(ws,'import')(bkg_a2,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_b2,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_c2,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_d2,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_e2,ROOT.RooCmdArg())
	
	# background systematics
	bkg_syst_a = RooRealVar('bkg_syst_a_dielectron_2017_EBEE','bkg_syst_a_dielectron_2017_EBEE',1.0)
	bkg_syst_b = RooRealVar('bkg_syst_b_dielectron_2017_EBEE','bkg_syst_b_dielectron_2017_EBEE',0.000)
	#bkg_syst_b = RooRealVar('bkg_syst_b','bkg_syst_b',-0.000017)
	bkg_syst_a.setConstant()
	bkg_syst_b.setConstant()
	getattr(ws,'import')(bkg_syst_a,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_syst_b,ROOT.RooCmdArg())
	if useShapeUncert:
		bkgParamsUncert = provideUncertainties(1000)["bkgParams"]
		for uncert in bkgParamsUncert:
			addBkgUncertPrior(ws,uncert,"dielectron_2017_EBEE",bkgParamsUncert[uncert] )

	# background shape
		ws.factory("ZPrimeEleBkgPdf3::bkgpdf_dielectron_2017_EBEE(mass_dielectron_2017_EBEE, bkg_a_dielectron_2017_EBEE_forUse, bkg_b_dielectron_2017_EBEE_forUse, bkg_c_dielectron_2017_EBEE_forUse,bkg_d_dielectron_2017_EBEE_forUse,bkg_e_dielectron_2017_EBEE_forUse,bkg_a2_dielectron_2017_EBEE_forUse, bkg_b2_dielectron_2017_EBEE_forUse, bkg_c2_dielectron_2017_EBEE_forUse,bkg_d2_dielectron_2017_EBEE_forUse,bkg_e2_dielectron_2017_EBEE_forUse,bkg_syst_a_dielectron_2017_EBEE,bkg_syst_b_dielectron_2017_EBEE)")		
		ws.factory("ZPrimeEleBkgPdf3::bkgpdf_fullRange(massFullRange, bkg_a_dielectron_2017_EBEE_forUse, bkg_b_dielectron_2017_EBEE_forUse, bkg_c_dielectron_2017_EBEE_forUse,bkg_d_dielectron_2017_EBEE_forUse,bkg_e_dielectron_2017_EBEE_forUse,bkg_a2_dielectron_2017_EBEE_forUse, bkg_b2_dielectron_2017_EBEE_forUse, bkg_c2_dielectron_2017_EBEE_forUse,bkg_d2_dielectron_2017_EBEE_forUse,bkg_e2_dielectron_2017_EBEE_forUse,bkg_syst_a_dielectron_2017_EBEE,bkg_syst_b_dielectron_2017_EBEE)")		
	else:	
		ws.factory("ZPrimeEleBkgPdf3::bkgpdf_dielectron_2017_EBEE(mass_dielectron_2017_EBEE, bkg_a_dielectron_2017_EBEE, bkg_b_dielectron_2017_EBEE, bkg_c_dielectron_2017_EBEE,bkg_d_dielectron_2017_EBEE,bkg_e_dielectron_2017_EBEE,bkg_a2_dielectron_2017_EBEE, bkg_b2_dielectron_2017_EBEE, bkg_c2_dielectron_2017_EBEE,bkg_d2_dielectron_2017_EBEE,bkg_e2_dielectron_2017_EBEE,bkg_syst_a_dielectron_2017_EBEE,bkg_syst_b_dielectron_2017_EBEE)")		
		ws.factory("ZPrimeEleBkgPdf3::bkgpdf_fullRange(massFullRange, bkg_a_dielectron_2017_EBEE, bkg_b_dielectron_2017_EBEE, bkg_c_dielectron_2017_EBEE,bkg_d_dielectron_2017_EBEE,bkg_e_dielectron_2017_EBEE,bkg_a2_dielectron_2017_EBEE, bkg_b2_dielectron_2017_EBEE, bkg_c2_dielectron_2017_EBEE,bkg_d2_dielectron_2017_EBEE,bkg_e2_dielectron_2017_EBEE,bkg_syst_a_dielectron_2017_EBEE,bkg_syst_b_dielectron_2017_EBEE)")		
	return ws
