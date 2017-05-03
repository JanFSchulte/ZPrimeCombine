
leptons = "mumu"
systematics = ["sigEff","bkgUncert","massScale"]
correlate = False
#systematics = ["massScale","sigEff"]
masses = [[5,400,1000], [10,1000,2000], [20,2000,4500]]
massesExp = [[100,450,955,100,10,500000], [50,1050,1250,100,10,500000],[250,1375,3376,100,10,50000]]
#massesExp = [[100,400,600,100,10,500000], [100,600,1000,50,20,500000], [250,1000,2000,50,20,50000], [250,2000,4600,20,50,500000]]
libraries = ["ZPrimeBkgPdf_cxx.so","ZPrimeMuonBkgPdf_cxx.so","PowFunc_cxx.so"]

#channels = ["dimuon_BB","dimuon_BEpos","dimuon_BEneg"]
channels = ["dimuon_BB","dimuon_BEpos","dimuon_BEneg","dielectron_EBEB","dielectron_EBEE"]
numInt = 500000
numToys = 10
exptToys = 500
width = 0.0325
submitTo = "Purdue"

binWidth = 10
CB = False
signalInjection = {"mass":2000,"width":0.006,"nEvents":10,"CB":True}
		
