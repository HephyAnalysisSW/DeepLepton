import ROOT
import sys
c = ROOT.TChain('tree')
c.Add('root://eos.grid.vbc.ac.at//'+sys.argv[1])
lep_str = "lep_pt>-1000&&lep_eta>-1000&&lep_phi>-1000&&lep_pdgId>-1000&&lep_mediumId>-1000&&lep_miniPFRelIso_all>-1000&&lep_pfRelIso03_all>-1000&&lep_sip3d>-1000&&lep_dxy>-1000&&lep_dz>-1000&&lep_charge>-1000&&lep_dxyErr>-1000&&lep_dzErr>-1000&&lep_ip3d>-1000&&lep_jetPtRelv2>-1000&&lep_jetRelIso>-1000&&lep_miniPFRelIso_chg>-1000&&lep_mvaLowPt>-1000&&lep_nStations>-1000&&lep_nTrackerLayers>-1000&&lep_pfRelIso03_all>-1000&&lep_pfRelIso03_chg>-1000&&lep_pfRelIso04_all>-1000&&lep_ptErr>-1000&&lep_segmentComp>-1000&&lep_tkRelIso>-1000&&lep_tunepRelPt>-1000&&lep_genPartFlav>-1000&&lep_isPromptId_Training>-1000&&lep_isNonPromptId_Training>-1000&&lep_isNotPromptId_Training>-1000&&lep_isFakeId_Training>-1000"

n_str = "npfCand_charged>-1000&&npfCand_neutral>-1000&&npfCand_photon>-1000&&npfCand_electron>-1000&&npfCand_muon>-1000&&nSV>-1000"
gen_str = "event>-1000&&luminosityBlock>-1000&&run>-1000"
neutral_str = "npfCand_neutral>-1000&&pfCand_neutral_eta>-1000&&pfCand_neutral_phi>-1000&&pfCand_neutral_pt>-1000&&pfCand_neutral_puppiWeight>-1000&&pfCand_neutral_puppiWeightNoLep>-1000&&pfCand_neutral_ptRel>-1000&&pfCand_neutral_deltaR>-1000"
photon_str = "npfCand_photon>-1000&&pfCand_photon_eta>-1000&&pfCand_photon_phi>-1000&&pfCand_photon_pt>-1000&&pfCand_photon_puppiWeight>-1000&&pfCand_photon_puppiWeightNoLep>-1000&&pfCand_photon_ptRel>-1000&&pfCand_photon_deltaR>-1000&&nSV>-1000"
sv_str = "SV_dlen>-1000&&SV_dlenSig>-1000&&SV_dxy>-1000&&SV_dxySig>-1000&&SV_pAngle>-1000&&SV_chi2>-1000&&SV_eta>-1000&&SV_mass>-1000&&SV_ndof>-1000&&SV_phi>-1000&&SV_pt>-1000&&SV_x>-1000&&SV_y>-1000&&SV_z>-1000&&SV_ptRel>-1000&&SV_deltaR>-1000&&npfCand_muon>-1000"
muon_str = "pfCand_muon_d0>-1000&&pfCand_muon_d0Err>-1000&&pfCand_muon_dz>-1000&&pfCand_muon_dzErr>-1000&&pfCand_muon_eta>-1000&&pfCand_muon_mass>-1000&&pfCand_muon_phi>-1000&&pfCand_muon_pt>-1000&&pfCand_muon_puppiWeight>-1000&&pfCand_muon_puppiWeightNoLep>-1000&&pfCand_muon_trkChi2>-1000&&pfCand_muon_vtxChi2>-1000&&pfCand_muon_charge>-1000&&pfCand_muon_lostInnerHits>-1000&&pfCand_muon_pvAssocQuality>-1000&&pfCand_muon_trkQuality>-1000&&pfCand_muon_ptRel>-1000&&pfCand_muon_deltaR>-1000"
charged_str = "npfCand_charged>-1000&&pfCand_charged_d0>-1000&&pfCand_charged_d0Err>-1000&&pfCand_charged_dz>-1000&&pfCand_charged_dzErr>-1000&&pfCand_charged_eta>-1000&&pfCand_charged_mass>-1000&&pfCand_charged_phi>-1000&&pfCand_charged_pt>-1000&&pfCand_charged_puppiWeight>-1000&&pfCand_charged_puppiWeightNoLep>-1000&&pfCand_charged_trkChi2>-1000&&pfCand_charged_vtxChi2>-1000&&pfCand_charged_charge>-1000&&pfCand_charged_lostInnerHits>-1000&&pfCand_charged_pvAssocQuality>-1000&&pfCand_charged_trkQuality>-1000&&pfCand_charged_ptRel>-1000&&pfCand_charged_deltaR>-1000"
electron_str = "npfCand_electron>-1000&&pfCand_electron_d0>-1000&&pfCand_electron_d0Err>-1000&&pfCand_electron_dz>-1000&&pfCand_electron_dzErr>-1000&&pfCand_electron_eta>-1000&&pfCand_electron_mass>-1000&&pfCand_electron_phi>-1000&&pfCand_electron_pt>-1000&&pfCand_electron_puppiWeight>-1000&&pfCand_electron_puppiWeightNoLep>-1000&&pfCand_electron_trkChi2>-1000&&pfCand_electron_vtxChi2>-1000&&pfCand_electron_charge>-1000&&pfCand_electron_lostInnerHits>-1000&&pfCand_electron_pvAssocQuality>-1000&&pfCand_electron_trkQuality>-1000&&pfCand_electron_ptRel>-1000&&pfCand_electron_deltaR>-1000"



n1 = c.GetEntries(lep_str)
n2 = c.GetEntries(n_str)
n3 = c.GetEntries(gen_str)
n4 = c.GetEntries(neutral_str)
n5 = c.GetEntries(photon_str)
n6 = c.GetEntries(sv_str)
n7 = c.GetEntries(muon_str)
n8 = c.GetEntries(charged_str)
n9 = c.GetEntries(electron_str)

if n1>0 and n2>0 and n3>0 and n4>0 and n5>0 and n6>0 and n7>0 and n8>0 and n9>0:
    sys.exit(0) 
else:   
    sys.exit(1) 
