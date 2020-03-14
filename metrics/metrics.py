import pandas as pd
from typing import Dict, Tuple, Sequence
import numpy as np
import datetime

def percent_values_by_range(values, lower_threshold: int, upper_threshold: int):
    calc_low_thresh, calc_upper_thresh = _validate_input(lower_threshold, upper_threshold)
    values_list = values['values'].tolist()
    set_length = float(len(values_list))
    match_length = len([i for i in values_list  if  i <= calc_upper_thresh and i >= calc_low_thresh ])
    return round(match_length / set_length * 100, 2)


def percent_time_in_range(values, lower_threshold: int, upper_threshold: int):
    calc_low_thresh, calc_upper_thresh = _validate_input(lower_threshold, upper_threshold)
    #pd.to_datetime(values['date'], format='%m/%d/%Y %H:%M:%S')

    from_date = None
    date = None
    match_length = 0
    mins_in_range = 0
    values_sorted = values.sort_values(by='date').reindex()
    values_sorted.reset_index(drop=True, inplace=True)
    set_length = values_sorted.shape[0]
    hit = False
    for i in values_sorted.index:
        value = values_sorted.loc[i, 'values']
        date_time_str = values_sorted.loc[i, 'date']
        date = datetime.datetime.strptime(date_time_str, '%m/%d/%Y %H:%M:%S')
        if   value <= calc_upper_thresh and value >= calc_low_thresh:
            match_length += 1
            hit = True
            if from_date is None or date < from_date:
                from_date = date
        else:
            if hit:
                 sec = date - from_date
                 mins_in_range += sec.seconds / 60

            from_date = None
            hit = False
    if hit:
        sec = date - from_date
        mins_in_range += sec.seconds / 60
 
    return mins_in_range 
 

     

def _validate_input(lower_threshold: int, upper_threshold: int):
    calc_low_thresh = 0
    if lower_threshold < 0 or upper_threshold < 0:
        raise Exception("lower and upper thresholds must be a non-negative number")

    if lower_threshold and lower_threshold is not 0:
        calc_low_thresh = lower_threshold

    calc_upper_thresh = 1000
    if upper_threshold and upper_threshold is not 0:
        calc_upper_thresh = upper_threshold

    if calc_low_thresh > calc_upper_thresh:
        raise Exception("lower threshold is higher than the upper threshold.")

    return calc_low_thresh, calc_upper_thresh

