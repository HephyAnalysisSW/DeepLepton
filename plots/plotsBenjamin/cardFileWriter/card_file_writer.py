from Analysis.Tools.cardFileWriter import cardFileWriter
import argparse
# from DeepLepton.plots.plotsBenjamin.Bin import*
import pickle
import os
import numpy as np

# load the Bin class
execfile("../Bin.py")

parser = argparse.ArgumentParser(description="specify signal sample")
parser.add_argument("--signal",
                    action="store", 
                    help="specify path to signal yield.pkl")
parser.add_argument("--eff_table_path",
                    action="store",
                    default="",
                    help="path to eff_table.pkl, "
                         "if not empty then scale yields with dnn_eff")
parser.add_argument("--small", action="store_true", help="mk small files for debugging")
parser.add_argument("--debug", action="store_true", help="debugging?")

args = parser.parse_args()
# load the signal yield pickle file
# is a dict with keys: pt_bins, dxy_bins, yields
# yields is not a flat list i.e. [i_pt][j_dxy] for access
with open(args.signal, "rb") as f:
    signal_yields = pickle.load(f)

pt_bins = signal_yields["pt_bins"]
dxy_bins = signal_yields["dxy_bins"]

# the signal yields should be in the same directory as the bkg samples.
bkg_yield_file_names = ["yield_TTSingleLep_pow.pkl",
                        "yield_TTHad_pow.pkl",
                        "yield_TTLep_pow.pkl"]

# store here the data of the bkg yield pkl files
bkg_yield_vars = {  "yield_TTSingleLep_pow":None,
                    "yield_TTHad_pow":None, 
                    "yield_TTLep_pow":None}

# load all the bkg yields:
def load_bkg_yield_data(filename=bkg_yield_file_names[0],
                        key_to_store_data="yield_TTSingleLep_pow"):
    basename = "/".join(args.signal.split("/")[:-1])
    with open(os.path.join(basename, filename), "rb") as f:
        bkg_yield_vars[key_to_store_data] = pickle.load(f)

for filename in bkg_yield_file_names:
    key_to_store_data = filename.split(".")[0]
    # fills the bkg_yield_vars dict
    load_bkg_yield_data(filename=filename, key_to_store_data=key_to_store_data)

# done loading the yield data.


# add up the three bkg yields
bkg_yields = {"yields":  np.array(bkg_yield_vars["yield_TTSingleLep_pow"]["yields"]) + 
                                            np.array(bkg_yield_vars["yield_TTHad_pow"]["yields"]) +
                                            np.array(bkg_yield_vars["yield_TTLep_pow"]["yields"]) }

