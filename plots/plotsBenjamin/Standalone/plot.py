#!/usr/bin/env python
''' 
This is a very basic plotting program aiming at plotting basic features of
simulated data such as:
    d_xy of muons -> Normalized to 1
    relIso of muons
    absIso of muons
! THE PATH FOR SAVING IS HARDCODED ADJUST IF NECCESSARY !
'''

from __future__ import print_function
import os
import time
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.EnableImplicitMT()

# import cProfile
# import pstats

t_start = time.perf_counter()

PATH = "/eos/vbc/user/robert.schoefbeck/DeepLepton/nanoAODUL17_PFCands/signal_stops_compressed"


def isFromSUSY(event, genpart_id):
    '''
    This function reconstructs from which particle the muon candidate originates from,
    especially if its from a susy particle (>1000000)
    returns True if it has a susy particle as mother
    '''
    tmp_index = genpart_id
    while(tmp_index > 0 and abs(event.GenPart_pdgId[tmp_index]) <= 1000000):
        tmp_index = event.GenPart_genPartIdxMother[tmp_index]

    if abs(event.GenPart_pdgId[tmp_index]) > 1000000:
        return True
    else:
        return False

def isFromSUSYnonprompt(event, genpart_id):
    '''(genpart_id is the index of GenPart)
    This function goes back in the history of the lepton (muon) and finds out if it comes
    directly from the susy particle (stop=1000006), meaning the only intermediate
    particles allowed are the lepton itself and W-bosons

    returns True if the lepton came from other intermediate particles for example:
        b/c or mesons, etc...
    returns False if the lepton came 'directly' from the susy particle 
    '''
    tmp_index = genpart_id
    lep_pdgId = event.GenPart_pdgId[tmp_index]

    # check if the mother is the same particle or a W-boson
    while(lep_pdgId == event.GenPart_pdgId[tmp_index] or abs(event.GenPart_pdgId[tmp_index]) in [24, 34]):
        tmp_index = event.GenPart_genPartIdxMother[tmp_index]

    # check if the previous particle was a susy particle
    if event.GenPart_pdgId[tmp_index] > 1000000:
        # then the lepton came directly from susy part.
        return False
    else:
        return True

def isFakelep(event, Muon_index, GenPart_index):
    '''determines if the given lepton is real(False) or fake(True)
    '''
    result = False if event.Muon_pdgId[Muon_index] == event.GenPart_pdgId[GenPart_index] else True
    return result

dxy_bins = 100
dxy_range = 5
Iso_bins = 100
absIso_range = 200
# xaxis range for relIso04:
relIso_range = 50
relIso_range03 = 15


hist_stop = ROOT.TH1D("#mu d_{xy} directly from susy", "#mu d_{xy} directly from susy",dxy_bins, -dxy_range, dxy_range)
hist_stop_nonprompt = ROOT.TH1D("#mu d_{xy} from susy, nonprompt", "#mu d_{xy} from susy, nonprompt", dxy_bins, -dxy_range, dxy_range)
hist_prompt = ROOT.TH1D("#mu d_{xy} prompt", "#mu d_{xy} prompt", dxy_bins, -dxy_range, dxy_range)
hist_notprompt = ROOT.TH1D("#mu d_{xy} notprompt", "#mu d_{xy} notprompt", dxy_bins, -dxy_range, dxy_range)
h_fake_dxy = ROOT.TH1D("Fake #mu d_{xy}", "Fake #mu d_{xy}", dxy_bins, -dxy_range, dxy_range)


# plot only for pt >=20
h_stop_relIso = ROOT.TH1D("#mu relIso directly from susy", "#mu relIso directly from susy", Iso_bins, 0, relIso_range03)
h_stop_nprom_relIso = ROOT.TH1D("#mu relIso from susy, nonprompt", "#mu relIso from susy, nonprompt", Iso_bins, 0, relIso_range03)
h_prompt_relIso = ROOT.TH1D("#mu relIso prompt", "#mu relIso prompt", Iso_bins, 0, relIso_range03)
h_notprompt_relIso = ROOT.TH1D("#mu relIso notprompt", "#mu relIso notprompt", Iso_bins, 0, relIso_range03)
h_fake_relIso = ROOT.TH1D("Fake #mu relIsoR03", "Fake #mu relIsoR03", Iso_bins, 0, relIso_range03)

# histograms for pt <20 -> abs iso
h_stop_absIso = ROOT.TH1D("#mu absIso directly from susy", "#mu absIso directly from susy", Iso_bins, 0, absIso_range)
h_stop_nprom_absIso = ROOT.TH1D("#mu absIso from susy, nonprompt", "#mu absIso from susy, nonprompt", Iso_bins, 0, absIso_range)
h_prompt_absIso = ROOT.TH1D("#mu absIso prompt", "#mu absIso prompt", Iso_bins, 0, absIso_range)
h_notprompt_absIso = ROOT.TH1D("#mu absIso notprompt", "#mu absIso notprompt", Iso_bins, 0, absIso_range)
h_fake_absIso = ROOT.TH1D("Fake #mu absIsoR03", "Fake #mu absIsoR03", Iso_bins, 0, relIso_range)


