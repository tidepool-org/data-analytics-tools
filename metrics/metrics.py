import numpy as np
from typing import Tuple


def cv_of_glucose(bg_values):
    """
        Calculate the average within a set of glucose values

        Arguments:
        values -- numpy array contains a list of bg values.

        Output: Calculated Average
    """
    std_dev = std_deviation(bg_values)
    avg_glu = avg_glucose(bg_values)
    return round(std_dev/avg_glu * 100, 2)

"""
Still working on implementation
def gmi(values):
    mean_val = mean_glucose(values)
    GMI( %) = 3.31 + 0.02392 x[mean glucose in mg / dL]
    GMI(mmol / mol) = 12.71 + 4.70587 x[mean glucose in mmol / L]
    #For example, if the SD is 50 mg/dl, and the average glucose is 150 mg/dl,
# then you divide 50 by 150, multiply by 100, and you get a CV of 33%.
"""



def mean_glucose(bg_values):
    """
        Calculate the mean within a set of glucose values

        Arguments:
        values -- numpy array contains a list of bg values.

        Output: Calculated Mean
    """
    return round(np.mean(bg_values), 2)

def avg_glucose(bg_values):
    """
        Calculate the average within a set of glucose values

        Arguments:
        values -- numpy array contains a list of bg values.

        Output: Calculated Average
    """
    return round(np.average(bg_values), 2)

def std_deviation(bg_values):
    """
            Calculate the standard deviation within a set of glucose values

            Arguments:
            values -- numpy array contains a list of bg values.

            Output: Calculated standard deviation
        """
    return round(np.std(bg_values), 2)

def percent_values_by_range(bg_values, lower_threshold: int, upper_threshold: int):
    """
        Calculate the percent of values that match has a bg within the lower and upper threshold.
        The lower and upper values will be included in the range to calculate on.

        Arguments:
        bg_values -- numpy array contains a list of bg values.
        lower_threshold -- The the lower value in the range to calculate on.
        upper_threshold -- The the upper value in the range to calculate on.

        Output:
        Percent value
    """
    calc_low_thresh, calc_upper_thresh = _validate_input(lower_threshold, upper_threshold)
    results = round(np.where((bg_values <= calc_upper_thresh) & (bg_values >= calc_low_thresh), 1, 0).sum()/bg_values.size*100, 2)
    return results


def percent_time_in_range(bg_values, lower_threshold: int, upper_threshold: int, time_delta=5):
    """
        Calculate the number of minutes the bg was within the lower and upper range.
        The lower and upper values will be included in the range to calculate on.

        Arguments:
        bg_values -- Panda Dataframe with a column named values that contains a list of bg values and a column named date
        containing a python datetime value.
        lower_threshold -- The the lower value in the range to calculate on.
        upper_threshold -- The the upper value in the range to calculate on.

        Output:
        Percent of bg values in range
    """
    calc_low_thresh, calc_upper_thresh = _validate_input(lower_threshold, upper_threshold)
    bg_df = bg_values['bg_values']
    bg_np = bg_df.to_numpy()
    in_range = np.count_nonzero((bg_np > calc_low_thresh) & (bg_np < calc_upper_thresh))
    val_count = bg_df.count()
    return round(in_range/val_count*100, 2)
 

def _validate_input(lower_threshold: int, upper_threshold: int) -> Tuple[int, int]:
    if any(num < 0 for num in [lower_threshold, upper_threshold]):
        raise Exception("lower and upper thresholds must be a non-negative number")
    if upper_threshold == 0:
        upper_threshold = 1000
    if lower_threshold > upper_threshold:
        raise Exception("lower threshold is higher than the upper threshold.")
    return lower_threshold, upper_threshold

