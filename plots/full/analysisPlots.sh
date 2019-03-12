#!/bin/sh

#small
python -i analysisPlots.py --small --data Run2016 --reduceMC 10 --trainingInput
python -i analysisPlots.py --small --data Run2016 --reduceMC 10 --tag --pfCandInput
python -i analysisPlots.py --small --data Run2016 --reduceMC 10 --sampleSelection DY --selection njet1p --trainingInput
python -i analysisPlots.py --small --data Run2016 --reduceMC 10 --sampleSelection DY --selection njet1p --tag --pfCandInput

#TTs
python -i analysisPlots.py --data Run2016 --reduceMC 10 --pfCandInput   --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 10 --trainingInput --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 10 --pfCandInput   --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 10 --trainingInput --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 10 --pfCandInput   --eta_min 1.6 --eta_max 2.5
python -i analysisPlots.py --data Run2016 --reduceMC 10 --trainingInput --eta_min 1.6 --eta_max 2.5
python -i analysisPlots.py --data Run2016 --reduceMC 10 --pfCandInput   
python -i analysisPlots.py --data Run2016 --reduceMC 10 --trainingInput 

python -i analysisPlots.py --data Run2016 --reduceMC 10 --tag --pfCandInput   --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 10 --tag --trainingInput --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 10 --tag --pfCandInput   --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 10 --tag --trainingInput --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 10 --tag --pfCandInput   --eta_min 1.6 --eta_max 2.5
python -i analysisPlots.py --data Run2016 --reduceMC 10 --tag --trainingInput --eta_min 1.6 --eta_max 2.5
python -i analysisPlots.py --data Run2016 --reduceMC 10 --tag --pfCandInput   
python -i analysisPlots.py --data Run2016 --reduceMC 10 --tag --trainingInput 

#DY
python -i analysisPlots.py --data Run2016 --reduceMC 10 --sampleSelection DY --selection njet1p --pfCandInput   --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 10 --sampleSelection DY --selection njet1p --trainingInput --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 10 --sampleSelection DY --selection njet1p --pfCandInput   --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 10 --sampleSelection DY --selection njet1p --trainingInput --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 10 --sampleSelection DY --selection njet1p --pfCandInput   --eta_min 1.6 --eta_max 2.5
python -i analysisPlots.py --data Run2016 --reduceMC 10 --sampleSelection DY --selection njet1p --trainingInput --eta_min 1.6 --eta_max 2.5
python -i analysisPlots.py --data Run2016 --reduceMC 10 --sampleSelection DY --selection njet1p --pfCandInput   
python -i analysisPlots.py --data Run2016 --reduceMC 10 --sampleSelection DY --selection njet1p --trainingInput 

python -i analysisPlots.py --data Run2016 --reduceMC 10 --sampleSelection DY --selection njet1p --tag --pfCandInput   --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 10 --sampleSelection DY --selection njet1p --tag --trainingInput --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 10 --sampleSelection DY --selection njet1p --tag --pfCandInput   --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 10 --sampleSelection DY --selection njet1p --tag --trainingInput --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 10 --sampleSelection DY --selection njet1p --tag --pfCandInput   --eta_min 1.6 --eta_max 2.5
python -i analysisPlots.py --data Run2016 --reduceMC 10 --sampleSelection DY --selection njet1p --tag --trainingInput --eta_min 1.6 --eta_max 2.5
python -i analysisPlots.py --data Run2016 --reduceMC 10 --sampleSelection DY --selection njet1p --tag --pfCandInput   
python -i analysisPlots.py --data Run2016 --reduceMC 10 --sampleSelection DY --selection njet1p --tag --trainingInput 

#DY reduceMC 20
python -i analysisPlots.py --data Run2016 --reduceMC 20 --sampleSelection DY --selection njet1p --pfCandInput   
python -i analysisPlots.py --data Run2016 --reduceMC 20 --sampleSelection DY --selection njet1p --trainingInput 
python -i analysisPlots.py --data Run2016 --reduceMC 20 --sampleSelection DY --selection njet1p --tag --pfCandInput   
python -i analysisPlots.py --data Run2016 --reduceMC 20 --sampleSelection DY --selection njet1p --tag --trainingInput 

python -i analysisPlots.py --data Run2016 --reduceMC 20 --sampleSelection DY --selection njet1p --pfCandInput   --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 20 --sampleSelection DY --selection njet1p --trainingInput --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 20 --sampleSelection DY --selection njet1p --pfCandInput   --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 20 --sampleSelection DY --selection njet1p --trainingInput --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 20 --sampleSelection DY --selection njet1p --pfCandInput   --eta_min 1.6 --eta_max 2.5
python -i analysisPlots.py --data Run2016 --reduceMC 20 --sampleSelection DY --selection njet1p --trainingInput --eta_min 1.6 --eta_max 2.5

python -i analysisPlots.py --data Run2016 --reduceMC 20 --sampleSelection DY --selection njet1p --tag --pfCandInput   --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 20 --sampleSelection DY --selection njet1p --tag --trainingInput --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016 --reduceMC 20 --sampleSelection DY --selection njet1p --tag --pfCandInput   --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 20 --sampleSelection DY --selection njet1p --tag --trainingInput --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016 --reduceMC 20 --sampleSelection DY --selection njet1p --tag --pfCandInput   --eta_min 1.6 --eta_max 2.5
python -i analysisPlots.py --data Run2016 --reduceMC 20 --sampleSelection DY --selection njet1p --tag --trainingInput --eta_min 1.6 --eta_max 2.5

