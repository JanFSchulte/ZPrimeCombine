import ROOT,sys
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = 1 
from ROOT import *
from math import sqrt
from plot_crujiff import getResolution as getRes
#nBkg = -1
nBkg = -1 
#### to be updated!
dataFile = "input/dielectron_13TeV_2016_EBEB.txt"

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
	nz   =  5730975 
	nsig_scale = 11.17318 # 1./0.895 signal efficiency at z peak       
	eff = signalEff(mass,spin2)
	result = (nsig_scale*nz*eff)

	return result

def signalEff(mass,spin2=False):

	eff_a     = 0.6484
	eff_b     = -500.3
	eff_c     = 362.3 
	eff_d     = 6.863e04
	eff_e	  = 1.209e05
	if spin2:
		eff_a = 0.5043
		eff_b = 1173.
		eff_c = 1.1e04
		eff_d = -1.716e05
		eff_e = 6.212e05
	
	return (eff_a+eff_b/(mass+eff_c)+eff_d/(mass*mass+eff_e))
	


	

def provideUncertainties(mass):

	result = {}

	result["sigEff"] = [1.06]
	result["massScale"] = 0.02
	result ["bkgUncert"] = 1.4
	result ["res"] = 0.0

 	result["bkgParams"] = {"bkg_a":0.19973471017800093,"bkg_b":0.13034553014819417,"bkg_c":0.,"bkg_d":0.3025558475689882,"bkg_e":0.013621123981721175,"bkg_a2":0.24501686064901437,"bkg_b2":0.06311748743032082,"bkg_c2":0.0,"bkg_d2":0.13369398559319584,"bkg_e2":0.01877138240091732}	
 	#result["bkgParams"] = {"bkg_a":0.24391455519910865,"bkg_b":0.03963999446145325,"bkg_c":44.56738363916309,"bkg_d":0.35495154369249793,"bkg_e":0.001701404156849987,"bkg_a2":0.1575451905377131,"bkg_b2":0.04733064954639549,"bkg_c2":0.93272729080101,"bkg_d2":0.6290363984210399,"bkg_e2":0.0024446111862020054}	
	return result


def getResolution(mass):

	result = {}
	params = getRes(mass)
	if mass > 2300:
		result['alpha'] = params['alpha']['BB']
		result['n'] = params['n']['BB']
		result['res'] = params['sigma']['BB']/100.
		result['scale'] = params['scale']['BB']

	else:
		result['alphaL'] = params['alphaL']['BB']
		result['alphaR'] = params['alphaR']['BB']
		result['res'] = params['sigma']['BB']
		result['scale'] = params['scale']['BB']

	return result



