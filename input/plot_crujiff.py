import ROOT
import math
#from ROOT import RooFit, RooRealVar, RooGaussian, RooDataSet, RooArgList, RooTreeData, RooArgSet
from ROOT import *
ROOT.gROOT.SetBatch(ROOT.kTRUE) 

import sys,getopt
from math import sqrt

#def getResolution(mass):
#   return res_scale*0.01*(sqrt(res_s*res_s/mass+res_n*res_n/mass/mass+res_c*res_c)+res_slope*mass)

def getResolution(mass):

   if mass > 2300:
	   parameters={}
	   parameters['alpha']={}
	   parameters['n'    ]={}
	   parameters['scale']={}
	   parameters['sigma']={}

	   parameters['alpha']['BB']=2.167-3.076e-4*mass
	   parameters['alpha']['BE']=1.638-7.983e-5*mass
	   parameters['n'    ]['BB']=0.598+4.383e-4*mass
	   parameters['n'    ]['BE']=1.992-5.805e-5*mass
	   parameters['scale']['BB']=1+0.0002551-1.692e-6*mass
	   parameters['scale']['BE']=1-0.002736 +4.085e-7*mass
	   parameters['sigma']['BB']=0.7623+9.264e-5*mass#(sigma extra BB is already added in quadrature)
	   parameters['sigma']['BE']=1.515 +1.540e-5*mass#(sigma extra BE is already added in quadrature)
   else:
   	parameters={}
   	parameters['alphaL']={}
   	parameters['alphaR']={}
   	parameters['scale'] ={}
   	parameters['sigma'] ={}

   	#####alphaL BB
   	a_BB=1400
   	b_BB=1.3
   	c_BB=0.7
   	d_BB=8.56e-9
   	e_BB=0.24
   	parameters['alphaL']['BB']=(mass<a_BB)*(pow(mass,-b_BB) -b_BB*pow(a_BB,-c_BB)) + (mass>a_BB)*d_BB*(mass-a_BB)*(mass-a_BB) +e_BB #power law + parabola
   
   	#####alphaL BE
   	a_BE=2.0
   	b_BE=0.
   	c_BE=0.2
   	d_BE=6.78e-6
   	parameters['alphaL']['BE']=sqrt(a_BE*a_BE/mass + b_BE*b_BE/mass/mass + c_BE*c_BE) + d_BE*mass #resolution function with linear term

   	#####alphaR BB
   	a_BB=1.29e-4
   	b_BB=1700
   	c_BB=2.24e-8
   	d_BB=8.61e-9
   	parameters['alphaR']['BB']=a_BB + (mass<b_BB)*c_BB*(mass-b_BB)*(mass-b_BB) + (mass>b_BB)*d_BB*(mass-b_BB)*(mass-b_BB) #asymmetric parabola

   	#####alphaR BE
   	a_BE=2.78e-2
   	b_BE=1300
   	c_BE=-1.90e-8
   	d_BE=-2.44e-9
   	parameters['alphaR']['BE']=a_BE + (mass<b_BE)*c_BE*(mass-b_BE)*(mass-b_BE) + (mass>b_BE)*d_BE*(mass-b_BE)*(mass-b_BE) #asymmetric parabola

   	#####scale BB
   	a_BB=1.
   	b_BB=654.84
   	c_BB=-5.469e-9
   	d_BB=-4.279e-10
   	parameters['scale']['BB']=a_BB + (mass<b_BB)*c_BB*(mass-b_BB)*(mass-b_BB) + (mass>b_BB)*d_BB*(mass-b_BB)*(mass-b_BB) #asymmetric parabola 

   	#####scale BE
   	a_BE=1.
   	b_BE=1245.01
   	c_BE=-4.447e-9
   	d_BE=1.525e-10
   	parameters['scale']['BE']=a_BE + (mass<b_BE)*c_BE*(mass-b_BE)*(mass-b_BE) + (mass>b_BE)*d_BE*(mass-b_BE)*(mass-b_BE) #asymmetric parabola

   	#####resolution BB (sigma extra BB is already added in quadrature)
   	s_BB=10.3
   	n_BB=10
   	c_BB=0.87
   	l_BB=5.6e-5
   	parameters['sigma']['BB']=(sqrt(s_BB*s_BB/mass + n_BB*n_BB/mass/mass + c_BB*c_BB) + l_BB*mass)*0.01 #resolution function with linear term

   	#####resolution BE (sigma extra BE is already added in quadrature)
   	s_BE=14.5
   	n_BE=10
   	c_BE=1.49
   	parameters['sigma']['BE']=(sqrt(s_BE*s_BE/mass + n_BE*n_BE/mass/mass + c_BE*c_BE))*0.01 #resolution function w/o linear term


   return parameters


