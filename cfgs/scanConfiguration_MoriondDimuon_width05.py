leptons = "mumu"
systematics = ["sigEff","bkgUncert","massScale","res","bkgParams"]
correlate = False
masses = [[5,200,1000], [10,1000,2000], [20,2000,5500]]
massesExp = [[100,200,600,1000,1,500000], [100,600,1000,500,2,500000], [250,1000,2000,100,10,50000], [250,2000,5600,100,10,500000]]



libraries = ["ZPrimeMuonBkgPdf2_cxx.so","PowFunc_cxx.so",'RooCruijff_cxx.so']
channels = ["dimuon_Moriond2017_BB","dimuon_Moriond2017_BE"]
numInt = 500000
numToys = 10
exptToys = 10
width = 0.05
submitTo = "Purdue"

binWidth = 10
CB = False
signalInjection = {"mass":2000,"width":0.006,"nEvents":10,"CB":True}
		
