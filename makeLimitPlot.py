#/usr/bin/env python
import os
import sys
sys.path.append('cfgs/')

import numpy
import math
import ROOT
from ROOT import TCanvas,TGraphAsymmErrors,TFile,TH1D,TH1F,TGraph,TGraphErrors,gStyle,TLegend,TLine,TGraphSmooth,TPaveText,TGraphAsymmErrors,TPaveLabel,gROOT

ROOT.gROOT.SetBatch(True)

def printPlots(canvas,name):
    	canvas.Print('plots/'+name+".png","png")
    	canvas.Print('plots/'+name+".pdf","pdf")
    	canvas.SaveSource('plots/'+name+".C","cxx")
    	canvas.Print('plots/'+name+".root","root")
    	canvas.Print('plots/'+name+".eps","eps")


def makeLimitPlot(output,obs,exp,chan,printStats=False,obs2="",ratioLabel=""):

    	fileObs=open(obs,'r')
   	fileExp=open(exp,'r')

    	observedx=[]
    	observedy=[]
    	obsLimits={}
    	for entry in fileObs:
        	massPoint=float(entry.split()[0])
        	limitEntry=float(entry.split()[1])
        	if massPoint not in obsLimits: obsLimits[massPoint]=[]
        	obsLimits[massPoint].append(limitEntry)
    	if printStats: print "len obsLimits:", len(obsLimits)
    	for massPoint in sorted(obsLimits):
        	observedx.append(massPoint)
        	observedy.append(numpy.mean(obsLimits[massPoint]))
        	if (numpy.std(obsLimits[massPoint])/numpy.mean(obsLimits[massPoint])>0.05):
            		print massPoint," mean: ",numpy.mean(obsLimits[massPoint])," std dev: ",numpy.std(obsLimits[massPoint])," from: ",obsLimits[massPoint]

    	if not obs2 == "":
		fileObs2=open(obs2,'r')

		observedx2=[]
   		observedy2=[]
    		obsLimits2={}
    		for entry in fileObs2:
        		massPoint=float(entry.split()[0])
        		limitEntry=float(entry.split()[1])
        		if massPoint not in obsLimits2: obsLimits2[massPoint]=[]
        		obsLimits2[massPoint].append(limitEntry)
    		if printStats: print "len obsLimits:", len(obsLimits2)
    		for massPoint in sorted(obsLimits2):
        		observedx2.append(massPoint)
        		observedy2.append(numpy.mean(obsLimits2[massPoint]))
        		if (numpy.std(obsLimits2[massPoint])/numpy.mean(obsLimits2[massPoint])>0.05):
            			print massPoint," mean: ",numpy.mean(obsLimits2[massPoint])," std dev: ",numpy.std(obsLimits2[massPoint])," from: ",obsLimits2[massPoint]





    	limits={}
    	expectedx=[]
    	expectedy=[]
    	expected1SigLow=[]
   	expected1SigHigh=[]
    	expected2SigLow=[]
    	expected2SigHigh=[]
    	for entry in fileExp:
        	massPoint=float(entry.split()[0])
        	limitEntry=float(entry.split()[1])
        	if massPoint not in limits: limits[massPoint]=[]
        	limits[massPoint].append(limitEntry)

    	if printStats: print "len limits:", len(limits)
    	for massPoint in sorted(limits):
        	limits[massPoint].sort()
        	numLimits=len(limits[massPoint])
        	nrExpts=len(limits[massPoint])
        	medianNr=int(nrExpts*0.5)
        	#get indexes:
        	upper1Sig=int(nrExpts*(1-(1-0.68)*0.5))
        	lower1Sig=int(nrExpts*(1-0.68)*0.5)
        	upper2Sig=int(nrExpts*(1-(1-0.95)*0.5))
        	lower2Sig=int(nrExpts*(1-0.95)*0.5)
        	if printStats: print massPoint,":",limits[massPoint][lower2Sig],limits[massPoint][lower1Sig],limits[massPoint][medianNr],limits[massPoint][upper1Sig],limits[massPoint][upper2Sig]
    		#fill lists:
        	expectedx.append(massPoint)
        	expectedy.append(limits[massPoint][medianNr])
        	expected1SigLow.append(limits[massPoint][lower1Sig])
        	expected1SigHigh.append(limits[massPoint][upper1Sig])
        	expected2SigLow.append(limits[massPoint][lower2Sig])
        	expected2SigHigh.append(limits[massPoint][upper2Sig])
        
    	expX=numpy.array(expectedx)
    	expY=numpy.array(expectedy)

    	values2=[]
    	xPointsForValues2=[]
    	values=[]
    	xPointsForValues=[]
    	if printStats: print "length of expectedx: ", len(expectedx)
    	if printStats: print "length of expected1SigLow: ", len(expected1SigLow)
    	if printStats: print "length of expected1SigHigh: ", len(expected1SigHigh)

	#Here is some Voodoo via Sam:
    	for x in range (0,len(expectedx)):
        	values2.append(expected2SigLow[x])
        	xPointsForValues2.append(expectedx[x])
    	for x in range (len(expectedx)-1,0-1,-1):
        	values2.append(expected2SigHigh[x])
        	xPointsForValues2.append(expectedx[x])
    	if printStats: print "length of values2: ", len(values2)

    	for x in range (0,len(expectedx)):
        	values.append(expected1SigLow[x])
        	xPointsForValues.append(expectedx[x])
    	for x in range (len(expectedx)-1,0-1,-1):
        	values.append(expected1SigHigh[x])
        	xPointsForValues.append(expectedx[x])
    	if printStats: print "length of values: ", len(values)

    	exp2Sig=numpy.array(values2)
    	xPoints2=numpy.array(xPointsForValues2)
    	exp1Sig=numpy.array(values)
    	xPoints=numpy.array(xPointsForValues)
    	if printStats: print "xPoints2: ",xPoints2
    	if printStats: print "exp2Sig: ",exp2Sig
    	if printStats: print "xPoints: ",xPoints
    	if printStats: print "exp1Sig: ",exp1Sig
    	GraphErr2Sig=TGraphAsymmErrors(len(xPoints),xPoints2,exp2Sig)
    	GraphErr2Sig.SetFillColor(ROOT.kYellow+1)
    	GraphErr1Sig=TGraphAsymmErrors(len(xPoints),xPoints,exp1Sig)
    	GraphErr1Sig.SetFillColor(ROOT.kGreen)

    	cCL=TCanvas("cCL", "cCL",0,0,800,500)
    	gStyle.SetOptStat(0)

	if not obs2 == "":
    		plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
    		ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
    		plotPad.Draw()	
    		ratioPad.Draw()	
    		plotPad.cd()
	else:
    		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
    		plotPad.Draw()	
    		plotPad.cd()


    

    	expX=numpy.array(expectedx)
    	expY=numpy.array(expectedy)
    	GraphExp=TGraph(len(expX),expX,expY)
    	GraphExp.SetLineWidth(3)
    	GraphExp.SetLineStyle(2)
    	GraphExp.SetLineColor(ROOT.kBlue)

    	obsX=numpy.array(observedx)
    	obsY=numpy.array(observedy)
    	if printStats: print "obsX: ",obsX
    	if printStats: print "obsY: ",obsY

    	if SMOOTH:
        	smooth_obs=TGraphSmooth("normal")
        	GraphObs_nonSmooth=TGraph(len(obsX),obsX,obsY)
        	GraphObs=smooth_obs.SmoothSuper(GraphObs_nonSmooth,"linear",0,0.005)
    	else:
        	GraphObs=TGraph(len(obsX),obsX,obsY)
    
    	GraphObs.SetLineWidth(3)
    	if not obs2 == "":

		ratio = []
		ratiox = []
		for index,val in enumerate(observedy):
			mass = observedx[index]
			foundIndex = -1
			for index2, mass2 in enumerate(observedx2):
				if mass == mass2:
					foundIndex = index2

			if foundIndex > 0:
				ratio.append(observedy2[foundIndex]/val)
				ratiox.append(mass)
		ratioA = numpy.array(ratio)
		ratioX = numpy.array(ratiox)
    		obsX2=numpy.array(observedx2)
    		obsY2=numpy.array(observedy2)
		ratioGraph = TGraph(len(ratioX),ratioX,ratioA)
    		if printStats: print "obsX2: ",obsX2
    		if printStats: print "obsY2: ",obsY2

    		if SMOOTH:
        		smooth_obs2=TGraphSmooth("normal")
        		GraphObs2_nonSmooth=TGraph(len(obsX2),obsX2,obsY2)
        		GraphObs2=smooth_obs2.SmoothSuper(GraphObs2_nonSmooth,"linear",0,0.005)
    		else:
        		GraphObs2=TGraph(len(obsX2),obsX2,obsY2)
    
    		GraphObs2.SetLineWidth(3)
    	smoother=TGraphSmooth("normal")
    	smoother2=TGraphSmooth("normal")
    
    	zprimeX=[]
    	zprimeY=[]
    	fileZPrime=open('tools/xsec_SSM.txt','r')
    	for entries in fileZPrime:
        	entry=entries.split()
        	zprimeX.append(float(entry[0]))
        	zprimeY.append(float(entry[1])*1.3/1928)
    	zpX=numpy.array(zprimeX)
    	zpY=numpy.array(zprimeY)
    	GraphZPrime=TGraph(481,zpX,zpY)
    	GraphZPrimeSmooth=smoother2.SmoothSuper(GraphZPrime,"linear")
    	GraphZPrimeSmooth.SetLineWidth(3)
    	GraphZPrimeSmooth.SetLineColor(ROOT.kGreen+3)
    	GraphZPrimeSmooth.SetLineStyle(2)

    	zprimePsiX=[]
    	zprimePsiY=[]
    	fileZPrimePsi=open('tools/xsec_PSI.txt','r')
    	for entries in fileZPrimePsi:
        	entry=entries.split()
        	zprimePsiX.append(float(entry[0]))
        	zprimePsiY.append(float(entry[1])*1.3/1928)
   	zpPsiX=numpy.array(zprimePsiX)
	zpPsiY=numpy.array(zprimePsiY)
    	GraphZPrimePsi=TGraph(481,zpPsiX,zpPsiY)
    	GraphZPrimePsiSmooth=smoother.SmoothSuper(GraphZPrimePsi,"linear")
   	GraphZPrimePsiSmooth.SetLineWidth(3)
    	GraphZPrimePsiSmooth.SetLineColor(ROOT.kBlue)

