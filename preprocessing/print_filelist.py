# Standard imports
import ROOT
import os

import numpy

#leptonFlavour  = ['ele', 'muo']
#leptonFlavour   = ['ele']
leptonFlavour   = ['muo']
sampleSelections = [
                    #'DYvsQCD', 
                    'TTJets',
                    #'TTs',
                    #'all',
                   ]

ptSelections    = [
                    #'pt_5_-1',
                    #'pt_5_15',
                    #'pt_15_25',
                    #'pt_25_-1',
                    'pt_15_-1',
                  ]

ratioTrain      = 80
ratioTest       = 20

for flavour in leptonFlavour:
    for sampleSelection in sampleSelections:
        for ptSelection in ptSelections:
        #write file path of step3 output in following line
           # filepath = os.path.join('/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016',flavour,ptSelection,sampleSelection)
           # filepath = os.path.join('/afs/hephy.at/work/s/sschneider/DeepLepton/skims/v1_small_simon/step3/2016',flavour,ptSelection,sampleSelection)
           # filepath = os.path.join('/afs/hephy.at/data/cms01/DeepLepton/skims/v1/step3/2016',flavour,ptSelection,sampleSelection)
           # filepath = os.path.join('/afs/hephy.at/data/cms02/DeepLepton/skims/v1/step3/2016',flavour,ptSelection,sampleSelection)
            filepath = os.path.join('/afs/hephy.at/data/cms03/tbrueckler/DeepLepton/skims/v1/step3/2016',flavour,ptSelection,sampleSelection)
            filelist = os.listdir(filepath)
            #print filepath
            #print filelist
            numpy.random.shuffle(filelist)

            trainfilelist = []
            testfilelist  = []

            for i in xrange(len(filelist)):
                if i < len(filelist)*ratioTrain/(ratioTrain+ratioTest):
                    trainfilelist.append(filelist[i])
                else:
                    testfilelist.append(filelist[i])

            with open(filepath+'/train_'+flavour+'.txt', 'w') as f:
                for trainfile in trainfilelist:
                    #print trainfile
                    f.write("%s\n" % trainfile)

            with open(filepath+'/test_'+flavour+'.txt', 'w') as f:
                for testfile in testfilelist:
                    #print testfile
                    f.write("%s\n" % testfile)


