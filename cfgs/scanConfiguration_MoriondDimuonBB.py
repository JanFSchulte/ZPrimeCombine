leptons = "mumu"
systematics = ["bkgUncert",'res']
#systematics = ["sigEff","bkgUncert","massScale"]
correlate = False
masses = [[5,200,1000], [10,1000,2000], [20,2000,4500]]
#masses = [[5,200,1000], [10,1000,2000], [20,2000,4500]]
massesExp = [[100,200,600,250,4,500000], [100,600,1000,250,4,500000], [250,1000,2000,100,10,50000], [250,2000,4600,100,10,500000]]



libraries = ["ZPrimeMuonBkgPdf2_cxx.so","PowFunc_cxx.so",'RooCruijff_cxx.so']

channels = ["dimuon_Moriond2017_BB"]
numInt = 500000
numToys = 6
exptToys = 10
width = 0.006
submitTo = "Purdue"

binWidth = 10
CB = True
signalInjection = {"mass":2000,"width":0.006,"nEvents":10,"CB":True}
		