#Draw the graphs:
    	plotPad.SetLogy()
	if "Moriond" in output:
    		DummyGraph=TH1F("DummyGraph","",100,120,4500)
    	else:	
		DummyGraph=TH1F("DummyGraph","",100,400,4500)
    	DummyGraph.GetXaxis().SetTitle("M [GeV]")
    	if chan=="mumu":
        	DummyGraph.GetYaxis().SetTitle("#sigma(pp#rightarrowZ'+X#rightarrow#mu#mu+X) / #sigma(pp#rightarrowZ+X#rightarrow#mu#mu+X)")
    	elif chan=="elel":
        	DummyGraph.GetYaxis().SetTitle("#sigma(pp#rightarrowZ'+X#rightarrowee+X) / #sigma(pp#rightarrowZ+X#rightarrowee+X)")
    	elif chan=="elmu":
        	DummyGraph.GetYaxis().SetTitle("#sigma(pp#rightarrowZ'+X#rightarrow#font[12]{ll}+X) / #sigma(pp#rightarrowZ+X#rightarrow#font[12]{ll}+X)")

    	gStyle.SetOptStat(0)
	if "Moriond" in output:
    		DummyGraph.GetXaxis().SetRangeUser(120,4500)
    	else:	
		DummyGraph.GetXaxis().SetRangeUser(400,4500)

    	DummyGraph.SetMinimum(1e-8)
    	DummyGraph.SetMaximum(4e-4)
    	DummyGraph.GetXaxis().SetLabelSize(0.04)
    	DummyGraph.GetXaxis().SetTitleSize(0.045)
   	DummyGraph.GetXaxis().SetTitleOffset(1.)
    	DummyGraph.GetYaxis().SetLabelSize(0.04)
    	DummyGraph.GetYaxis().SetTitleSize(0.045)
    	DummyGraph.GetYaxis().SetTitleOffset(1.)
    	DummyGraph.Draw()
    	if (FULL):
        	GraphErr2Sig.Draw("F")
        	GraphErr1Sig.Draw("F")
        	GraphExp.Draw("lpsame")
    	else:
		if obs2 == "":
        		GraphExp.Draw("lp")

    	GraphObs.Draw("plsame")
    	if not obs2 == "":
		GraphObs2.SetLineColor(ROOT.kRed)
		GraphObs2.SetLineStyle(ROOT.kDashed)
		GraphObs2.Draw("plsame")
    	if not SPIN2:
        	GraphZPrimeSmooth.Draw("lsame")
        	GraphZPrimePsiSmooth.Draw("lsame")

    	cCL.SetTickx(1)
    	cCL.SetTicky(1)
    	cCL.RedrawAxis()
    	cCL.Update()
    
    	#leg=TLegend(0.65,0.65,0.87,0.87,"","brNDC")   
    	leg=TLegend(0.540517,0.623051,0.834885,0.878644,"","brNDC")   
