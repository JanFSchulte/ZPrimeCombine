import ROOT

def main():



	#ROOT.gSystem.Load("shapes/ZPrimeMuonBkgPdf_cxx.so")
	f = ROOT.TFile("dataCards_ICHEPDimuon/dimuon_BB_400.root")

	ws = f.Get("dimuon_BB")

	frame = ws.var('mass').frame(ROOT.RooFit.Title('bla'))

	c1 = ROOT.TCanvas("c1","c1",800,600)	

	ROOT.RooAbsData.plotOn(ws.data("data_dimuon_BB"), frame)

	ws.pdf('bkgpdf_dimuon_BB').plotOn(frame,
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
