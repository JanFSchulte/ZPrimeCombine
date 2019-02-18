from ROOT import * 
from numpy import array as ar
from array import array
from copy import deepcopy
import pickle



def main():
	gROOT.SetBatch(True)

	
	histos = ["BB","BE"]
	labels = ["dimuon_2017","dielectron_2017"]
	suffixesMu = ["nominal","scaledown","smeared","muonid"]
	suffixesEle = ["nominal","scaledown","scaleup","pileup","piledown"]
	#~ suffixesMu = ["nominal"]
	#~ suffixesEle = ["nominal"]
	#~ suffixes = ["smeared"]
	lambdas = [10,16,22,28,34,40]
	models = ["ConLL","ConLR","ConRR","DesLL","DesLR","DesRR"]
	#~ lambdas = [10]
	#~ models = ["ConLL"]

	massBins = [400,500,700,1100,1900,3500]
	#~ massBins = [400]
	signalYields = {}
	
	
	for label in labels:
		if "dimuon" in label:
			suffixes = suffixesMu
		else:
			suffixes = suffixesEle
		for suffix in suffixes:
			for histo in histos:
					for model in models:			
						if "dimuon" in label:
							name = "cito2mu"
						else:
							name = "cito2e"	
						fitFile = TFile("%s_%s_%s_inc_parametrization.root"%(name,suffix,histo.lower()),"READ")
						for l in lambdas:
							if "dimuon" in label:
								name = "CITo2Mu_Lam%dTeV%s"%(l,model)
							else:	
								name = "CITo2E_Lam%dTeV%s"%(l,model)
							signalYields["%s_%s_%s"%(name,label,histo)] = {}
							for index, massBin in enumerate(massBins):
								function = fitFile.Get("fn_m%d_%s"%(massBin,model))
								fitR = fitFile.Get("fitR_m%d_%s"%(massBin,model))
								pars = fitR.GetParams()
								errs = fitR.Errors()
								function.SetParameter(0,pars[0])
								function.SetParameter(1,pars[1])
								function.SetParameter(2,pars[2])
								function.SetParError(0,errs[0])
								function.SetParError(1,errs[1])
								function.SetParError(2,errs[2])
								functionUnc = fitFile.Get("fn_unc_m%d_%s"%(massBin,model))
								uncert = ((functionUnc.Eval(l)/function.Eval(l))**2 + (functionUnc.Eval(100000)/function.Eval(100000)))**0.5								
								signalYields["%s_%s_%s"%(name,label,histo)][str(index)] = [(function.Eval(l)-function.Eval(100000)),uncert]


			


			#~ print signalYields
			if "dimuon" in label:
				fileName = "signalYields"
			else:
				fileName = "signalYieldsEle"
			
			if suffix == "nominal":
				otherSuffix = "default"
			elif suffix == "scaledown":
				otherSuffix = "scaleDown"
			elif suffix == "scaleup":
				otherSuffix = "scaleUp"
			elif suffix == "smeared":
				otherSuffix = "resolution"
			elif suffix == "muonid":
				otherSuffix = "ID"
			elif suffix == "pileup":
				otherSuffix = "pileup"
			elif suffix == "piledown":
				otherSuffix = "piledown"
			else:
				print suffix
			outFilePkl = open("%s_%s.pkl"%(fileName,otherSuffix),"w")
			pickle.dump(signalYields, outFilePkl)
			outFilePkl.close()		
	
	
			
							
main()
