
"""
Configuration file for step2_sample.py
"""

# Standard imports
import numpy as np
from DeepLepton.Tools.user import skim_directory
from RootTools.core.standard import *
import RootTools.core.logger as logger_rt
import DeepLepton.Tools.logger as logger
import ROOT
import os
import sys
import importlib
import random
random.seed(100)
import copy

nMax = 500  # For the read and write buffer


# RootTools

# DeepLepton

DY = {2016: ['DYJetsToLL_M50_LO',],
             # 'DYJetsToLL_M50_LO_ext2',
             # 'DYJetsToLL_M50_ext2',
             # 'DYJetsToLL_M10to50_LO',
             # 'DYJetsToLL_M10to50',

             # 'DYJetsToLL_M50_HT70to100',
             # 'DYJetsToLL_M50_HT100to200_ext',
             # 'DYJetsToLL_M50_HT200to400',
             # 'DYJetsToLL_M50_HT200to400_ext',
             # 'DYJetsToLL_M50_HT400to600',
             # 'DYJetsToLL_M50_HT400to600_ext',
             # 'DYJetsToLL_M50_HT600to800',
             # 'DYJetsToLL_M50_HT800to1200',
             # 'DYJetsToLL_M50_HT1200to2500',
             # 'DYJetsToLL_M50_HT2500toInf',

             # 'DYJetsToLL_M5to50_HT70to100',
             # 'DYJetsToLL_M5to50_HT100to200',
             # 'DYJetsToLL_M5to50_HT100to200_ext',
             # 'DYJetsToLL_M5to50_HT200to400',
             # 'DYJetsToLL_M5to50_HT200to400_ext',
             # 'DYJetsToLL_M5to50_HT400to600',
             # 'DYJetsToLL_M5to50_HT400to600_ext',
             # 'DYJetsToLL_M5to50_HT600toInf', ],

      2017: ['DYJetsToLL_M10to50_LO',
             'DYJetsToLL_M4to50_HT100to200_LO',
             'DYJetsToLL_M4to50_HT100to200_LO_ext1',
             'DYJetsToLL_M4to50_HT200to400_LO',
             'DYJetsToLL_M4to50_HT200to400_LO_ext1',
             'DYJetsToLL_M4to50_HT200to400_new_pmx_LO',
             'DYJetsToLL_M4to50_HT400to600_LO',
             'DYJetsToLL_M4to50_HT400to600_LO_ext1',
             'DYJetsToLL_M4to50_HT600toInf_LO',
             'DYJetsToLL_M4to50_HT600toInf_LO_ext1',
             'DYJetsToLL_M50_HT100to200_LO',
             'DYJetsToLL_M50_HT100to200_LO_ext1',
             'DYJetsToLL_M50_HT1200to2500_LO',
             'DYJetsToLL_M50_HT200to400_LO',
             'DYJetsToLL_M50_HT200to400_LO_ext1',
             'DYJetsToLL_M50_HT2500toInf_LO',
             'DYJetsToLL_M50_HT400to600_LO',
             'DYJetsToLL_M50_HT400to600_LO_ext1',
             'DYJetsToLL_M50_HT600to800_LO',
             'DYJetsToLL_M50_HT70to100_LO',
             'DYJetsToLL_M50_HT800to1200_LO',
             'DYJetsToLL_M50_LO',
             'DYJetsToLL_M50_LO_ext1',
             'DYJetsToLL_M50_NLO', ],

      2018: [
    'DYJetsToLL_M10to50_LO',
    'DYJetsToLL_M4to50_HT100to200_LO',
    'DYJetsToLL_M4to50_HT100to200_LO_ext1',
    'DYJetsToLL_M4to50_HT200to400_LO',
    'DYJetsToLL_M4to50_HT200to400_LO_ext1',
    'DYJetsToLL_M4to50_HT200to400_new_pmx_LO',
    'DYJetsToLL_M4to50_HT400to600_LO',
    'DYJetsToLL_M4to50_HT400to600_LO_ext1',
    'DYJetsToLL_M4to50_HT600toInf_LO',
    'DYJetsToLL_M4to50_HT600toInf_LO_ext1',
    'DYJetsToLL_M50_HT100to200_LO',
    'DYJetsToLL_M50_HT100to200_LO_ext1',
    'DYJetsToLL_M50_HT1200to2500_LO',
    'DYJetsToLL_M50_HT200to400_LO',
    'DYJetsToLL_M50_HT200to400_LO_ext1',
    'DYJetsToLL_M50_HT2500toInf_LO',
    'DYJetsToLL_M50_HT400to600_LO',
    'DYJetsToLL_M50_HT400to600_LO_ext1',
    'DYJetsToLL_M50_HT600to800_LO',
    'DYJetsToLL_M50_HT70to100_LO',
    'DYJetsToLL_M50_HT800to1200_LO',
    'DYJetsToLL_M50_LO',
    'DYJetsToLL_M50_LO_ext1',
    'DYJetsToLL_M50_NLO', ]}


