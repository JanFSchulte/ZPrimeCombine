import ROOT,sys
ROOT.gROOT.SetBatch(True)

from ROOT import *

nBkg = 1



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

	return [0.96,1.01]



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
		gROOT.ProcessLine(".L "+f+"+")
	
	
	with open("input/dimuon_13TeV_2016_ICHEPDataset_BB.txt") as f:
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

	ws = RooWorkspace("dimuon_BB")
	
	mass = RooRealVar('mass','mass',massVal, massLow, massHigh )
	getattr(ws,'import')(mass,ROOT.RooCmdArg())
	
	peak = RooRealVar("peak","peak",massVal, massLow, massHigh)
	peak.setConstant()
	getattr(ws,'import')(peak,ROOT.RooCmdArg())
	
	### configure resolution	

        res_p0 = RooRealVar('res_p0','res_p0',1.9E-02)
        res_p1 = RooRealVar('res_p1','res_p1',2.4E-05)
        res_p2 = RooRealVar('res_p2','res_p2',-2.4E-09)

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

	ws.factory("Voigtian::sig_pdf_dimuon_BB(mass, peak, width, sigma)")


	bkg_a = RooRealVar('bkg_a','bkg_a',28.51)
	bkg_b = RooRealVar('bkg_b','bkg_b',-3.614E-4)
	bkg_c = RooRealVar('bkg_c','bkg_c',-1.470E-7)
	bkg_d = RooRealVar('bkg_d','bkg_d',6.885E-12)
	bkg_e = RooRealVar('bkg_e','bkg_e',-4.196)
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
	ws.factory("ZPrimeMuonBkgPdf::bkgpdf_dimuon_BB(mass, bkg_a, bkg_b, bkg_c,bkg_d,bkg_e,bkg_syst_a,bkg_syst_b)")		

	ds = RooDataSet.read("input/dimuon_13TeV_2016_ICHEPDataset_BB.txt",RooArgList(mass))
	ds.SetName('data_dimuon_BB')
	ds.SetTitle('data_dimuon_BB')
	getattr(ws,'import')(ds,ROOT.RooCmdArg())

#	ws.addClassDeclImportDir("shapes/")	
	ws.importClassCode()	


	ws.writeToFile("%s.root"%name,True)

	
	return ws.data("data_dimuon_BB").sumEntries()
