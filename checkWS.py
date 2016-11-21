import ROOT

def main():

	import glob
	for f in glob.glob("userfuncs/*.so"):
		ROOT.gSystem.Load(f)
	

	#ROOT.gSystem.Load("shapes/ZPrimeMuonBkgPdf_cxx.so")
	f = ROOT.TFile("dataCards_ICHEPDimuon_toy100/dimuon_BB_4000.root")

	ws = f.Get("dimuon_BB")
	ws.Print()
	frame = ws.var('mass_dimuon_BB').frame(ROOT.RooFit.Title(''),ROOT.RooFit.Range(400,4500))
	
	c1 = ROOT.TCanvas("c1","c1",800,600)
	#pad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	#pad.cd()
	#pad.Draw()
	ws.data("data_dimuon_BB").plotOn(frame,ROOT.RooFit.Range(500,4500))

	#frame.SetMaximum(20)
	ws.pdf('bkgpdf_dimuon_BB').plotOn(frame,
								 ROOT.RooFit.Range(400,4500),
								  #~ ROOT.RooFit.VisualizeError(fitOFOS, 1),
								  #~ ROOT.RooFit.FillColor(ROOT.kGreen + 2),
								  #~ ROOT.RooFit.FillStyle(3009),
								  ROOT.RooFit.LineWidth(2))	

	ws.pdf('sig_pdf_dimuon_BB').plotOn(frame,
								  ROOT.RooFit.Range(400,4500),
								  #~ ROOT.RooFit.VisualizeError(fitOFOS, 1),
								  ROOT.RooFit.LineColor(ROOT.kGreen + 2),
								  #~ ROOT.RooFit.FillStyle(3009),
								  ROOT.RooFit.LineWidth(2))	
	
	ws.Print()
	#pad.DrawFrame(800,0,3200,20,";M [GeV]; Events")
	frame.Draw()
	c1.Print("bkgToy_mass_BB_100.pdf")
main()
