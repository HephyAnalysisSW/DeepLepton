###########
# imports #
###########

# Standard imports
import ROOT
import os
from array import array
from copy import deepcopy
import math
from ROOT import gStyle

# RootTools
from RootTools.core.standard import *
from RootTools.core.Sample import *

# User specific 
from DeepLepton.Tools.user import plot_directory

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',           default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--small',              action='store_true',                help='Run only on a small subset of the data?', )
argParser.add_argument('--plot_directory',     action='store',           default='deepLepton')
argParser.add_argument('--ptMin',              action='store',      type=int,     default=25)
argParser.add_argument('--ptMax',              action='store',      type=int,     default=0)
argParser.add_argument('--flat',               action='store_true',                 help='Run on flat ntuple data?', )
argParser.add_argument('--flatSample',         action='store',           default='TTJets_Muons_balanced_pt5toInf_2016')

argParser.add_argument('--year',               action='store', type=int, choices=[2016,2017],   default=2016,   help="Which year?")
argParser.add_argument('--flavour',            action='store', type=str, choices=['ele','muo'], default='muo',  help="Which Flavour?")
argParser.add_argument('--testData',           action='store_true',       help="plot test or train data?")
argParser.add_argument('--lumi_weight',        action='store_true',       help="apply lumi weight?")

argParser.add_argument('--binned',             action='store', type=str, choices=['pt','eta','nTrueInt'], default='pt',                 help="Which variable for binning?")
argParser.add_argument('--eS',                 action='store', type=int, default=90,                                    help="Draw efficiencies for an overall signal efficiency?")
#argParser.add_argument('--selection',          action='store',      default='dilepOS-njet3p-btag1p-onZ')
args = argParser.parse_args()

# Logger
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

##############################
# load samples and variables #
##############################
args.eS=args.eS/100.

maxN = -1
if args.small:
    maxN = 1

#get flat sample
if args.flat:
    
    from DeepLepton.samples.flat_training_samples import *
    sampleInfo = vars()[args.flatSample]
    flat_files, predict_files = get_flat_files( sampleInfo['flat_directory'], sampleInfo['predict_directory' if args.testData else 'predict_directory_trainData'], maxN)
    sample = get_flat_sample( sampleInfo['training_name'], sampleInfo['sample_name'], flat_files, predict_files )

    # variables to read
    noTraining = False
    variables = get_flat_variables(noTraining)

else:
    print "FIXME: implement full events first."

#########################
# define plot structure #
#########################
isTestData = args.testData

leptonFlavour = {'fullName':'Electron' if args.flavour=='ele' else 'Muon', 'name':args.flavour, 'pdgId': 11 if args.flavour=='ele' else 13, 'trainDates': [], 'plotTestData': isTestData}
leptonFlavour['trainDates'].append({'date': sampleInfo['training_date'],  'plots': [
                                      {'name': 'LeptonMVA_TTH',       'MVAType': 'MVA_Id', 'var': 'lep_mvaTTH',                   'color':ROOT.kGray,    'lineWidth': 2, 'thresholds':[ i/100. for i in range(0,100)]},
                                      {'name': 'LeptonMVA_TTV',       'MVAType': 'MVA_Id', 'var': 'lep_mvaTTV',                   'color':ROOT.kGray+1,  'lineWidth': 2, 'thresholds':[ i/100. for i in range(-100,101)]},
                                      {'name': 'DeepLepton',          'MVAType': 'DL_Id',  'var': 'prob_lep_isPromptId_Training', 'color':ROOT.kGreen+2, 'lineWidth': 2, 'thresholds':[ i/100. for i in range(-100,101)]},
                                                                                   ]})


binnedList={}
binnedList.update({"pt":       {"varName":"|pt|",                                           "Var":"lep_pt",                                             "abs":1, "cuts":[0, 250],      "bins":50, "eS": args.eS }})
binnedList.update({"eta":      {"varName":"|etaSc|" if args.flavour=='ele' else "|eta|",    "Var":"lep_etaSc" if args.flavour=='ele' else "lep_eta",    "abs":1, "cuts":[0, 2.5],      "bins":50, "eS": args.eS }})
binnedList.update({"nTrueInt": {"varName":"nTrueInt",                                       "Var":"nTrueInt",                                           "abs":0, "cuts":[0, 50],       "bins":50, "eS": args.eS }})

###############
# define cuts #
###############

