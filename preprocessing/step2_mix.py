# Standard imports
import ROOT
import os
import sys
import importlib
import random

# RootTools
from RootTools.core.standard import *

# DeepLepton
from DeepLepton.Tools.user import skim_directory 

#TODO commented samples ned step 1 redone
DY  = { 2016:['DYJetsToLL_M50_LO',
              'DYJetsToLL_M50_LO_ext2',
              'DYJetsToLL_M50_ext2',
              'DYJetsToLL_M10to50_LO',
              'DYJetsToLL_M10to50',
 
              'DYJetsToLL_M50_HT70to100',
              'DYJetsToLL_M50_HT100to200_ext',
              'DYJetsToLL_M50_HT200to400',
              'DYJetsToLL_M50_HT200to400_ext',
              'DYJetsToLL_M50_HT400to600',
              'DYJetsToLL_M50_HT400to600_ext',
              'DYJetsToLL_M50_HT600to800',
              'DYJetsToLL_M50_HT800to1200',
              'DYJetsToLL_M50_HT1200to2500',
              'DYJetsToLL_M50_HT2500toInf',

              'DYJetsToLL_M5to50_HT70to100',
              'DYJetsToLL_M5to50_HT100to200',
              'DYJetsToLL_M5to50_HT100to200_ext',
              'DYJetsToLL_M5to50_HT200to400',
              'DYJetsToLL_M5to50_HT200to400_ext',
              'DYJetsToLL_M5to50_HT400to600',
              'DYJetsToLL_M5to50_HT400to600_ext',
              'DYJetsToLL_M5to50_HT600toInf',], 
        2017:[], 
        2018:[]}

Top = { 2016:['TTTo2L2Nu_noSC_pow',
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
              'ST_tW_antitop_5f_pow',
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
              'TGG',], 
        2017:[], 
        2018:[]}

QCD = { 'muo': {2016: ['QCD_Mu_pt15to20',
                       'QCD_Mu_pt20to30',
                       'QCD_Mu_pt30to50',
                       'QCD_Mu_pt50to80',
                       'QCD_Mu_pt80to120',
                       'QCD_Mu_pt80to120_ext1',
                       'QCD_Mu_pt120to170',
                       'QCD_Mu_pt170to300',
                       'QCD_Mu_pt170to300_ext1',
                       'QCD_Mu_pt300to470',
                       'QCD_Mu_pt300to470_ext1',
                       'QCD_Mu_pt470to600',
                       'QCD_Mu_pt470to600_ext1',
                       'QCD_Mu_pt600to800',
                       'QCD_Mu_pt600to800_ext1',
                       'QCD_Mu_pt800to1000',
                       'QCD_Mu_pt800to1000_ext1',
                       'QCD_Mu_pt1000toInf',], 
                2017: [], 
                2018: []},

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
                       'QCD_bcToE_pt250toInf',], 
                2017: [], 
                2018: []}} 