# if we want to scale the yields
if args.eff_table_path:
    print("---\nWARNING: Is {} consistent with {}?\n---".format(  args.signal.split("/")[-1],
                                                        args.eff_table_path.split("/")[-1]))
    with open(args.eff_table_path, "rb") as f:
        # a dict with keys: "pt_bins", "dxy_bins", "data"
        # "data" contains instances of the Bin class in a flat list
        eff_table = pickle.load(f)

    # scale the yields already here
    for i, pt_b in enumerate(pt_bins[:-1]):
        # for higher pt there are not enough muons -> no eff estimate for scaling
        # disable if temporarly
        if pt_b<10 or True:
            # get the signal and bkg efficiencies for dnn and cut 
            for j in range(len(dxy_bins)-1):
                selected_bin = eff_table["data"][i*(len(dxy_bins)-1)+j]

                signal_yield_signal_eff_dnn = selected_bin.get("s_eff_dnn")
                signal_yield_signal_eff_cut = selected_bin.get("s_eff_cut")

                bkg_yield_bkg_eff_dnn = selected_bin.get("b_eff_dnn")
                bkg_yield_bkg_eff_cut = selected_bin.get("b_eff_cut")

                try:
                    # try scaling signal yield
                    bin_number = i*(len(dxy_bins)-1)+j+1
                    if args.debug:
                        print("Bin {}:\n"\
                                "\t signal_eff_dnn={} signal_eff_cut={}".format(bin_number,
                                                                                signal_yield_signal_eff_dnn,
                                                                                signal_yield_signal_eff_cut))
                        print("\t with signal yield={}".format(signal_yields["yields"][i][j]))
                        print("\t type signal_eff_dnn = {}, np.isnan({})={}".format(  type(signal_yield_signal_eff_dnn),
                                                                                        signal_yield_signal_eff_dnn,
                                                                                        np.isnan(signal_yield_signal_eff_dnn)))

                    if signal_yield_signal_eff_cut == 0:
                        # then take the cut yield for dnn prediction
                        print("signal_eff_cut is zero. Dont scale bin {}".format(bin_number))
                    elif signal_yield_signal_eff_dnn in [None,] or np.isnan(signal_yield_signal_eff_dnn):
                        print("signal yield eff_dnn in None or np.isnan."\
                                "do no scaling of yield of bin {}".format(bin_number))
                    elif signal_yield_signal_eff_cut in [None,] or np.isnan(signal_yield_signal_eff_cut):
                        print("???signal_eff_cut is None or nan."\
                                "Dont scale yield for bin {}".format(bin_number))
                        # signal_yields["yields"][i][j] = 0
                    else:
                        signal_yields["yields"][i][j] = signal_yields["yields"][i][j]*signal_yield_signal_eff_dnn/signal_yield_signal_eff_cut
                # since np apparently allows calculations with nan this can be removed I think.
                except Exception as e:
                    # if the cut-id had no muons or mis-classified all;
                    # set dnn yield to zero as well
                    if signal_yield_signal_eff_cut in [None,]:
                        # signal_yields["yields"][i][j] = 0
                        print(" --- \n THIS SHOULD NOT HAPPEN!!! -> UNCAUGHT signal_eff_cut=None \n ---")
                        print("Bin {} --> {}".format(bin_number, signal_yields["yields"][i][j]))
                        # pass
                    # do the same if there were no muons for dnn classifier
                    elif signal_yield_signal_eff_dnn in [None,]:
                        # signal_yields["yields"][i][j] = 0
                        print(" --- \n THIS SHOULD NOT HAPPEN!!! -> UNCAUGHT signal_eff_dnn=None \n ---")
                        print("Bin {} --> {}".format(bin_number, signal_yields["yields"][i][j]))
                        # pass
                    else:
                        print("Error in signal yield scaling, bin {}:".format(bin_number))
                        print(selected_bin, pt_b, dxy_bins[j], dxy_bins[j+1])
                        print(e)
                        raise e
                try:
                    # if bkg_eff_dnn == 0 set the yield to a very small value...
                    # because combine wants a bkg rate
                    if bkg_yield_bkg_eff_dnn == 0:
                        print("bkg_eff_dnn was zero in bin {}.".format(bin_number)\
                                + "Setting bkg_yield to 0.000000001")
                        bkg_yields["yields"][i,j] = 0.000000001

                    # for the same reason as in signal_yield_... catch before throw
                    elif bkg_yield_bkg_eff_cut == 0:
                        print("bkg_eff_cut was zero. Dont scale bin {}".format(bin_number))
                    elif bkg_yield_bkg_eff_dnn in [None,] or np.isnan(bkg_yield_bkg_eff_dnn):
                        print("bkg_eff_dnn was None or nan. Dont scale bin {}".format(bin_number))
                        # bkg_yields["yields"][i,j] = 0.000000001
                    else:
                        # try scaling bkg yield (is a np array)
                        bkg_yields["yields"][i,j] = bkg_yields["yields"][i,j] * bkg_yield_bkg_eff_dnn/bkg_yield_bkg_eff_cut
                except Exception as e:
                    # if the cut-id had no muons or mis-classified all;
                    # set dnn yield to zero as well
                    if bkg_yield_bkg_eff_cut in [None,]:
                        # bkg_yields["yields"][i, j] = 0
                        print(" --- \n THIS SHOULD NOT HAPPEN!!! -> UNCAUGHT bkg_eff_cut=None \n ---")

                    # do the same if there were no muons for dnn classifier
                    elif bkg_yield_bkg_eff_dnn in [None,]:
                        # bkg_yields["yields"][i, j] = 0
                        print(" --- \n THIS SHOULD NOT HAPPEN!!! -> UNCAUGHT bkg_eff_dnn=None \n ---")
                    else:
                        print("Error in bkg yield scaling:")
                        print(selected_bin, pt_b, dxy_bins[j], dxy_bins[j+1])
                        print(e)
                        raise e


c = cardFileWriter.cardFileWriter()

cardFileNameTxt = "./card_file_{}".format(args.signal.split("/")[-1].split(".pkl")[0]) \
                    + ("_DNN" if args.eff_table_path else "") \
                    + ("_debug" if args.small else "") + ".txt"

processes = [ "tt" ]
signal_region_names = []

c.addUncertainty( "lumi", "lnN" )

# for each bin (pt<=10) add a bin in cardfile:
for i, pt_b in enumerate(pt_bins[:-1]):
    # for higher pt there are not enough muons -> no eff estimate for scaling
    # disable if temporarily
    if pt_b<10 or True:
        # get the signal and bkg efficiencies for dnn and cut 
        for j in range(len(dxy_bins)-1):
            # name = "pt_{}--{}_dxy_{}_--_{}".format( pt_b, pt_bins[i+1],
            #                                         dxy_bins[j],
            #                                         dxy_bins[j+1])
            if signal_yields["yields"][i][j]:
                name = "bin"+str(i*(len(dxy_bins)-1)+j+1)
                signal_region_names.append(name)
                bkg_obs = bkg_yields["yields"][i,j]
                # for debugging
                print("{:5s}".format(name)+"{:25s}".format(": signal={}".format(signal_yields["yields"][i][j]))\
                        +"{:20s}".format(" | bkg=obs={}".format(bkg_obs)))
                c.addBin(name, processes)
                c.specifyExpectation(name, "signal", signal_yields["yields"][i][j])
                c.specifyExpectation(name, "tt", bkg_obs)
                c.specifyObservation(name, int(round(bkg_obs)))
        if args.small:
            break
for p in processes+["signal"]:
    for n in signal_region_names:
        c.specifyUncertainty( "lumi", n, p, 1.036 ) #1.036

c.writeToFile( cardFileNameTxt )

c.calcLimit()


