import ROOT
import os
import subprocess


redirector =  "root://eos.grid.vbc.ac.at/"

p = subprocess.Popen( ["xrdfs root://eos.grid.vbc.ac.at/ ls /eos/vbc/user/maximilian.moser/DeepLepton/v2/step1/2016/muo/Prompt/pt_3.5_-1/TT_pow/"], 
                                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
n = subprocess.Popen( ["xrdfs root://eos.grid.vbc.ac.at/ ls /eos/vbc/user/maximilian.moser/DeepLepton/v2/step1/2016/muo/Prompt/pt_3.5_-1/TT_pow/"], 
                                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
a = subprocess.Popen( ["xrdfs root://eos.grid.vbc.ac.at/ ls /eos/vbc/user/maximilian.moser/DeepLepton/v2/step1/2016/muo/Prompt/pt_3.5_-1/TT_pow/"], 
                                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )


filesPrompt    = [ redirector+'/'+f.rstrip("\n") for f in p.stdout.readlines() if f.endswith('.root\n') ]
filesNonPrompt = [ redirector+'/'+f.rstrip("\n") for f in n.stdout.readlines() if f.endswith('.root\n') ]
filesFake      = [ redirector+'/'+f.rstrip("\n") for f in a.stdout.readlines() if f.endswith('.root\n') ]


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
print(chainPrompt.GetEntries())

print("Getting NonPrompt Entries")
print(chainNonPrompt.GetEntries())

print("Getting Fake Entries")
print(chainFake.GetEntries())


