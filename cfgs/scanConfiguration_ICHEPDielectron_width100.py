
leptons = "elel"
systematics = ["sigEff","bkgUncert","massScale"]
correlate = False
#systematics = ["massScale","sigEff"]
masses = [[5,400,1000], [10,1000,2000], [20,2000,4500]]
#massesExp = [[100,400,600,200,5,500000], [100,600,1000,200,5,500000], [250,1000,2000,50,20,50000], [250,2000,4600,50,20,500000]]
#massesExp = [[100,450,955,100,10,500000], [50,1050,1250,100,10,500000],[250,1375,3376,100,10,50000]]
massesExp = [[50,400,1255,100,10,500000],[125,1375,4600,100,10,50000]]

libraries = ["ZPrimeBkgPdf_cxx.so","PowFunc_cxx.so"]

#channels = ["dimuon_BB","dimuon_BEpos","dimuon_BEneg"]
channels = ["dielectron_EBEB","dielectron_EBEE"]
numInt = 500000
numToys = 10
exptToys = 500
width = 0.01
submitTo = "Purdue"

binWidth = 10
CB = False
signalInjection = {"mass":750,"width":0.1000,"nEvents":100,"CB":True}
		
