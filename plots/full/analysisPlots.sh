#!/bin/sh

##Small
#python -i analysisPlots.py --small --data Run2016 --reduceMC 5 --pfCandInput
#python -i analysisPlots.py --small --data Run2016 --reduceMC 5 --trainingInput
#
#python -i analysisPlots.py --small --data Run2016 --reduceMC 5 --sampleSelection DY --pfCandInput
#python -i analysisPlots.py --small --data Run2016 --reduceMC 5 --sampleSelection DY --trainingInput

#TTs
python -i analysisPlots.py --data Run2016EF --reduceMC 10 --pfCandInput   --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016EF --reduceMC 10 --trainingInput --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016EF --reduceMC 10 --pfCandInput   --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016EF --reduceMC 10 --trainingInput --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016EF --reduceMC 10 --pfCandInput   --eta_min 1.6 --eta_max 2.5
python -i analysisPlots.py --data Run2016EF --reduceMC 10 --trainingInput --eta_min 1.6 --eta_max 2.5
python -i analysisPlots.py --data Run2016EF --reduceMC 10 --pfCandInput   
python -i analysisPlots.py --data Run2016EF --reduceMC 10 --trainingInput 

#DY
python -i analysisPlots.py --data Run2016EF --reduceMC 10 --sampleSelection DY --pfCandInput   --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016EF --reduceMC 10 --sampleSelection DY --trainingInput --eta_min 0.  --eta_max 1.0
python -i analysisPlots.py --data Run2016EF --reduceMC 10 --sampleSelection DY --pfCandInput   --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016EF --reduceMC 10 --sampleSelection DY --trainingInput --eta_min 1.0 --eta_max 1.6
python -i analysisPlots.py --data Run2016EF --reduceMC 10 --sampleSelection DY --pfCandInput   --eta_min 1.6 --eta_max 2.5
python -i analysisPlots.py --data Run2016EF --reduceMC 10 --sampleSelection DY --trainingInput --eta_min 1.6 --eta_max 2.5
python -i analysisPlots.py --data Run2016EF --reduceMC 10 --sampleSelection DY --pfCandInput   
python -i analysisPlots.py --data Run2016EF --reduceMC 10 --sampleSelection DY --trainingInput 


