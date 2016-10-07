# ZPrimeCombine
Tools to create datacards for combine for the Z' -> ll analysis 

## Update and compile combine: 
cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit;

git fetch origin;

git checkout v6.3.0;

scramv1 b clean; scramv1 b

## CREATING WORKSPACE (for now a dummy example):  

cd $CMSSW_BASE/src/ZPrimeCombine;

python createWSForShape.py;
