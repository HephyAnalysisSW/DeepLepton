from regions import regions

sample_list = ["DY", "TTJets_DiLepton", "WJets", "VV", "TTJets_SingleLepton", "SMS", "Data"]

sh_file_name = "launch_cache.sh"

#for region in regions:
#    print(str(region))

selections = ["lep_SR_mu-jet_SR-lower_met-filters-Compressed_Stops_special","lep_SR_all-jet_SR-med_met-filters-Compressed_Stops_special","lep_SR_all-jet_SR-met_pt300-filters-Compressed_Stops_special"]


with open(sh_file_name, 'w') as sh_file:
    for sample in sample_list:
        for i_region, region in enumerate(regions):
            selection = selections[i_region%3]
            if 'low_met' in selection:
                lumi = 33.2
            else: 
                lumi = 35.9
            sh_file.write('python cacheRegion.py --year 2016  --lumi %f --selection "%s" --sample  "%s" --region %i'%(lumi, selection, sample, i_region)+'\n')



