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
#argParser.add_argument('--ptMin',              action='store',      type=int,     default=25)
#argParser.add_argument('--ptMax',              action='store',      type=int,     default=0)
argParser.add_argument('--flat',               action='store_true',                 help='Run on flat ntuple data?', )
argParser.add_argument('--flatSample',         action='store',           default='TTJets_Muons_balanced_pt5toInf_2016')

argParser.add_argument('--year',               action='store', type=int, choices=[2016,2017],   default=2016,   help="Which year?")
argParser.add_argument('--flavour',            action='store', type=str, choices=['ele','muo'], default='muo',  help="Which Flavour?")
argParser.add_argument('--testData',           action='store_true',       help="plot test or train data?")
argParser.add_argument('--lumi_weight',        action='store_true',       help="apply lumi weight?")

argParser.add_argument('--binned',             action='store', type=str, choices=['pt','low_pt','high_pt','eta','nTrueInt'], default='pt',                 help="Which variable for binning?")
argParser.add_argument('--eS_TTV',                 action='store', type=int, default=90,                                    help="Draw TTV/TTH efficiencies for an overall signal efficiency?")
argParser.add_argument('--eS_DL',                  action='store', type=int, default=90,                                    help="Draw DeepLepton efficiencies for an overall signal efficiency?")
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

maxN = -1
if args.small:
    maxN = 1

#get flat sample
if args.flat:
    
    from DeepLepton.samples.flat_training_samples import *
    flat_sampleInfo = vars()[args.flatSample]
    flat_files, predict_files = get_flat_files( flat_sampleInfo['flat_directory'], flat_sampleInfo['predict_directory' if args.testData else 'predict_directory_trainData'], maxN)
    sample = get_flat_sample( flat_sampleInfo['training_name'], flat_sampleInfo['sample_name'], flat_files, predict_files )

    # variables to read
    variables = get_flat_variables("fullClasses")

else:
    print "FIXME: implement full events first."

#########################
# define plot structure #
#########################
isTestData = args.testData

leptonFlavour = {'fullName':'Electron' if args.flavour=='ele' else 'Muon', 'name':args.flavour, 'pdgId': 11 if args.flavour=='ele' else 13, 'trainDates': [], 'plotTestData': isTestData}
leptonFlavour['trainDates'].append({'date': flat_sampleInfo['training_date'],  'plots': [
                                      {'name': 'TTH',       'MVAType': 'MVA_Id', 'var': 'lep_mvaTTH',                   'color':ROOT.kGray,    'lineWidth': 2, 'eS': args.eS_TTV, 'thresholds':[ i/100. for i in range(0,100)]},
                                      {'name': 'TTV',       'MVAType': 'MVA_Id', 'var': 'lep_mvaTTV',                   'color':ROOT.kGray+1,  'lineWidth': 2, 'eS': args.eS_TTV, 'thresholds':[ i/100. for i in range(-100,101)]},
                                      {'name': 'DeepLepton',          'MVAType': 'DL_Id',  'var': 'prob_lep_isPromptId_Training', 'color':ROOT.kGreen+2, 'lineWidth': 2, 'eS': args.eS_DL, 'thresholds':[ i/100. for i in range(-100,101)]},
                                                                                   ]})


binnedList={}
binnedList.update({"pt":       {"varName":"|p_{T}|",                                        "Var":"lep_pt",                                             "abs":1, "cuts":[0, 200],      "bins":40}})
binnedList.update({"low_pt":   {"varName":"|p_{T}|",                                        "Var":"lep_pt",                                             "abs":1, "cuts":[0, 50],       "bins":50}})
binnedList.update({"high_pt":  {"varName":"|p_{T}|",                                        "Var":"lep_pt",                                             "abs":1, "cuts":[0, 100],      "bins":100}})
binnedList.update({"eta":      {"varName":"|etaSc|" if args.flavour=='ele' else "|#eta|",   "Var":"lep_etaSc" if args.flavour=='ele' else "lep_eta",    "abs":1, "cuts":[0, 2.5],      "bins":50}})
binnedList.update({"nTrueInt": {"varName":"N_{vertex}",                                       "Var":"nTrueInt",                                           "abs":0, "cuts":[0, 50],       "bins":50}})

