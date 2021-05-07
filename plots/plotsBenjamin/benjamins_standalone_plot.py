#!/usr/bin/env python

from __future__ import print_function

import os

import ROOT

PATH = "/eos/vbc/user/robert.schoefbeck/DeepLepton/nanoAODUL17_PFCands/signal_stops_compressed"

def isFromSUSY(event, genpart_id):
    tmp_index = genpart_id
    while(tmp_index > 0 and abs(event.GenPart_pdgId[tmp_index]) not in [1000006, 1000022]):
        tmp_index = event.GenPart_genPartIdxMother[tmp_index]

    # print("tmp index = {}, pdgId = {}".format(tmp_index, event.GenPart_pdgId[tmp_index]))

    if abs(event.GenPart_pdgId[tmp_index]) in [1000006, 1000022]:
        return True
    else:
        return False
hist_stop = ROOT.TH1D("muon from stop", "title;x-label;ylabel", 100, -5, 5)
hist_prompt = ROOT.TH1D("prompt muon", "title;d_{xy} [cm];Nr. of events", 100, -5, 5)
hist_notprompt = ROOT.TH1D("notprompt muon", "title;x;y", 100, -5, 5)

def main():
    # here we select from the file (which contains several trees) the
    # event tree. we then put these into the chain
    # (a chain is a collection of trees)
    chain = ROOT.TChain("Events")
    # This is to run the program not over the fuse mount because like this 
    # the program is more reliable, especially when processing large quantities
    # of data
    # root:// is the protocoll to be used 
    # another protocol is https://
    for name in os.listdir(PATH):
        chain.Add("root://eos.grid.vbc.ac.at//{}/{}".format(PATH, name))


    # particle ids can be found in
    # https://pdg.lbl.gov/2007/reviews/montecarlorpp.pdf

    icnt = 0
    for event in chain:
        icnt += 1
        if icnt < 2:
            print_GenPart(event)

        # for i in range(event.nGenPart):

        #     # follow leptons to their origin from SUSY particles
        #     if abs(event.GenPart_pdgId[i]) in [11, 13]:
        #         #print("The lepton is from susy: {}".format(isFromSUSY(event, i)))
        #         if isFromSUSY(event, i):
        #             # hist_stop.Fill()
        #             print("index = {}, nsv = {}".format(i, event.nSV))
        for n in range(event.nMuon):
            # print()
            # print("With the muon class:")
            # print("The genPartIdx is {}".format(event.Muon_genPartIdx[n]))
            # print("Is the muon from Susy: {}".format(isFromSUSY(event, event.Muon_genPartIdx[n])))
            # print("Muon_genPartFlav = {}".format(event.Muon_genPartFlav[n]))
            if isFromSUSY(event, event.Muon_genPartIdx[n]):
                hist_stop.Fill(event.Muon_dxy[n])
            else:
                if event.Muon_genPartFlav[n]==1:
                    hist_prompt.Fill(event.Muon_dxy[n])
                else:
                    hist_notprompt.Fill(event.Muon_dxy[n])
        # for n in range(event.nElectron):
        #     print()
        #     print("With the electron class:")
        #     print("Is the electron from Susy: {}".format(isFromSUSY(event, event.Electron_genPartIdx[n])))
        if icnt >= 100:
            break


def print_GenPart(event):

    print(
        "| Index  | Mother | PDG_id   | Status | Flags  |      Mass |       p_t |       eta |      phi |"
    )
    print(
        "-----------------------------------------------------------------------------------------------"
    )
    for i in range(event.nGenPart):
        print(
            "| {:6d} | {:6d} | {:8d} | {:6d} | {:06x} | {:9.2f} | {:9.2f} | {:9.2f} | {:9.2f} |".format(
                i,
                event.GenPart_genPartIdxMother[i],
                event.GenPart_pdgId[i],
                event.GenPart_status[i],
                event.GenPart_statusFlags[i],
                event.GenPart_mass[i],
                event.GenPart_pt[i],
                event.GenPart_eta[i],
                event.GenPart_phi[i],
            )
        )


if __name__ == "__main__":

    main()
    c1 = ROOT.TCanvas("c1", "L", 200,100,1000,1000)
    c1.SetLogy()
    c1.Divide(2, 2)
    c1.cd(1)

    hist_stop.SetTitle("#mu from SUSY; d_{xy} [cm]; Nr. Events")
    hist_stop.SetLineColorAlpha(2, 0.7)
    hist_stop.Scale(1.)

    hist_notprompt.SetTitle("Not prompt")
    hist_notprompt.SetLineColorAlpha(3, 0.7)
    hist_notprompt.Scale(1.)

    hist_prompt.SetTitle("Prompt")
    hist_prompt.SetLineColorAlpha(4, 0.7)
    hist_prompt.Scale(1.)

    hist_stop.Draw()
    hist_notprompt.Draw("SAME")
    hist_prompt.Draw("SAME")

    c1.BuildLegend(0.7,0.4, 1, 0.6)

# Here the muons from susy non-prompt
    c1.cd(2)        

# Here the relIso and AbsIso plots
    c1.cd(3)
    # Do stuff

    c1.cd(4)
    # Do stuff

    c1.Print('/users/benjamin.wilhelmy/StandealonePlotting/muon_multiplefeatures.png')