h_dR04_stop_relIso = ROOT.TH1D("#mu relIso04 directly from susy", "#mu relIso04 directly from susy", Iso_bins, 0, relIso_range)
h_dR04_stop_nproom_relIso = ROOT.TH1D("#mu relIso04 from susy, nonprompt", "#mu relIso04 from susy, nonprompt", Iso_bins, 0, relIso_range)
h_dR04_prompt_relIso = ROOT.TH1D("#mu relIso04 prompt", "#mu relIso04 prompt", Iso_bins, 0, relIso_range)
h_dR04_notprompt_relIso = ROOT.TH1D("#mu relIso04 notprompt", "#mu relIso04 notprompt", Iso_bins, 0, relIso_range)
h_dR04_fake_relIso = ROOT.TH1D("Fake #mu relIso04", "Fake #mu relIso04", Iso_bins, 0, relIso_range)

h_dR04_stop_absIso = ROOT.TH1D("#mu absIso04 directly from susy", "#mu absIso04 directly from susy", Iso_bins, 0, absIso_range)
h_dR04_stop_nproom_absIso = ROOT.TH1D("#mu absIso04 from susy, nonprompt", "#mu absIso04 from susy, nonprompt", Iso_bins, 0, absIso_range)
h_dR04_prompt_absIso = ROOT.TH1D("#mu absIso04 prompt", "#mu absIso04 prompt", Iso_bins, 0, absIso_range)
h_dR04_notprompt_absIso = ROOT.TH1D("#mu absIso04 notprompt", "#mu absIso04 notprompt", Iso_bins, 0, absIso_range)
h_dR04_fake_absIso = ROOT.TH1D("Fake #mu absIso04", "Fake #mu absIso04", Iso_bins, 0, absIso_range)

maxiter = 10000
def main():
    chain = ROOT.TChain("Events")
    for name in os.listdir(PATH):
        chain.Add("root://eos.grid.vbc.ac.at//{}/{}".format(PATH, name))

    icnt = 0
    for event in chain:
        icnt += 1
        for n in range(event.nMuon):
            if isFakelep(event, n, event.Muon_genPartIdx[n]):
                h_fake_dxy.Fill(event.Muon_dxy[n])
                if event.Muon_pt[n] >= 20:
                    h_fake_relIso.Fill(event.Muon_pfRelIso03_all[n])
                    h_dR04_fake_relIso.Fill(event.Muon_pfRelIso04_all[n])
                else: 
                    h_fake_absIso.Fill(event.Muon_pfRelIso03_all[n] * event.Muon_pt[n])
                    h_dR04_fake_absIso.Fill(event.Muon_pfRelIso04_all[n] * event.Muon_pt[n])
        
            elif isFromSUSY(event, event.Muon_genPartIdx[n]):
                if not isFromSUSYnonprompt(event, event.Muon_genPartIdx[n]):
                    hist_stop.Fill(event.Muon_dxy[n])
                    if event.Muon_pt[n] >= 20:
                        h_stop_relIso.Fill(event.Muon_pfRelIso03_all[n])
                        h_dR04_stop_relIso.Fill(event.Muon_pfRelIso04_all[n])
                    else:
                        h_stop_absIso.Fill(event.Muon_pfRelIso03_all[n]*event.Muon_pt[n])
                        h_dR04_stop_absIso.Fill(event.Muon_pfRelIso04_all[n]*event.Muon_pt[n])
                else:
                    hist_stop_nonprompt.Fill(event.Muon_dxy[n])
                    if event.Muon_pt[n] >=20:
                        h_stop_nprom_relIso.Fill(event.Muon_pfRelIso03_all[n])
                        h_dR04_stop_nproom_relIso.Fill(event.Muon_pfRelIso04_all[n])
                    else:
                        h_stop_nprom_absIso.Fill(event.Muon_pfRelIso03_all[n]*event.Muon_pt[n])
                        h_dR04_stop_nproom_absIso.Fill(event.Muon_pfRelIso04_all[n]*event.Muon_pt[n])
            else:
                if event.Muon_genPartFlav[n]==1:
                    hist_prompt.Fill(event.Muon_dxy[n])
                    if event.Muon_pt[n] >= 20:
                        h_prompt_relIso.Fill(event.Muon_pfRelIso03_all[n])
                        h_dR04_prompt_relIso.Fill(event.Muon_pfRelIso04_all[n])
                    else:
                        h_prompt_absIso.Fill(event.Muon_pfRelIso03_all[n]*event.Muon_pt[n])
                        h_dR04_prompt_absIso.Fill(event.Muon_pfRelIso04_all[n]*event.Muon_pt[n])

                else:
                    hist_notprompt.Fill(event.Muon_dxy[n])
                    if event.Muon_pt[n] >= 20:
                        h_notprompt_relIso.Fill(event.Muon_pfRelIso03_all[n])
                        h_dR04_notprompt_relIso.Fill(event.Muon_pfRelIso04_all[n])
                    else:
                        h_notprompt_absIso.Fill(event.Muon_pfRelIso03_all[n]*event.Muon_pt[n])
                        h_dR04_notprompt_absIso.Fill(event.Muon_pfRelIso04_all[n]*event.Muon_pt[n])
        if icnt >= maxiter:
            break


