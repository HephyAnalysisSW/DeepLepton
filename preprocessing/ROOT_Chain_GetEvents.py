import ROOT
import os
import subprocess
import random

# Selection string: eg Job 0 of 50:
selectionString = "(event%50)==0&&abs(lep_pdgId)==flavour"

redirector =  "root://eos.grid.vbc.ac.at/"

Samples = [   'TTTo2L2Nu_noSC_pow',
              'TTTo2L2Nu_pow_CP5',
              'TTTo2L2Nu_pow',
              'TTToSemilepton_pow',
              'TTToSemilepton_pow_CP5',
              'TT_pow',
              
              'ST_schannel_4f_NLO',
              'ST_schannel_4f_CP5',
              'ST_tchannel_antitop_4f_pow',
              'ST_tchannel_antitop_4f_pow_CP5',
              'ST_tchannel_top_4f_pow',
              'ST_tchannel_top_4f_pow_CP5',
              'ST_tW_antitop_NoFullyHad_5f_pow',
              'ST_tW_antitop_5f_pow_ext1',
              'ST_tW_antitop_5f_pow_CP5',
              'ST_tW_top_NoFullyHad_5f_pow',
              'ST_tW_top_NoFullyHad_5f_pow_ext',
              'ST_tW_top_5f_pow_ext1',
              'ST_tW_top_5f_pow',
              'ST_tW_top_5f_pow_CP5',
              'ST_tWll_5f_LO',
              'ST_tWnunu_5f_LO',
             
              'THQ_LO',
              'THW_LO',
              
              'TTTT_NLO',
              'TTWW_NLO',
              'TTWZ_NLO',
              'TTZZ_NLO',

              'TTW_LO',
              'TTWJetsToLNu_NLO',
              'TTWJetsToQQ_NLO',
              'TTZToLLNuNu_NLO_ext2',
              'TTZToLLNuNu_NLO_ext3',
              'TTZToQQ_NLO',
              'TGG',
              ]

filesPrompt    = []
filesNonPrompt = []
filesFake      = []

for s in Samples:

    p = subprocess.Popen( ["xrdfs root://eos.grid.vbc.ac.at/ ls /eos/vbc/user/maximilian.moser/DeepLepton/v2/step1/2016/muo/Prompt/pt_3.5_-1/{}/".format(s)], 
                                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
    n = subprocess.Popen( ["xrdfs root://eos.grid.vbc.ac.at/ ls /eos/vbc/user/maximilian.moser/DeepLepton/v2/step1/2016/muo/NonPrompt/pt_3.5_-1/{}/".format(s)], 
                                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
    a = subprocess.Popen( ["xrdfs root://eos.grid.vbc.ac.at/ ls /eos/vbc/user/maximilian.moser/DeepLepton/v2/step1/2016/muo/Fake/pt_3.5_-1/{}/".format(s)], 
                                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )

    filesPrompt    += [ redirector+'/'+f.rstrip("\n") for f in p.stdout.readlines() if f.endswith('.root\n') ]
    filesNonPrompt += [ redirector+'/'+f.rstrip("\n") for f in n.stdout.readlines() if f.endswith('.root\n') ]
    filesFake      += [ redirector+'/'+f.rstrip("\n") for f in a.stdout.readlines() if f.endswith('.root\n') ]

random.shuffle(filesPrompt)
random.shuffle(filesNonPrompt)
random.shuffle(filesFake)


print(filesPrompt[0])
print(filesNonPrompt[0])
print(filesFake[0])

print(len(filesPrompt))
print(len(filesNonPrompt))
print(len(filesFake))

chainPrompt = ROOT.TChain("tree")
chainNonPrompt = ROOT.TChain("tree")
chainFake = ROOT.TChain("tree")


print("Building Prompt Chain")
for f in filesPrompt:
    chainPrompt.AddFile(f)

print("Building NonPrompt Chain")
for f in filesNonPrompt:
    chainNonPrompt.AddFile(f)

print("Building Fake Chain")
for f in filesFake:
    chainFake.AddFile(f)

print("Getting Prompt Entries")
print(chainPrompt.GetEntries(selectionString))

print("Getting NonPrompt Entries")
print(chainNonPrompt.GetEntries(selectionString))

print("Getting Fake Entries")
print(chainFake.GetEntries(selectionString))


