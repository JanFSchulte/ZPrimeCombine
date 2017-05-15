
leptons = "elel"
systematics = ["sigEff","bkgUncert","massScale"]
correlate = False
masses = [[5,400,1000], [10,1000,2000], [20,2000,4500]]
massesExp = [[50,400,1255,100,10,500000],[125,1375,4600,100,10,50000]]

libraries = ["ZPrimeBkgPdf_cxx.so","PowFunc_cxx.so"]

#channels = ["dimuon_BB","dimuon_BEpos","dimuon_BEneg"]
channels = ["dielectron_EBEB","dielectron_EBEE"]
numInt = 500000
numToys = 10
exptToys = 500
width = 0.02
submitTo = "Purdue"

binWidth = 10
CB = False
signalInjection = {"mass":750,"width":0.1000,"nEvents":100,"CB":True}
		