#    	leg=TLegend(0.55,0.55,0.87,0.87,"","brNDC")   
    	leg.SetTextSize(0.032)
	if not obs2 == "":
		if ratioLabel == "":
			ratioLabel = "Variant/Default"
		ratioLabels = ratioLabel.split("/")
		
		leg.AddEntry(GraphObs, "% Observed 95% CL limit"%ratioLabel[1],"l")
    		leg.AddEntry(GraphObs2,"%s Observed 95% CL limit"%ratioLabel[0],"l")
    	
	else:
		leg.AddEntry(GraphObs,"Observed 95% CL limit","l")
    		leg.AddEntry(GraphExp,"Expected 95% CL limit, median","l")
        	if (FULL):
   		     	leg.AddEntry(GraphErr1Sig,"Expected 95% CL limit, 1 s.d.","f")
        		leg.AddEntry(GraphErr2Sig,"Expected 95% CL limit, 2 s.d.","f")


    	leg1=TLegend(0.665517,0.483051,0.834885,0.623051,"","brNDC")
    	leg1.SetTextSize(0.032)
	
      	if not SPIN2:
        	leg1.AddEntry(GraphZPrimePsiSmooth,"Z'_{#Psi} (LOx1.3)","l")
        	leg1.AddEntry(GraphZPrimeSmooth,"Z'_{SSM} (LOx1.3)","l")

    	leg.SetLineWidth(0)
    	leg.SetLineStyle(0)
    	leg.SetLineColor(0)
    	leg.Draw("hist")

    	leg1.SetLineWidth(0)
    	leg1.SetLineStyle(0)
    	leg1.SetLineColor(0)
    	leg1.Draw("hist")
	if "Moriond" in output:
         	if (chan=="mumu"): 
            		plLumi=TPaveLabel(.65,.905,.9,.99,"36.3 fb^{-1} (13 TeV, #mu#mu)","NBNDC")
        	elif (chan=="elel"):
            		plLumi=TPaveLabel(.65,.905,.9,.99,"2.7 fb^{-1} (13 TeV, ee)","NBNDC")
        	elif (chan=="elmu"):
            		plLumi=TPaveLabel(.4,.905,.9,.99,"12.4 fb^{-1} (13 TeV, ee) + 13.0 fb^{-1} (13 TeV, #mu#mu)","NBNDC")
	else:
 	      	if (chan=="mumu"): 
            		plLumi=TPaveLabel(.65,.905,.9,.99,"13.0 fb^{-1} (13 TeV, #mu#mu)","NBNDC")
        	elif (chan=="elel"):
            		plLumi=TPaveLabel(.65,.905,.9,.99,"2.7 fb^{-1} (13 TeV, ee)","NBNDC")
        	elif (chan=="elmu"):
            		plLumi=TPaveLabel(.4,.905,.9,.99,"12.4 fb^{-1} (13 TeV, ee) + 13.0 fb^{-1} (13 TeV, #mu#mu)","NBNDC")

    	plLumi.SetTextSize(0.5)
    	plLumi.SetTextFont(42)
    	plLumi.SetFillColor(0)
    	plLumi.SetBorderSize(0)
    	plLumi.Draw()
    


    	plCMS=TPaveLabel(.12,.81,.22,.88,"CMS","NBNDC")
