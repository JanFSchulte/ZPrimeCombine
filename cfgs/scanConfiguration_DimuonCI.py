leptons = "mumu"
systematics = ["lumi",'res','massScale',"zPeak","trig","jets","xSecOther","pdf","ID","stats"]
backgrounds = ['DY','Other','Jets']

correlate = False

lambdas = [10,16,22,28,34]
#interferences = ["ConLL","ConLR","ConRR","DesLL","DesLR","DesRR"]
interferences = ["ConLL","ConLR","ConRR"]

binning = [400,500,700,1100,1900,3500,5000]

libraries = ["ZPrimeMuonBkgPdf2_cxx.so","PowFunc_cxx.so"]

channels = ["dimuon_BB","dimuon_BE"]
numInt = 100000
numToys = 6
exptToys = 500
submitTo = "Purdue"

		