###############
# define cuts #
###############

#preselection
if args.flavour=='ele':
    loose_id = "abs(lep_pdgId)==11&&lep_pt>7&&abs(lep_eta)<2.5&&lep_miniRelIso<0.4&&lep_sip3d<8&&abs(lep_dxy)<0.05&&abs(lep_dz)<0.1&&lep_lostHits<=1"
    sample.setSelectionString(loose_id)
else:
    loose_id = "abs(lep_pdgId)==13&&lep_pt>5&&abs(lep_eta)<2.4&&lep_miniRelIso<0.4&&lep_sip3d<8&&abs(lep_dxy)<0.05&&abs(lep_dz)<0.1&&lep_pfMuonId&&lep_mediumMuonId"
    sample.setSelectionString(loose_id)

## pt selection
#kinematic_selection = "lep_pt>{ptMin}".format(ptMin = args.ptMin) if args.ptMax==0 else "lep_pt>{ptMin}&&lep_pt<={ptMax}".format(ptMin = args.ptMin, ptMax = args.ptMax)
#
#ptCuts=[]
#ptCuts.append({"Name":"pt{ptMin}to{ptMax}".format(ptMin=args.ptMin, ptMax='Inf' if args.ptMax==0 else args.ptMax),"lower_limit":int(args.ptMin), "upper_limit":float("Inf") if args.ptMax==0 else int(args.ptMax)})

relIsoCuts = [0.5]

logY=0

ptCuts=[]
if args.binned=='pt':
    ptCuts.append({"Name":"pt10to200", "lower_limit":10, "upper_limit":200         })
elif args.binned=='low_pt':
    ptCuts.append({"Name":"pt15to50" ,"lower_limit":15, "upper_limit":50})
    #ptCuts.append({"Name":"pt10to50" ,"lower_limit":10, "upper_limit":50})
    #ptCuts.append({"Name":"pt10to25" ,"lower_limit":10, "upper_limit":25})
elif args.binned=='high_pt':
    ptCuts.append({"Name":"pt50to100","lower_limit":50, "upper_limit":100})
    #ptCuts.append({"Name":"pt50toInf","lower_limit":50, "upper_limit":float("Inf")})
    #ptCuts.append({"Name":"pt25toInf","lower_limit":25, "upper_limit":float("Inf")})
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

def eS_err(p, rocdataset):
    ntruth=0.
    ntruthid=0.
    for data in rocdataset:
        if data[0]==1:
            ntruth+=data[2]
            if data[1]>=p:
                ntruthid+=data[2]
    #print ntruth, ntruthid
    return 0. if ntruth==0. else sqrt(1./ntruth*(ntruthid/ntruth)*(1.-ntruthid/ntruth))

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

def eB_err(p, rocdataset):
    ntruth=0.
    ntruthid=0.
    for data in rocdataset:
        if not data[0]==1:
            ntruth+=data[2]
            if data[1]>=p:
                ntruthid+=data[2]
    #print ntruth, ntruthid
    return 0. if ntruth==0. else sqrt(1./ntruth*(ntruthid/ntruth)*(1.-ntruthid/ntruth))

