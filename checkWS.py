import ROOT

def main():



	ROOT.gSystem.Load("shapes/ZPrimeMuonBkgPdf_cxx.so")
	f = ROOT.TFile("shapesCard.root")

	ws = f.Get("w")

	ws.Print()


main()
