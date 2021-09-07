import tensorflow
import ROOT
import os
import sys
from math import *
import numpy as np
# RootTools
from RootTools.core.standard import *

import DeepLepton.Tools.logger as _logger
logger  = _logger.get_logger(options.logLevel, logFile = None)

import tensorflow as tf


class DLmodel:
    
    def __init__(self, mode="DYvsQCD", year="2016", flavour="muo"):
        if not mode in ["DYvsQCD", "Top"]:
        logger.error('mode is invalid')
            raise NotImplementedError
        if not year in ["2016", "2017", "2018"]:
            logger.error('year is invalid')
            raise NotImplementedError
        if not flavour in ["ele", "muo"]:
            logger.error('flavour is invalid')
            raise NotImplementedError
    
        self.model = tf.keras.load_model( "../models/Model_{}_{}_{}.h5".format( flavour, year, mode ) )
        self.flavour = flavour
        self.year = year
        self.mode = mode
        
        if flavour == "ele":
            self.global_branches = ['lep_phi', 'lep_pdgId', 'lep_cutBased',
                                    'lep_miniPFRelIso_all', 'lep_pfRelIso03_all',
                                    'lep_sip3d', 'lep_lostHits',
                                    'lep_convVeto', 'lep_dxy',
                                    'lep_dz', 'lep_charge',
                                    'lep_deltaEtaSC', 'lep_vidNestedWPBitmap',
                                    'lep_dr03EcalRecHitSumEt', 'lep_dr03HcalDepth1TowerSumEt',
                                    'lep_dr03TkSumPt', 'lep_dxyErr',
                                    'lep_dzErr', 'lep_eCorr',
                                    'lep_eInvMinusPInv', 'lep_energyErr',
                                    'lep_hoe', 'lep_ip3d',
                                    'lep_jetPtRelv2', 'lep_jetRelIso',
                                    'lep_miniPFRelIso_chg', 'lep_mvaFall17V2noIso',
                                    'lep_pfRelIso03_chg', 'lep_r9',
                                    'lep_sieie',]
        elif flavour == "muo":
            self.global_branches = ['lep_phi',
                                    'lep_mediumId',
                                    'lep_miniPFRelIso_all',
                                    'lep_sip3d', 'lep_dxy', 'lep_dz',
                                    'lep_charge',
                                    'lep_dxyErr', 'lep_dzErr', 'lep_ip3d',
                                    'lep_jetPtRelv2', 'lep_jetRelIso',
                                    'lep_miniPFRelIso_chg', 'lep_mvaLowPt', 'lep_nStations', 'lep_nTrackerLayers',
                                    'lep_pfRelIso03_all', 'lep_pfRelIso03_chg', 'lep_pfRelIso04_all', 'lep_ptErr',
                                    'lep_segmentComp', 'lep_tkRelIso', 'lep_tunepRelPt',]

        self.pfCand_neutral_branches  = ['pfCand_neutral_eta', 'pfCand_neutral_phi', 'pfCand_neutral_pt', 'pfCand_neutral_puppiWeight', 'pfCand_neutral_puppiWeightNoLep',
                            'pfCand_neutral_ptRel', 'pfCand_neutral_deltaR',]
        self.pfCand_charged_branches  = ['pfCand_chargeid_d0', 'pfCand_charged_d0Err', 'pfCand_charged_dz', 'pfCand_charged_dzErr', 'pfCand_charged_eta', 'pfCand_charged_mass',
                            'pfCand_charged_phi', 'pfCand_charged_pt', 'pfCand_charged_puppiWeight', 'pfCand_charged_puppiWeightNoLep', 'pfCand_charged_trkChi2',
                            'pfCand_charged_vtxChi2', 'pfCand_charged_charge', 'pfCand_charged_lostInnerHits', 'pfCand_charged_pvAssocQuality',
                            'pfCand_charged_trkQuality', 'pfCand_charged_ptRel', 'pfCand_charged_deltaR',]
        self.pfCand_photon_branches   = ['pfCand_photon_eta', 'pfCand_photon_phi', 'pfCand_photon_pt', 'pfCand_photon_puppiWeight', 'pfCand_photon_puppiWeightNoLep',
                            'pfCand_photon_ptRel', 'pfCand_photon_deltaR',]
        self.pfCand_electron_branches = ['pfCand_electron_d0', 'pfCand_electron_d0Err', 'pfCand_electron_dz', 'pfCand_electron_dzErr', 'pfCand_electron_eta', 'pfCand_electron_mass',
                            'pfCand_electron_phi', 'pfCand_electron_pt', 'pfCand_electron_puppiWeight', 'pfCand_electron_puppiWeightNoLep', 'pfCand_electron_trkChi2',
                            'pfCand_electron_vtxChi2', 'pfCand_electron_charge', 'pfCand_electron_lostInnerHits', 'pfCand_electron_pvAssocQuality',
                            'pfCand_electron_trkQuality', 'pfCand_electron_ptRel', 'pfCand_electron_deltaR',]
        self.pfCand_muon_branches     = ['pfCand_muon_d0', 'pfCand_muon_d0Err', 'pfCand_muon_dz', 'pfCand_muon_dzErr', 'pfCand_muon_eta', 'pfCand_muon_mass', 'pfCand_muon_phi',
                            'pfCand_muon_pt', 'pfCand_muon_puppiWeight', 'pfCand_muon_puppiWeightNoLep', 'pfCand_muon_trkChi2', 'pfCand_muon_vtxChi2', 'pfCand_muon_charge',
                            'pfCand_muon_lostInnerHits', 'pfCand_muon_pvAssocQuality', 'pfCand_muon_trkQuality', 'pfCand_muon_ptRel', 'pfCand_muon_deltaR']
        self.SV_branches              = ['SV_dlen', 'SV_dlenSig', 'SV_dxy', 'SV_dxySig', 'SV_pAngle', 'SV_chi2', 'SV_eta', 'SV_mass',
                            'SV_ndof', 'SV_phi', 'SV_pt', 'SV_x', 'SV_y', 'SV_z', 'SV_ptRel', 'SV_deltaR',]
        
        self.npfCand_neutral  = 10
        self.npfCand_charged  = 80
        self.npfCand_photon   = 50
        self.npfCand_electron = 4
        self.npfCand_muon     = 6
        self.nSV              = 10
    


    def predict(self, X):
        return self.model.predict(X)[0]
    def help(self):
        print("To input the lepton into the predict method, it has to follow these rules:")        
        print("X is a list, that contains: [ globalB, neutralB, chargedB, photonB, electronB, muonB, svB ]  - L286 of postprocessing/predictOnSample.py")        
        print("global branches has a shape of (1, len(self.global_branches)) and is a numpy array. The PFCand and SV branches")        
        print("are of shape (npfCand*, len(self.pfCand*branches) and also numpy arrays. As they don't usually have npfCand pfCands,")        
        print("they need to be 0-padded, ie filled with zeros. (See L270 of postprocessing/predictOnSample.py")        


