
leptons = "mumu"
systematics = ["sigEff","bkgUncert","massScale"]
correlate = False
#systematics = ["massScale","sigEff"]
masses = [[5,400,1000], [10,1000,2000], [20,2000,4500]]

libraries = ["ZPrimeBkgPdf_cxx.so","ZPrimeMuonBkgPdf_cxx.so","PowFunc_cxx.so"]

#channels = ["dimuon_BB","dimuon_BEpos","dimuon_BEneg"]
channels = ["dimuon_BB","dimuon_BEpos","dimuon_BEneg","dielectron_EBEB","dielectron_EBEE"]
numInt = 500000
numToys = 10
exptToys = 500
width = 0.0275
submitTo = "Purdue"

binWidth = 10
CB = False
signalInjection = {"mass":2000,"width":0.006,"nEvents":10,"CB":True}
		
