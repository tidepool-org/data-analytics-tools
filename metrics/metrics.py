import numpy as np


def percent_values_by_range(values, lower_threshold: int, upper_threshold: int):
    """
        Calculate the percent of values that match has a bg within the lower and upper threshold.
        The lower and upper values will be included in the range to calculate on.

        Arguments:
        values -- numpy array contains a list of bg values.
        lower_threshold -- The the lower value in the range to calculate on.
        upper_threshold -- The the upper value in the range to calculate on.

        Output:
        Percent value
    """
    calc_low_thresh, calc_upper_thresh = _validate_input(lower_threshold, upper_threshold)
    results = round(np.where((values <= calc_upper_thresh) & (values >= calc_low_thresh), 1, 0).sum()/values.size*100, 2)
    return results


def percent_time_in_range(values, lower_threshold: int, upper_threshold: int):
    """
        Calculate the number of minutes the bg was within the lower and upper range.
        The lower and upper values will be included in the range to calculate on.

        Arguments:
        values -- Panda Dataframe with a column named values that contains a list of bg values and a column named date
        containing a python datetime value.
        lower_threshold -- The the lower value in the range to calculate on.
        upper_threshold -- The the upper value in the range to calculate on.

        Output:
        Percent value
    """
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
        date = values_sorted.loc[i, 'date']
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

