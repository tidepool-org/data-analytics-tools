
from data_analytics_tools.clean.clean import removeDuplicates, round_time, removeInvalidCgmValues, \
    removeNegativeDurations_EDS, removeNegativeDurations_JASONS, removeCgmDuplicates, largeTimezoneOffsetCorrection

import pandas as pd
from pandas.util import testing as tm
import pytest


def test_remove_duplicates(valid_df):

    duplicated_data =  [["jjety", "AB9960", "response1", "response2", "Sun Nov 19 23:59:59 2018",
                         pd.to_datetime("2018-11-20 00:00:00")],
                  ["jjety", "AB9958", "response1", "response2", "Sun Nov 19 23:56:59 2018",
                   pd.to_datetime("2018-11-19 23:55:00")],
                  ["hqoh", "AB9953", "response1", "response2", "Sun Nov 19 23:29:59 2018",
                   pd.to_datetime("2018-11-19 23:30:00")],
                  ["hhawe", "AB8769", "response1", "response2", "Sun Nov 19 23:20:01 2018",
                   pd.to_datetime("2018-11-19 23:20:00")],
                  ["hhawe", "AB8769", "response1", "response2", "Sun Nov 19 23:20:01 2018",
                   pd.to_datetime("2018-11-19 23:20:00")]]

    duplicated_df = pd.DataFrame(duplicated_data, columns=['userID', 'studyID',"getData.response1", "getData.response2",
                                                           "time", "roundedTime"])

    pandas_drop_df = duplicated_df.drop_duplicates('time')

    clean_df, duplicate_count = removeDuplicates(duplicated_df, "time")

    tm.assert_frame_equal(valid_df, clean_df)
    tm.assert_frame_equal(valid_df, pandas_drop_df)
    assert duplicate_count == 1


def test_round_time(valid_df):
    raw_data = [["hhawe", "AB8769", "response1", "response2", "Sun Nov 19 23:20:01 2018"],
                  ["hqoh", "AB9953", "response1", "response2", "Sun Nov 19 23:29:59 2018"],
                  ["jjety", "AB9958", "response1", "response2", "Sun Nov 19 23:56:59 2018"],
                  ["jjety", "AB9960", "response1", "response2", "Sun Nov 19 23:59:59 2018"]]


    raw_df = pd.DataFrame(raw_data, columns=['userID', 'studyID', "getData.response1", "getData.response2", "time"])
    rounded_df = round_time(raw_df)
    tm.assert_frame_equal(valid_df, rounded_df)


def test_round_time_across_month(valid_df):
    raw_data = [["hhawe", "AB8769", "newyear", "response2", "2018-11-30 23:59:10"]]
    raw_df = pd.DataFrame(raw_data, columns=['userID', 'studyID', "getData.response1", "getData.response2", "time"])
    rounded_df = round_time(raw_df)
    expected_time = pd.Timestamp('2018-12-01')

    rounded_new_year = rounded_df.iloc[0]['roundedTime']
    assert( pd.Timestamp(rounded_new_year) == expected_time)


def test_round_time_across_year():
    raw_data = [["hhawe", "AB8769", "newyear", "response2", "2018-12-31 23:59:10"]]
    raw_df = pd.DataFrame(raw_data, columns=['userID', 'studyID', "getData.response1", "getData.response2", "time"])
    rounded_df = round_time(raw_df)
    expected_time = pd.Timestamp('2019-01-01')

    rounded_new_year = rounded_df.iloc[0]['roundedTime']
    assert( pd.Timestamp(rounded_new_year) == expected_time)


def test_round_time_early_hour():
    raw_data = [["hhawe", "AB8769", "newyear", "response2", "2018-11-29 00:01:10"]]
    raw_df = pd.DataFrame(raw_data, columns=['userID', 'studyID', "getData.response1", "getData.response2", "time"])
    rounded_df = round_time(raw_df)
    expected_time = pd.Timestamp('2018-11-29')

    rounded_new_year = rounded_df.iloc[0]['roundedTime']
    assert( pd.Timestamp(rounded_new_year) == expected_time)


def test_round_invalid_date():
    raw_data = [["hhawe", "AB8769", "newyear", "response2", "2018-11-31 00:01:10"]]
    raw_df = pd.DataFrame(raw_data, columns=['userID', 'studyID', "getData.response1", "getData.response2", "time"])
    with pytest.raises(ValueError) as excinfo:
        round_time(raw_df)

    assert("day is out of range for month: %s" == excinfo.value.args[0])

def test_round_invalid_time():
    raw_data = [["hhawe", "AB8769", "newyear", "response2", "2018-11-31 25:01:10"]]
    raw_df = pd.DataFrame(raw_data, columns=['userID', 'studyID', "getData.response1", "getData.response2", "time"])
    with pytest.raises(ValueError) as excinfo:
        round_time(raw_df)

    assert("day is out of range for month: %s" == excinfo.value.args[0])


