leptons = "elmu"
systematics = ["lumi",'res','massScale',"zPeak","trig","jets","xSecOther","pdf","ID","stats","PU"]
#systematics = []
backgrounds = ['DY','Other','Jets']

correlate = True

lambdas = [10,16,22,28,34,40,46]
interferences = ["ConLL","ConLR","ConRR","DesLL","DesLR","DesRR"]
#interferences = ["ConLL","ConLR","ConRR"]

binning = [400,500,700,1100,1900,3500,10000]

libraries = ["ZPrimeMuonBkgPdf2_cxx.so","PowFunc_cxx.so"]

channels = ["dielectron_2016_BB","dielectron_2016_BE","dimuon_2016_BB","dimuon_2016_BE","dielectron_2017_BB","dielectron_2017_BE","dimuon_2017_BB","dimuon_2017_BE","dielectron_2018_BB","dielectron_2018_BE","dimuon_2018_BB","dimuon_2018_BE"]
numInt = 100000
numToys = 6
exptToys = 500
submitTo = "Purdue"
LPCUsername = "jschulte"
		
