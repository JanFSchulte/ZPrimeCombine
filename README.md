# ZPrimeCombine
Tools to perform statistical analyses for the Z' -> ll analysis using the Higgs combine toolkit

## Current combine installation recipe:
export SCRAM_ARCH=slc6_amd64_gcc530
cmsrel CMSSW_8_1_0
cd CMSSW_8_1_0/src 
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v7.0.10
scramv1 b clean; scramv1 b # always make a clean build
## Check out ZPrimeCombine toolkit:
git clone https://USERNAME@gitlab.cern.ch/cms-zprime-dileptons/ZPrimeCombine.git
git fetch origin
git checkout v2.0.0
## General considerations:  
This repository consits of python scripts fulfilling two purposes:

1) Create datacards and ROOT files containing workspaces as input for combine,

2) Serve as a user-friendly interface to execute combine in the appropriate configuration for limits and p-values/significance,

For detailed instructions on usage, please see the manual in the documentation folder
