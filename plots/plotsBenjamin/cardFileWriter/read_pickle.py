import pickle
import array
execfile("../Bin.py")

bkg_yields_file_names = ["yield_TTSingleLep_pow.pkl", 
                         "yield_TTHad_pow.pkl",
                         "yield_TTLep_pow.pkl"]

godata="/groups/hephy/cms/benjamin.wilhelmy/DeepLepton/Yields/"
deeplepton_plots=   "/users/benjamin.wilhelmy/CMSSW_10_2_18/src/"\
                    "DeepLepton/plots/plotsBenjamin/"


# Chose here: (and)
# file_to_read = deeplepton_plots + "Efficiencies_STop1vsTTbar.pkl" 
file_to_read = godata + "yield_Stop250dm10.pkl" # bkg_yields_file_names[0] # "yield_Stop600dm20.pkl"



def printLonglist(a_long_list):
    '''This function prints the efficiencies tables a bit nicer'''
    for i, a_dict in enumerate(a_long_list):
        print_string = ""
        for k, v in a_dict.iteritems():
            if k in ["s_eff_cut", "dnn_threshold", "b_eff_dnn", "s_eff_dnn", "b_eff_cut"]:
                try:
                    print_string += k + ": {}".format(round(v, 3)) + ", "
                except:
                    print_string += k + ": {}".format(v) + ", "

            else:
                print_string += k + ": {}".format(v) + ", "
        print(i+1, print_string)

def print_yields(data):
    '''This func. prints the yields a bit nicer'''
    # length of a row befor newline 9=all dxy yields of fixed pt
    length_row = 3
    cnt = 0
    print_string = ""
    print_data = ""
    for i, pt_b in enumerate(data["pt_bins"][:-1]):
        for j, dxy_b in enumerate(data["dxy_bins"][:-1]):
            if cnt%length_row == 0:
                print(print_string)
                print(print_data+"\n")
                print_string = ""
                print_data = ""

            len_print_block_pt = len("pt([{:.1f}, {:.1f}])".format(pt_b, data["pt_bins"][i+1]))
            len_print_block_dxy = len("dxy([{:.3f}, {:.3f}])".format(dxy_b, data["dxy_bins"][j+1]))
            # print(len_print_block_pt, len_print_block_dxy)
            print_string += "pt([{:.1f}, {:.1f}])".format(pt_b, data["pt_bins"][i+1])\
                            + " & "\
                            + "dxy([{:.3f}, {:.3f}])".format(dxy_b, data["dxy_bins"][j+1]) \
                            + " || "
            print_data   += "{:^42f}".format(data["yields"][i][j])
            cnt += 1


with open(file_to_read, "rb") as f:
    data = pickle.load(f)


# Chose here:
print_yields(data)
# printLonglist(data["data"])
