import ROOT,sys
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = 1 
from ROOT import *
from numpy import exp
nBkg = -1
from muonResolution import getResolution as getRes
dataFile = "input/dimuon_Mordion2017_BE.txt"
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
	nz   =  73255                      #From Alexander (80X prompt)
	nsig_scale = 978.0579591836735       # prescale/eff_z (167.73694/0.1715) -->derives the lumi 
	eff = signalEff(mass,spin2)
	result = (nsig_scale*nz*eff)

	return result


def signalEff(mass,spin2=False):

	if spin2:
		eff_a = 0.211629
		eff_b = 0.124469
		eff_c = 0.885894
		eff_d = -2605.605215
		eff_e = 611.338233	
		return	eff_a + eff_b * mass**eff_c * exp(- ((mass - eff_d ) / eff_e) )

	else:

##### default
		if mass <= 450:
			a =  13.56
			b =  6.672
			c = -4.879e+06
			d = -7.233e+06
			e = -826.
			f = -1.567
			return a - b * exp( -( (mass - c) / d) ) + e * mass**f
		else:
			eff_a     =  0.2529
			eff_b     =  0.06511
			eff_c     =  0.8755
			eff_d     = -4601.
			eff_e     =  1147.
			return	eff_a + eff_b * mass**eff_c * exp(- ((mass - eff_d ) / eff_e) )

#### flat after 2 TeV
#		if mass <= 450:
#			a =  13.37
#			b = 6.707
#			c = -4.869e+06
#			d = -7.405e+06
#			e = -1476.
#			f = -1.702
#			return a - b * exp( -( (mass - c) / d) ) + e * mass**f
#		else:
#			eff_a     =  0.2174
#			eff_b     =  0.08822
#			eff_c     =  0.7599
#			eff_d     = -4281.
#			eff_e     =  1209.
#			return	eff_a + eff_b * mass**eff_c * exp(- ((mass - eff_d ) / eff_e) )
##### linear
#		if mass <= 450:
#			a =  13.38
#			b = 6.707
#			c = -4.869e+06
#			d = -7.403e+06
#			e = -1472.
#			f = -1.701
#			return a - b * exp( -( (mass - c) / d) ) + e * mass**f
#		else:
#			eff_a     =  0.1924
#			eff_b     =  0.09908
#			eff_c     =  0.6725
#			eff_d     =  -4112.
#			eff_e     =  1356.
#			return	eff_a + eff_b * mass**eff_c * exp(- ((mass - eff_d ) / eff_e) )



		

def signalEffUncert(mass):
	if mass <= 450:

		a =  13.56
		b =  6.672
		c = -4.879e+06
		d = -7.233e+06
		e = -826.
		f = -1.567

		eff_default= a - b * exp( -( (mass - c) / d) ) + e * mass**f
	else:
		eff_a     =  0.2529
		eff_b     =  0.06511
		eff_c     =  0.8755
		eff_d     = -4601.
		eff_e     =  1147.
		eff_default =  eff_a + eff_b * mass**eff_c * exp(- ((mass - eff_d ) / eff_e) )
	if mass <= 450:
		a =  13.38
		b =  6.705
		c = -4.865e+06
		d = -7.413e+06
		e = -995.2
		f = -1.61
		eff_syst= a - b * exp( -( (mass - c) / d) ) + e * mass**f
	else:
		eff_a     =  0.2265
		eff_b     =  0.08241
		eff_c     =  0.7638
		eff_d     = -4358.
		eff_e     =  1251.
		eff_syst =  eff_a + eff_b * mass**eff_c * exp(- ((mass - eff_d ) / eff_e) )



	effDown = eff_default/eff_syst
	
	return [1./effDown,1.0]



def provideUncertainties(mass):

	result = {}

	result["sigEff"] = signalEffUncert(mass)
	result["massScale"] = 0.03
	result ["bkgUncert"] = 1.4	
	result ["res"] = 0.15
	result["bkgParams"] = {"bkg_a":0.0009545020680878141,"bkg_b":0.02363157894736842,"bkg_c":0.03163023110555902,"bkg_d":0.03849293563579278,"bkg_e":0.0015616866215512754, "bkg_a2":0.002012072434607646,"bkg_b2":0.010820559062218215,"bkg_c2":0.031979147941758046,"bkg_e2":0.004791238877481177}
	return result

def provideUncertaintiesCI(mass):

	result = {}

	result["trig"] = 1.007
	result["zPeak"] = 1.05
	result["xSecOther"] = 1.07
	result["jets"] = 1.5
	result["lumi"] = 1.025
	result["massScale"] = 0.0 ## dummy value
	result["stats"] = 0.0 ## dummy value
	result["res"] = 0.0 ## dummy value
	result["pdf"] = 0.0 ## dummy value
	result["ID"] = 0.0 ## dummy value
	result["PU"] = 0.0 ## dummy value
	return result



def getResolution(mass):
	result = {}
	params = getRes(mass)
	result['alphaL'] = params['alphaL']['BE']
	result['alphaR'] = params['alphaR']['BE']
	result['res'] = params['sigma']['BE']
	result['scale'] = params['scale']['BE']
	return result


