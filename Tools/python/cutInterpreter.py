''' Class to interpret string based cuts
'''

from math import sqrt, cos, sin, pi, cosh
import logging
logger = logging.getLogger(__name__)

jetSelection    = "njet"
bJetSelectionM  = "nBTag"

mIsoWP = { "VT":5, "T":4, "M":3 , "L":2 , "VL":1, 0:"None" }

special_cuts = {
    #"lepSel":            "nlep==2&&lep_pt[0]>40&&lep_pt[1]>20",
    "dilepOS":           "nlep>=2&&(lep_pdgId[0]*lep_pdgId[1])<0",
    "dilepOSmumu":       "nlep>=2&&(lep_pdgId[0]==-lep_pdgId[1])&&abs(lep_pdgId[0])==13",
    "dilepOSmumuDY":     "nlep>=2&&(lep_pdgId[0]==-lep_pdgId[1])&&abs(lep_pdgId[0])==13&&(lep_pt[0]>20||(lep_ip3d[0]>0.1&&lep_ip3d[1]>0.1)||(lep_sip3d[0]>2&&lep_sip3d[1]>2))",
    #"dilepSel":          "nlep==2&&lep_pt[0]>40&&lep_pt[1]>20",
    #"dilepSelOS":        "nlep==2&&lep_pt[0]>40&&lep_pt[1]>20&&(lep_pdgId[0]*lep_pdgId[1]<0)",  #&&abs(lep_pdgId[0])==13&&abs(lep_pdgId[1])==13", 
    #"dilepSelSFSS":      "nlep==2&&lep_pt[0]>40&&lep_pt[1]>20&&(lep_pdgId[0]==lep_pdgId[1])",
    #"dilepSelSFOS":      "nlep==2&&lep_pt[0]>40&&lep_pt[1]>20&&(lep_pdgId[0]==-lep_pdgId[1])",
    #"dilepZmass":        "nlep==2&&(sqrt(2*lep_pt[0]*lep_pt[1]*( cosh(lep_eta[0]-lep_eta[1]) - cos(lep_phi[0]-lep_phi[1])))<(91.19+15.))&&(sqrt(2*lep_pt[0]*lep_pt[1]*( cosh(lep_eta[0]-lep_eta[1]) - cos(lep_phi[0]-lep_phi[1])))>(91.19-15.))",   
    
    "lep_CR_tt2l":       "((Sum$(abs(lep_pdgId)==13&&lep_pt>5&&( abs(lep_eta)<2.4&&lep_ip3d<0.01&&lep_sip3d<2&&((lep_relIso03<0.5&&(lep_relIso03*lep_pt)<5)||lep_relIso03<0.1) ))) + (Sum$(abs(lep_pdgId)==11&&lep_pt>5&&( abs(lep_eta)<2.5&&lep_ip3d<0.01&&lep_sip3d<2&&((lep_relIso03<0.5&&(lep_relIso03*lep_pt)<5)||lep_relIso03<0.1) )))) == 2"   ,
    "lep_CR_tt2l_mumu":       "(Sum$(abs(lep_pdgId)==13&&lep_pt>5&&( abs(lep_eta)<2.4&&lep_ip3d<0.01&&lep_sip3d<2&&((lep_relIso03<0.5&&(lep_relIso03*lep_pt)<5)||lep_relIso03<0.1) ))) == 2"   ,
    
    #"jet_CR_tt2l":       "Sum$(jet_btagDeepCSV>0.6321&&jet_pt>40&&abs(jet_eta)<2.4)>=1&&Sum$(jet_btagDeepCSV>0.6321&&abs(jet_eta)<2.4)<3"   , 
    "jet_CR_tt2l":       "Sum$(jet_btagCSV>0.46&&jet_pt>40&&abs(jet_eta)<2.4)>=1&&Sum$(jet_btagCSV>0.46&&abs(jet_eta)<2.4)<3"   , 
    #"jet_CR_tt2l":       "Sum$(jet_btagDeepCSV>0.2217&&jet_pt>40&&abs(jet_eta)<2.4)>=1"   , 
    
    #"lep_CR_DY":         "((Sum$(abs(lep_pdgId)==13&&lep_pt>5&&abs(lep_eta)<2.4&&lep_ip3d<0.0175&&lep_sip3d<2.5&&((lep_relIso03<0.5&&(lep_relIso03*lep_pt)<5)||lep_relIso03<0.1)  )==2) || (Sum$(abs(lep_pdgId)==11&&lep_pt>5&&abs(lep_eta)<2.5&&lep_ip3d<0.0175&&lep_sip3d<2.5&&((lep_relIso03<0.5&&(lep_relIso03*lep_pt)<5)||lep_relIso03<0.1) )==2)) "   ,#&& Sum$( lep_pt>20||lep_ip3d>0.01||lep_sip3d>2  )>=1"   , 
    "lep_CR_DY_all":     "(Sum$(abs(lep_pdgId)==13&&lep_pt>5&&abs(lep_eta)<2.4&&lep_ip3d<0.0175&&lep_sip3d<2.5&&((lep_relIso03<0.5&&(lep_relIso03*lep_pt)<5)||lep_relIso03<0.1)) + Sum$(abs(lep_pdgId)==11&&lep_pt>5&&abs(lep_eta)<2.5&&lep_ip3d<0.0175&&lep_sip3d<2.5&&((lep_relIso03<0.5&&(lep_relIso03*lep_pt)<5)||lep_relIso03<0.1) ))==2 "   ,#&& Sum$( lep_pt>20||lep_ip3d>0.01||lep_sip3d>2  )>=1"   , 
    "lep_CR_DY_mumu_ee": "(((Sum$(abs(lep_pdgId)==13&&lep_pt>5&&abs(lep_eta)<2.4&&lep_ip3d<0.0175&&lep_sip3d<2.5&&((lep_relIso03<0.5&&(lep_relIso03*lep_pt)<5)||lep_relIso03<0.1)))==2) || (Sum$(abs(lep_pdgId)==11&&lep_pt>5&&abs(lep_eta)<2.5&&lep_ip3d<0.0175&&lep_sip3d<2.5&&((lep_relIso03<0.5&&(lep_relIso03*lep_pt)<5)||lep_relIso03<0.1) ))==2)"   , 
    "lep_CR_DY_mumu":    "(Sum$(abs(lep_pdgId)==13&&lep_pt>5&&abs(lep_eta)<2.4&&lep_ip3d<0.0175&&lep_sip3d<2.5&&((lep_relIso03<0.5&&(lep_relIso03*lep_pt)<5)||lep_relIso03<0.1)))==2 "   , 
    "lep_CR_DY_ee":    "(Sum$(abs(lep_pdgId)==11&&lep_pt>5&&abs(lep_eta)<2.5&&lep_ip3d<0.0175&&lep_sip3d<2.5&&((lep_relIso03<0.5&&(lep_relIso03*lep_pt)<5)||lep_relIso03<0.1)))==2 "   , 
    #"jet_CR_DY":         "Sum$(jet_pt>25&&jet_eta<2.4&&jet_btagCSV<0.1460)>=1&&Sum$(jet_pt>25&&jet_btagCSV>0.14)==0"  ,   #"Sum$(jet_pt>25&&jet_eta<2.4)>=1&&nBTag==0"   , 
    "jet_CR_DY":         "Sum$(jet_pt>25&&abs(jet_eta)<2.4)>=1&&Sum$(jet_pt>25&&jet_btagDeepCSV>0.2217)==0"  ,   #"Sum$(jet_pt>25&&jet_eta<2.4)>=1&&nBTag==0"   , 
   
    "ht_met":            "ht>100&&0.6<(met_pt/ht)&&(met_pt/ht)<1.4"   ,
    "lower_met":         "met_pt>125&&met_pt<200"   ,
    "med_met":           "met_pt>200&&met_pt<300"   ,


    "lep_SR_all":        "(Sum$(abs(lep_pdgId)==13&&(lep_pt>3.5)&&lep_pt<30&&( abs(lep_eta)<2.4&&lep_ip3d<0.01&&lep_sip3d<2&&lep_relIso03<0.5&&(lep_relIso03*lep_pt)<5 )) + Sum$(abs(lep_pdgId)==11&&lep_pt>5&&lep_pt<30&&( abs(lep_eta)<2.5&&lep_ip3d<0.01&&lep_sip3d<2&&lep_relIso03<0.5&&(lep_relIso03*lep_pt)<5 ))) == 2"   ,
    "lep_SR_mumu_ee":    "(Sum$(abs(lep_pdgId)==13&&lep_pt>3.5&&lep_pt<30&&( abs(lep_eta)<2.4&&lep_ip3d<0.01&&lep_sip3d<2&&lep_relIso03<0.5&&(lep_relIso03*lep_pt)<5 )) + Sum$(abs(lep_pdgId)==11&&lep_pt>5&&lep_pt<30&&( abs(lep_eta)<2.5&&lep_ip3d<0.01&&lep_sip3d<2&&lep_relIso03<0.5&&(lep_relIso03*lep_pt)<5 ))) == 2"   ,
    "lep_SR_mu":         "(Sum$(abs(lep_pdgId)==13&&lep_pt>5&&lep_pt<30&&( abs(lep_eta)<2.4&&lep_ip3d<0.01&&lep_sip3d<2&&lep_relIso03<0.5&&(lep_relIso03*lep_pt)<5 ))) == 2"   ,
    "jet_SR":            "Sum$(jet_pt>25&&jet_eta<2.4)>=1&&Sum$(jet_pt>25&&jet_btagCSV>0.46)==0"  , 

    #"T2tt_350_20":       "Sum$(genPartAll_pdgId==1000006&&genPartAll_mass==350)>=1&&Sum$(genPartAll_pdgId==-1000006&&genPartAll_mass==350)>=1&&Sum$(genPartAll_pdgId==1000022&&genPartAll_mass==330)>=2",
    "T2tt_350_20":       "Sum$(abs(genPartAll_pdgId)==1000006 && genPartAll_mass==350)>=1 && Sum$(abs(genPartAll_pdgId)==1000022 && genPartAll_mass==330)>=1" ,
    #"T2tt_350_20":        "Sum$(abs(genPartAll_pdgId)==13&&abs(genPartAll_grandmotherId)==1000006)>=2 && Sum$(abs(genPartAll_pdgId)==1000006&&genPartAll_mass==350)>=2 && Sum$(abs(genPartAll_pdgId)==1000022&&genPartAll_mass==330)>=2" ,
   
    "filters":           "Flag_goodVertices==1&&Flag_HBHENoiseFilter==1&&Flag_HBHENoiseIsoFilter==1&&Flag_eeBadScFilter==1&&Flag_EcalDeadCellTriggerPrimitiveFilter==1&&Flag_globalTightHalo2016Filter==1&&Flag_badMuonSummer2016==1&&Flag_badChargedHadronSummer2016==1" , 
 

    "lep_SR_all_DL_sigeff":        "(Sum$(abs(lep_pdgId)==13&&(lep_pt>3.5)&&lep_pt<30&&abs(lep_eta)<2.4&& (lep_miniRelIso<0.4&&lep_sip3d<8&&abs(lep_dz)<0.1&&abs(lep_dxy)<0.05&&lep_pfMuonId&&lep_mediumMuonId&&lep_deepLepton_prompt<999&&lep_deepLepton_prompt>0.046 ) ) + Sum$(abs(lep_pdgId)==11&&lep_pt>5&&lep_pt<30&&abs(lep_eta)<2.5&& (lep_miniRelIso<0.4&&lep_sip3d<8&&abs(lep_dz)<0.1&&abs(lep_dxy)<0.05&&lep_lostHits<=1&&lep_deepLepton_prompt<999&&lep_deepLepton_prompt>0.082) )) == 2"   ,
    "lep_SR_all_DL_bgr":        "(Sum$(abs(lep_pdgId)==13&&(lep_pt>3.5)&&lep_pt<30&&abs(lep_eta)<2.4&& (lep_miniRelIso<0.4&&lep_sip3d<8&&abs(lep_dz)<0.1&&abs(lep_dxy)<0.05&&lep_pfMuonId&&lep_mediumMuonId&&lep_deepLepton_prompt<999&&lep_deepLepton_prompt>0.407 ) ) + Sum$(abs(lep_pdgId)==11&&lep_pt>5&&lep_pt<30&&abs(lep_eta)<2.5&& (lep_miniRelIso<0.4&&lep_sip3d<8&&abs(lep_dz)<0.1&&abs(lep_dxy)<0.05&&lep_lostHits<=1&&lep_deepLepton_prompt<999&&lep_deepLepton_prompt>0.864) )) == 2"   ,


    "lep_SR_mu_DL_sigeff":        "(Sum$(abs(lep_pdgId)==13&&(lep_pt>3.5)&&lep_pt<30&&abs(lep_eta)<2.4&& (lep_miniRelIso<0.4&&lep_sip3d<8&&abs(lep_dz)<0.1&&abs(lep_dxy)<0.05&&lep_pfMuonId&&lep_mediumMuonId&&lep_deepLepton_prompt<999&&lep_deepLepton_prompt>0.046 ) )) == 2"   ,
    "lep_SR_mu_DL_bgr":        "(Sum$(abs(lep_pdgId)==13&&(lep_pt>3.5)&&lep_pt<30&&abs(lep_eta)<2.4&& (lep_miniRelIso<0.4&&lep_sip3d<8&&abs(lep_dz)<0.1&&abs(lep_dxy)<0.05&&lep_pfMuonId&&lep_mediumMuonId&&lep_deepLepton_prompt<999&&lep_deepLepton_prompt>0.407 ) ) ) == 2"   ,

    "Compressed_Stops_special":   "(mtautau>160||mtautau<0)&&ptll>3&&mll<50&&mll>4&&(mll>10.5||mll<9)&&ht25>100&&met_pt/ht25<1.4&&met_pt/ht25>0.6&&SR&&((dimu&&metMuSubtracted>125)||(dimu==0&&metMuSubtracted>200))"   ,

    "test":                     "met_pt>200&&met_pt<300&&leadingLep_pt>20&&leadingLep_pt<30"
   
    #"genZtoTau":         "genZ_daughter_flavor==15",
 }

