# Standard imports
import ROOT
import os
import sys

# RootTools
from RootTools.core.Sample import *

# DeepLepton
from DeepLepton.Tools.user import skim_directory

# parser
def get_parser():
    ''' Argument parser for post-processing module.
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser for cmgPostProcessing")

    argParser.add_argument('--logLevel',                    action='store',         nargs='?',              choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET', 'SYNC'],     default='INFO',                     help="Log level for logging")
    argParser.add_argument('--directory',                    action='store',         nargs='?',              )

    return argParser

options = get_parser().parse_args()

# Logging
import DeepLepton.Tools.logger as logger
logger  = logger.get_logger(options.logLevel, logFile = None)
import RootTools.core.logger as logger_rt
logger_rt = logger_rt.get_logger(options.logLevel, logFile = None )

def varList(pfCandId):
    
    if pfCandId=='final_muon':
        pfCandVarList = [
        #'lep_pt',
        #'lep_eta', 
        #'lep_dxy',
        #'lep_dz',
        #'lep_ip3d', 
        #'lep_sip3d',
        #'lep_innerTrackChi2',
        #'lep_innerTrackValidHitFraction',
        #'lep_ptErrTk', 
        #'lep_rho', 
        #'lep_jetDR',
        #'lep_trackerLayers_float', 
        #'lep_pixelLayers_float', 
        #'lep_trackerHits_float', 
        #'lep_lostHits_float', 
        #'lep_lostOuterHits_float',
        #'lep_relIso03', 
        #'lep_miniRelIsoCharged', 
        #'lep_miniRelIsoNeutral',
        #'lep_jetPtRatiov2', 
        #'lep_jetPtRelv2',
        #'lep_jetBTagDeepCSV',
        #'lep_segmentCompatibility', 
        #'lep_muonInnerTrkRelErr', 
        #'lep_isGlobalMuon_float',
        #'lep_chi2LocalPosition', 
        #'lep_chi2LocalMomentum', 
        #'lep_globalTrackChi2',
        #'lep_glbTrackProbability', 
        #'lep_trkKink', 
        #'lep_caloCompatibility',
        #'lep_nStations_float',
        #'pfCand_neutral_ptRel_ptRelSorted',
        #'pfCand_neutral_deltaR_ptRelSorted',  
        #'pfCand_neutral_pt_ptRelSorted',
        #'pfCand_neutral_puppiWeight_ptRelSorted', 
        #'pfCand_neutral_fromPV_ptRelSorted',
        #'pfCand_charged_ptRel_ptRelSorted',  
        #'pfCand_charged_deltaR_ptRelSorted',  
        #'pfCand_charged_pt_ptRelSorted',  
        #'pfCand_charged_puppiWeight_ptRelSorted', 
        #'pfCand_charged_fromPV_ptRelSorted', 
        #'pfCand_charged_dxy_pf_ptRelSorted', 
        'pfCand_charged_dz_pf_ptRelSorted', 
        'pfCand_charged_dzAssociatedPV_ptRelSorted',
        #'pfCand_photon_ptRel_ptRelSorted',   
        #'pfCand_photon_deltaR_ptRelSorted',   
        #'pfCand_photon_pt_ptRelSorted',   
        #'pfCand_photon_puppiWeight_ptRelSorted',  
        #'pfCand_photon_fromPV_ptRelSorted',
        #'pfCand_electron_ptRel_ptRelSorted', 
        #'pfCand_electron_deltaR_ptRelSorted', 
        #'pfCand_electron_pt_ptRelSorted', 
        #'pfCand_electron_dxy_pf_ptRelSorted', 
        #'pfCand_electron_dz_pf_ptRelSorted',
        #'pfCand_muon_ptRel_ptRelSorted',     
        #'pfCand_muon_deltaR_ptRelSorted',     
        #'pfCand_muon_pt_ptRelSorted',     
        #'pfCand_muon_dxy_pf_ptRelSorted',     
        #'pfCand_muon_dz_pf_ptRelSorted',
        #'SV_pt_ptSorted', 
        #'SV_chi2_ptSorted', 
        #'SV_ndof_ptSorted', 
        #'SV_dxy_ptSorted', 
        #'SV_ip3d_ptSorted', 
        #'SV_eip3d_ptSorted', 
        #'SV_sip3d_ptSorted',
        #'SV_cosTheta_ptSorted', 
        #'SV_deltaR_ptSorted', 
        #'SV_maxDxyTracks_ptSorted', 
        #'SV_secDxyTracks_ptSorted', 
        #'SV_maxD3dTracks_ptSorted_patch',
        #'SV_secD3dTracks_ptSorted_patch',
        ]

    if pfCandId=='ele':
        pfCandVarList = [
        'lep_pt',
        'lep_eta', 
        'lep_dxy',
        'lep_dz',
        'lep_ip3d', 
        'lep_sip3d',
        'lep_innerTrackChi2',
        'lep_innerTrackValidHitFraction',
        'lep_ptErrTk', 
        'lep_rho', 
        'lep_jetDR',
        'lep_trackerLayers_float', 
        'lep_pixelLayers_float', 
        'lep_trackerHits_float', 
        'lep_lostHits_float', 
        'lep_lostOuterHits_float',
        'lep_relIso03', 
        'lep_miniRelIsoCharged', 
        'lep_miniRelIsoNeutral',
        'lep_jetPtRatiov2', 
        'lep_jetPtRelv2',
        'lep_jetBTagDeepCSV',
        'lep_etaSc',
        'lep_full5x5_sigmaIetaIeta',
        'lep_dEtaInSeed',
        'lep_dPhiScTrkIn',
        'lep_dEtaScTrkIn',
        'lep_eInvMinusPInv',
        'lep_convVeto_float',
        'lep_hadronicOverEm',
        'lep_r9',
        'lep_mvaIdSpring16',
        'pfCand_neutral_ptRel_ptRelSorted',
        'pfCand_neutral_deltaR_ptRelSorted',  
        'pfCand_neutral_pt_ptRelSorted',
        'pfCand_neutral_puppiWeight_ptRelSorted', 
        'pfCand_neutral_fromPV_ptRelSorted',
        'pfCand_charged_ptRel_ptRelSorted',  
        'pfCand_charged_deltaR_ptRelSorted',  
        'pfCand_charged_pt_ptRelSorted',  
        'pfCand_charged_puppiWeight_ptRelSorted', 
        'pfCand_charged_fromPV_ptRelSorted', 
        'pfCand_charged_dxy_pf_ptRelSorted', 
        'pfCand_charged_dz_pf_ptRelSorted', 
        'pfCand_charged_dzAssociatedPV_ptRelSorted',
        'pfCand_photon_ptRel_ptRelSorted',   
        'pfCand_photon_deltaR_ptRelSorted',   
        'pfCand_photon_pt_ptRelSorted',   
        'pfCand_photon_puppiWeight_ptRelSorted',  
        'pfCand_photon_fromPV_ptRelSorted',
        'pfCand_electron_ptRel_ptRelSorted', 
        'pfCand_electron_deltaR_ptRelSorted', 
        'pfCand_electron_pt_ptRelSorted', 
        'pfCand_electron_dxy_pf_ptRelSorted', 
        'pfCand_electron_dz_pf_ptRelSorted',
        'pfCand_muon_ptRel_ptRelSorted',     
        'pfCand_muon_deltaR_ptRelSorted',     
        'pfCand_muon_pt_ptRelSorted',     
        'pfCand_muon_dxy_pf_ptRelSorted',     
        'pfCand_muon_dz_pf_ptRelSorted',
        'SV_pt_ptSorted', 
        'SV_chi2_ptSorted', 
        'SV_ndof_ptSorted', 
        'SV_dxy_ptSorted', 
        'SV_ip3d_ptSorted', 
        'SV_eip3d_ptSorted', 
        'SV_sip3d_ptSorted',
        'SV_cosTheta_ptSorted', 
        'SV_deltaR_ptSorted', 
        'SV_maxDxyTracks_ptSorted', 
        'SV_secDxyTracks_ptSorted', 
        #'SV_maxD3dTracks_ptSorted_patch',
        #'SV_secD3dTracks_ptSorted_patch',
        'SV_maxD3dTracks_ptSorted',
        'SV_secD3dTracks_ptSorted',
        ]

    elif pfCandId=='SV':
        pfCandVarList = [
        'SV_pt',
        'SV_eta',
        'SV_phi',
        'SV_mass',
        'SV_charge',
        'SV_ntracks',
        'SV_chi2',
        'SV_ndof',
        'SV_dxy',
        'SV_edxy',
        'SV_ip3d',
        'SV_eip3d',
        'SV_sip3d',
        'SV_cosTheta',
        'SV_mva',
        'SV_jetPt',
        'SV_jetEta',
        'SV_jetDR',
        'SV_jetBTagCSV',
        'SV_jetBTagCMVA',
        'SV_jetBTagDeepCSV',
        'SV_mcMatchNTracks',
        'SV_mcMatchNTracksHF',
        'SV_mcMatchFraction',
        'SV_mcFlavFirst',
        'SV_mcFlavHeaviest',
        'SV_maxDxyTracks',
        'SV_secDxyTracks',
        'SV_maxD3dTracks',
        'SV_secD3dTracks',
        'SV_deltaR',
        ]

    else:
        #define related variables of PF candidates
        pfCandVarList = [
        'pfCand_'+pfCandId+'_pdgId',
        'pfCand_'+pfCandId+'_pt',
        'pfCand_'+pfCandId+'_eta',
        'pfCand_'+pfCandId+'_phi',
        'pfCand_'+pfCandId+'_mass',
        'pfCand_'+pfCandId+'_puppiWeight',
        'pfCand_'+pfCandId+'_hcalFraction',
        'pfCand_'+pfCandId+'_fromPV',
        'pfCand_'+pfCandId+'_dxy_pf',
        'pfCand_'+pfCandId+'_dz_pf',
        'pfCand_'+pfCandId+'_dzAssociatedPV',
        'pfCand_'+pfCandId+'_deltaR',
        'pfCand_'+pfCandId+'_ptRel',
                        ]

    return pfCandVarList

#define PF candidates for loop
pfCandIdList = [
                'neutral',
                'charged',
                'photon',
                'electron',
                'muon',
                'SV',
               ]

vetoNanSelection = "||".join(["((TMath::IsNaN(%s)))"%var for var in varList('ele')])
#vetoNanSelection = "||".join(["isinf(%s)"%var for var in varList('ele')])
print("selction: ", vetoNanSelection)

c = ROOT.TChain("tree")
#c.Add( options.directory +"/*_0.root" )
c.Add( options.directory +"*.root" )


