#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 11:09:34 2020
@author: ed
CREDIT/REFERENCE:
    Klonoff, David C., et al. "The surveillance error grid."
    Journal of diabetes science and technology 8.4 (2014): 658-672.
"""
# %% LOAD LIBRARIES AND DATA
import pandas as pd
import numpy as np

# this dataset is available in google drive
# https://drive.google.com/open?id=1F-AlUNimKofHmMshUYNIhltc2Nrqo9bd
seg_risk_score_matrix = pd.read_csv(
    "RiskPairWIDE_formatted.csv",
    low_memory=False,
    index_col="meas_index"
)


def get_seg_risk_score(measured_bg, reference_bg):
    # TODO put in requirement that bg values must be between [0-600]
    meas_name = "meas_{}".format(measured_bg)
    ref_name = "ref_{}".format(reference_bg)
    seg_risk_score = seg_risk_score_matrix.loc[meas_name, ref_name]
    return np.abs(seg_risk_score)

# %% FUNCTIONS

# measured_bg = 0
# meas_name = "meas_{}".format(measured_bg)
# reference_bg = 600
# ref_name = "ref_{}".format(reference_bg)
# seg_risk_score = seg_risk_score_matrix.loc[meas_name, ref_name]
# print(np.abs(seg_risk_score))

print(get_seg_risk_score(0, 609))

