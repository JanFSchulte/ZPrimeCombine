
leptons = "elmu"
systematics = ["sigEff","bkgUncert","massScale",'res',"bkgParams"]
#systematics = ["bkgUncert","massScale"]
correlate = False
#systematics = ["massScale","sigEff"]
masses = [[5,200,1000], [10,1000,2000], [20,2000,5500]]
#masses = [[5,5500,5505]]
massesExp = [[100,200,600,500,4,500000], [100,600,1000,250,8,500000], [250,1000,2000,100,20,50000], [250,2000,5600,100,20,500000]]
#massesExp = [[250,5250,5600,1,1,500000]]



libraries = ["ZPrimeMuonBkgPdf2_cxx.so","ZPrimeEleBkgPdf3_cxx.so","PowFunc_cxx.so","RooCruijff_cxx.so"]

#channels = ["dimuon_BB","dimuon_BEpos","dimuon_BEneg"]
channels = ["dielectron_Moriond2017_EBEB","dielectron_Moriond2017_EBEE","dimuon_Moriond2017_BB","dimuon_Moriond2017_BE"]
numInt = 500000
numToys = 6
exptToys = 1000
width = 0.006
#submitTo = "Purdue"
submitTo = "FNAL"
LPCUsername = "jschulte"

binWidth = 10
CB = True
signalInjection = {"mass":750,"width":0.1000,"nEvents":0,"CB":True,"scale":1}
		
