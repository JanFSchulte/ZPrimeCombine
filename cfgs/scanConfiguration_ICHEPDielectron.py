
leptons = "elel"
systematics = ["sigEff","bkgUncert","massScale"]
correlate = False
#systematics = ["massScale","sigEff"]
masses = [[5,400,1000], [10,1000,2000], [20,2000,4500]]

libraries = ["ZPrimeBkgPdf_cxx.so","PowFunc_cxx.so"]

#channels = ["dimuon_BB","dimuon_BEpos","dimuon_BEneg"]
channels = ["dielectron_EBEB","dielectron_EBEE"]
numInt = 500000
numToys = 10
exptToys = 500
width = 0.006
submitTo = "Purdue"

binWidth = 10
CB = False
signalInjection = {"mass":750,"width":0.1000,"nEvents":100,"CB":True}
		