#preselection
loose_id = "abs(lep_pdgId)==13&&lep_pt>5&&abs(lep_eta)<2.4&&lep_miniRelIso<0.4&&lep_sip3d<8&&abs(lep_dxy)<0.05&&abs(lep_dz)<0.1&&lep_pfMuonId&&lep_mediumMuonId"
sample.setSelectionString(loose_id)

# pt selection
kinematic_selection = "lep_pt>{ptMin}".format(ptMin = args.ptMin) if args.ptMax==0 else "lep_pt>{ptMin}&&lep_pt<={ptMax}".format(ptMin = args.ptMin, ptMax = args.ptMax)
kinematic_selection_name = "pt{ptMin}to{ptMax}".format(ptMin = args.ptMin, ptMax = 'Inf' if args.ptMax==0 else args.ptMax)

ptCuts=[]
ptCuts.append({"Name":"pt{ptMin}to{ptMax}".format(ptMin=args.ptMin, ptMax='Inf' if args.ptMax==0 else args.ptMax),"lower_limit":int(args.ptMin), "upper_limit":float("Inf") if args.ptMax==0 else int(args.ptMax)})

relIsoCuts = [0.5]

logY=0

ptCuts=[]
if args.binned=='pt':
    ptCuts.append({"Name":"pt5to250", "lower_limit":10, "upper_limit":250         })
else:
    ptCuts.append({"Name":"pt25toInf","lower_limit":25, "upper_limit":float("Inf")})
    ptCuts.append({"Name":"pt10to25" ,"lower_limit":10, "upper_limit":25})


####################################
# loop over samples and draw plots #
####################################

#functions to calculate eS and eB
def eS(p, rocdataset):
    ntruth=0.
    ntruthid=0.
    for data in rocdataset:
        if data[0]==1:
            ntruth+=data[2]
            if data[1]>=p:
                ntruthid+=data[2]
    #print ntruth, ntruthid
    return 0. if ntruth==0. else  ntruthid/ntruth

def eB(p, rocdataset):
    ntruth=0.
    ntruthid=0.
    for data in rocdataset:
        if not data[0]==1:
            ntruth+=data[2]
            if data[1]>=p:
                ntruthid+=data[2]
    #print ntruth, ntruthid
    return 0. if ntruth==0. else ntruthid/ntruth