def loadBackgroundShape(ws,useShapeUncert):
#	bkg_a = RooRealVar('bkg_a_dielectron_Moriond2017_EBEB','bkg_a_dielectron_Moriond2017_EBEB',2.60285e+01)
#	bkg_b = RooRealVar('bkg_b_dielectron_Moriond2017_EBEB','bkg_b_dielectron_Moriond2017_EBEB',-1.29998e-03)
#	bkg_c = RooRealVar('bkg_c_dielectron_Moriond2017_EBEB','bkg_b_dielectron_Moriond2017_EBEB',1.50029e-09)
#	bkg_d = RooRealVar('bkg_d_dielectron_Moriond2017_EBEB','bkg_c_dielectron_Moriond2017_EBEB',-2.19992e-11)
#	bkg_e = RooRealVar('bkg_e_dielectron_Moriond2017_EBEB','bkg_d_dielectron_Moriond2017_EBEB',-3.81154e+00)
#	bkg_a2 = RooRealVar('bkg_a2_dielectron_Moriond2017_EBEB','bkg_a2_dielectron_Moriond2017_EBEB', 3.49852e+01)
#	bkg_b2 = RooRealVar('bkg_b2_dielectron_Moriond2017_EBEB','bkg_b2_dielectron_Moriond2017_EBEB',-1.04827e-03)
#	bkg_c2 = RooRealVar('bkg_c2_dielectron_Moriond2017_EBEB','bkg_c2_dielectron_Moriond2017_EBEB',2.01196e-08)
#	bkg_d2 = RooRealVar('bkg_d2_dielectron_Moriond2017_EBEB','bkg_d2_dielectron_Moriond2017_EBEB',-1.23879e-11)
#	bkg_e2 = RooRealVar('bkg_e2_dielectron_Moriond2017_EBEB','bkg_e2_dielectron_Moriond2017_EBEB',-3.89158e+00)
	bkg_a = RooRealVar('bkg_a_dielectron_Moriond2017_EBEB','bkg_a_dielectron_Moriond2017_EBEB',2.80448e+00)
	bkg_b = RooRealVar('bkg_b_dielectron_Moriond2017_EBEB','bkg_b_dielectron_Moriond2017_EBEB',-1.56079e-03)
	bkg_c = RooRealVar('bkg_c_dielectron_Moriond2017_EBEB','bkg_b_dielectron_Moriond2017_EBEB',0)
	bkg_d = RooRealVar('bkg_d_dielectron_Moriond2017_EBEB','bkg_c_dielectron_Moriond2017_EBEB',-2.13080e-11)
	bkg_e = RooRealVar('bkg_e_dielectron_Moriond2017_EBEB','bkg_d_dielectron_Moriond2017_EBEB',-3.73547e+00)
	bkg_a2 = RooRealVar('bkg_a2_dielectron_Moriond2017_EBEB','bkg_a2_dielectron_Moriond2017_EBEB',3.73058e+00)
	bkg_b2 = RooRealVar('bkg_b2_dielectron_Moriond2017_EBEB','bkg_b2_dielectron_Moriond2017_EBEB',-9.66214e-04)
	bkg_c2 = RooRealVar('bkg_c2_dielectron_Moriond2017_EBEB','bkg_c2_dielectron_Moriond2017_EBEB',0.)
	bkg_d2 = RooRealVar('bkg_d2_dielectron_Moriond2017_EBEB','bkg_d2_dielectron_Moriond2017_EBEB',-1.03701e-11)
	bkg_e2 = RooRealVar('bkg_e2_dielectron_Moriond2017_EBEB','bkg_e2_dielectron_Moriond2017_EBEB',-3.94191e+00)
	

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
	bkg_syst_a = RooRealVar('bkg_syst_a_dielectron_Moriond2017_EBEB','bkg_syst_a_dielectron_Moriond2017_EBEB',1.0)
	bkg_syst_b = RooRealVar('bkg_syst_b_dielectron_Moriond2017_EBEB','bkg_syst_b_dielectron_Moriond2017_EBEB',0.000)
	#bkg_syst_b = RooRealVar('bkg_syst_b','bkg_syst_b',-0.000017)
	bkg_syst_a.setConstant()
	bkg_syst_b.setConstant()
	getattr(ws,'import')(bkg_syst_a,ROOT.RooCmdArg())
	getattr(ws,'import')(bkg_syst_b,ROOT.RooCmdArg())
	if useShapeUncert:
		bkgParamsUncert = provideUncertainties(1000)["bkgParams"]
		for uncert in bkgParamsUncert:
			addBkgUncertPrior(ws,uncert,"dielectron_Moriond2017_EBEB",bkgParamsUncert[uncert] )
		ws.factory("ZPrimeEleBkgPdf3::bkgpdf_dielectron_Moriond2017_EBEB(mass_dielectron_Moriond2017_EBEB, bkg_a_dielectron_Moriond2017_EBEB_forUse, bkg_b_dielectron_Moriond2017_EBEB_forUse, bkg_c_dielectron_Moriond2017_EBEB_forUse,bkg_d_dielectron_Moriond2017_EBEB_forUse,bkg_e_dielectron_Moriond2017_EBEB_forUse,bkg_a2_dielectron_Moriond2017_EBEB_forUse, bkg_b2_dielectron_Moriond2017_EBEB_forUse, bkg_c2_dielectron_Moriond2017_EBEB_forUse,bkg_d2_dielectron_Moriond2017_EBEB_forUse,bkg_e2_dielectron_Moriond2017_EBEB_forUse,bkg_syst_a_dielectron_Moriond2017_EBEB,bkg_syst_b_dielectron_Moriond2017_EBEB)")		
		ws.factory("ZPrimeEleBkgPdf3::bkgpdf_fullRange(massFullRange, bkg_a_dielectron_Moriond2017_EBEB_forUse, bkg_b_dielectron_Moriond2017_EBEB_forUse, bkg_c_dielectron_Moriond2017_EBEB_forUse,bkg_d_dielectron_Moriond2017_EBEB_forUse,bkg_e_dielectron_Moriond2017_EBEB_forUse,bkg_a2_dielectron_Moriond2017_EBEB_forUse, bkg_b2_dielectron_Moriond2017_EBEB_forUse, bkg_c2_dielectron_Moriond2017_EBEB_forUse,bkg_d2_dielectron_Moriond2017_EBEB_forUse,bkg_e2_dielectron_Moriond2017_EBEB_forUse,bkg_syst_a_dielectron_Moriond2017_EBEB,bkg_syst_b_dielectron_Moriond2017_EBEB)")		
	else:
	# background shape
		ws.factory("ZPrimeEleBkgPdf3::bkgpdf_dielectron_Moriond2017_EBEB(mass_dielectron_Moriond2017_EBEB, bkg_a_dielectron_Moriond2017_EBEB, bkg_b_dielectron_Moriond2017_EBEB, bkg_c_dielectron_Moriond2017_EBEB,bkg_d_dielectron_Moriond2017_EBEB,bkg_e_dielectron_Moriond2017_EBEB,bkg_a2_dielectron_Moriond2017_EBEB, bkg_b2_dielectron_Moriond2017_EBEB, bkg_c2_dielectron_Moriond2017_EBEB,bkg_d2_dielectron_Moriond2017_EBEB,bkg_e2_dielectron_Moriond2017_EBEB,bkg_syst_a_dielectron_Moriond2017_EBEB,bkg_syst_b_dielectron_Moriond2017_EBEB)")		
		ws.factory("ZPrimeEleBkgPdf3::bkgpdf_fullRange(massFullRange, bkg_a_dielectron_Moriond2017_EBEB, bkg_b_dielectron_Moriond2017_EBEB, bkg_c_dielectron_Moriond2017_EBEB,bkg_d_dielectron_Moriond2017_EBEB,bkg_e_dielectron_Moriond2017_EBEB,bkg_a2_dielectron_Moriond2017_EBEB, bkg_b2_dielectron_Moriond2017_EBEB, bkg_c2_dielectron_Moriond2017_EBEB,bkg_d2_dielectron_Moriond2017_EBEB,bkg_e2_dielectron_Moriond2017_EBEB,bkg_syst_a_dielectron_Moriond2017_EBEB,bkg_syst_b_dielectron_Moriond2017_EBEB)")		
	return ws
