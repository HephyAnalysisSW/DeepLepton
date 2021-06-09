# Standard imports
from RootTools.core.helpers import shortTypeDict
import RootTools.core.logger as logger_rt
import ROOT
import os
import sys
import importlib
# import random

# RootTools
from RootTools.core.standard import *

# DeepLepton
from DeepLepton.Tools.user import skim_directory

# here the sample configuration is handeled in particular parsing is done there
# also loggers are instanitated there
from step2_config import *


# find leaf structure
structure = {'': []}

# loop over the sample with the most general list of leaves which should
# be the last element of leptonClasses
for l in leptonClasses[-1]['sample'].chain.GetListOfLeaves():
    # this is an element of a vector branch:
    if l.GetLeafCount():
        counter_var = l.GetLeafCount().GetName()
        vector_name = counter_var[1:]
        vector_branch_declaration = (
            l.GetName()[len(vector_name)+1:], shortTypeDict[l.GetTypeName()])

        if not structure.has_key(vector_name):
            structure[vector_name] = [vector_branch_declaration]
        else:
            structure[vector_name].append(vector_branch_declaration)
    else:
        structure[''].append((l.GetName(), shortTypeDict[l.GetTypeName()]))

# define variables for reading and writing
# they should be the same no?
read_variables = []
write_variables = []
for key, value in structure.iteritems():
    if key == '':
        read_variables.extend(map(lambda v: '/'.join(v), value))
        write_variables.extend(map(lambda v: '/'.join(v), value))
    else:
        read_variables.append(
            key+'[%s]' % (','.join(map(lambda v: '/'.join(v), value))))
        write_variables.append(
            key+'[%s]' % (','.join(map(lambda v: '/'.join(v), value))))
        read_variables.append('n'+key+'/I')

variables = []
for v in read_variables:
    if v.startswith("SV") or v.startswith("pfCand"):
        variables.append(VectorTreeVariable.fromString(v, nMax=nMax))
    else:
        variables.append(TreeVariable.fromString(v))
read_variables = variables

variables = []
for v in write_variables:
    if v.startswith("SV") or v.startswith("pfCand"):
        variables.append(VectorTreeVariable.fromString(v, nMax=nMax))
    else:
        variables.append(TreeVariable.fromString(v))
write_variables = variables


# Loop over samples
for leptonClass in leptonClasses:
    logger.info("Constructing the reader for class %s", leptonClass['name'])
    leptonClass['reader'] = leptonClass['sample'].treeReader(
        # map( lambda v: TreeVariable.fromString(v) if type(v)==type("") else v, read_variables ),
        variables=read_variables,
        selectionString=selectionString
    )

# decide on whether we write all events or balance the output
if args.ratio == 'balanced':
    balance(leptonRatios)

x = [[i for i in range(len(leptonClasses))],
     [leptonentries for leptonentries in leptonRatios[args.ratio]]]

choices = sum(([t] * w for t, w in zip(*x)), [])
random.shuffle(choices)


n_maxfileentries = 100000
n_current_entries = 0
n_file = 0

# consider changing back to skimdir
outputDir = os.path.join("/scratch-cbe/users/benjamin.wilhelmy/DeepLepton", #skim_directory,
                         args.version + ("_small" if args.small else ""),
                         "step2",
                         str(args.year),
                         args.flavour,
                         args.ratio,
                         args.ptSelection,
                         args.sampleSelection)


try:
    os.makedirs(outputDir)
except OSError as err:
    pass


def make_maker(n_file):
    tmp_directory = ROOT.gDirectory
    outfile = ROOT.TFile.Open(os.path.join(
        outputDir, 'modulo_'+str(args.job)+'_trainfile_%i.root' % n_file), 'recreate')
    outfile.cd()
    maker = TreeMaker(sequence=[],
                      # map( lambda v: TreeVariable.fromString(v) if type(v)==type("") else v, write_variables),
                      variables=write_variables,
                      treeName='tree')
    tmp_directory.cd()
    maker.outfile = outfile
    return maker


logger.info("Starting Readers")

# start all readers
for leptonClass in leptonClasses:
    leptonClass['reader'].start()
    leptonClass['counter'] = 0

logger.info('Begin Lepton Loop')


for i_choice, choice in enumerate(choices):

    # (re)create and save output files
    if n_current_entries == 0 and n_file == 0:
        maker = make_maker(n_file)
        maker.start()
    if n_current_entries == 0 and n_file > 0:
        logger.info("%i entries copied to %s",
                    maker.tree.GetEntries(), maker.outfile.GetName())
        logger_string = "Counter: "
        for leptonClass in leptonClasses:
            logger_string += leptonClass['name'] + " {}; ".format(leptonClass['counter'])
        logger.info(logger_string)
        maker.outfile.Write()
        maker.outfile.Close()
        logger.info("Written %s", maker.outfile.GetName())

        maker = make_maker(n_file)
        maker.start()

    # increase counters
    leptonClasses[choice]['counter'] += 1
    n_current_entries += 1

    reader = leptonClasses[choice]['reader']
    reader.run()
    r = reader.event

    # copy
    for name, value in structure.iteritems():
        if name == '':
            for branch_name, _ in value:
                # if some samples have branches other samples doesnt have they will be written but with
                # some default value (for integers its -1).
                # in the susy case we want the value to be 0
                if branch_name in ['lep_isFromSUSY_Training', 'lep_isFromSUSYHF_Training', 'lep_isFromSUSYandHF_Training'] and \
                        not "SUSY" in leptonClasses[choice]['name']:
                    setattr(maker.event, branch_name, 0)

                else:
                    setattr(maker.event, branch_name, getattr(r, branch_name))
        else:
            setattr(maker.event, "n"+name, getattr(r, "n"+name))
            # sorting of SV and candidates
            n_objs = min(nMax, getattr(r, "n"+name))

            # obtain sorting values as list ( [val, i_val], ...) and sort descending wrt. to val (ascending for deltaR).

            if name == 'SV':
                sort_vals = [(getattr(r, "%s_%s" % (name, args.SV_sorting))[
                              i], i) for i in range(n_objs)]
                if args.SV_sorting == 'deltaR':
                    sort_vals.sort()
                else:
                    sort_vals.sort(key=lambda v: -v[0])
            elif name.startswith('pfCand_'):
                sort_vals = [(getattr(r, "%s_%s" % (name, args.pfCand_sorting))[
                              i], i) for i in range(n_objs)]
                if args.pfCand_sorting == 'deltaR':
                    sort_vals.sort()
                else:
                    sort_vals.sort(key=lambda v: -v[0])
            else:
                raise RuntimeError("Don't know what to do with %r." % name)
            for val in value:
                for i in range(n_objs):
                    getattr(maker.event, "%s_%s" % (name, val[0]))[i] = getattr(
                        r, "%s_%s" % (name, val[0]))[sort_vals[i][1]]
    maker.run()

    # check if maximal file entries reached
    if n_current_entries >= n_maxfileentries:
        n_current_entries = 0
        n_file += 1


# Save and Close last output File
logger.info("%i entries copied to %s",
            maker.tree.GetEntries(), maker.outfile.GetName())
logger_string = "Counter: "
for leptonClass in leptonClasses:
    logger_string += leptonClass['name'] + " {}, ".format(leptonClass['counter'])
logger.info(logger_string)
maker.outfile.Write()
maker.outfile.Close()
logger.info("Written %s", maker.outfile.GetName())
logger.info('Successfully Finished')
