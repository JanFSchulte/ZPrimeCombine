leptons = "elmu"
systematics = ["lumi",'res','massScale',"zPeak","trig","jets","xSecOther","pdf","ID","stats","PU"]
#systematics = []
backgrounds = ['DY','Other','Jets']

correlate = True

lambdas = [10,16,22,28,34,40]
interferences = ["ConLL","ConLR","ConRR","DesLL","DesLR","DesRR"]
#interferences = ["ConLL","ConLR","ConRR"]

binning = [400,500,700,1100,1900,3500,5000]

libraries = ["ZPrimeMuonBkgPdf2_cxx.so","PowFunc_cxx.so"]

channels = ["dielectron_Moriond2017_BB","dielectron_Moriond2017_BE","dimuon_Moriond2017_BB","dimuon_Moriond2017_BE"]
numInt = 1000000
numToys = 6
exptToys = 500
submitTo = "Purdue"
LPCUsername = "jschulte"
		