for relIsoCut in relIsoCuts:

    for ptCut in ptCuts:    

        kinematic_selection_name = 'pt > '+str(ptCut["lower_limit"])+' GeV' if ptCut["upper_limit"]==float("Inf") else str(ptCut["lower_limit"])+' GeV < pt < '+str(ptCut["upper_limit"])+' GeV'
        colorList=[]
        lineWidthList=[]
        
        #Initialize Mulitgraph
        gStyle.SetOptTitle(0)
        #gStyle.SetLegendBorderSize(0)
        #gStyle.SetFillStyle(4000)
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
            x        = array('d')
            x_err    = array('d')
            y_eS     = array('d')
            y_eB     = array('d')
            y_eS_err = array('d')
            y_eB_err = array('d')
            
            WP = plot["eS"]/100.

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
                if eSVal<=WP and not eSVal<=0.:
                    maxpval = pval
                    break

                print maxpval, pval, eSVal

            #calculate bin values
            factor = 3. if not ptCut["Name"]=="pt10to25" else 1.
            for dataset in readerData:
                j += 1
                if not len(dataset)==0:
                    x.append(j*binWidth)
                    x_err.append(0.)
                    y_eS.append(eS(maxpval,dataset))
                    y_eB.append(eB(maxpval,dataset)*factor)
                    y_eS_err.append(eS_err(maxpval,dataset))
                    y_eB_err.append(eB_err(maxpval,dataset))

                    print j*binWidth, maxpval, y_eB[-1], y_eS[-1], y_eS_err[-1], y_eB_err[-1]

            #Draw Graphs
            n=len(x)
            g.append(ROOT.TGraphErrors(n,x,y_eS,x_err,y_eS_err))
            gname=(plot["name"]+" sig eff ".format(sigeff=str(WP)))
            g[ng].SetName(gname)
            g[ng].SetTitle(gname)
            g[ng].SetLineColor( colorList[ng] )
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
            graph=ROOT.TGraphErrors(n,x,y_eB,x_err,y_eB_err)
            gname=(plot["name"]+" bkg eff "+("x "+str(int(factor))+" " if not ptCut["Name"]=="pt10to25" else "   "))
            graph.SetName(gname)
            graph.SetTitle(gname)
            #graph.SetLineStyle( 2 )
            graph.SetLineColor( colorList[ng] )
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
        mg.GetYaxis().SetTitle('sig, bkg eff')
        if logY==0:
            mg.GetYaxis().SetRangeUser(0.0,1.02)
        yleg1 = 0.37
        yleg2 = yleg1 + 0.24
        c.SetGrid()
        c.BuildLegend(0.60,yleg1,0.875,yleg2)

        header = [
        #{'text': ROOT.TPaveLabel(.00,0.96,.20,1.0,  "CMS preliminary",                                                                                                                   "nbNDC"), 'font': 30  },
        {'text': ROOT.TPaveLabel(.00,0.965,1.0,1.0,  "training reference: {trainData}  -  {ref}".format( trainData=flat_sampleInfo['train_data'], ref=flat_sampleInfo['training_name'] ), "nbNDC"), 'font': 130 },
        {'text': ROOT.TPaveLabel(.00,0.905,1.0,0.960, "{testData} {pt}, loose ID selection".format( testData=flat_sampleInfo['test_data'], pt=kinematic_selection_name ),                 "nbNDC"), 'font': 130 },
                 ]

        for line in header:
            line['text'].SetFillColor(gStyle.GetTitleFillColor())
            line['text'].SetTextFont(line['font'])
            line['text'].Draw()

        if args.flat:
            directory = os.path.join(   plot_directory, "DeepLepton",
                                        flat_sampleInfo['sample_name'],
                                        flat_sampleInfo['training_date'],
                                        'TestData' if args.testData else 'TrainData',
                                        'binnedEfficiencies',
                                        args.binned,
                                    )
        else:
            directory = os.path.join( plot_directory, "DeepLepton" )
        if not os.path.exists(directory):
            os.makedirs(directory)
        c.Print(os.path.join( directory, "binned_{binVar}_{kin}_{lumi}_eS_TTV{eS_TTV}_eS_DL{eS_DL}{eBscaled}.png".format( 
                            binVar = args.binned, kin = ptCut["Name"], lumi = 'lumi' if args.lumi_weight else 'noLumi',
                            eS_TTV = str(args.eS_TTV/100.), eS_DL = str(args.eS_DL/100.) , eBscaled = "_eBscaled" if factor!=1. else "" )))
        if args.binned=='pt':
            c.Print(os.path.join( directory, "root_binned_{binVar}_{kin}_{lumi}_eS_TTV{eS_TTV}_eS_DL{eS_DL}{eBscaled}.root".format( 
                                binVar = args.binned, kin = ptCut["Name"], lumi = 'lumi' if args.lumi_weight else 'noLumi',
                                eS_TTV = str(args.eS_TTV/100.), eS_DL = str(args.eS_DL/100.) , eBscaled = "_eBscaled" if factor!=1. else "" )))