#plCMS.SetTextSize(0.8)
    	plCMS.SetTextAlign(12)
    	plCMS.SetTextFont(62)
    	plCMS.SetFillColor(0)
    	plCMS.SetBorderSize(0)
    
    	plCMS.Draw()

    	plPrelim=TPaveLabel(.12,.76,.25,.82,"Preliminary","NBNDC")
    	plPrelim.SetTextSize(0.6)
    	plPrelim.SetTextAlign(12)
    	plPrelim.SetTextFont(52)
    	plPrelim.SetFillColor(0)
    	plPrelim.SetBorderSize(0)
    	plPrelim.Draw()
	
	if not obs2 == "":

    		ratioPad.cd()

    		line = ROOT.TLine(400,1,4500,1)
    		line.SetLineStyle(ROOT.kDashed)

    		ROOT.gStyle.SetTitleSize(0.12, "Y")
    		ROOT.gStyle.SetTitleYOffset(0.35) 
    		ROOT.gStyle.SetNdivisions(000, "Y")
    		ROOT.gStyle.SetNdivisions(408, "Y")
    		ratioPad.DrawFrame(400,0.9,4500,1.1, "; ; %s"%ratioLabel)

    		line.Draw("same")

    		ratioGraph.Draw("sameP")




    
    	cCL.Update()
    	printPlots(cCL,output)
    

