import ROOT

def main():



	#ROOT.gSystem.Load("shapes/ZPrimeMuonBkgPdf_cxx.so")
	f = ROOT.TFile("p.root")

	ws = f.Get("hmumu")

	ws.Print()


main()