Top = {2016: ['TTTo2L2Nu_noSC_pow',
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
              ],

       2017: ['ST_schannel_4f_NLO',
              'ST_schannel_4f_NLO_PS',
              'ST_tchannel_antitop_4f_incl_pow',
              'ST_tchannel_antitop_5f_pow_PS',
              'ST_tchannel_antitop_5f_pow_PS_old_pmx',
              'ST_tchannel_top_4f_incl_pow',
              'ST_tchannel_top_5f_pow',
              'ST_tchannel_top_5f_pow_old_pmx',
              'ST_tW_antitop_incl_5f_pow',
              'ST_tW_antitop_incl_5f_pow_PS',
              'ST_tW_antitop_NoFullyHad_5f_pow_PS',
              'ST_tW_top_incl_5f_pow',
              'ST_tW_top_incl_5f_pow_PS',
              'ST_tW_top_NoFullyHad_5f_pow',
              'ST_tW_top_NoFullyHad_5f_pow_PS',
              'ST_tWll_5f_LO',
              'ST_tWnunu_5f_LO',
              'TTHH_LO',
              'TTJets_dilep_genMET150_LO',
              'TTJets_dilep_LO',
              'TTJets_HT1200to2500_LO',
              'TTJets_HT2500toInf_LO',
              'TTJets_HT600to800_LO',
              'TTJets_HT800to1200_LO',
              'TTJets_LO',
              'TTJets_NLO',
              'TTJets_semilepFromT_genMET150_LO',
              'TTJets_semilepFromT_LO',
              'TTJets_semilepFromTbar_genMET150_LO',
              'TTJets_semilepFromTbar_LO',
              'TTTo2L2Nu_pow',
              'TTTo2L2Nu_pow_PS',
              'TTToSemiLeptonic_pow',
              'TTToSemiLeptonic_pow_PS',
              'TTWH_LO',
              'TTWW_LO',
              'TTWZ_LO',
              'TTZH_LO',
              'TTZZ_LO', ],

       2018: ['ST_schannel_4f_NLO',
              'ST_schannel_4f_NLO_PS',
              'ST_tchannel_antitop_4f_incl_pow',
              'ST_tchannel_antitop_5f_pow_PS',
              'ST_tchannel_antitop_5f_pow_PS_old_pmx',
              'ST_tchannel_top_4f_incl_pow',
              'ST_tchannel_top_5f_pow',
              'ST_tchannel_top_5f_pow_old_pmx',
              'ST_tW_antitop_incl_5f_pow',
              'ST_tW_antitop_incl_5f_pow_PS',
              'ST_tW_antitop_NoFullyHad_5f_pow_PS',
              'ST_tW_top_incl_5f_pow',
              'ST_tW_top_incl_5f_pow_PS',
              'ST_tW_top_NoFullyHad_5f_pow',
              'ST_tW_top_NoFullyHad_5f_pow_PS',
              'ST_tWll_5f_LO',
              'ST_tWnunu_5f_LO',
              'TTHH_LO',
              'TTJets_dilep_genMET150_LO',
              'TTJets_dilep_LO',
              'TTJets_HT1200to2500_LO',
              'TTJets_HT2500toInf_LO',
              'TTJets_HT600to800_LO',
              'TTJets_HT800to1200_LO',
              'TTJets_LO',
              'TTJets_NLO',
              'TTJets_semilepFromT_genMET150_LO',
              'TTJets_semilepFromT_LO',
              'TTJets_semilepFromTbar_genMET150_LO',
              'TTJets_semilepFromTbar_LO',
              'TTTo2L2Nu_pow',
              'TTTo2L2Nu_pow_PS',
              'TTToSemiLeptonic_pow',
              'TTToSemiLeptonic_pow_PS',
              'TTWH_LO',
              'TTWW_LO',
              'TTWZ_LO',
              'TTZH_LO',
              'TTZZ_LO', ]}


