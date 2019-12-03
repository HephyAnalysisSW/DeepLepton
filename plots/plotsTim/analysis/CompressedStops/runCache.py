from regions import regions

sample_list = ["DY", "TTJets_DiLepton", "WJets", "VV", "TTJets_SingleLepton", "SMS", "Data"]

sh_file_name = "run_cache.sh"

with open(sh_file_name, 'w') as sh_file:
    for sample in sample_list:
        for region in range(len(regions)):
            sh_file.write('python cacheRegion.py --year 2016 --selection "lep_SR_all-jet_SR-med_met-filters" --sample  "%s" --region %i'%(sample, region)+'\n')




