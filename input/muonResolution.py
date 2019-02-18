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
   parameters={}
   parameters['alphaL']={}
   parameters['alphaR']={}
   parameters['scale'] ={}
   parameters['sigma'] ={}

   #####alphaL BB
   a_BB=0.218
   b_BB=-4.8e-06
   c_BB=1e-10
   parameters['alphaL']['BB'] = a_BB + b_BB*mass + c_BB*mass*mass

   #####alphaL BE
   a_BE= 0.248
   b_BE= -1.03e-05
   c_BE=1e-10
   parameters['alphaL']['BE']= a_BE + b_BE*mass + c_BE*mass*mass

   #####alphaR BB
   a_BB= 0.07
   b_BB= 6.53e-06
   c_BB= 1e-10
   parameters['alphaR']['BB']=a_BB + b_BB*mass + c_BB*mass*mass

   #####alphaR BE
   a_BE= 0.159
   b_BE= 1e-07
   c_BE= -2.06e-09
   parameters['alphaR']['BE']=a_BE + b_BE*mass + c_BE*mass*mass

   #####scale BB
   a_BB = 2.46e-05
   b_BB = -3.17e-06
   c_BB = 9.61e-10
   d_BB = -1.38e-13
   parameters['scale']['BB']= a_BB + b_BB*mass + c_BB*mass**2 + d_BB*mass**3

   #####scale BE
   a_BE = -0.000148
   b_BE = -8.24e-06
   c_BE = 3.19e-09
   d_BE = -4.4e-13
   parameters['scale']['BE']= a_BB + b_BB*mass + c_BB*mass**2 + d_BB*mass**3


   #####sigma BB
   a_BB=0.00701
   b_BB=3.32e-05
   c_BB=-1.29e-08
   d_BB=2.73e-12
   e_BB=-2.05e-16
   parameters['sigma']['BB'] = a_BB + b_BB*mass + c_BB*mass*mass + d_BB*mass**3 + e_BB*mass**4

   #####sigma BE
   a_BE=0.0124
   b_BE=3.75e-05
   c_BE=-1.52e-08
   d_BE=3.44e-12
   e_BE=-2.85e-16
   parameters['sigma']['BE'] = a_BE + b_BE*mass + c_BE*mass*mass + d_BE*mass**3 + e_BE*mass**4


   return parameters




