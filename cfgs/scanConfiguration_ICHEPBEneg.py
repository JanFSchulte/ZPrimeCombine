
leptons = "mumu"
systematics = ["sigEff","bkgUncert","massScale"]
correlate = False
#systematics = ["massScale"]
masses = [[5,400,1000], [10,1000,2000], [20,2000,4500]]

libraries = ["ZPrimeMuonBkgPdf_cxx.so","PowFunc_cxx.so"]

channels = ["dimuon_BEneg"]
numInt = 500000
numToys = 10
exptToys = 100
width = 0.006

binWidth = 1
CB=False
submitTo = "Purdue"
		
