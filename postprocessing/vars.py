cand_vars_read = ["d0/F", "d0Err/F", "dz/F", "dzErr/F", "eta/F", "mass/F", "phi/F", "pt/F", "puppiWeight/F", "puppiWeightNoLep/F", "trkChi2/F", "vtxChi2/F", "charge/I", "lostInnerHits/I", "pdgId/I", "pvAssocQuality/I", "trkQuality/I"]
cand_vars_train = {'charged': ["d0/F", "d0Err/F", "dz/F", "dzErr/F", "eta/F", "mass/F", "phi/F", "pt/F", "puppiWeight/F", "puppiWeightNoLep/F", "trkChi2/F", "vtxChi2/F", "charge/F", "lostInnerHits/F", "pvAssocQuality/F", "trkQuality/F"],
                   'neutral': ["eta/F", "phi/F", "pt/F", "puppiWeight/F", "puppiWeightNoLep/F"],
                   'photon':  ["eta/F", "phi/F", "pt/F", "puppiWeight/F", "puppiWeightNoLep/F"],
                   'electron':["d0/F", "d0Err/F", "dz/F", "dzErr/F", "eta/F", "mass/F", "phi/F", "pt/F", "puppiWeight/F", "puppiWeightNoLep/F", "trkChi2/F", "vtxChi2/F", "charge/F", "lostInnerHits/F", "pvAssocQuality/F", "trkQuality/F"],
                   'muon':    ["d0/F", "d0Err/F", "dz/F", "dzErr/F", "eta/F", "mass/F", "phi/F", "pt/F", "puppiWeight/F", "puppiWeightNoLep/F", "trkChi2/F", "vtxChi2/F", "charge/F", "lostInnerHits/F", "pvAssocQuality/F", "trkQuality/F"],
                }
SV_vars   = ['dlen/F', 'dlenSig/F', 'dxy/F', 'dxySig/F', 'pAngle/F', 'chi2/F', 'eta/F', 'mass/F', 'ndof/F', 'phi/F', 'pt/F', 'x/F', 'y/F', 'z/F']

ele_vars = ['pt/F', 'eta/F', 'phi/F', 'pdgId/I', 'cutBased/I', 'miniPFRelIso_all/F', 'pfRelIso03_all/F', 'sip3d/F', 'lostHits/b', 'convVeto/O', 'dxy/F', 'dz/F', 'charge/I', 'deltaEtaSC/F', 'vidNestedWPBitmap/I', 'dr03EcalRecHitSumEt/F', 'dr03HcalDepth1TowerSumEt/F', 'dr03TkSumPt/F', 'dxyErr/F', 'dzErr/F', 'eCorr/F', 'eInvMinusPInv/F', 'energyErr/F', 'hoe/F', 'ip3d/F', 'jetPtRelv2/F', 'jetRelIso/F', 'miniPFRelIso_chg/F', 'mvaFall17V2noIso/F', 'pfRelIso03_chg/F', 'r9/F', 'sieie/F']
muo_vars = ["pt/F", "eta/F", "phi/F", "pdgId/I", "mediumId/O", "miniPFRelIso_all/F", "pfRelIso03_all/F", "sip3d/F", "dxy/F", "dz/F", "charge/I", 'dxyErr/F', 'dzErr/F', 'ip3d/F', 'jetPtRelv2/F', 'jetRelIso/F', 'miniPFRelIso_chg/F', 'mvaLowPt/F', 'nStations/I', 'nTrackerLayers/I', 'pfRelIso03_all/F', 'pfRelIso03_chg/F', 'pfRelIso04_all/F', 'ptErr/F', 'segmentComp/F', 'tkRelIso/F', 'tunepRelPt/F']
