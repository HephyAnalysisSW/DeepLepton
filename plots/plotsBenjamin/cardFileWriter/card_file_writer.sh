godata="/groups/hephy/cms/benjamin.wilhelmy/DeepLepton/Yields/"

signal1="${godata}yield_Stop250dm10.pkl"
signal2="${godata}yield_Stop250dm20.pkl"
signal3="${godata}yield_Stop600dm10.pkl"
signal4="${godata}yield_Stop600dm20.pkl"


deeplepton_plots="/users/benjamin.wilhelmy/CMSSW_10_2_18/src/DeepLepton/plots/plotsBenjamin/"

# HAS TO BE CONSISTENT WITH "signal?"!
table1="${deeplepton_plots}Efficiencies_STop1vsTTbar.pkl" #-> 250dm10
table2="${deeplepton_plots}Efficiencies_STop2vsTTbar.pkl" #-> 250dm20
table3="${deeplepton_plots}Efficiencies_STop3vsTTbar.pkl" #-> 600dm10
table4="${deeplepton_plots}Efficiencies_STop4vsTTbar.pkl" #-> 600dm20

# python card_file_writer.py --signal ${signal1} --eff_table_path ${table1} 
# combine card_file_yield_Stop600dm20_DNN.txt --rMin 0 --rMax 0.01

# STop1
python card_file_writer.py --signal ${signal1} --eff_table_path ${table1} > Asympt_STop1_DNN.txt
combine card_file_yield_Stop250dm10_DNN.txt  --rMin 0 --rMax 0.01 >> Asympt_STop1_DNN.txt
echo "Stop250dm10_DNN-----------" > Results.txt
combine card_file_yield_Stop250dm10_DNN.txt  --rMin 0 --rMax 0.01 >> Results.txt
python card_file_writer.py --signal ${signal1} > Asympt_STop1_cut.txt
combine card_file_yield_Stop250dm10.txt --rMin 0 --rMax 0.01 >> Asympt_STop1_cut.txt
echo "STop250dm10_cut-----------" >> Results.txt
combine card_file_yield_Stop250dm10.txt --rMin 0 --rMax 0.01 >> Results.txt

# STop2
python card_file_writer.py --signal ${signal2} --eff_table_path ${table2} > Asympt_STop2_DNN.txt
combine card_file_yield_Stop250dm20_DNN.txt --rMin 0 --rMax 0.01 >> Asympt_STop2_DNN.txt
echo "Stop250dm20_DNN--------------" >> Results.txt
combine card_file_yield_Stop250dm20_DNN.txt --rMin 0 --rMax 0.01 >> Results.txt

python card_file_writer.py --signal ${signal2}> Asympt_STop2_cut.txt
combine card_file_yield_Stop250dm20.txt --rMin 0 --rMax 0.01 >> Asympt_STop2_cut.txt
echo "Stop250dm20_cut--------------" >> Results.txt
combine card_file_yield_Stop250dm20.txt --rMin 0 --rMax 0.01 >> Results.txt

# STop3
python card_file_writer.py --signal ${signal3} --eff_table_path ${table3} > Asympt_STop3_DNN.txt
combine card_file_yield_Stop600dm10_DNN.txt --rMin 0 --rMax 0.01 >> Asympt_STop3_DNN.txt
echo "Stop600dm10_DNN-------------" >> Results.txt
combine card_file_yield_Stop600dm10_DNN.txt --rMin 0 --rMax 0.01 >> Results.txt
python card_file_writer.py --signal ${signal3}> Asympt_STop3_cut.txt
combine card_file_yield_Stop600dm10.txt --rMin 0 --rMax 0.01 >> Asympt_STop3_cut.txt
echo "Stop600dm10_cut--------------" >> Results.txt
combine card_file_yield_Stop600dm10.txt --rMin 0 --rMax 0.01 >> Results.txt

# STop4
python card_file_writer.py --signal ${signal4} --eff_table_path ${table4} > Asympt_STop4_DNN.txt
combine card_file_yield_Stop600dm20_DNN.txt --rMin 0 --rMax 0.01 >> Asympt_STop4_DNN.txt
echo "Stop600dm20_DNN--------------" >> Results.txt
combine card_file_yield_Stop600dm20_DNN.txt --rMin 0 --rMax 0.01 >> Results.txt

python card_file_writer.py --signal ${signal4} > Asympt_STop4_cut.txt
combine card_file_yield_Stop600dm20.txt --rMin 0 --rMax 0.01 >> Asympt_STop4_cut.txt
echo "Stop600dm20_cut--------------" >> Results.txt
combine card_file_yield_Stop600dm20.txt --rMin 0 --rMax 0.01 >> Results.txt
# Remove card files again to keep directory clean
rm -f card_file_yield*.txt
