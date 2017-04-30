leptons = "mumu"
systematics = ["sigEff","bkgUncert","massScale"]
correlate = False
masses = [[5,400,1000], [10,1000,2000], [20,2000,4500]]
massesExp = [[100,400,600,100,10,500000], [100,600,1000,50,20,500000], [250,1000,2000,50,20,50000], [250,2000,4600,20,50,500000]]



libraries = ["ZPrimeMuonBkgPdf_cxx.so","PowFunc_cxx.so"]

channels = ["dimuon_BB","dimuon_BEpos","dimuon_BEneg"]
numInt = 500000
numToys = 10
exptToys = 10
width = 0.02
submitTo = "Purdue"

binWidth = 10
CB = False
signalInjection = {"mass":2000,"width":0.006,"nEvents":10,"CB":True}
		