QCD = {'muo': {2016: [# 'QCD_Mu_pt15to20',
                      # 'QCD_Mu_pt20to30',
                      'QCD_Mu_pt30to50',],
                      # 'QCD_Mu_pt50to80',
                      # 'QCD_Mu_pt80to120',
                      # 'QCD_Mu_pt80to120_ext1',
                      # 'QCD_Mu_pt120to170',
                      # 'QCD_Mu_pt170to300',
                      # 'QCD_Mu_pt170to300_ext1',
                      # 'QCD_Mu_pt300to470',
                      # 'QCD_Mu_pt300to470_ext1',
                      # 'QCD_Mu_pt470to600',
                      # 'QCD_Mu_pt470to600_ext1',
                      # 'QCD_Mu_pt600to800',
                      # 'QCD_Mu_pt600to800_ext1',
                      # 'QCD_Mu_pt800to1000',
                      # 'QCD_Mu_pt800to1000_ext1',
                      # 'QCD_Mu_pt1000toInf', ],

               2017: ['QCD_Mu_pt1000toInf',
                      'QCD_Mu_pt120to170',
                      'QCD_Mu_pt15to20',
                      'QCD_Mu_pt170to300',
                      'QCD_Mu_pt20to30',
                      'QCD_Mu_pt300to470',
                      'QCD_Mu_pt30to50',
                      'QCD_Mu_pt470to600',
                      'QCD_Mu_pt50to80',
                      'QCD_Mu_pt600to800',
                      'QCD_Mu_pt800to1000',
                      'QCD_Mu_pt80to120', ],

               2018: ['QCD_Mu_pt1000toInf',
                      'QCD_Mu_pt120to170',
                      'QCD_Mu_pt15to20',
                      'QCD_Mu_pt170to300',
                      'QCD_Mu_pt20to30',
                      'QCD_Mu_pt300to470',
                      'QCD_Mu_pt30to50',
                      'QCD_Mu_pt470to600',
                      'QCD_Mu_pt50to80',
                      'QCD_Mu_pt600to800',
                      'QCD_Mu_pt800to1000',
                      'QCD_Mu_pt80to120', ]},


       'ele': {2016: ['QCD_Mu_pt1000toInf_ext1',
                      'QCD_EMEnriched_pt20to30',
                      'QCD_EMEnriched_pt30to50',
                      'QCD_EMEnriched_pt30to50_ext1',
                      'QCD_EMEnriched_pt50to80',
                      'QCD_EMEnriched_pt50to80_ext1',
                      'QCD_EMEnriched_pt80to120',
                      'QCD_EMEnriched_pt80to120_ext1',
                      'QCD_EMEnriched_pt120to170',
                      'QCD_EMEnriched_pt120to170_ext1',
                      'QCD_EMEnriched_pt170to300',
                      'QCD_EMEnriched_pt300toInf',
                      'QCD_bcToE_pt15to20',
                      'QCD_bcToE_pt20to30',
                      'QCD_bcToE_pt30to80',
                      'QCD_bcToE_pt80to170',
                      'QCD_bcToE_pt170to250',
                      'QCD_bcToE_pt250toInf', ],

               2017: ['QCD_bcToE_pt170to250',
                      'QCD_bcToE_pt20to30',
                      'QCD_bcToE_pt20to30_new_pmx',
                      'QCD_bcToE_pt250toInf',
                      'QCD_bcToE_pt30to80',
                      'QCD_bcToE_pt80to170',
                      'QCD_EMEnriched_pt120to170',
                      'QCD_EMEnriched_pt170to300',
                      'QCD_EMEnriched_pt20to30',
                      'QCD_EMEnriched_pt300toInf',
                      'QCD_EMEnriched_pt30to50',
                      'QCD_EMEnriched_pt50to80',
                      'QCD_EMEnriched_pt80to120', ],

               2018: ['QCD_bcToE_pt170to250',
                      'QCD_bcToE_pt20to30',
                      'QCD_bcToE_pt20to30_new_pmx',
                      'QCD_bcToE_pt250toInf',
                      'QCD_bcToE_pt30to80',
                      'QCD_bcToE_pt80to170',
                      'QCD_EMEnriched_pt120to170',
                      'QCD_EMEnriched_pt170to300',
                      'QCD_EMEnriched_pt20to30',
                      'QCD_EMEnriched_pt300toInf',
                      'QCD_EMEnriched_pt30to50',
                      'QCD_EMEnriched_pt50to80',
                      'QCD_EMEnriched_pt80to120', ]}}

