
systematics = ["sigEff","bkgUncert","massScale"] # list of systematics to consider
correlate = False # correlate systematics betweeen channels? 

masses = [[5,400,1000], [10,1000,2000], [20,2000,4500]] #parameters of mass scan

libraries = ["ZPrimeMuonBkgPdf_cxx.so","PowFunc_cxx.so"]

channels = ["dimuon_BB","dimuon_BEpos","dimuon_BEneg"] # channels to combine
numInt = 500000 # Number of iterations for the Markov Chain
numToys = 10 # number of toys for MC
exptToys = 100 # number of toys for expected limit
width = 0.1 # intrincis width of the signal
submitTo = "Purdue" # which computing reaource to use

binWidth = 10 # bin width for binned approch
CB = True # use Crystal ball as signal shape
signalInjection = {"mass":500,"width":0.1,"nEvents":200,"CB":True} # parameters of signal injectetion 
		
