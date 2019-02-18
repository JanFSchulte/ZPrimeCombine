import ROOT,sys
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = 1 
from ROOT import *
from muonResolution import getResolution as getRes
nBkg = -1

dataFile = "input/dimuon_Mordion2017_BB.txt"
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
	nz   =  53134                      #From Alexander (80X Moriond ReReco)
	nsig_scale = 1376.0208367514358       # prescale/eff_z (167.73694/0.1219) -->derives the lumi 
	eff = signalEff(mass,spin2)
	result = (nsig_scale*nz*eff)

	return result
	

def signalEff(mass,spin2=False):


	if spin2:
		eff_a = 1.020382
		eff_b = -1166.881533
		eff_c = 1468.989496
		eff_d = 0.000044
	 	return eff_a + eff_b / (mass + eff_c) - mass*eff_d
	else:
#### default	
		if mass <= 600:
			a = 2.129
			b = 0.1268
			c = 119.2
			d = 22.35
			e = -2.386
			f = -0.03619
			from math import exp
			return a - b * exp( -(mass - c) / d ) + e * mass**f
		else:

			eff_a     =   2.891
			eff_b     =  -2.291e+04
			eff_c     =  8294.
			eff_d     =  0.0001247

			return	eff_a + eff_b / (mass + eff_c) - mass*eff_d
		

def signalEffUncert(mass):


	if mass <= 600:
		a = 2.129
		b = 0.1268
		c = 119.2
		d = 22.38
		e = -2.386
		f = -0.03623
		from math import exp
		eff_default =  a - b * exp( -(mass - c) / d ) + e * mass**f
	else:
		eff_a     =   2.891
		eff_b     =  -2.291e+04
		eff_c     =  8294.
		eff_d     =  0.0001247


		eff_default = eff_a + eff_b / (mass + eff_c) - mass*eff_d
	if mass <= 600:
		a = 2.13
		b = 0.1269
		c = 119.2
		d = 22.42
		e = -2.384
		f = -0.03596
		from math import exp
		eff_syst =  a - b * exp( -(mass - c) / d ) + e * mass**f
	else:

		eff_a     =  2.849
		eff_b     = -2.221e+04
		eff_c     =  8166.
		eff_d     =  0.0001258
		eff_syst = eff_a + eff_b / (mass + eff_c) - mass*eff_d


	effDown = eff_default/eff_syst
	
	return [1./effDown,1.0]



def provideUncertainties(mass):

	result = {}

	result["sigEff"] = signalEffUncert(mass)
	result["massScale"] = 0.01
	result["bkgUncert"] = 1.4
	result["res"] = 0.15
	result["bkgParams"] = {"bkg_a":0.0008870490833826137,"bkg_b":0.0735080058224163,"bkg_c":0.020865265760197774,"bkg_d":0.13546622914957615,"bkg_e":0.0011148272017837235, "bkg_a2":0.0028587764436821044,"bkg_b2":0.008506113769271665,"bkg_c2":0.019418985270049097,"bkg_e2":0.0015616866215512754}
	return result

def provideUncertaintiesCI(mass):

	result = {}

	result["trig"] = 1.003
	result["zPeak"] = 1.05
	result["xSecOther"] = 1.07
	result["jets"] = 1.5
	result["lumi"] = 1.025
	result["stats"] = 0.0 ##dummy values
	result["massScale"] = 0.0 ##dummy values
	result["res"] = 0.0 ## dummy values
	result["pdf"] = 0.0 ## dummy values
	result["ID"] = 0.0 ## dummy values
	result["PU"] = 0.0 ## dummy values

	return result



def getResolution(mass):
	result = {}
	params = getRes(mass)
	result['alphaL'] = params['alphaL']['BB']
	result['alphaR'] = params['alphaR']['BB']
	result['res'] = params['sigma']['BB']
	result['scale'] = params['scale']['BB']

	return result