#### ========= MAIN =======================
SMOOTH=False
FULL=False
SPIN2=False
TWOENERGY=False
if __name__ == "__main__":
    	import argparse
    	parser = argparse.ArgumentParser(usage="makeLimitPlot.py [options] -o OUTPUTFILE --obs CARD1 --exp CARD2",description="Check if all the ascii files have been produced with the right number of iterations",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    	parser.add_argument("--obs",dest="obs", default='', help='Observed datacard')
    	parser.add_argument("--obs2",dest="obs2", default='', help='2nd Observed datacard')
    	parser.add_argument("--exp",dest="exp", default='', help='Expected datacard')
    	parser.add_argument("--stats",dest="stats", action="store_true", default=False, help='Print stats')
    	parser.add_argument("--smooth",dest="smooth",action="store_true",default=False, help="Smooth observed values")
    	parser.add_argument("--full",dest="full",action="store_true",default=False, help="Draw 2sigma bands")
    	parser.add_argument("--spin2",dest="spin2",action="store_true",default=False, help="Make Spin2 limits")
    	parser.add_argument("-c","--config",dest="config",default='', help="config name")
    	parser.add_argument("-t","--tag",dest="tag",default='', help="limit tag")
    	parser.add_argument("--ratioLabel",dest="ratioLabel",default='', help="label for ratio")
    	args = parser.parse_args()
    	SMOOTH=args.smooth
    	FULL=args.full
    	SPIN2=args.spin2
       
	configName = "scanConfiguration_%s"%args.config

        config =  __import__(configName)

    	if ("mumu" in config.leptons):  
        	print "Running Limts for dimuon channel"
    	elif ("elel" in config.leptons):
        	print "Running Limts for dielectron channel"
    	elif ("elmu" in config.leptons):
        	print "Running Limts for Combination of dielectron and dimuon channel"
    	else: 
        	print "ERROR, --chan must be mumu, elel or elmu"
        	exit
	
	outputfile = "limitPlot_%s"%args.config
	if not args.tag == "":
		outputfile += "_"+args.tag        

	obs = "cards/limitCard_%s_Obs"%args.config 
	exp = "cards/limitCard_%s_Exp"%args.config 
	if not args.tag == "":
		obs += "_" + args.tag
		exp += "_" + args.tag
	obs += ".txt"
	exp += ".txt"
	if not args.obs == "":
		obs = args.obs
	if not args.exp == "":
		exp = args.exp

    	print "Saving histograms in %s" %(outputfile)
    	print " - Obs file: %s" %(obs)
    	print " - Exp file: %s" %(exp)
    	if (SMOOTH):
        	print "                  "
        	print "Smoothing observed lines..." 
    	print "\n"


	
    	makeLimitPlot(outputfile,obs,exp,config.leptons,args.stats,args.obs2,args.ratioLabel)
    