STopvsTop = {2017: ['CompSUSY', ]}


# parser
def get_parser():
    ''' Argument parser for post-processing module.
    '''
    import argparse
    argParser = argparse.ArgumentParser(description="Argument parser for \
                                        cmgPostProcessing")

    argParser.add_argument('--year',
                           action='store',
                           type=int,
                           choices=[2016, 2017],
                           required=True,
                           help="Which year?")

    argParser.add_argument('--logLevel',
                           action='store',
                           nargs='?',
                           choices=['CRITICAL',
                                    'ERROR',
                                    'WARNING',
                                    'INFO',
                                    'DEBUG',
                                    'TRACE',
                                    'NOTSET',
                                    'SYNC'],
                           default='INFO',
                           help="Log level for logging")

    argParser.add_argument('--sample',
                           action='store',
                           nargs='?',
                           type=str,
                           default='WZTo3LNu',
                           help="List of samples to be post-processed, given \
                               as CMG component name")

    argParser.add_argument('--nJobs',
                           action='store',
                           nargs='?',
                           type=int,
                           default=1,
                           help="Maximum number of simultaneous jobs.")

    argParser.add_argument('--job',
                           action='store',
                           type=int,
                           default=0,
                           help="Run only job i")

    argParser.add_argument('--version',
                           action='store',
                           nargs='?',
                           type=str,
                           required=True,
                           help="Version for output directory")

    argParser.add_argument('--flavour',
                           action='store',
                           type=str,
                           choices=['ele', 'muo'],
                           required=True,
                           help="Which flavour?")

    argParser.add_argument('--sampleSelection',
                           action='store',
                           type=str,
                           choices=['DYvsQCD', 'Top', 'all', 'STopvsTop'],
                           required=True,
                           help="Which flavour?")

    argParser.add_argument('--small',
                           action='store_true',
                           help="Run the file on a small sample \
                               (for test purpose), bool flag set to \
                                   True if used")

    argParser.add_argument('--ptSelectionStep1',
                           action='store',
                           type=str,
                           default="pt_5_-1",
                           help="Which ptSelection in step1?")

    argParser.add_argument('--ptSelection',
                           action='store',
                           type=str,
                           default="pt_5_-1",
                           help="Which ptSelection for step2?")

    argParser.add_argument('--ratio',
                           action='store',
                           type=str,
                           choices=['balanced', 'unbalanced'],
                           required=True,
                           help="Which signal to background ratio?")

    argParser.add_argument('--SV_sorting',
                           action='store',
                           type=str,
                           choices=['pt', 'ptRel', 'deltaR'],
                           default='pt',
                           help="How to sort SVs?")

    argParser.add_argument('--pfCand_sorting',
                           action='store',
                           type=str,
                           choices=['pt', 'ptRel', 'deltaR'],
                           default='ptRel',
                           help="How to sort pfCands?")

    return argParser


args = get_parser().parse_args()

# Logging
logger = logger.get_logger(args.logLevel, logFile=None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile=None)

# Generating SelectionString:
# pt selection option for different pt sub selection of ptSelection in step1
pt_threshold = (float(args.ptSelection.split('_')[1]),
                float(args.ptSelection.split('_')[2]))

kinematicSelection = 'lep_pt>{pt_min}'.format(pt_min=pt_threshold[0]) \
    if pt_threshold[1] < 0 \
    else 'lep_pt>{pt_min}&&lep_pt<={pt_max}'.format(pt_min=pt_threshold[0],
                                                    pt_max=pt_threshold[1])

