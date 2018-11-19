'''
Extract cmg samples from dpm'''

if __name__ == '__main__':
    # Parse args if main
    maxN_def = -1
    def get_parser():
        ''' Argument parser for post-processing module.
        '''
        import argparse
        argParser = argparse.ArgumentParser(description = "Argument parser for cmgPostProcessing")
        argParser.add_argument('--logLevel', action='store', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'DEBUG', 'DEBUG', 'TRACE', 'NOTSET'], default='INFO', help="Log level for logging" )
        argParser.add_argument('--overwrite', action='store_true', default=False, help="Overwrite cache?" )
        argParser.add_argument('--nomultithreading', action='store_true', default=False, help="No multithreading?" )
        argParser.add_argument('--maxN', action='store', type=int, default=maxN_def, help="Overwrite cache?" )

        return argParser

    options = get_parser().parse_args()

    # Logging
    import DeepLepton.Tools.logger as logger_
    logger = logger_.get_logger(options.logLevel, logFile = None )
    
    overwrite = options.overwrite
    multithreading = not options.nomultithreading
    maxN = options.maxN
    forceProxy = False

else:
    # Logging
    import logging
    import subprocess
    logger = logging.getLogger(__name__)
    multithreading = False
    overwrite = False
    forceProxy = False
    try:
        proxyCheck = subprocess.check_output( 'voms-proxy-info' )
    except subprocess.CalledProcessError:
        forceProxy = True
    #if proxyCheck.startswith("Error: Could not find or load main class error"): 
    #    forceProxy = True
    maxN =      -1

# DeepLepton
from DeepLepton.samples.walk_dpm import walk_dpm
from RootTools.core.helpers import checkRootFile

# Standard imports
import os
import pickle

class heppy_mapper:

    def __init__(self, heppy_samples, dpm_directories, cache_file, multithreading=True, path_substrings = None):
        # Read cache file, if exists
        if os.path.exists( cache_file ) and not overwrite:
            self.sample_map = pickle.load( file(cache_file) )
            logger.info( "Loaded cache file %s" % cache_file )
        else:
            logger.info( "Cache file %s not found. Recreate map.", cache_file)
            logger.info( "Check proxy.")

            # Proxy certificate
            from RootTools.core.helpers import renew_proxy
            # Make proxy in afs to allow batch jobs to run
            proxy_path = os.path.expandvars('$HOME/private/.proxy')
            proxy = renew_proxy( proxy_path )
            logger.info( "Using proxy %s"%proxy )

            # Read dpm directories
            self.cmg_directories = {}
            for data_path in dpm_directories:
                logger.info( "Walking dpm directory %s", data_path )
                walker = walk_dpm( data_path )
                self.cmg_directories[ data_path ] = walker.walk_dpm_cmgdirectories('.',  maxN = maxN, path_substrings = path_substrings)
                
                #del walker

            logger.info( "Now mapping directories to heppy samples" )
            for heppy_sample in heppy_samples:
                heppy_sample.candidate_directories = []
                pd, era = heppy_sample.dataset.split('/')[1:3]
                for data_path in self.cmg_directories.keys():
                    for dpm_directory in self.cmg_directories[data_path].keys():
                        if not ('/%s/'%pd in dpm_directory):
                            logger.debug( "/%s/ not in dpm_directory %s", pd, dpm_directory )
                            continue
                        if not ('/'+era in dpm_directory):
                            logger.debug( "/%s not in dpm_directory %s", era, dpm_directory )
                            continue
                        heppy_sample.candidate_directories.append([data_path, dpm_directory])
                        logger.debug( "heppy sample %s in %s", heppy_sample.name, dpm_directory)
                logger.info(  "Found heppy sample %s in %i directories.", heppy_sample.name, len(heppy_sample.candidate_directories) ) 

            # Merge
            from RootTools.core.Sample import Sample
            logger.info( "Now making new sample map from %i directories and for %i heppy samples to be stored in %s", len(dpm_directories), len(heppy_samples), cache_file )
            self.sample_map = {}
            for heppy_sample in heppy_samples:
                if len(heppy_sample.candidate_directories)==0:
                    logger.info("No directory found for %s", heppy_sample.name)
                else:
                    normalization, files = walker.combine_cmg_directories(\
                            cmg_directories = {dpm_directory:self.cmg_directories[data_path][dpm_directory] for data_path, dpm_directory in heppy_sample.candidate_directories }, 
                            multithreading = multithreading, 
                        )
                    logger.info( "Sample %s: Found a total of %i files with normalization %3.2f", heppy_sample.name, len(files), normalization)
                    tmp_files = []
                    for f in files:
                        isGoodFile = False
                        try:
                            isGoodFile = checkRootFile("root://hephyse.oeaw.ac.at/" + os.path.join( f ))
                            logger.debug("File %s got added", f)
                        except IOError:
                            logger.info("File %s is corrupted, skipping",f)
                        if isGoodFile: tmp_files.append(f)
                    self.sample_map[heppy_sample] = Sample.fromFiles(
                        heppy_sample.name,
                        files = ['root://hephyse.oeaw.ac.at/'+f for f in tmp_files],
                        normalization = normalization, 
                        treeName = 'tree', isData = heppy_sample.isData, maxN = maxN)
                    
                    logger.info("Combined %i directories for sample %s to a total of %i files with normalization %3.2f", len(heppy_sample.candidate_directories), heppy_sample.name, len(files), normalization)

            # Store cache file
            dir_name = os.path.dirname( cache_file ) 
            if len(self.sample_map.keys())>0:
                if not os.path.exists( dir_name ): os.makedirs( dir_name )
                pickle.dump( self.sample_map, file( cache_file, 'w') )
                logger.info( "Created MC sample cache %s", cache_file )
            else:
                logger.info( "Skipping to write %s because map is empty.", cache_file )

    def dump_files_dict( self, filename):
        pickle.dump( {k.name:val.files for k, val in self.sample_map.iteritems()}, file(filename,'w') )
        logger.info( "Written %s", filename )
    
    @property                
    def heppy_sample_names( self ):
        return [s.name for s in self.sample_map.keys()]

    def from_heppy_sample( self, heppy_sample, maxN = -1):
        if self.sample_map.has_key( heppy_sample ):
            res = self.sample_map[heppy_sample]
            if maxN>0: res.files = res.files[:maxN]
            res.heppy = heppy_sample
            return res
    def from_heppy_samplename( self, heppy_samplename, maxN = -1):
        for heppy_sample in self.sample_map.keys():
            if heppy_samplename==heppy_sample.name:
                res = self.sample_map[heppy_sample]
                if maxN>0: res.files = res.files[:maxN]
                res.heppy = heppy_sample
                return res
        
