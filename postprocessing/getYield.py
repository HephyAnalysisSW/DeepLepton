import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions=True
import os
from copy import deepcopy
from RootTools.core.standard import *
from DeepLepton.Tools.helpers import getCollection
from Samples.nanoAOD.Autumn18_private_nanoAODv6 import TTLep_pow, TTSingleLep_pow, TTHad_pow, TTbar, TTLep_NLO

bkg_sample_list = [TTLep_pow, TTSingleLep_pow, TTHad_pow, TTbar, TTLep_NLO]
signal_sample_list = ["Stop250dm10", "Stop250dm20",
                      "Stop600dm10", "Stop600dm20"]
# for s in sample_list:
#     print(s.name, s.xSection)

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
                       choices = ["TTLep_pow", "TTSingleLep_pow",
                                  "TTHad_pow", "TTbar", "TTLep_NLO",
                                  "Stop250dm10", "Stop250dm20",
                                  "Stop600dm10", "Stop600dm20"],
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

compressed_id = "Muon_pt<=25 ? (Muon_pfRelIso03_all * Muon_pt < 5.0 ? 1:0) : (Muon_pfRelIso03_all < 0.2 ? 1 : 0)"
preselection = ["MET_pt>200",
                "Sum$(Jet_pt * (Jet_pt>30 && abs(Jet_eta)<2.4))>300",
                "(Sum$(Jet_pt>100 && abs(Jet_eta)<2.4)) >= 1",
                "Sum$((Jet_pt>60 && abs(Jet_eta)<2.4))<3",
                "nMuon>=1",
                "Sum$((Muon_pt>20 && {}))<2".format(compressed_id),
                "nTau==0",
                "Muon_pt<=30"
                ]

preselection = "&&".join(preselection)

def select(r, jet, lep):
    result = []
    result.append(r.MET_pt>200)
    result.append((sum(j.get("pt")*(j.get("pt")>30 and abs(j.get("eta") < 2.4)) for j in jet))>300)
    result.append((sum( (j.get("pt")>100 and abs(j.get("eta") < 2.4)) for j in jet))>=1)
    result.append((sum( (j.get("pt")>60 and abs(j.get("eta") < 2.4)) for j in jet))<3)
    result.append(r.nMuon >= 1)
    # compressed id:
    comp_id = True
    for l in lep:
        # print(l.keys())
        if l["pt"] <= 25:
            if l["pfRelIso03_all"]*l["pt"] < 5.0:
                comp_id *= True
            else:
                comp_id *= False
        else:
            if l["pfRelIso03_all"] < 0.2:
                comp_id *= True
            else:
                comp_id *= False
    result.append((sum((l.get("pt")>20 and comp_id  for l in lep))<2))
    result.append(r.nTau==0)
    # TODO: needs modification
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
    # if len(lep) >1:
    #     pass
        # print("found multiple muons")

    # print(result)
    return False if 0 in result else True

data_paths = {"TTLep_pow":[os.path.join("/eos/vbc/experiments/cms/store/user/schoef/",
                            "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/",
                            "crab_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_v6_PFCands/",
                            "211014_093132/0000")],
              "TTSingleLep_pow":[os.path.join("/eos/vbc/experiments/cms/store/user/schoef/",
                                  "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/",
                                  "crab_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_v6_PFCands/",
                                  "211014_093234/0000")],
              "TTHad_pow":[os.path.join("/eos/vbc/experiments/cms/store/user/schoef/",
                            "TTToHadronic_TuneCP5_13TeV-powheg-pythia8/",
                            "crab_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_v6_PFCands/",
                            "211014_093156/0000"),
                           os.path.join("/eos/vbc/experiments/cms/store/user/schoef/",
                            "TTToHadronic_TuneCP5_13TeV-powheg-pythia8/",
                            "crab_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_v6_PFCands/",
                            "211014_093156/0001")],
              "TTbar":[os.path.join("/eos/vbc/experiments/cms/store/user/schoef/",
                        "TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/",
                        "crab_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_v6_PFCands/",
                        "211014_093046/0000")],
              "TTLep_NLO":[os.path.join("/eos/vbc/experiments/cms/store/user/",
                            "schoef/TT_DiLept_TuneCP5_13TeV-amcatnlo-pythia8/",
                            "crab_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2_v6_PFCands/",
                            "211014_093110/0000")],
              "Stop250dm10":["/eos/vbc/experiments/cms/store/user/liko/CompStop/SUS-RunIIAutumn18FSPremix-Stop250-dm10-006-nanoAOD/210819_215726/0000"],
              "Stop250dm20":["/eos/vbc/experiments/cms/store/user/liko/CompStop/SUS-RunIIAutumn18FSPremix-Stop250-dm20-006-nanoAOD/210819_215740/0000"],
              "Stop600dm10":["/eos/vbc/experiments/cms/store/user/liko/CompStop/SUS-RunIIAutumn18FSPremix-Stop600-dm10-006-nanoAOD/210819_215757/0000"],
              "Stop600dm20":["/eos/vbc/experiments/cms/store/user/liko/CompStop/SUS-RunIIAutumn18FSPremix-Stop600-dm20-006-nanoAOD/210819_215811/0000"],
                            }

