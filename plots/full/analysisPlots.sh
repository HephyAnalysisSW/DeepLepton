#!/bin/sh

##small
#python -i analysisPlots.py --small --data Run2016 --reduceMC 5 --trainingInput
#python -i analysisPlots.py --small --data Run2016 --reduceMC 5 --tag --pfCandInput
#python -i analysisPlots.py --small --data Run2016 --reduceMC 5 --sampleSelection DY --selection njet1p --trainingInput
#python -i analysisPlots.py --small --data Run2016 --reduceMC 5 --sampleSelection DY --selection njet1p --tag --pfCandInput

#DY
python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --trainingInput 
python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --pfCandInput   
python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --tag --trainingInput 
python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --tag --pfCandInput   

#python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --selection njet1p --trainingInput 
#python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --selection njet1p --pfCandInput   
#python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --selection njet1p --tag --trainingInput 
#python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --selection njet1p --tag --pfCandInput   

#TTs
python -i analysisPlots.py --data Run2016 --reduceMC 5 --pfCandInput   
python -i analysisPlots.py --data Run2016 --reduceMC 5 --trainingInput 
python -i analysisPlots.py --data Run2016 --reduceMC 5 --tag --pfCandInput   
python -i analysisPlots.py --data Run2016 --reduceMC 5 --tag --trainingInput 

#TTs eta
python -i analysisPlots.py --data Run2016 --reduceMC 5 --pfCandInput   --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 5 --trainingInput --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 5 --pfCandInput   --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 5 --trainingInput --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 5 --pfCandInput   --eta_min 1.6 --eta_max 2.5
python -i analysisPlots.py --data Run2016 --reduceMC 5 --trainingInput --eta_min 1.6 --eta_max 2.5

python -i analysisPlots.py --data Run2016 --reduceMC 5 --tag --pfCandInput   --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 5 --tag --trainingInput --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 5 --tag --pfCandInput   --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 5 --tag --trainingInput --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 5 --tag --pfCandInput   --eta_min 1.6 --eta_max 2.5
python -i analysisPlots.py --data Run2016 --reduceMC 5 --tag --trainingInput --eta_min 1.6 --eta_max 2.5

#DY eta
python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --pfCandInput   --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --trainingInput --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --pfCandInput   --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --trainingInput --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --pfCandInput   --eta_min 1.6 --eta_max 2.5
python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --trainingInput --eta_min 1.6 --eta_max 2.5

python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --tag --pfCandInput   --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --tag --trainingInput --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --tag --pfCandInput   --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --tag --trainingInput --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --tag --pfCandInput   --eta_min 1.6 --eta_max 2.5
python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --tag --trainingInput --eta_min 1.6 --eta_max 2.5

#python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --selection njet1p --pfCandInput   --eta_min 0.  --eta_max 1.0
#python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --selection njet1p --trainingInput --eta_min 0.  --eta_max 1.0
#python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --selection njet1p --pfCandInput   --eta_min 1.0 --eta_max 1.6
#python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --selection njet1p --trainingInput --eta_min 1.0 --eta_max 1.6
#python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --selection njet1p --pfCandInput   --eta_min 1.6 --eta_max 2.5
#python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --selection njet1p --trainingInput --eta_min 1.6 --eta_max 2.5
#
#python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --selection njet1p --tag --pfCandInput   --eta_min 0.  --eta_max 1.0
#python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --selection njet1p --tag --trainingInput --eta_min 0.  --eta_max 1.0
#python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --selection njet1p --tag --pfCandInput   --eta_min 1.0 --eta_max 1.6
#python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --selection njet1p --tag --trainingInput --eta_min 1.0 --eta_max 1.6
#python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --selection njet1p --tag --pfCandInput   --eta_min 1.6 --eta_max 2.5
#python -i analysisPlots.py --data Run2016 --reduceMC 5 --sampleSelection DY --selection njet1p --tag --trainingInput --eta_min 1.6 --eta_max 2.5