continous_variables = [ ("metSig", "metSig"), ("met", "met_pt"), ]
discrete_variables  = [ ("njet", "nJetSelected"), ("btag", "nBTag") , ("nlep","nlep") ]

class cutInterpreter:
    ''' Translate var100to200-var2p etc.
    '''

    @staticmethod
    def translate_cut_to_string( string ):

        # special cuts
        if string in special_cuts.keys(): return special_cuts[string]

        # continous Variables
        for var, tree_var in continous_variables:
            if string.startswith( var ):
                num_str = string[len( var ):].replace("to","To").split("To")
                upper = None
                lower = None
                if len(num_str)==2:
                    lower, upper = num_str
                elif len(num_str)==1:
                    lower = num_str[0]
                else:
                    raise ValueError( "Can't interpret string %s" % string )
                res_string = []
                if lower: res_string.append( tree_var+">="+lower )
                if upper: res_string.append( tree_var+"<"+upper )
                return "&&".join( res_string )

        # discrete Variables
        for var, tree_var in discrete_variables:
            logger.debug("Reading discrete cut %s as %s"%(var, tree_var))
            if string.startswith( var ):
                # So far no njet2To5
                if string[len( var ):].replace("to","To").count("To"):
                    raise NotImplementedError( "Can't interpret string with 'to' for discrete variable: %s. You just volunteered." % string )

                num_str = string[len( var ):]
                # logger.debug("Num string is %s"%(num_str))
                # var1p -> tree_var >= 1
                if num_str[-1] == 'p' and len(num_str)==2:
                    # logger.debug("Using cut string %s"%(tree_var+">="+num_str[0]))
                    return tree_var+">="+num_str[0]
                # var123->tree_var==1||tree_var==2||tree_var==3
                else:
                    vls = [ tree_var+"=="+c for c in num_str ]
                    if len(vls)==1:
                      # logger.debug("Using cut string %s"%vls[0])
                      return vls[0]
                    else:
                      # logger.debug("Using cut string %s"%'('+'||'.join(vls)+')')
                      return '('+'||'.join(vls)+')'
        raise ValueError( "Can't interpret string %s. All cuts %s" % (string,  ", ".join( [ c[0] for c in continous_variables + discrete_variables] +  special_cuts.keys() ) ) )

    @staticmethod
    def cutString( cut, select = [""], ignore = [], photonEstimated=False):
        ''' Cutstring syntax: cut1-cut2-cut3
        '''
        cuts = cut.split('-')
        # require selected
        cuts = filter( lambda c: any( sel in c for sel in select ), cuts )
        # ignore
        cuts = filter( lambda c: not any( ign in c for ign in ignore ), cuts )

        cutString = "&&".join( map( cutInterpreter.translate_cut_to_string, cuts ) )

        if photonEstimated:
          for var in ['met_pt','met_phi','metSig','dl_mt2ll','dl_mt2bb']:
            cutString = cutString.replace(var, var + '_photonEstimated')

        return cutString
    
    @staticmethod
    def cutList ( cut, select = [""], ignore = []):
        ''' Cutstring syntax: cut1-cut2-cut3
        '''
        cuts = cut.split('-')
        # require selected
        cuts = filter( lambda c: any( sel in c for sel in select ), cuts )
        # ignore
        cuts = filter( lambda c: not any( ign in c for ign in ignore ), cuts )
        return [ cutInterpreter.translate_cut_to_string(cut) for cut in cuts ] 
        #return  "&&".join( map( cutInterpreter.translate_cut_to_string, cuts ) )

if __name__ == "__main__":
    #print cutInterpreter.cutString("lepSel-njet3p-btag1p-Zpt100")
    print cutInterpreter.cutString("lepSel-njet3p-btag1p-met0To100")
    print cutInterpreter.cutList("lepSel-njet3p-btag1p-ZptTo100")