signal_sample_norms = {"Stop250dm10": "genEventSumw_T2tt_dM_10to80_genHT_160_genMET_80_250_240",
                       "Stop250dm20": "genEventSumw_T2tt_dM_10to80_genHT_160_genMET_80_250_230",
                       "Stop600dm10": "genEventSumw_T2tt_dM_10to80_genHT_160_genMET_80_600_590",
                       "Stop600dm20": "genEventSumw_T2tt_dM_10to80_genHT_160_genMET_80_600_580"
                        }
L = 137.
is_signal = False
PATH = data_paths[args.sample]

NORMALIZATION = 0
if args.sample in signal_sample_list:
    # get the xsec and br ...
    is_signal = True
    sample_normalization = Sample.fromDirectory(args.sample + "_norm",
                                                PATH,
                                                redirector="root://eos.grid.vbc.ac.at/",
                                                treeName = "Runs")
    v = ["{}/D".format(signal_sample_norms[args.sample])]
    norm_reader = sample_normalization.treeReader(variables = map( lambda v: TreeVariable.fromString(v) \
                                            if type(v)==type("") else v, v),
                                                  selectionString = None)
    norm_reader.start()
    while norm_reader.run():
        r = norm_reader.event
        NORMALIZATION += getattr(r, signal_sample_norms[args.sample]) 
   # TODO: 
    XSecBR = -1
    logger.info("found a normalization {}".format(NORMALIZATION))

else:
    bkg_sample = eval(args.sample)
    XSecBR = bkg_sample.xSection 
    NORMALIZATION = bkg_sample.normalization

logger.info("selected path is \n {}".format(PATH))
logger.info("Found xsec {} and normalization {}".format(XSecBR, NORMALIZATION))


r_vars = ["MET_pt/F", "nMuon/I", "nTau/I", "genWeight/F"]
jet_vars = ["pt/F", "phi/F", "eta/F"]
read_vars = [VectorTreeVariable.fromString("Jet[{}]".format(",".join(jet_vars)))]
lep_vars = ["pt/F","phi/F", "eta/F", "pfRelIso03_all/F"]
read_vars.append(VectorTreeVariable.fromString("Muon[{}]".format(",".join(lep_vars))))
read_vars.append("nJet/I")
read_vars.extend(r_vars)

jet_vars = map( lambda n:n.split('/')[0], jet_vars )
lep_vars = map( lambda n:n.split('/')[0], lep_vars)

logger.info("constructing sample: {}".format(args.sample))
sample = Sample.fromDirectory(args.sample, PATH, redirector="root://eos.grid.vbc.ac.at/",\
            selectionString = preselection, weightString = None, normalization = NORMALIZATION,\
            xSection = XSecBR,  treeName = "Events")

if args.small:
    sample.reduceFiles(to=1)
logger.info("constructing reader")
reader = sample.treeReader(variables = map( lambda v: TreeVariable.fromString(v) \
                                            if type(v)==type("") else v, read_vars),
                           selectionString = None)
logger.info("starting reader")
reader.start()
# counter = 0
Yield = 0
event_counter = 0
signal_normalization = 0
while reader.run():
    r = reader.event
    jet = getCollection(r, "Jet", jet_vars, "nJet")
    lep = getCollection(r, "Muon", lep_vars, "nMuon")
    # signal_normalization += r.genWeight
    # Event must pass the selection:
    if select(r, jet, lep):
        weight = L*XSecBR*r.genWeight / float(NORMALIZATION)
        Yield += weight
        event_counter += 1

logger.info("Got yield = {}, with {} leptons passing selection".format(Yield, event_counter))
with open("/scratch-cbe/users/benjamin.wilhelmy/DeepLepton/Yields/yield_bkg_{}{}.txt".format("small_" if args.small else "", args.sample), "w") as f:
    f.write("Sample name: {} \n".format(args.sample))
    f.writelines("Yield: {} \n".format(Yield))
    f.write("{} events passed selection \n".format(event_counter))






