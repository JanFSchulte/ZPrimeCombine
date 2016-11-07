import ROOT

def main():

	import glob
	for f in glob.glob("userfuncs/*.so"):
		ROOT.gSystem.Load(f)
	

	#ROOT.gSystem.Load("shapes/ZPrimeMuonBkgPdf_cxx.so")
	f = ROOT.TFile("dataCards_ICHEPDimuon_2000_0.0060_10/dimuon_BB_400.root")

	ws = f.Get("dimuon_BB")
	ws.Print()
	frame = ws.var('massFullRange').frame(ROOT.RooFit.Title(''))

	c1 = ROOT.TCanvas("c1","c1",800,600)	

	ws.data("data_dimuon_BB").plotOn(frame)

	ws.pdf('bkgpdf_dimuon_:BB').plotOn(frame,
								  #~ ROOT.RooFit.VisualizeError(fitOFOS, 1),
								  #~ ROOT.RooFit.FillColor(ROOT.kGreen + 2),
								  #~ ROOT.RooFit.FillStyle(3009),
								  ROOT.RooFit.LineWidth(2))	

	ws.pdf('sig_pdf_dimuon_BB').plotOn(frame,
								  #~ ROOT.RooFit.VisualizeError(fitOFOS, 1),
								  ROOT.RooFit.FillColor(ROOT.kGreen + 2),
								  #~ ROOT.RooFit.FillStyle(3009),
								  ROOT.RooFit.LineWidth(2))	

	ws.Print()
	frame.Draw()
	c1.Print("test.pdf")
main()
