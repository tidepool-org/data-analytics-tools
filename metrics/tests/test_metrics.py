import pandas as pd
from pandas.util import testing as tm
import pytest
import numpy as np
from metrics.metrics import percent_values_by_range, percent_time_in_range
import datetime

def test_calculation():
    percent = percent_values_by_range(get_values(), 100, 0)
    assert 22.0 == percent
    
def test_invalid_lower_number():
    with pytest.raises(Exception) as excinfo:
        percent = percent_values_by_range(get_values(), -1, 0)
    assert "lower and upper thresholds must be a non-negative number" in str(excinfo.value)

def test_invalid_upper_number():
    with pytest.raises(Exception) as excinfo:
        percent = percent_values_by_range(get_values(), 0, -1)
    assert "lower and upper thresholds must be a non-negative number" in str(excinfo.value)


def test_missing_lower_number():
     with pytest.raises(TypeError) as excinfo:
        percent = percent_values_by_range(get_values(), 100)


def test_lower_number_highjer_than_upper_number():
    with pytest.raises(Exception) as excinfo:
        percent = percent_values_by_range(get_values(), 100, 20)
    assert "lower threshold is higher than the upper threshold." in str(excinfo.value)

def test_percent_time_in_range():
    percent = percent_time_in_range(get_date_values(), 100, 150)
    assert 40 == percent


#100 values
def get_values():
    values = [[100],
    [105],
    [108],
    [104],
    [101],
    [106],
    [100],
    [105],
    [105],
    [99],
    [96],
    [101],
    [86],
    [85],
    [80],
    [83],
    [80],
    [82],
    [73],
    [74],
    [73],
    [73],
    [78],
    [76],
    [76],
    [71],
    [75],
    [77],
    [76],
    [74],
    [75],
    [76],
    [85],
    [82],
    [82],
    [83],
    [85],
    [84],
    [92],
    [92],
    [87],
    [97],
    [94],
    [94],
    [100],
    [101],
    [103],
    [100],
    [105],
    [105],
    [112],
    [103],
    [102],
    [98],
    [105],
    [105],
    [97],
    [97],
    [100],
    [98],
    [98],
    [93],
    [90],
    [86],
    [86],
    [88],
    [87],
    [83],
    [81],
    [84],
    [82],
    [83],
    [80],
    [76],
    [74],
    [82],
    [75],
    [71],
    [80],
    [76],
    [74],
    [72],
    [79],
    [79],
    [80],
    [77],
    [80],
    [76],
    [79],
    [76],
    [83],
    [81],
    [86],
    [82],
    [84],
    [84],
    [80],
    [70],
    [60],
    [50]]

    return pd.DataFrame(values, columns=['values'])

def get_date_values():
    values = [['8/15/2019 00:40:00',87],
    ['8/15/2019 00:45:00',90],
    ['8/15/2019 01:55:00', 104],
    ['8/15/2019 00:50:00',92],
    ['8/15/2019 00:55:00',96],
    ['8/15/2019 01:00:00',94],
    ['8/15/2019 01:05:00',97],
    ['8/15/2019 01:10:00',95],
    ['8/15/2019 01:15:00',100],
    ['8/15/2019 01:20:00',102],
    ['8/15/2019 01:25:00',101],
    ['8/15/2019 01:30:00',105],
    ['8/15/2019 01:35:00',80],
    ['8/15/2019 01:40:00',103],
    ['8/15/2019 01:45:00',108],
    ['8/15/2019 01:50:00',103],
    ['8/15/2019 02:00:00',108]]

    return pd.DataFrame(values, columns=['date','values'])