selectionString = \
    '(event%{nJobs}=={job}&&abs(lep_pdgId)=={flavour}&&{kinematic})'.format(
        nJobs=args.nJobs, job=args.job, flavour='11'
        if args.flavour == 'ele'
        else '13', kinematic=kinematicSelection)


def getInputFromOthers(sub_directories,
                       class_name,
                       inputdirs=skim_directory,
                       version=args.version,
                       year=args.year):
    '''
    Description
    -----------
    loads the samples living in different directories. Returns an instance of
    Sample

    Parameters
    ----------
    sub_directories : list of lists of strings [[""], [""], ...]
        The sub-directories where the samples live. Trys to convert
        string or list into the above form
    class_name : string
        Indicates the classification (Prompt, NonPrompt, Fake, FromSUSY,
                                      FromSUSYHF).
    inputdirs : string or list of strings, optional
        The skim directory where the step1 files live.
        The default is skim_directory.
    version : string or list of string, optional
        Specifies which versions were chosen in step1.
        The default is args.version.
    year : int or list of int, optional
        Specifies the years of samples. The default is args.year.
    '''
    #-----------Checking the input for mistakes and type conversion-----------
    assert len(sub_directories) > 0, "sub_directories can not be empty!"
    assert len(class_name) > 0, "class_name can not be empty!"

    if isinstance(sub_directories, list):
        if isinstance(sub_directories[0], str):
            sub_directories = [sub_directories]
        elif not isinstance(sub_directories[0], list):
            raise TypeError("sub_directories has wrong format, must be list-of-lists")
    elif isinstance(sub_directories, str):
        sub_directories = [[sub_directories]]
    else:
        raise TypeError("sub_directories has wrong format, must be list-of-lists")

    # make inputdirs a list and use FromDirectory to take
    # also a list of directories
    if isinstance(inputdirs, list):
        nr_of_indirs = len(inputdirs)
    elif isinstance(inputdirs, str):
        nr_of_indirs = 1
        inputdirs = [inputdirs]
    else:
        raise TypeError("Don't know what to do with type of inputdirs \
                        expected list or string")

    # make year and version a list as well
    if not isinstance(year, list):
        if nr_of_indirs == 1:
            year = [str(year)]
        else:
            year = [str(year) for i in range(nr_of_indirs)]

    if not isinstance(version, list):
        if nr_of_indirs == 1:
            version = [version]
        else:
            version = [version for i in range(nr_of_indirs)]

    # For every different inputdir there must be 1 list in sub_directories
    try:
        if len(sub_directories) != nr_of_indirs:
            raise TypeError("For each element of inputdirs there must be a \
                            list in sub_directories which corresponds to it")
        elif not isinstance(sub_directories[0], list):
            raise TypeError("Each element of sub_directories must be a list \
                            \n Example: inputdirs = [skimdir1, skimdir2] then \
                                sub_directories=[[subdirs_of_sikdir1], \
                                                 [subdirs_of_skimdir2]]")
    except:
        # print("len subdirs = {}, nr of  subdirs = {}".format(\
        # len(sub_directories), nr_of_indirs))
        raise TypeError("getInputFromOthers: Format of sub_directories and \
                        inputdirs do not match.")
    #----END:---Checking the input for mistakes and type conversion-----------

    inputPath = [os.path.join(inputdirs[i],
                              version[i],
                              "step1",
                              str(year[i]),
                              args.flavour,
                              class_name,
                              str(args.ptSelectionStep1)) for i in range(nr_of_indirs)]

    directory = []
    # Fill directory with the directories where the step1 root files live
    for i in range(nr_of_indirs):
        for j in range(len(sub_directories[i])):
            directory.append(os.path.join(inputPath[i], sub_directories[i][j]))

    use_redirector = False
    for inputpath in inputPath:
        if inputpath.startswith('/eos/'):
            use_redirector = True

    sample = Sample.fromDirectory(
        name=class_name,
        directory=directory,
        treeName='tree', selectionString=selectionString,
        redirector="root://eos.grid.vbc.ac.at/" if use_redirector else None,
        skipCheck=True
    )

    # now flatten sub_directories for loggin info
    sub_directories = [sub_directories[i][j] for i in range(nr_of_indirs)
                       for j in range(len(sub_directories[i]))]

    for s in sub_directories:
        logger.debug("Loaded sample %s", s)

    logger.info("shuffeling sample files for {}".format(sample.name))
    random.shuffle(sample.files)
    return sample