def loadBackgroundShape(ws,useShapeUncert=False):

	bkg_a = RooRealVar('bkg_a_dimuon_Moriond2017_BB','bkg_a_dimuon_Moriond2017_BB', 33.82)
	bkg_b = RooRealVar('bkg_b_dimuon_Moriond2017_BB','bkg_b_dimuon_Moriond2017_BB',-0.0001374)
	bkg_c = RooRealVar('bkg_c_dimuon_Moriond2017_BB','bkg_c_dimuon_Moriond2017_BB',-1.618e-07)
	bkg_d = RooRealVar('bkg_d_dimuon_Moriond2017_BB','bkg_d_dimuon_Moriond2017_BB', 3.657E-12)
	bkg_e = RooRealVar('bkg_e_dimuon_Moriond2017_BB','bkg_e_dimuon_Moriond2017_BB',-4.485)
	bkg_a2 = RooRealVar('bkg_a2_dimuon_Moriond2017_BB','bkg_a2_dimuon_Moriond2017_BB', 17.49)
	bkg_b2 = RooRealVar('bkg_b2_dimuon_Moriond2017_BB','bkg_b2_dimuon_Moriond2017_BB',-0.01881)
	bkg_c2 = RooRealVar('bkg_c2_dimuon_Moriond2017_BB','bkg_c2_dimuon_Moriond2017_BB', 1.222e-05)
	bkg_e2 = RooRealVar('bkg_e2_dimuon_Moriond2017_BB','bkg_e2_dimuon_Moriond2017_BB',-0.8486)
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
	bkg_syst_b = RooRealVar('bkg_syst_b','bkg_syst_b',0.0)
	#bkg_syst_b = RooRealVar('bkg_syst_b','bkg_syst_b',-0.00016666666666)
	bkg_syst_a.setConstant()
	bkg_syst_b.setConstant()
	getattr(ws,'import')(bkg_syst_a,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_syst_b,ROOT.RooCmdArg())

	# background shape
	if useShapeUncert:
		bkgParamsUncert = provideUncertainties(1000)["bkgParams"]
		for uncert in bkgParamsUncert:
			addBkgUncertPrior(ws,uncert,"dimuon_Moriond2017_BB",bkgParamsUncert[uncert] )

		ws.factory("ZPrimeMuonBkgPdf2::bkgpdf_dimuon_Moriond2017_BB(mass_dimuon_Moriond2017_BB, bkg_a_dimuon_Moriond2017_BB_forUse, bkg_b_dimuon_Moriond2017_BB_forUse, bkg_c_dimuon_Moriond2017_BB_forUse,bkg_d_dimuon_Moriond2017_BB_forUse,bkg_e_dimuon_Moriond2017_BB_forUse,bkg_a2_dimuon_Moriond2017_BB_forUse, bkg_b2_dimuon_Moriond2017_BB_forUse, bkg_c2_dimuon_Moriond2017_BB_forUse,bkg_e2_dimuon_Moriond2017_BB_forUse,bkg_syst_a,bkg_syst_b)")		
		ws.factory("ZPrimeMuonBkgPdf2::bkgpdf_fullRange(massFullRange, bkg_a_dimuon_Moriond2017_BB_forUse, bkg_b_dimuon_Moriond2017_BB_forUse, bkg_c_dimuon_Moriond2017_BB_forUse,bkg_d_dimuon_Moriond2017_BB_forUse,bkg_e_dimuon_Moriond2017_BB_forUse, bkg_a2_dimuon_Moriond2017_BB_forUse, bkg_b2_dimuon_Moriond2017_BB_forUse, bkg_c2_dimuon_Moriond2017_BB_forUse,bkg_e2_dimuon_Moriond2017_BB,bkg_syst_a,bkg_syst_b)")		

	else:
		ws.factory("ZPrimeMuonBkgPdf2::bkgpdf_dimuon_Moriond2017_BB(mass_dimuon_Moriond2017_BB, bkg_a_dimuon_Moriond2017_BB, bkg_b_dimuon_Moriond2017_BB, bkg_c_dimuon_Moriond2017_BB,bkg_d_dimuon_Moriond2017_BB,bkg_e_dimuon_Moriond2017_BB,bkg_a2_dimuon_Moriond2017_BB, bkg_b2_dimuon_Moriond2017_BB, bkg_c2_dimuon_Moriond2017_BB,bkg_e2_dimuon_Moriond2017_BB,bkg_syst_a,bkg_syst_b)")		
		ws.factory("ZPrimeMuonBkgPdf2::bkgpdf_fullRange(massFullRange, bkg_a_dimuon_Moriond2017_BB, bkg_b_dimuon_Moriond2017_BB, bkg_c_dimuon_Moriond2017_BB,bkg_d_dimuon_Moriond2017_BB,bkg_e_dimuon_Moriond2017_BB, bkg_a2_dimuon_Moriond2017_BB, bkg_b2_dimuon_Moriond2017_BB, bkg_c2_dimuon_Moriond2017_BB,bkg_e2_dimuon_Moriond2017_BB,bkg_syst_a,bkg_syst_b)")		
	return ws