#parser
def get_parser():
    ''' Argument parser for post-processing module.
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser for cmgPostProcessing")

    argParser.add_argument('--year',                        action='store',                     type=int,   choices=[2016,2017],    required = True,               help="Which year?")
    argParser.add_argument('--logLevel',                    action='store',         nargs='?',              choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET', 'SYNC'],     default='INFO',                     help="Log level for logging")
    argParser.add_argument('--sample',                      action='store',         nargs='?',  type=str,                           default='WZTo3LNu',            help="List of samples to be post-processed, given as CMG component name")
    argParser.add_argument('--nJobs',                       action='store',         nargs='?',  type=int,                           default=1,                     help="Maximum number of simultaneous jobs.")
    argParser.add_argument('--job',                         action='store',                     type=int,                           default=0,                     help="Run only job i")
    argParser.add_argument('--version',                     action='store',         nargs='?',  type=str,  required = True,                                        help="Version for output directory")
    argParser.add_argument('--flavour',                     action='store',                     type=str,   choices=['ele','muo'],    required = True,             help="Which flavour?")
    argParser.add_argument('--sampleSelection',             action='store',                     type=str,   choices=['DYvsQCD', 'Top', 'all'],           required = True,             help="Which flavour?")
    argParser.add_argument('--small',                       action='store_true',                                                                                   help="Run the file on a small sample (for test purpose), bool flag set to True if used")        
    argParser.add_argument('--ptSelectionStep1',            action='store',                     type=str,   default = "pt_5_-1",                                   help="Which ptSelection in step1?")
    argParser.add_argument('--ptSelection',                 action='store',                     type=str,   default = "pt_5_-1",                                   help="Which ptSelection for step2?")
    argParser.add_argument('--ratio',                       action='store',                     type=str,   choices=['balanced', 'unbalanced'], required = True,   help="Which signal to background ratio?")
    argParser.add_argument('--SV_sorting',                  action='store',                     type=str,   choices=['pt', 'ptRel', 'deltaR'], default ='pt',      help="How to sort SVs?")
    argParser.add_argument('--pfCand_sorting',              action='store',                     type=str,   choices=['pt', 'ptRel', 'deltaR'], default ='ptRel',   help="How to sort pfCands?")

    return argParser

args = get_parser().parse_args()

# Logging
import DeepLepton.Tools.logger as logger
logger  = logger.get_logger(args.logLevel, logFile = None)
import RootTools.core.logger as logger_rt
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None )

#pt selection option for different pt sub selection of ptSelection in step1
pt_threshold = (float(args.ptSelection.split('_')[1]), float(args.ptSelection.split('_')[2]))
kinematicSelection = 'lep_pt>{pt_min}'.format( pt_min=pt_threshold[0] ) if pt_threshold[1]<0 else 'lep_pt>{pt_min}&&lep_pt<={pt_max}'.format( pt_min=pt_threshold[0], pt_max=pt_threshold[1] )

selectionString = '(event%{nJobs}=={job}&&abs(lep_pdgId)=={flavour}&&{kinematic})'.format( nJobs=args.nJobs, job=args.job, flavour='11' if args.flavour=='ele' else '13', kinematic = kinematicSelection)

random.seed(100) # Otherwise file shuffling not deterministic!
def getInput( sub_directories, class_name):
    assert len(sub_directories)>0, "sub_directories can not be empty!"
    inputPath = os.path.join( skim_directory, args.version, "step1", str(args.year), args.flavour, class_name, args.ptSelectionStep1)
    # prepend redirector for /eos/ paths
    sample = Sample.fromDirectory( 
        name = class_name, 
        directory = [os.path.join( inputPath, s ) for s in sub_directories], 
        treeName = 'tree', selectionString=selectionString,
        redirector = "root://eos.grid.vbc.ac.at/" if inputPath.startswith('/eos/') else None,
        )
    random.shuffle( sample.files )
    return sample

#settings
if args.sampleSelection == "DYvsQCD":
    samplePrompt    = getInput( DY[args.year], "Prompt")
    sampleNonPrompt = getInput( QCD[args.flavour][args.year], "NonPrompt")
    sampleFake      = getInput( QCD[args.flavour][args.year], "Fake")
elif args.sampleSelection == "TT":
    samplePrompt    = getInput( Top[args.year], "Prompt")
    sampleNonPrompt = getInput( Top[args.year], "NonPrompt")
    sampleFake      = getInput( Top[args.year], "Fake")
elif args.sampleSelection == "all":
    samplePrompt    = getInput( Top[args.year]+DY[args.year],  "Prompt")
    sampleNonPrompt = getInput( Top[args.year]+QCD[args.flavour][args.year], "NonPrompt")
    sampleFake      = getInput( Top[args.year]+QCD[args.flavour][args.year], "Fake")

nMax = 500 # For the read and write buffer

if args.small:
    for s in [ samplePrompt, sampleNonPrompt, sampleFake ]: 
        s.reduceFiles( to = 2 )

prompt    =  {'name':'Prompt',    'sample':samplePrompt,    }
nonPrompt =  {'name':'NonPrompt', 'sample':sampleNonPrompt, }
fake      =  {'name':'Fake',      'sample':sampleFake,      }

leptonClasses  = [ prompt, nonPrompt, fake ]

# find leaf structure
from RootTools.core.helpers import shortTypeDict
structure = {'':[]}
for l in prompt['sample'].chain.GetListOfLeaves():
    # this is anm element of a vector branch:
    if l.GetLeafCount():
        counter_var = l.GetLeafCount().GetName()
        vector_name = counter_var[1:]

        vector_branch_declaration = ( l.GetName()[len(vector_name)+1:], shortTypeDict[l.GetTypeName()] )
        if not structure.has_key(vector_name):
            structure[vector_name] = [ vector_branch_declaration ]
        else:
            structure[vector_name].append( vector_branch_declaration )
    else:
        structure[''].append( (l.GetName(), shortTypeDict[l.GetTypeName()]))

# define variables for reading and writing
read_variables = []
write_variables = []
for key, value in structure.iteritems():
    if key=='':
        read_variables.extend(  map( lambda v: '/'.join(v), value ) )
        write_variables.extend( map( lambda v: '/'.join(v), value ) )
    else:
        read_variables.append( key+'[%s]'% (','.join (map( lambda v: '/'.join(v), value )) ) )
        write_variables.append( key+'[%s]'% (','.join(map( lambda v: '/'.join(v), value )) ) )
        read_variables.append( 'n'+key+'/I' )

variables = []
for v in read_variables:
    if v.startswith("SV") or v.startswith("pfCand"):
        variables.append(VectorTreeVariable.fromString( v, nMax=nMax ) )
    else:
        variables.append( TreeVariable.fromString( v ) )
read_variables = variables

variables = []
for v in write_variables:
    if v.startswith("SV") or v.startswith("pfCand"):
        variables.append(VectorTreeVariable.fromString( v, nMax=nMax ) )
    else:
        variables.append( TreeVariable.fromString( v ) )
write_variables = variables

#Loop over samples
for leptonClass in leptonClasses:
    logger.info( "Class %s", leptonClass['name'] )
    leptonClass['Entries'] = leptonClass['sample'].chain.GetEntries(selectionString)
    logger.info( "flavour %s class %s entries %i", args.flavour, leptonClass['name'], leptonClass['Entries'] )
    leptonClass['reader'] = leptonClass['sample'].treeReader( \
        variables = variables_r, #map( lambda v: TreeVariable.fromString(v) if type(v)==type("") else v, read_variables ),
        selectionString = selectionString
        )

# decide on whether we write all events or balance the output
if args.ratio == 'balanced':
    x = [[0,1,2], [nonPrompt['Entries']+fake['Entries'], nonPrompt['Entries'], fake['Entries']]]
else:
    x = [[0,1,2], [leptonClass['Entries'] for leptonClass in leptonClasses]]

choices = sum(([t] * w for t, w in zip(*x)), [])
random.shuffle(choices)

n_maxfileentries    = 100000
n_current_entries   = 0
n_file              = 0

outputDir = os.path.join( skim_directory, args.version + ("_small" if args.small else ""), "step2", str(args.year), args.flavour, args.ptSelection, args.sampleSelection)

try:
    os.makedirs(outputDir)
except OSError as err:
    pass

def make_maker( n_file ):
    tmp_directory = ROOT.gDirectory
    outfile = ROOT.TFile.Open(os.path.join( outputDir, 'modulo_'+str(args.job)+'_trainfile_%i.root'%n_file ), 'recreate')
    outfile.cd()
    maker = TreeMaker( sequence  = [ ],
        variables = variables_w, #map( lambda v: TreeVariable.fromString(v) if type(v)==type("") else v, write_variables),
        treeName = 'tree')
    tmp_directory.cd()
    maker.outfile = outfile
    return maker

#start all readers
for leptonClass in leptonClasses:
    leptonClass['reader'].start()
    leptonClass['counter'] = 0

for i_choice, choice in enumerate(choices):

    #(re)create and save output files
    if n_current_entries==0 and n_file==0:
        maker = make_maker( n_file )
        maker.start()
    if n_current_entries==0 and n_file>0:
        logger.info("%i entries copied to %s", maker.tree.GetEntries(), maker.outfile.GetName() )
        logger.info("Counter: prompt %i nonprompt %i fake %i", prompt['counter'], nonPrompt['counter'], fake['counter'])
        maker.outfile.Write()
        maker.outfile.Close()
        logger.info( "Written %s", maker.outfile.GetName())

        maker = make_maker( n_file )
        maker.start()

    #increase counters
    leptonClasses[choice]['counter'] += 1
    n_current_entries += 1

    reader = leptonClasses[choice]['reader']
    reader.run()
    r = reader.event

    # copy
    for name, value in structure.iteritems():
        if name=='':
            for branch_name, _ in value:
                setattr( maker.event, branch_name, getattr( r, branch_name ) )
        else:
            setattr( maker.event, "n"+name, getattr( r, "n"+name ) )
            # sorting of SV and candidates
            n_objs = min( nMax, getattr( r, "n"+name ) )

            # obtain sorting values as list ( [val, i_val], ...) and sort descending wrt. to val (ascending for deltaR). 
            
            if name=='SV':
                sort_vals = [ ( getattr( r, "%s_%s"%(name, args.SV_sorting) )[i], i) for i in range( n_objs ) ]
                if args.SV_sorting=='deltaR':
                    sort_vals.sort()
                else: 
                    sort_vals.sort(key=lambda v:-v[0])
                #print name, args.SV_sorting, sort_vals 
            elif name.startswith('pfCand_'):
                sort_vals = [ ( getattr( r, "%s_%s"%(name, args.pfCand_sorting) )[i], i) for i in range( n_objs ) ] 
                if args.pfCand_sorting=='deltaR':
                    sort_vals.sort()
                else: 
                    sort_vals.sort(key=lambda v:-v[0])
                #print name, args.pfCand_sorting, sort_vals 
            else:
                raise RuntimeError("Don't know what to do with %r."%name) 
            for val in value:
                for i in range( n_objs ):
                    getattr( maker.event, "%s_%s"%(name, val[0]) )[i] =  getattr( r, "%s_%s"%(name, val[0]) )[sort_vals[i][1]]
    maker.run()

    #check if maximal file entries reached
    if n_current_entries>=n_maxfileentries:
        n_current_entries=0
        n_file += 1

    # in balanced running, we could have too few prompt events to balance fake+nonprompt. When we reach the end of the prompt tree, we therefore stop.
    if args.ratio == 'balanced' and prompt['Entries'] == prompt['counter']:
        logger.info("Balanced ratio: Stopping early because there are no more prompt events.")
        break 

#Save and Close last output File        
logger.info("%i entries copied to %s", maker.tree.GetEntries(), maker.outfile.GetName() ) 
logger.info("Counter: prompt %i nonprompt %i fake %i", prompt['counter'], nonPrompt['counter'], fake['counter'])
maker.outfile.Write()
maker.outfile.Close()
logger.info( "Written %s", maker.outfile.GetName())
logger.info('Successfully Finished')