logger.info("Getting Filenames")

# settings
if args.sampleSelection == "DYvsQCD":
    samplePrompt = getInputFromOthers(DY[args.year],
                                      "Prompt")

    sampleNonPrompt = getInputFromOthers(QCD[args.flavour][args.year],
                                         "NonPrompt")

    sampleFake = getInputFromOthers(QCD[args.flavour][args.year], "Fake")

    prompt = {'sample': samplePrompt, }
    nonPrompt = {'sample': sampleNonPrompt, }
    fake = {'sample': sampleFake, }
    leptonClasses = [prompt, nonPrompt, fake]
    
    # balanced condition prompt = nonPrompt+fake 
    leptonRatios = {'balanced': [[prompt], [nonPrompt, fake]],
                    'unbalanced': [leptonClass for leptonClass in leptonClasses],}




elif args.sampleSelection == "Top":
    samplePrompt = getInputFromOthers(Top[args.year], "Prompt")
    sampleNonPrompt = getInputFromOthers(Top[args.year], "NonPrompt")
    sampleFake = getInputFromOthers(Top[args.year], "Fake")

    prompt = {'sample': samplePrompt, }
    nonPrompt = {'sample': sampleNonPrompt, }
    fake = {'sample': sampleFake, }
    leptonClasses = [prompt, nonPrompt, fake]
    
    # balanced condition prompt = nonPrompt+fake 
    leptonRatios = {'balanced': [[prompt], [nonPrompt, fake]],
                    'unbalanced': [leptonClass for leptonClass in leptonClasses],}





elif args.sampleSelection == "all":
    samplePrompt = getInputFromOthers(Top[args.year]+DY[args.year], "Prompt")
    sampleNonPrompt = getInputFromOthers(Top[args.year] +
                                         QCD[args.flavour][args.year],
                                         "NonPrompt")

    sampleFake = getInputFromOthers(Top[args.year] +
                                    QCD[args.flavour][args.year],
                                    "Fake")

    prompt = {'sample': samplePrompt, }
    nonPrompt = {'sample': sampleNonPrompt, }
    fake = {'sample': sampleFake, }
    leptonClasses = [prompt, nonPrompt, fake]

    # balanced condition prompt = nonPrompt+fake 
    leptonRatios = {'balanced': [[prompt], [nonPrompt, fake]],
                    'unbalanced': [leptonClass for leptonClass in leptonClasses],}




elif args.sampleSelection == "STopvsTop":
    # prepare vars for getInputFromOthers for the Fake class
    sub_dirs = [Top[args.year], STopvsTop[2017]]
    inputdirs = ["/eos/vbc/experiments/cms/store/user/liko/skims/",
                 "/eos/vbc/user/benjamin.wilhelmy/DeepLepton/"]

    version = ["v3", "v3"]
    year = [args.year, 2017]

    samplePrompt = getInputFromOthers(sub_dirs,
                                      "Prompt",
                                      inputdirs=inputdirs,
                                      version=version,
                                      year=year)

    sampleNonPrompt = getInputFromOthers(sub_dirs,
                                         "NonPrompt",
                                         inputdirs=inputdirs,
                                         version=version,
                                         year=year)

    sampleFake = getInputFromOthers([Top[args.year]],
                                    "Fake",
                                    inputdirs=inputdirs[0],
                                    version=version[0],
                                    year=year[0])

    sampleFromSUSY = getInputFromOthers(
        [["CompSUSY"]],
        "FromSUSY",
        inputdirs=inputdirs[1],
        version=version[1],
        year=year[1])

    sampleFromSUSYHF = getInputFromOthers(
        [["CompSUSY"]],
        "FromSUSYHF",
        inputdirs=inputdirs[1],
        version=version[1],
        year=year[1])

    prompt = {'sample': samplePrompt, }
    nonPrompt = {'sample': sampleNonPrompt, }
    fake = {'sample': sampleFake, }
    fromSUSY = {'sample': sampleFromSUSY, }
    fromSUSYHF = {'sample': sampleFromSUSYHF, }
    leptonClasses = [prompt, nonPrompt, fake, fromSUSY, fromSUSYHF]
    
    # The value of balanced should be a list containing two lists
    # the balance function will balance the first list against the second
    leptonRatios = {'balanced': [[prompt, nonPrompt, fake],
                                  [fromSUSY, fromSUSYHF]],
                     'unbalanced': [leptonClass for leptonClass in leptonClasses],}

