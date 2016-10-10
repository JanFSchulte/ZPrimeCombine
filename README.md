# ZPrimeCombine
Tools to perform statistical analyses for the Z' -> ll analysis using the Higgs combine toolkit

## Current combine installation recipe:
export SCRAM_ARCH=slc6_amd64_gcc491

cmsrel CMSSW_7_4_7

cd CMSSW_7_4_7/src 

cmsenv

git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
 
cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit;

git fetch origin;

git checkout v6.3.0;

scramv1 b clean; scramv1 b

## General considerations:  
This repository consits of python scripts fulfilling two purposes:

1) Create datacards and ROOT files containing workspaces as input for combine,

2) Serve as a user-friendly interface to execute combine in the appropriate configuration for limits and p-values/significance,

This framework is under construction! 

Available functionality:
- Datacards creation for single channels and channel combination for full mass scans, including full set of uncertainties of the ICHEP 2016 dimuon analysis 
- Calculation of observed and expcted limits
- Calculation of local p-values/significances
- Performing mass scans as well as single point operiation locally

Functionality NOT yet availabe:
- Submission to computing clusters/GRID
- Binned Analysis
- Handleling of more than one background contribution
- Plotting of the results

Limits are calculated using the MarkovChainMC option of combine, for significances the ProfileLikelihood method is used.
## Usage
The user has to configure two basics inputs to the system:

1) A cfg/scanConfiguration_xxx.py file, holding the basic configuration of the statistical interpretation to be performed: Channels to include, mass scan parameters, uncertainties to consider, configuration of the MCMC, etc. The intention is to create a new configuration file for each new result to maintain reproducibility. The placeholder in the file name is to be replaced by a meaningful name for the configuration. It will be used to label all output. 

2) A input/createWS_yyy.py file per channel, containing the functions needed to create the workspaces and to provide all information to write the datacards. All the physics information about each channel goes here. There are a couple of functions providing specific information that have to be implemented in each of these channel modules. For more information, have a look at one of the pratical examples

Once the config files are in place, the interpretation can be run by calling runInterpretation.py (such creativity, much wow). Most important arguments for this tool are:

-c specifies name of the scanConfiguratin to be use

-s launches submission to some computing resources, to be implemented

-r re-writes the datacards and workspaces - has to be used the first time a new config is used

-m specifies a signel mass point to be run

-e runs expected limits instead of observed ones. Does nothing when computing significances


