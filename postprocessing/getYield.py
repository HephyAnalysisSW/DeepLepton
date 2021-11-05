import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions=True
import os
from copy import deepcopy
from RootTools.core.standard import *
from DeepLepton.Tools.helpers import getCollection
from Samples.nanoAOD.Autumn18_private_nanoAODv6 import TTLep_pow, TTSingleLep_pow, TTHad_pow, TTbar, TTLep_NLO

sample_list = [TTLep_pow, TTSingleLep_pow, TTHad_pow, TTbar, TTLep_NLO]
for s in sample_list:
    print(s.name, s.xSection)

import argparse
argParser = argparse.ArgumentParser(description="Parser for getYield to select sample")

argParser.add_argument('--logLevel',
                       action='store',
                       nargs='?',
                       choices=['CRITICAL',
                                'ERROR',
                                'WARNING',
                                'INFO',
                                'DEBUG',
                                'TRACE',
                                'NOTSET',
                                'SYNC'],
                       default='INFO',
                       help="Log level for logging")

argParser.add_argument('--sample',
                       action='store',
                       nargs='?',
                       type=str,
                       default='TTLep_pow',
                       help="sample name from Samples repository")

argParser.add_argument('--nJobs',
                       action='store',
                       nargs='?',
                       type=int,
                       default=1,
                       help="Maximum number of simultaneous jobs.")

argParser.add_argument('--job',
                       action='store',
                       type=int,
                       default=0,
                       help="Run only job i")
argParser.add_argument('--small',
                        action='store_true')

args = argParser.parse_args()

import RootTools.core.logger as logger_rt
import DeepLepton.Tools.logger as logger
# Logging
logger = logger.get_logger(args.logLevel, logFile=None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile=None)

logger.info("loaded samples")


preselection = ["MET_pt>200", "Sum$(Jet_pt * (Jet_pt>30))>300", "(Sum$(Jet_pt>100)) >= 1", "Sum$(Jet_pt>60)<3", "nMuon>=1", "Sum$(Muon_pt>20)<2", "nTau==0", "Muon_pt<=30"]

preselection = "&&".join(preselection)

def select(r, jet, lep):
    result = []
    result.append(r.MET_pt>200)
    result.append((sum(j.get("pt")*(j.get("pt")>30) for j in jet))>300)
    result.append((sum(j.get("pt")>100 for j in jet))>=1)
    result.append((sum(j.get("pt")>60 for j in jet))<3)
    result.append(r.nMuon >= 1)
    result.append((sum(l.get("pt")>20 for l in lep))<2)
    result.append(r.nTau==0)
    result.append(lep[0]["pt"]<=30)
    jet2 = deepcopy(jet)
    store = False
    for j1 in jet:
        jet2.pop(0)
        for j2 in jet2:
            if j2["pt"]>60 and abs(j1["phi"]-j2["phi"])<=2.5:
                store = True
                break
    result.append(store)
    if len(lep) >1:
        print("found multiple muons")
    print(result)
    return False if 0 in result else True

r_vars = ["MET_pt/F", "nMuon/I", "nTau/I", "genWeight/F"]
jet_vars = ["pt/F", "phi/F"]
read_vars = [VectorTreeVariable.fromString("Jet[{}]".format(",".join(jet_vars)))]
lep_vars = ["pt/F","phi/F"]
read_vars.append(VectorTreeVariable.fromString("Muon[{}]".format(",".join(lep_vars))))
read_vars.append("nJet/I")
read_vars.extend(r_vars)

jet_vars = map( lambda n:n.split('/')[0], jet_vars )
lep_vars = map( lambda n:n.split('/')[0], lep_vars)

PATH = ["/eos/vbc/experiments/cms/store/user/schoef/TT_DiLept_TuneCP5_13TeV-amcatnlo-pythia8/crab_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2_v6_PFCands/211014_093110/0000"]

chain = ROOT.TChain("Events")
icnt = 0 
for path in PATH:
    for name in os.listdir(path):
        if name.endswith(".root"):
            if icnt >0:
                break
            chain.Add("{}/{}".format(path, name))
            print(name)
            icnt += 1

sample = Sample.fromDirectory("ttbar", PATH, redirector="root://eos.grid.vbc.ac.at/",\
            selectionString = preselection, weightString = None, normalization = None,\
            xSection = -1,  treeName = "Events")
if args.small:
    sample.reduceFiles(to=1)
reader = sample.treeReader(variables = map( lambda v: TreeVariable.fromString(v) if type(v)==type("") else v, read_vars),
                selectionString = None)
print("init reader")
reader.start()
counter = 0
while reader.run():
    print(counter)
    r = reader.event
    jet = getCollection(r, "Jet", jet_vars, "nJet")
    # print(r.Muon_pt)
    lep = getCollection(r, "Muon", ["pt",], "nMuon")
    # print(jet)
    # print(lep)
    # print(len(lep))
    # print(type(lep))
    # print(select(r, jet))
    if counter < 0:
        break
    counter +=1
    if not select(r, jet, lep):
        print("happens if there are several muons and bec of ISR jet")
        # break
    else:
        weight = r.genWeight
        print(weight)
print(reader.nEvents)
print(sample._chain.GetEntries())
print(chain.GetEntries(preselection))