# Reducing number of files if wanted
if args.small:
    for leptonClass in leptonClasses:
        leptonClass['sample'].reduceFiles(to=2)

# Counting entries in lepton classes and adding name and Entry to leptonClasses
for leptonClass in leptonClasses:
    leptonClass['name'] = leptonClass['sample'].name
    logger.info("Counting Entries for sample {}".format(leptonClass['name']))
    leptonClass['Entries'] = leptonClass['sample'].chain.GetEntries(selectionString)
    logger.info("flavour %s class %s entries %i", args.flavour, leptonClass['name'], leptonClass['Entries'])

# Preparing leptonRatios for balancing:
# create a new entry containing the names
leptonRatios['names'] = copy.deepcopy(leptonRatios['balanced'])
# an example what this transformation does to leptonRatios is shown below
for i in range(2):
    for leptonClass_i in range(len(leptonRatios['balanced'][i])):
        leptonRatios['balanced'][i][leptonClass_i] = leptonRatios['balanced'][i][leptonClass_i]['Entries']
        leptonRatios['names'][i][leptonClass_i] = leptonRatios['names'][i][leptonClass_i]['name']
for i in range(len(leptonClasses)):
    leptonRatios['unbalanced'][i] = leptonRatios['unbalanced'][i]['Entries']
# giving for in the susy example:
# leptonRatios = {'balanced': [[prompt['Entries'], nonPrompt['Entries'], fake['Entries']],
#                              [fromSUSY['Entries'], fromSUSYHF['Entries']]],
#                 'unbalanced': [leptonClass['Entries'] for leptonClass in leptonClasses],
#                 'names': [[prompt['name'], nonPrompt['name'], fake['name']],
#                           [fromSUSY['name'], fromSUSYHF['name']]]}
# 


def balance(lepRatios):
    '''
    takes the leptonRatios dict and changes leptonRatios['balanced'] s.t.
    the first list has as many entries as the second list.
    leptonRatios['balanced'] is a list containing two lists.

    Parameters
    ----------
    lepRatios : TYPE dict
        contains the info how to balance.
    '''

    if len(lepRatios['balanced']) != 2:
        raise TypeError("balance: Dont know how to \
                            balance list has wrong format")

    if args.ratio == 'unbalance':
        logger.info(
            "Calling the balance function even args.ratio is unbalance!")

    if sum(lepRatios['balanced'][0]) >= sum(lepRatios['balanced'][1]):
        # we call the lep classes with more entries background and the others
        # signal. Signal stores also which lep classes we call background. 
        # We will rescale the 'background' s.t. it matches the number of signal entries
        background = [float(sum(lepRatios['balanced'][0])), 0]
        signal = float(sum(lepRatios['balanced'][1]))
    else:
        background = [float(sum(lepRatios['balanced'][1])), 1]
        signal = float(sum(lepRatios['balanced'][0]))

    background_array = np.array(lepRatios['balanced'][background[1]])

    try:
        background_array = signal * background_array / background[0]
    except:
        raise ZeroDivisionError(
            "empty sample divition through zero while balancing")

    # throwing away events to balance
    for i in range(len(background_array)):
        diff = lepRatios['balanced'][background[1]][i] - int(round(background_array[i]))
        lepRatios['balanced'][background[1]][i] = int(round(background_array[i]))
        logger.info("BALANCING: Throwing {} {} leptons away to balance, keeping {} leptons".format(
            diff,
            lepRatios['names'][background[1]][i],
            lepRatios['balanced'][background[1]][i]))

    logger.info("BALANCING: first category has {} leptons, the second {}".format(sum(lepRatios['balanced'][0]), sum(lepRatios['balanced'][1])))
    # now flatten the lepRatios['balanced'] list
    lepRatios['balanced'] = lepRatios['balanced'][0] + lepRatios['balanced'][1]


