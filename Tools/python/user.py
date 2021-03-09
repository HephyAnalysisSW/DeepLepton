import os

if os.environ['USER'] in ['robert.schoefbeck']:
    #plot_directory   = "/afs/hephy.at/user/r/rschoefbeck/www/DeepLepton/"
    #skim_directory   = "/scratch-cbe/users/robert.schoefbeck/DeepLepton/"
    skim_directory   = "/eos/vbc/user/maximilian.moser/DeepLepton"
    #data_directory   = "/afs/hephy.at/data/rschoefbeck02/cmgTuples/"

if os.environ['USER'] in ['maximilian.moser']:     
    plot_directory   = "/scratch-cbe/users/maximilian.moser/www/DeepLepton/"
    #plot_directory   = "~/Plots/"
    #skim_directory   = "/scratch-cbe/users/maximilian.moser/DeepLepton/"
    skim_directory   = "/eos/vbc/user/maximilian.moser/DeepLepton"
    #data_directory   = "/afs/hephy.at/data/mmoser/cmgTuples/"

if os.environ['USER'] in ['gmoertl']:
    plot_directory   = "/afs/hephy.at/user/g/gmoertl/www/"
    skim_directory   = "/afs/hephy.at/data/cms02/DeepLepton/skims/"
    data_directory   = "/afs/hephy.at/data/rschoefbeck02/cmgTuples/"

if os.environ['USER'] in ['sschneider']:
    plot_directory   = "/afs/hephy.at/user/s/sschneider/www/"
    skim_directory   = "/afs/hephy.at/data/cms01/DeepLepton/skims/"
    data_directory   = "/afs/hephy.at/data/rschoefbeck02/cmgTuples/"

if os.environ['USER'] in ['tbrueckler']:
    plot_directory   = "/afs/hephy.at/user/t/tbrueckler/www/"
    skim_directory   = "/afs/hephy.at/data/cms03/tbrueckler/DeepLepton/skims/"
    data_directory   = "/afs/hephy.at/data/rschoefbeck02/cmgTuples/"
    cache_directory  = "/afs/hephy.at/data/cms03/tbrueckler/CompressedStops/caches_valid/"

