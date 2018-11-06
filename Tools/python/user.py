import os

if os.environ['USER'] in ['schoef', 'rschoefbeck']:
    plot_directory      = "/afs/hephy.at/user/r/rschoefbeck/www/DeepLepton/"
    skim_directory   = "/afs/hephy.at/data/rschoefbeck01/DeepLepton/skims/"

if os.environ['USER'] in ['gmoertl']:
    plot_directory          = "/afs/hephy.at/user/g/gmoertl/www/"
    skim_directory   = "/afs/hephy.at/data/gmoertl01/DeepLepton/skims/"
