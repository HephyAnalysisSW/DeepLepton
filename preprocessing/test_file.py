import ROOT
import sys
c = ROOT.TChain('tree')
c.Add('root://eos.grid.vbc.ac.at/'+sys.argv[1])
n = c.GetEntries("run>0")
if n>0:
    sys.exit(0) 
else:   
    sys.exit(1) 