# Proxy certificate
from RootTools.core.helpers import renew_proxy
# Make proxy in afs to allow batch jobs to run
proxy_path = os.path.expandvars('$HOME/private/.proxy')
if not forceProxy:
    proxy = renew_proxy( proxy_path )
else:
    logger.info("Not checking your proxy. Asuming you know it's still valid.")
    proxy = proxy_path
logger.info( "Using proxy %s"%proxy )


# Summer16 MC for Deeplepton training
lepton_2016_cache_file = '/afs/hephy.at/data/rschoefbeck01/TopEFT/dpm_sample_caches/80X_MC_Summer16_2016_lepton2016_v4.pkl' 
robert_lepton2016_v4 = ['/dpm/oeaw.ac.at/home/cms/store/user/schoef/cmgTuples/lepton/']
mc_dpm_directories = robert_lepton2016_v4
from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import mcSamples as heppy_mc_Moriond_samples
lepton_2016_heppy_mapper = heppy_mapper( heppy_mc_Moriond_samples, mc_dpm_directories, lepton_2016_cache_file, multithreading=multithreading, path_substrings = ["lepton2016_v3"])

# Summer16 MC fullevents for Deeplepton
lepton_2016_cache_file = '/afs/hephy.at/data/rschoefbeck01/TopEFT/dpm_sample_caches/80X_MC_Summer16_2016_lepton2016_v3_full_events_v3.pkl' 
robert_2016_1l_full_events = ['/dpm/oeaw.ac.at/home/cms/store/user/schoef/cmgTuples/full_events']
mc_dpm_directories =robert_2016_1l_full_events 
from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import mcSamples as heppy_mc_Moriond_samples
lepton_2016_mc_heppy_mapper = heppy_mapper( heppy_mc_Moriond_samples, mc_dpm_directories, lepton_2016_cache_file, multithreading=multithreading)
#lepton_2016_mc_heppy_mapper.dump_files_dict( lepton_2016_cache_file.replace('.pkl', '_files_dict.pkl') )

# Data 2016, 07Aug17
data_cache_file = '/afs/hephy.at/data/rschoefbeck01/TopEFT/dpm_sample_caches/Run2016_data_2016_full_events_v3.pkl'
robert_2016_1l_v3 = ['/dpm/oeaw.ac.at/home/cms/store/user/schoef/cmgTuples/full_events']
data_dpm_directories = robert_2016_1l_v3
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import dataSamples as heppy_data_samples
data_07Aug17_heppy_mapper = heppy_mapper( heppy_data_samples, data_dpm_directories , data_cache_file, multithreading=multithreading)
