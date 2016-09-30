import ROOT,sys
ROOT.gROOT.SetBatch(True)

from ROOT import *



def main():

	#ROOT.gSystem.Load("shapes/ZPrimeMuonBkgPdf_cxx.so")
#	ROOT.gSystem.AddIncludePath("-Ishapes")
	import glob
	for f in glob.glob("shapes/*.cxx"):
		gROOT.ProcessLine(".L "+f+"+")
	

	ws = RooWorkspace("dimuon_13TeV")

	mass = RooRealVar('mass','mass',1000.0, 200.0, 5000.)
	getattr(ws,'import')(mass,ROOT.RooCmdArg())
	
	peak = RooRealVar("peak","peak",2000.0, 200.0, 5000.)
	peak.setConstant()
	getattr(ws,'import')(peak,ROOT.RooCmdArg())
	
	ws.factory('Gaussian:sig_pdf_dimuon(mass,peak,0.1*peak)')	

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
	print " - loading Background shape"
	ws.factory("ZPrimeMuonBkgPdf::bkgpdf_dimuon(mass, bkg_a, bkg_b, bkg_c,bkg_d,bkg_e,bkg_syst_a,bkg_syst_b)")		


	ds = RooDataSet.read("data.txt",RooArgList(mass))
	ds.SetName('data_dimuon')
	ds.SetTitle('data_dimuon')
	print "    Data loaded with %d entries" %(ds.numEntries())
	getattr(ws,'import')(ds,ROOT.RooCmdArg())

#	ws.addClassDeclImportDir("shapes/")	
	ws.importClassCode("ZPrimeMuonBkgPdf")	

	ws.Print()

	ws.writeToFile("ws.root",True)

main()
