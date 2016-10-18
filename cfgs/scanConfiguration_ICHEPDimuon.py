
leptons = "mumu"
systematics = ["sigEff","bkgUncert","massScale"]
correlate = False
#systematics = ["massScale"]
masses = [[5,400,1000], [10,1000,2000], [20,2000,4500]]
cardDir = "dataCards_ICHEPDimuon"

libraries = ["ZPrimeMuonBkgPdf_cxx.so","Pol2_cxx.so"]

#channels = ["dimuon_BB","dimuon_BEpos","dimuon_BEneg"]
channels = ["dimuon_BB","dimuon_BEpos","dimuon_BEneg"]
numInt = 500000
numToys = 10
exptToys = 100
width = 0.006
submitTo = "Purdue"

binWidth = 1

signalInjection = {"mass":2000,"width":0.006,"nEvents":10}
		
