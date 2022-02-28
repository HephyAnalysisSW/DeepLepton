import numpy as np
from sklearn.metrics import roc_curve, auc


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def rm_nans_from_lists(truth, pred, cut):
    '''remove the indices where pred is nan'''
    nans = np.isnan(np.array(pred))
    if nans.any() == True:
        logger.info("ATTENTION FOUND NANS IN PREDICTION...REMOVING THEM, BE CAREFUL")
    truth = np.array(truth)
    truth = truth[np.logical_not(nans)]
    cut   = np.array(cut)
    cut   = cut[np.logical_not(nans)]
    pred = np.array(pred)
    pred = pred[np.logical_not(nans)]
    return [list(truth), list(pred), list(cut)]

class Bin(object):
    def __init__(self, pt_l, pt_u, dxy_l, dxy_u):
        '''giving upper and lower bin edges'''
        self.bin_pt_l = pt_l
        self.bin_pt_u = pt_u
        self.bin_dxy_l = dxy_l
        self.bin_dxy_u = dxy_u
        self.s = []
        self.p = []
        self.c = []
    def add_value(self, was_signal, prob_signal, cut_signal):
        self.s.append(was_signal)
        self.p.append(prob_signal)
        self.c.append(cut_signal)
    def get_signal(self):
        return self.s
    def get_prob(self):
        return self.p
    def get_cut(self):
        return self.c
    def __mk_roc(self):
        self.s, self.p, self.c = rm_nans_from_lists(self.s, self.p, self.c)
        if len(self.s) == 0:
            logger.info("{} was empty".format(self))
            self.empty = True
            self.fpr_dnn = None
            self.fpr_cut = None
            self.threshold = None
            self.threshold_cut = None
            self.tpr_dnn = None
            self.tpr_cut = None
        elif self.s.count(1)<=2:
            logger.info("The following bin has no/one/two signal muons: {}\n".format(self))
            try:
                self.fpr_dnn, self.tpr_dnn, self.threshold = roc_curve(self.s, self.p)
                self.fpr_cut, self.tpr_cut, self.threshold_cut = roc_curve(self.s, self.c, drop_intermediate=True)
                self.empty = False
            except Exception as e:
                print(e)
                logger.info("Exception bec. no signal muons in bin setting all no None...")
                self.fpr_dnn = None
                self.fpr_cut = None
                self.threshold = None
                self.threshold_cut = None
                self.tpr_dnn = None
                self.tpr_cut = None
                self.empty = True

        else:
            self.fpr_dnn, self.tpr_dnn, self.threshold = roc_curve(self.s, self.p)
            self.fpr_cut, self.tpr_cut, self.threshold_cut = roc_curve(self.s, self.c, drop_intermediate=True)
            self.empty = False
            # except Exception as e:
            #     print(e)
            #     logger.info("signal: {}".format(self.s))
            #     logger.info("prob:   {}".format(self.p))
    def get_eff(self):
        self.__mk_roc()
        if self.empty:
            self.t_dnn = None
            self.s_eff_dnn = self.tpr_dnn
            self.b_eff_dnn = self.fpr_dnn

            self.s_eff_cut = self.tpr_cut
            self.b_eff_cut = self.fpr_cut
        else:
            dnn_i = find_nearest(self.tpr_dnn, 0.9)
            self.t_dnn = self.threshold[dnn_i]
            self.s_eff_dnn = self.tpr_dnn[dnn_i]
            self.b_eff_dnn = self.fpr_dnn[dnn_i]

            self.s_eff_cut = self.tpr_cut[1]
            self.b_eff_cut = self.fpr_cut[1]
        return {"s_eff_dnn": self.s_eff_dnn, "b_eff_dnn":self.b_eff_dnn, "dnn_threshold":self.t_dnn,
                "s_eff_cut": self.s_eff_cut, "b_eff_cut":self.b_eff_cut}
    def get_roc_dnn(self):
        return [self.fpr_dnn, self.tpr_dnn, self.threshold]
    def get_roc_cut(self):
        return [self.fpr_cut, self.tpr_cut, self.threshold_cut]
    def print_me(self):
        string1 = "pt=[{} -- {}], dxy=[{} -- {}]".format(self.bin_pt_l, self.bin_pt_u, self.bin_dxy_l, self.bin_dxy_u)
        try:
            string2 = "E_s: {:.3f}, ({:.3f})".format(self.s_eff_dnn, self.s_eff_cut)
            string3 = "E_b: {:.3f}, ({:.3f})".format(self.b_eff_dnn, self.b_eff_cut)
        except:
            try:
                string2 = "E_s: {:.5s}, ({:.5s})".format(self.s_eff_dnn, self.s_eff_cut)
                string3 = "E_b: {:.3f}, ({:.3f})".format(self.b_eff_dnn, self.b_eff_cut)
            except ValueError as v:
                string2 = "E_s: {:.5s}, ({:.5s})".format(self.s_eff_dnn, self.s_eff_cut)
                string3 = "E_b: {:.5s}, ({:.5s})".format(self.b_eff_dnn, self.b_eff_cut)

        print("{:<45}".format(string1)+"{:23}".format(string2)+"{:23}".format(string3))
    def __repr__(self):
        return "Bin(pt=[{} -- {}], dxy=[{} -- {}]) containing {} elements".format(\
                            self.bin_pt_l, self.bin_pt_u, self.bin_dxy_l, self.bin_dxy_u, len(self.s))

