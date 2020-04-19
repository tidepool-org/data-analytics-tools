import pandas as pd
import pytest
from metrics.metrics import get_percent_values_by_range, get_percent_time_in_range, \
    get_avg_glucose, get_std_deviation, get_cv_of_glucose, get_mean_glucose, get_gmi, \
    get_bgri, get_episodes
import datetime


def test_calculation():
    pd_values = get_values()
    percent = get_percent_values_by_range(pd_values.to_numpy(), 100, 0)
    assert 22.0 == percent

def test_invalid_lower_number():
    with pytest.raises(Exception) as excinfo:
        percent = get_percent_values_by_range(get_values(), -1, 0)
    assert "lower and upper thresholds must be a non-negative number" in str(excinfo.value)

def test_invalid_upper_number():
    with pytest.raises(Exception) as excinfo:
        percent = get_percent_values_by_range(get_values(), 0, -1)
    assert "lower and upper thresholds must be a non-negative number" in str(excinfo.value)


def test_missing_lower_number():
     with pytest.raises(TypeError) as excinfo:
        percent = get_percent_values_by_range(get_values(), 100)

def test_lower_number_higher_than_upper_number():
    with pytest.raises(Exception) as excinfo:
        percent = get_percent_values_by_range(get_values(), 100, 20)
    print(str(excinfo.value))
    assert "lower threshold is higher than the upper threshold." in str(excinfo.value)


def test_percent_time_in_range():
    percent = get_percent_time_in_range(get_date_values(), 100, 150)
    assert percent == 47.06

def test_percent_time_in_range_round():
    percent = get_percent_time_in_range(get_date_values(), 100, 150, 3)
    assert percent == 47.059

def test_avg_glucose():
    pd_values = get_values()
    average = get_avg_glucose(pd_values.to_numpy())
    assert average == 86.48

def test_gmi():
    pd_values = get_values()
    gmi_value = get_gmi(pd_values.to_numpy())
    assert  gmi_value == 5.38

def test_gmi_round():
    pd_values = get_values()
    gmi_value = get_gmi(pd_values.to_numpy(), 3)
    assert  gmi_value == 5.379

def test_mean_glucose():
    pd_values = get_values()
    val = get_mean_glucose(pd_values.to_numpy())
    assert val == 86.48

def test_std_deviation():
    pd_values = get_values()
    std = get_std_deviation(pd_values.to_numpy())
    assert  std == 11.90

def test_std_deviation_round():
    pd_values = get_values()
    std = get_std_deviation(pd_values.to_numpy(), 3)
    assert  std == 11.903

def test_cv_of_glucose():
    pd_values = get_values()
    std = get_cv_of_glucose(pd_values.to_numpy())
    assert std == 13.76

def test_cv_of_glucose_round():
    pd_values = get_values()
    std = get_cv_of_glucose(pd_values.to_numpy(), 3)
    assert std == 13.764

def test_get_bgri():
    pd_values = get_values()
    LBGI, HBGI, BGRI = get_bgri(pd_values)
    assert BGRI == 3.25
    assert HBGI == 0.0
    assert LBGI == 3.25

def test_get_bgri_round():
    pd_values = get_values()
    LBGI, HBGI, BGRI = get_bgri(pd_values, 3)
    assert BGRI == 3.245
    assert HBGI == 0.0
    assert LBGI == 3.245

def test_get_episodes_3_consecutive():
    pd_values = get_date_ep_values()
    std = get_episodes(pd_values, 55, 3)
    print("THE VALUE IS ", std)
    assert std == 3

def test_get_episodes_4_consecutive():
    pd_values = get_date_ep_values()
    std = get_episodes(pd_values, 55, 4)
    print("THE VALUE IS ", std)
    assert std == 1

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
    return pd.DataFrame(values, columns=['bg_values'])

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
    ['8/16/2019 02:00:00',108]]

    new_array =[]
    for i in values:
        date = datetime.datetime.strptime(i[0], '%m/%d/%Y %H:%M:%S')
        new_array.append([date, i[1]])
    return pd.DataFrame(new_array, columns=['date','bg_values'])

def get_date_ep_values():
    values = [['8/15/2019 00:40:00', 87],
              ['8/15/2019 00:45:00', 90],
              ['8/15/2019 00:50:00', 44],
              ['8/15/2019 00:55:00', 46],
              ['8/15/2019 01:00:00', 51],
              ['8/15/2019 01:05:00', 97],
              ['8/15/2019 01:10:00', 95],
              ['8/15/2019 01:15:00', 100],
              ['8/15/2019 01:20:00', 54],
              ['8/15/2019 01:25:00', 101],
              ['8/15/2019 01:30:00', 105],
              ['8/15/2019 01:35:00', 80],
              ['8/15/2019 01:40:00', 44],
              ['8/15/2019 01:45:00', 43],
              ['8/15/2019 01:50:00', 50],
              ['8/15/2019 01:55:00', 104],
              ['8/16/2019 02:00:00', 108]]

    new_array = []
    for i in values:
        date = datetime.datetime.strptime(i[0], '%m/%d/%Y %H:%M:%S')
        new_array.append([date, i[1]])
    return pd.DataFrame(new_array, columns=['roundedUtcTime', 'values'])

def get_date_ep_values():
    values = [['8/15/2019 00:40:00', 87],
              ['8/15/2019 00:45:00', 90],
              ['8/15/2019 00:50:00', 44],
              ['8/15/2019 00:55:00', 46],
              ['8/15/2019 01:00:00', 51],
              ['8/15/2019 01:05:00', 97],
              ['8/15/2019 01:10:00', 95],
              ['8/15/2019 01:15:00', 100],
              ['8/15/2019 01:20:00', 54],
              ['8/15/2019 01:25:00', 101],
              ['8/15/2019 01:30:00', 105],
              ['8/15/2019 01:35:00', 80],
              ['8/15/2019 01:40:00', 44],
              ['8/15/2019 01:45:00', 43],
              ['8/15/2019 01:50:00', 50],
              ['8/15/2019 01:55:00', 104],
              ['8/15/2019 02:00:00', 44],
              ['8/15/2019 02:10:00', 43],
              ['8/15/2019 02:15:00', 50],
              ['8/15/2019 02:20:00', 50],
              ['8/16/2019 02:25:00', 108]]
    new_array = []
    for i in values:
        date = datetime.datetime.strptime(i[0], '%m/%d/%Y %H:%M:%S')
        new_array.append([date, i[1]])
    return pd.DataFrame(new_array, columns=['roundedUtcTime', 'values'])