for relIsoCut in relIsoCuts:

    for ptCut in ptCuts:    

        colorList=[]
        lineWidthList=[]
        
        #Initialize Mulitgraph
        c=ROOT.TCanvas()
        if logY==1:
            c.SetLogy()
        mg=ROOT.TMultiGraph()
        g=[]
        ng=0
        binWidth = (binnedList[args.binned]["cuts"][1]-binnedList[args.binned]["cuts"][0])/binnedList[args.binned]["bins"]

        plots = leptonFlavour['trainDates'][0]['plots']
        for plot in plots:
            
            colorList.append(plot["color"])
            lineWidthList.append(plot["lineWidth"])

            # reader class
            readerData=[[] for i in xrange(binnedList[args.binned]["bins"])]
            reader = sample.treeReader(  map( TreeVariable.fromString, variables ) )
            reader.start()
            while reader.run():
                if abs(reader.event.lep_pdgId)==leptonFlavour["pdgId"] and reader.event.lep_pt>=ptCut["lower_limit"] and reader.event.lep_pt<=ptCut["upper_limit"]:
                    cut_val = abs(getattr(reader.event, binnedList[args.binned]["Var"])) 
                    if cut_val >= binnedList[args.binned]["cuts"][0] and cut_val <  binnedList[args.binned]["cuts"][1]:
                        
                        j=int(math.ceil(cut_val/(binnedList[args.binned]["cuts"][1]-binnedList[args.binned]["cuts"][0])*binnedList[args.binned]["bins"]))-1
                        readerData[j].append([getattr(reader.event, 'lep_isPromptId_Training'), getattr(reader.event, plot["var"]), reader.event.lumi_scaleFactor1fb if args.lumi_weight==1 else 1])

            #Draw eS plots
            j=0
            x    = array('d')
            y_eS = array('d')
            y_eB = array('d')

            #calculate cut value for overall eS 
            #select full reader data
            eSreaderData  = []
            for dataset in readerData:
                for datapoint in dataset:
                    eSreaderData.append(datapoint) 

            #find maxpval, for eS
            maxpval = 1.
            prange = plot['thresholds']
            for pval in prange:
                eSVal = eS(pval,eSreaderData)
                if eSVal<=args.eS and not eSVal<=0.:
                    maxpval = pval
                    break

                print '\n'
                print maxpval, eSVal

            #calculate bin values
            for dataset in readerData:
                j += 1
                if not len(dataset)==0:
                    x.append(j*binWidth)
                    y_eS.append(eS(maxpval,dataset))
                    y_eB.append(eB(maxpval,dataset)*10)
                    print j*binWidth, maxpval, y_eB[-1], y_eS[-1]

            #Draw Graphs
            n=len(x)
            g.append(ROOT.TGraph(n,x,y_eS))
            gname=("eS "+plot["name"]+" (for overall eS={sigeff})".format(sigeff=str(args.eS)))
            g[ng].SetName(gname)
            g[ng].SetTitle(gname)
            g[ng].SetLineColor( 0 )
            #g[ng].SetLineWidth(lineWidthList[ng])
            g[ng].SetMarkerColor(colorList[ng])
            g[ng].SetMarkerStyle( 9 ) #
            g[ng].SetFillStyle(0)
            g[ng].SetFillColor(0)
            #g[ng].SetMarkerSize(0)
            g[ng].SetMarkerSize(0.5)
            #g[ng].Draw("C")
            g[ng].Draw("P")
            #nmaxtext.DrawLatex(x[nmax],y[nmax],"mvaId=%1.2f" %p[nmax])
            mg.Add(g[ng])

            #Draw eB plots
            #Draw Graphs
            n=len(x)
            graph=ROOT.TGraph(n,x,y_eB)
            gname=("eB x 10 "+plot["name"]+" (for plotted eS)")
            graph.SetName(gname)
            graph.SetTitle(gname)
            #graph.SetLineStyle( 2 )
            graph.SetLineColor( 0 )
            #graph.SetLineWidth(lineWidthList[ng])
            graph.SetMarkerColor(colorList[ng])
            graph.SetMarkerStyle( 4 )
            graph.SetFillStyle( 0 )
            graph.SetFillColor( 0 )
            graph.SetMarkerSize( 0.5 )
            graph.Draw("P")
            #nmaxtext.DrawLatex(x[nmax],y[nmax],"mvaId=%1.2f" %p[nmax])
            mg.Add(graph)

            ng += 1

        #Draw Multigraph
        mg.Draw("AP")
        #mg.SetTitle(leptonFlavour["sample"].texName+(" - TrainData" if isTrainData else " - TestData"))
        mg.GetXaxis().SetTitle(binnedList[args.binned]["varName"])
        mg.GetYaxis().SetTitle('eS,eB')
        if logY==0:
            mg.GetYaxis().SetRangeUser(0.0,1.02)
        if args.flavour=='muo':
            if args.binned=='pt':
                yleg1 = 0.35
            else:
                yleg1 = 0.65
        if args.flavour=='ele':
            if ptCut['name']=="pt10to25":
                yleg1 = 0.65
            if ptCut['name']=="pt25toInf":
                yleg1 = 0.25
            else:
                yleg1 = 0.35
        yleg2 = yleg1 + 0.25
        c.BuildLegend(0.55,yleg1,0.9,yleg2)

        header = [
        {'text': ROOT.TPaveLabel(.00,0.93,.20,1.0,   "CMS preliminary",                                                                                                                 "nbNDC"), 'font': 30  },
        {'text': ROOT.TPaveLabel(.20,0.93,1.0,1.0,   "TestData: {sample}, {kin}    Training: {training}".format( sample = sample.texName, kin = ptCut["Name"], training = sample.name), "nbNDC"), 'font': 130 },
        {'text': ROOT.TPaveLabel(.00,0.91,1.0,0.929, "preselection: {preselect}".format( preselect = loose_id ),                                                                        "nbNDC"), 'font': 130 },
                 ]

        for line in header:
            line['text'].SetFillColor(gStyle.GetTitleFillColor())
            line['text'].SetTextFont(line['font'])
            line['text'].Draw()

        if args.flat:
            directory = os.path.join(   plot_directory, "DeepLepton",
                                        sampleInfo['sample_name'],
                                        sampleInfo['training_date'],
                                        'TestData' if args.testData else 'TrainData',
                                    )
        else:
            directory = os.path.join( plot_directory, "DeepLepton" )
        if not os.path.exists(directory):
            os.makedirs(directory)
        c.Print(os.path.join( directory, "{plot_name}_{kin}_{lumi}_roc_binned_{binVar}_for_eS_of_{sigeff}.png".format( 
                            plot_name = sample.name, kin = ptCut["Name"], lumi = 'lumi' if args.lumi_weight else 'noLumi', binVar = args.binned, sigeff = str(args.eS ) )))

