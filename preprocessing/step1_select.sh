######################
# lepton2016 samples #
######################

#before submitting get grid certificate:
#voms-proxy-init -voms cms -out ~/private/.proxy
#export X509_USER_PROXY=~/private/.proxy

#submit jobs to batch:
#submitBatch.py --dpm step1_select2016.sh

#job status:
#squeue|grep gmoertl

#job log if done/killed:
#vi /afs/hephy.at/work/g/gmoertl/batch_output/batch-test.123456789.out

#display samples names:
#ipython -i step1_select.py -- --year 2016 --sample TTJets  --logLevel DEBUG
#lepton_heppy_mapper.heppy_sample_names

##small test
#python -i step1_select.py  --version v6 --small --year 2016  --logLevel DEBUG --sample TTJets_DiLepton #SPLIT2
#python -i step1_select.py  --version v6 --small --year 2016  --logLevel DEBUG --sample TTJets_DiLepton_ext #SPLIT2
#python -i step1_select.py  --version v6 --small --year 2016  --logLevel DEBUG --sample TTJets_SingleLeptonFromTbar #SPLIT2
#python -i step1_select.py  --version v6 --small --year 2016  --logLevel DEBUG --sample TTJets_SingleLeptonFromTbar_ext #SPLIT2
#python -i step1_select.py  --version v6 --small --year 2016  --logLevel DEBUG --sample TTJets_SingleLeptonFromT #SPLIT2
#python -i step1_select.py  --version v6 --small --year 2016  --logLevel DEBUG --sample TTJets_SingleLeptonFromT_ext #SPLIT2
#

#Lepton 2016 v4 (Nov18 crab jobs processed by Robert)

#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample TTJets_DiLepton --nJobs 20 --job 0

#TTJets Dilepton
python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --ptSelection pt_5_-1 --sample TTJets_DiLepton #SPLIT20
python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --ptSelection pt_5_-1 --sample TTJets_DiLepton_ext #SPLIT20
#TTJets SingleLepton
python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --ptSelection pt_5_-1 --sample TTJets_SingleLeptonFromTbar #SPLIT20
python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --ptSelection pt_5_-1 --sample TTJets_SingleLeptonFromTbar_ext #SPLIT20
python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --ptSelection pt_5_-1 --sample TTJets_SingleLeptonFromT #SPLIT20
python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --ptSelection pt_5_-1 --sample TTJets_SingleLeptonFromT_ext #SPLIT20
#TTs other
python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --ptSelection pt_5_-1 --sample TT_pow #SPLIT20
python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --ptSelection pt_5_-1 --sample TTLep_pow #SPLIT20
python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --ptSelection pt_5_-1 --sample TTSemiLep_pow #SPLIT20
python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --ptSelection pt_5_-1 --sample TT_pow_ext3 #SPLIT20
python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --ptSelection pt_5_-1 --sample TTJets #SPLIT20
python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --ptSelection pt_5_-1 --sample TTJets_LO #SPLIT20

##DY
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample DY1JetsToLL_M50_LO #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample DY2JetsToLL_M50_LO #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample DY3JetsToLL_M50_LO #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample DY4JetsToLL_M50_LO #SPLIT20
##QCD MuEnriched
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt15to20_Mu5 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt20to30_Mu5 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt30to50_Mu5 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt50to80_Mu5 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt80to120_Mu5 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt80to120_Mu5_ext #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt120to170_Mu5 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt170to300_Mu5 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt170to300_Mu5_ext #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt300to470_Mu5 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt300to470_Mu5_ext #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt300to470_Mu5_ext2 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt470to600_Mu5 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt470to600_Mu5_ext #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt470to600_Mu5_ext2 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt600to800_Mu5 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt600to800_Mu5_ext #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt800to1000_Mu5 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt800to1000_Mu5_ext #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt800to1000_Mu5_ext2 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt1000toInf_Mu5 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt1000toInf_Mu5_ext #SPLIT20

##QCD
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt15to30 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt30to50 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt50to80 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt80to120 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt80to120_ext2 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt120to170 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt120to170_ext #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt170to300 #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt170to300_ext #SPLIT20
##QCD EMEnriched
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt20to30_EMEnriched #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt30to50_EMEnriched #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt30to50_EMEnriched_ext #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt50to80_EMEnriched_ext #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt80to120_EMEnriched_ext #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt120to170_EMEnriched #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt170to300_EMEnriched #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt300toInf_EMEnriched #SPLIT20
##QCD bcToE
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt_20to30_bcToE #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt_30to80_bcToE #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt_80to170_bcToE #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt_170to250_bcToE #SPLIT20
#python -i step1_select.py  --version v6 --year 2016  --logLevel DEBUG --sample QCD_Pt_250toInf_bcTo #SPLIT20