def test_removeInvalidCgmValues_less_than_38():
    """
    {"deviceTime": "2019-01-20T09:51:08", "id": "b12854e060f9d4abf08db3ecc446fdfc",
     "payload": {"realTimeValue": 137, "systemTime": "2019-01-20T14:51:08Z", "transmitterId": "41TU3L",
                 "transmitterTicks": 3760359, "trend": "flat", "trendRate": 0.3, "trendRateUnits": "mg/dL/min"},
     "time": "2019-01-20T14:51:08Z", "timezoneOffset": -300, "type": "cbg", "units": "mmol/L",
     "uploadId": "3f434e5abc1e456f807edf5c7c25f738", "value": 7.60452}
     """
    # remove values < 38 and > 402 mg/dL
    raw_data = [["cbg", 2.109284236597302]]
    raw_df = pd.DataFrame(raw_data, columns=['type', 'value'])
    df, nRemoved = removeInvalidCgmValues(raw_df)

    assert(nRemoved == 1)

def test_removeInvalidCgmValues_greater_than_402():
    """
    {"deviceTime": "2019-01-20T09:51:08", "id": "b12854e060f9d4abf08db3ecc446fdfc",
     "payload": {"realTimeValue": 137, "systemTime": "2019-01-20T14:51:08Z", "transmitterId": "41TU3L",
                 "transmitterTicks": 3760359, "trend": "flat", "trendRate": 0.3, "trendRateUnits": "mg/dL/min"},
     "time": "2019-01-20T14:51:08Z", "timezoneOffset": -300, "type": "cbg", "units": "mmol/L",
     "uploadId": "3f434e5abc1e456f807edf5c7c25f738", "value": 7.60452}
     """
    # remove values < 38 and > 402 mg/dL
    raw_data = [["cbg", 22.314006924003048]]
    raw_df = pd.DataFrame(raw_data, columns=['type', 'value'])
    df, nRemoved = removeInvalidCgmValues(raw_df)

    assert(nRemoved == 1)

def test_removeCgmDuplicates():
    """
    {"deviceTime":"2019-01-20T09:51:08","id":"b12854e060f9d4abf08db3ecc446fdfc",
    "payload":{"realTimeValue":137,"systemTime":"2019-01-20T14:51:08Z","transmitterId":"41TU3L",
    "transmitterTicks":3760359,"trend":"flat","trendRate":0.3,"trendRateUnits":"mg/dL/min"},"time":"2019-01-20T14:51:08Z",
    "timezoneOffset":-300,"type":"cbg","units":"mmol/L","uploadId":"3f434e5abc1e456f807edf5c7c25f738","value":7.60452},
     """

    raw_data = [["cbg", "2019-01-20T09:51:08", "testvalue", "2019-01-20T09:51:08"],
                ["cbg", "2019-01-20T09:51:08", "testvalue", "2019-01-20T08:51:09"]]
    raw_df = pd.DataFrame(raw_data, columns=['type', 'deviceTime', 'value', 'uploadTime'])
    df, nRemoved = removeCgmDuplicates(raw_df, "deviceTime")

    assert(nRemoved == 1)


def test_removeNegativeDurations():
    raw_data = [["cbg", 22.314006924003048, -1961000], ["cbg", 22.314006924003048, 1961000]]
    raw_df = pd.DataFrame(raw_data, columns=['type', 'value', 'duration'])
    df, removed_count = removeNegativeDurations_EDS(raw_df)
    #df = removeNegativeDurations_JASONS(raw_df)

    assert(raw_df.shape[0] == 2)
    assert(df.shape[0] == 1)
    assert(removed_count == 1)


@pytest.mark.skip(reason='need a valid dataframe example')
def test_largeTimezoneOffsetCorrection():

    raw_data = [["cbg", 22.314006924003048, -1961000, 54, 4], ["cbg", 22.314006924003048, 850, 1]]
    raw_df = pd.DataFrame(raw_data, columns=['type', 'value', 'timezoneOffset', 'conversionOffset'])
    test = raw_df.sum()

    df, removed_count = largeTimezoneOffsetCorrection(raw_df)
    #df = removeNegativeDurations_JASONS(raw_df)

    assert(raw_df.shape[0] == 2)
    assert(df.shape[0] == 1)
    assert(removed_count == 1)




"""  
@pytest.mark.skip(reason='need a valid dataframe example')
def test_flatten_json(current_path_clean):
    df = pd.read_json(current_path_clean + "/example_data.json")
    flattened_df = flatten_json(df)

    print(flattened_df)
"""