def scaling(histogram):
    '''Rescales the histogram s.t. the normalization is 1
    '''
    try:
        scale = 1./histogram.Integral()
        histogram.Scale(scale, option = "nosw2")
    except:
        print("{} has no events -> normalization failed".format(histogram.GetName()))

def makehisto(list_hists, title, outputname, xlabel, ylabel):
    '''takes a list of histograms or a histogram and makes and stores the plot
    '''
    canv = ROOT.TCanvas("c1", "L", 1200, 1200)
    canv.SetLogy()
    legend = ROOT.TLegend(0.67,0.44,0.98,0.74)
    color_cnt = 2
    if type(list_hists) != type([]):
        list_hists = [list_hists]
    
    maxval = []
    for hist in list_hists:
        scaling(hist)
        maxval.append(hist.GetMaximum())
    ymax = max(maxval)*1.1
    print("interval of maxval: {}, ymax = {}".format(maxval, ymax))
    for hist in list_hists:
        legend.AddEntry(hist, hist.GetTitle(), "l")
        hist.SetTitle("{}".format(title))
        hist.SetLineColorAlpha(color_cnt, 1)
        hist.SetXTitle(xlabel)
        hist.SetYTitle(ylabel)
        hist.GetYaxis().SetTitleOffset(1.0)
        hist.GetXaxis().SetTitleOffset(1.1)
        hist.SetMaximum(ymax) # good for most plots ymax = 1.2
        color_cnt += 1
        hist.Draw("SAME")

    legend.SetTextSize(0.02)
    # Sets the fraction of the width which the symbol in the legend takes
    legend.SetMargin(0.1)
    legend.Draw("SAME")
    canv.Print("/users/benjamin.wilhelmy/StandealonePlotting/plots/{}".format(outputname)+".png", "png")
    print("/users/benjamin.wilhelmy/StandealonePlotting/plots/{}".format(outputname)+".png")


if __name__ == "__main__":
    #pr = cProfile.Profile()
    #pr.enable()
    main()
    #pr.disable()

    dxy_histos = [hist_stop, hist_stop_nonprompt, hist_prompt, hist_notprompt, h_fake_dxy]
    makehisto(dxy_histos, "d_{xy} for #mu", "mu_dxy_{}".format(maxiter), "d_{xy}[cm] for #mu", "Nr. Events")
   
    relIso_histos = [h_stop_relIso, h_stop_nprom_relIso, h_prompt_relIso, h_notprompt_relIso, h_fake_relIso]
    makehisto(relIso_histos, "relIso dR03 all for #mu with p_{t} #geq 20 GeV", "relIso_{}".format(maxiter), "relIsodR03_all for #mu", "Nr. Events")

    absIso_histos = [h_stop_absIso, h_stop_nprom_absIso, h_prompt_absIso, h_notprompt_absIso, h_fake_absIso]
    makehisto(absIso_histos, "absIso dR03 all for #mu with p_{t} < 20 GeV", "absIso_{}".format(maxiter), "p_{t} * relIsodR03_all for #mu", "Nr.Events")

    relIso_04_histos = [h_dR04_stop_relIso, h_dR04_stop_nproom_relIso, h_dR04_prompt_relIso, h_dR04_notprompt_relIso, h_dR04_fake_relIso]
    makehisto(relIso_04_histos, "relIso dR04 all for #mu with p_{t} #geq 20 GeV", "relIso_dR04_{}".format(maxiter), "relIsodR04_all for #mu", "Nr. Events")
    
    # pr.enable()
    absIso_04_histos = [h_dR04_stop_absIso, h_dR04_stop_nproom_absIso, h_dR04_prompt_absIso, h_dR04_notprompt_absIso, h_dR04_fake_absIso]
    makehisto(absIso_04_histos, "absIso dR04 all for #mu with p_{t} < 20 GeV", "absIso_dR04_{}".format(maxiter), "p_{t} * relIsodR04_all for #mu", "Nr. Events")
    # pr.create_stats()
    # pr.dump_stats("myownProfiling")
    # pr.print_stats()
    # mystats = pstats.Stats("myownProfiling")
    # mystats.add("myownProfiling")
    # mystats.strip_dirs()
    # mystats.sort_stats('tottime', 'ncalls')
    # mystats.print_stats()
t_end = time.perf_counter()
print("Total time elapsed {}".format(int(t_end - t_start)))
