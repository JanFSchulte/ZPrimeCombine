leptons = "mumu"
systematics = ["lumi",'res','massScale',"zPeak","trig","jets","xSecOther","pdf","ID","stats","PU"]
backgrounds = ['DY','Other','Jets']

correlate = True

lambdas = [10,16,22,28,34,40]
#interferences = ["DesRR"]
interferences = ["ConLL","ConLR","ConRR","DesLL","DesLR","DesRR"]

binning = [400,500,700,1100,1900,3500,5000]

libraries = ["ZPrimeMuonBkgPdf2_cxx.so","PowFunc_cxx.so"]

channels = ["dimuon_Moriond2017_BB","dimuon_Moriond2017_BE"]
numInt = 100000
numToys = 6
exptToys = 250
submitTo = "Purdue"

		
