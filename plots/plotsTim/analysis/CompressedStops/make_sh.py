from regions import regions

sample_list = ["DY", "TTJets_DiLepton", "WJets", "VV", "TTJets_SingleLepton", "SMS"]#, "Data"]

sh_file_name = "launch_cache.sh"

#for region in regions:
#    print(str(region))

selections = ["lep_SR_mu-jet_SR-lower_met-filters-Compressed_Stops_special","lep_SR_all-jet_SR-med_met-filters-Compressed_Stops_special","lep_SR_all-jet_SR-met300-filters-Compressed_Stops_special"]


with open(sh_file_name, 'w') as sh_file:
    for sample in sample_list:
        for i_region, region in enumerate(regions):
            selection = selections[i_region%3]
            if 'lower_met' in selection:
                lumi = 33.2
            else: 
                lumi = 35.9
            if "SMS" in sample:
                for stopm in [(250+25*i) for i in range(23)]:
                    for lspm in [(stopm - delta) for delta in [10,20,30,40,50,60,70,80]]: 
                        selection = selections[i_region%3]
                        sig_selection = "T2tt_%i_%i"%(stopm, lspm) 
                        sample = "SMS_" + sig_selection
                        selection = selection + "-" + sig_selection 
                        sh_file.write('python cacheRegion.py --year 2016  --lumi %f --selection "%s" --sample  "%s" --region %i'%(lumi, selection, sample, i_region)+'\n')
            else:
                sh_file.write('python cacheRegion.py --year 2016  --lumi %f --selection "%s" --sample  "%s" --region %i'%(lumi, selection, sample, i_region)+'\n')
                 


