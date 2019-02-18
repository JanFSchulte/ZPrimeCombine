
leptons = "elel"
correlate = True
systematics = ["lumi",'res','massScale',"zPeak","trig","jets","xSecOther","pdf","ID","stats","PU"]
backgrounds = ['DY','Other','Jets']



lambdas = [10,16,22,28,34,40]
interferences = ["ConLL","ConLR","ConRR","DesLL","DesLR","DesRR"]



binning = [400,500,700,1100,1900,3500,5000]
libraries = ["ZPrimeBkgPdf_cxx.so","PowFunc_cxx.so","RooCruijff_cxx.so"]

#channels = ["dimuon_BB","dimuon_BEpos","dimuon_BEneg"]
channels = ["dielectron_Moriond2017_BB","dielectron_Moriond2017_BE"]
numInt = 500000
numToys = 10
exptToys = 500
width = 0.006
submitTo = "Purdue"

binWidth = 10
CB = True
signalInjection = {"mass":750,"width":0.1000,"nEvents":100,"CB":True}
		