def loadBackgroundShape(ws,useShapeUncert=False):


	bkg_a = RooRealVar('bkg_a_dimuon_Moriond2017_BE','bkg_a_dimuon_Moriond2017_BE', 31.43)
	bkg_b = RooRealVar('bkg_b_dimuon_Moriond2017_BE','bkg_b_dimuon_Moriond2017_BE',-0.0019)
	bkg_c = RooRealVar('bkg_c_dimuon_Moriond2017_BE','bkg_c_dimuon_Moriond2017_BE', 1.601e-07)
	bkg_d = RooRealVar('bkg_d_dimuon_Moriond2017_BE','bkg_d_dimuon_Moriond2017_BE',-1.911E-11)
	bkg_e = RooRealVar('bkg_e_dimuon_Moriond2017_BE','bkg_e_dimuon_Moriond2017_BE',-3.842)
	bkg_a2 = RooRealVar('bkg_a2_dimuon_Moriond2017_BE','bkg_a2_dimuon_Moriond2017_BE', 19.88)
	bkg_b2 = RooRealVar('bkg_b2_dimuon_Moriond2017_BE','bkg_b2_dimuon_Moriond2017_BE',-0.01109)
	bkg_c2 = RooRealVar('bkg_c2_dimuon_Moriond2017_BE','bkg_c2_dimuon_Moriond2017_BE', 5.563e-06)
	bkg_e2 = RooRealVar('bkg_e2_dimuon_Moriond2017_BE','bkg_e2_dimuon_Moriond2017_BE',-1.461)

	bkg_a.setConstant()
	bkg_b.setConstant()
	bkg_c.setConstant()
	bkg_d.setConstant()
	bkg_e.setConstant()
	bkg_a2.setConstant()
	bkg_b2.setConstant()
	bkg_c2.setConstant()
	bkg_e2.setConstant()
	getattr(ws,'import')(bkg_a,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_b,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_c,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_d,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_e,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_a2,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_b2,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_c2,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_e2,ROOT.RooCmdArg())
	
	# background systematics
	bkg_syst_a = RooRealVar('bkg_syst_a','bkg_syst_a',1.0)
	bkg_syst_b = RooRealVar('bkg_syst_b','bkg_syst_b',0.000)
	#bkg_syst_b = RooRealVar('bkg_syst_b','bkg_syst_b',-0.00016666666666)
	bkg_syst_a.setConstant()
	bkg_syst_b.setConstant()
	getattr(ws,'import')(bkg_syst_a,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_syst_b,ROOT.RooCmdArg())

	if useShapeUncert: 
		bkgParamsUncert = provideUncertainties(1000)["bkgParams"]
		for uncert in bkgParamsUncert:
			addBkgUncertPrior(ws,uncert,"dimuon_Moriond2017_BE",bkgParamsUncert[uncert] )

	# background shape
		ws.factory("ZPrimeMuonBkgPdf2::bkgpdf_dimuon_Moriond2017_BE(mass_dimuon_Moriond2017_BE, bkg_a_dimuon_Moriond2017_BE_forUse, bkg_b_dimuon_Moriond2017_BE_forUse, bkg_c_dimuon_Moriond2017_BE_forUse,bkg_d_dimuon_Moriond2017_BE_forUse,bkg_e_dimuon_Moriond2017_BE_forUse, bkg_a2_dimuon_Moriond2017_BE_forUse, bkg_b2_dimuon_Moriond2017_BE_forUse, bkg_c2_dimuon_Moriond2017_BE_forUse,bkg_e2_dimuon_Moriond2017_BE_forUse,bkg_syst_a,bkg_syst_b)")		
		ws.factory("ZPrimeMuonBkgPdf2::bkgpdf_fullRange(massFullRange, bkg_a_dimuon_Moriond2017_BE_forUse, bkg_b_dimuon_Moriond2017_BE_forUse, bkg_c_dimuon_Moriond2017_BE_forUse,bkg_d_dimuon_Moriond2017_BE_forUse,bkg_e_dimuon_Moriond2017_BE_forUse,bkg_a2_dimuon_Moriond2017_BE_forUse, bkg_b2_dimuon_Moriond2017_BE_forUse, bkg_c2_dimuon_Moriond2017_BE_forUse,bkg_e2_dimuon_Moriond2017_BE_forUse,bkg_syst_a,bkg_syst_b)")	
	else:
		ws.factory("ZPrimeMuonBkgPdf2::bkgpdf_dimuon_Moriond2017_BE(mass_dimuon_Moriond2017_BE, bkg_a_dimuon_Moriond2017_BE, bkg_b_dimuon_Moriond2017_BE, bkg_c_dimuon_Moriond2017_BE,bkg_d_dimuon_Moriond2017_BE,bkg_e_dimuon_Moriond2017_BE, bkg_a2_dimuon_Moriond2017_BE, bkg_b2_dimuon_Moriond2017_BE, bkg_c2_dimuon_Moriond2017_BE,bkg_e2_dimuon_Moriond2017_BE,bkg_syst_a,bkg_syst_b)")		
		ws.factory("ZPrimeMuonBkgPdf2::bkgpdf_fullRange(massFullRange, bkg_a_dimuon_Moriond2017_BE, bkg_b_dimuon_Moriond2017_BE, bkg_c_dimuon_Moriond2017_BE,bkg_d_dimuon_Moriond2017_BE,bkg_e_dimuon_Moriond2017_BE,bkg_a2_dimuon_Moriond2017_BE, bkg_b2_dimuon_Moriond2017_BE, bkg_c2_dimuon_Moriond2017_BE,bkg_e2_dimuon_Moriond2017_BE,bkg_syst_a,bkg_syst_b)")	

	return ws
