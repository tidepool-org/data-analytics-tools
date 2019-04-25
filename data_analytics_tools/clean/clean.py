#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
description: cleaning tools for tidals (tidepool data analytics tools)
created: 2018-07
author: Ed Nykaza
license: BSD-2-Clause
"""

import pandas as pd
import numpy as np


#Cleaning Functions
#removeNegativeDurations (Duplicate with differences)
#tslimCalibrationFix (Duplicate with differences)
#removeInvalidCgmValues
#round_time
#removeDuplicates
#removeCgmDuplicates
#largeTimezoneOffsetCorrection

##??
#convertDeprecatedTimezoneToAlias


# CLEAN DATA FUNCTIONS
def removeDuplicates(df, criteriaDF):
    nBefore = len(df)
    df = df.loc[~(df[criteriaDF].duplicated())]
    df = df.reset_index(drop=True)
    nDuplicatesRemoved = nBefore - len(df)

    return df, nDuplicatesRemoved

""" 
def remove_duplicates(df, upload_data):

    df = df.copy()
    upload_data = upload_data.copy()

    # Sort uploads by oldest uploads first
    upload_data = upload_data.sort_values(ascending=True, by="est.localTime")

    # Create an ordered dictionary (i.e. uploadId1 = 1, ,uploadId2 = 2, etc)
    upload_order_dict = dict(
                            zip(upload_data["uploadId"],
                                list(range(1, 1+len(upload_data.uploadId.unique())))
                                )
                            )

    # Sort data by upload order from the ordered dictionary
    # df["upload_order"] = df["uploadId"].copy()
    df["upload_order"] = df["uploadId"].map(upload_order_dict)
    df = df.sort_values(ascending=True, by="upload_order")

    # Replace any healthkit data deviceTimes (NaN) with a unique id
    # This prevents healthkit data with blank deviceTimes from being removed
    if("deviceTime" in list(df)):
        df.deviceTime.fillna(df.id, inplace=True)

    # Drop duplicates using est.localTime+value, time(utc time)+value,
    # deviceTime+value, and est.localTime alone
    # The last entry is kept, which contains the most recent upload data
    values_before_removal = len(df.value)
    df = df.drop_duplicates(subset=["est.localTime", "value"], keep="last")
    df = df.drop_duplicates(subset=["time", "value"], keep="last")
    if("deviceTime" in list(df)):
        df = df.drop_duplicates(subset=["deviceTime", "value"], keep="last")
    df = df.drop_duplicates(subset=["est.localTime"], keep="last")
    values_after_removal = len(df.value)
    duplicates_removed = values_before_removal-values_after_removal

    # Re-sort the data by est.localTime
    df = df.sort_values(ascending=True, by="est.localTime")

    return df, duplicates_removed
"""

def round_time(df, timeIntervalMinutes=5, timeField="time", roundedTimeFieldName="roundedTime", startWithFirstRecord=True,
               verbose=False):
    '''
    A general purpose round time function that rounds the "time"
    field to nearest <timeIntervalMinutes> minutes
    INPUTS:
        * a dataframe (df) that contains a time field that you want to round
        * timeIntervalMinutes (defaults to 5 minutes given that most cgms output every 5 minutes)
        * timeField to round (defaults to the UTC time "time" field)
        * roundedTimeFieldName is a user specified column name (defaults to roundedTime)
        * startWithFirstRecord starts the rounding with the first record if True, and the last record if False (defaults to True)
        * verbose specifies whether the extra columns used to make calculations are returned
    '''

    df.sort_values(by=timeField, ascending=startWithFirstRecord, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # make sure the time field is in the right form
    t = pd.to_datetime(df[timeField])

    # calculate the time between consecutive records
    t_shift = pd.to_datetime(df[timeField].shift(1))
    df["timeBetweenRecords"] = \
        round((t - t_shift).dt.days*(86400/(60 * timeIntervalMinutes)) +
              (t - t_shift).dt.seconds/(60 * timeIntervalMinutes)) * timeIntervalMinutes

    # separate the data into chunks if timeBetweenRecords is greater than
    # 2 times the <timeIntervalMinutes> minutes so the rounding process starts over
    largeGaps = list(df.query("abs(timeBetweenRecords) > " + str(timeIntervalMinutes * 2)).index)
    largeGaps.insert(0, 0)
    largeGaps.append(len(df))

    for gIndex in range(0, len(largeGaps) - 1):
        chunk = t[largeGaps[gIndex]:largeGaps[gIndex+1]]
        firstRecordChunk = t[largeGaps[gIndex]]

        # calculate the time difference between each time record and the first record
        df.loc[largeGaps[gIndex]:largeGaps[gIndex+1], "minutesFromFirstRecord"] = \
            (chunk - firstRecordChunk).dt.days*(86400/(60)) + (chunk - firstRecordChunk).dt.seconds/(60)

        # then round to the nearest X Minutes
        # NOTE: the ".000001" ensures that mulitples of 2:30 always rounds up.
        df.loc[largeGaps[gIndex]:largeGaps[gIndex+1], "roundedMinutesFromFirstRecord"] = \
            round((df.loc[largeGaps[gIndex]:largeGaps[gIndex+1],
                          "minutesFromFirstRecord"] / timeIntervalMinutes) + 0.000001) * (timeIntervalMinutes)

        roundedFirstRecord = (firstRecordChunk + pd.Timedelta("1microseconds")).round(str(timeIntervalMinutes) + "min")
        df.loc[largeGaps[gIndex]:largeGaps[gIndex+1], roundedTimeFieldName] = \
            roundedFirstRecord + \
            pd.to_timedelta(df.loc[largeGaps[gIndex]:largeGaps[gIndex+1],
                                   "roundedMinutesFromFirstRecord"], unit="m")

    # sort by time and drop fieldsfields
    df.sort_values(by=timeField, ascending=startWithFirstRecord, inplace=True)
    df.reset_index(drop=True, inplace=True)
    if verbose is False:
        df.drop(columns=["timeBetweenRecords",
                         "minutesFromFirstRecord",
                         "roundedMinutesFromFirstRecord"], inplace=True)

    return df


def removeInvalidCgmValues(df):
    nBefore = len(df)
    # remove values < 38 and > 402 mg/dL
    df = df.drop(df[((df.type == "cbg") &
                     (df.value < 2.109284236597303))].index)
    df = df.drop(df[((df.type == "cbg") &
                     (df.value > 22.314006924003046))].index)
    nRemoved = nBefore - len(df)

    return df, nRemoved



def removeNegativeDurations_EDS(df):
    if "duration" in list(df):
        nNegativeDurations = sum(df.duration < 0)
        if nNegativeDurations > 0:
            df = df[~(df.duration < 0)]
    else:
        nNegativeDurations = np.nan

    return df, nNegativeDurations


def removeNegativeDurations_JASONS(df):
    if "duration" in list(df):
        df_durations = df[~(df.type == "physicalActivity")]
        nNegativeDurations = sum(df_durations.duration.astype('float') < 0)
        if nNegativeDurations > 0:
            df = df_durations[~(df_durations.duration.astype('float') < 0)]

    return df



def tslimCalibrationFix_JASONS(df):
    if "deviceId" in list(df):
        searchfor = ['tan']
        tandemDataIndex = ((df.deviceId.str.contains('|'.join(searchfor))) &
                           (df.type == "deviceEvent"))

    if "payload.calibration_reading" in list(df):
        payloadCalReadingIndex = df["payload.calibration_reading"].notnull()

        nTandemAndPayloadCalReadings = sum(tandemDataIndex &
                                           payloadCalReadingIndex)

        if nTandemAndPayloadCalReadings > 0:
            # if reading is > 30 then it is in the wrong units
            if df["payload.calibration_reading"].min() > 30:
                df.loc[payloadCalReadingIndex, "value"] = \
                    df[tandemDataIndex & payloadCalReadingIndex] \
                        ["payload.calibration_reading"] / 18.01559
            else:
                df.loc[payloadCalReadingIndex, "value"] = \
                    df[tandemDataIndex &
                       payloadCalReadingIndex]["payload.calibration_reading"]
    else:
        nTandemAndPayloadCalReadings = 0
    return df, nTandemAndPayloadCalReadings


def tslimCalibrationFix_EDS(df):


    if "payload.calibration_reading" in list(df):

        searchfor = ['tan']
        tandemDataIndex = ((df.deviceId.str.contains('|'.join(searchfor))) &
                           (df.type == "deviceEvent"))


        payloadCalReadingIndex = df["payload.calibration_reading"].notnull()

        nTandemAndPayloadCalReadings = sum(tandemDataIndex &
                                           payloadCalReadingIndex)

        if nTandemAndPayloadCalReadings > 0:
            # if reading is > 30 then it is in the wrong units
            if df["payload.calibration_reading"].min() > 30:
                df.loc[payloadCalReadingIndex, "value"] = \
                    df[tandemDataIndex & payloadCalReadingIndex] \
                    ["payload.calibration_reading"] / 18.01559
            else:
                df.loc[payloadCalReadingIndex, "value"] = \
                    df[tandemDataIndex &
                        payloadCalReadingIndex]["payload.calibration_reading"]
    else:
        nTandemAndPayloadCalReadings = 0
    return df, nTandemAndPayloadCalReadings





def removeCgmDuplicates(df, timeCriterion):
    if timeCriterion in df:
        df.sort_values(by=[timeCriterion, "uploadTime"],
                       ascending=[False, False],
                       inplace=True)
        dfIsNull = df[df[timeCriterion].isnull()]
        dfNotNull = df[df[timeCriterion].notnull()]
        dfNotNull, nDuplicatesRemoved = removeDuplicates(dfNotNull, [timeCriterion, "value"])
        df = pd.concat([dfIsNull, dfNotNull])
        df.sort_values(by=[timeCriterion, "uploadTime"],
                       ascending=[False, False],
                       inplace=True)
    else:
        nDuplicatesRemoved = 0

    return df, nDuplicatesRemoved


def convertDeprecatedTimezoneToAlias(df, tzAlias):
    if "timezone" in df:
        uniqueTimezones = df.timezone.unique()
        uniqueTimezones = uniqueTimezones[pd.notnull(df.timezone.unique())]

        for uniqueTimezone in uniqueTimezones:
            alias = tzAlias.loc[tzAlias.tz.str.endswith(uniqueTimezone),
                                ["alias"]].values
            if len(alias) == 1:
                df.loc[df.timezone == uniqueTimezone, ["timezone"]] = alias

    return df


def largeTimezoneOffsetCorrection(df):

    while ((df.timezoneOffset > 840).sum() > 0):
        df.loc[df.timezoneOffset > 840, ["conversionOffset"]] = \
            df.loc[df.timezoneOffset > 840, ["conversionOffset"]] - \
            (1440 * 60 * 1000)

        df.loc[df.timezoneOffset > 840, ["timezoneOffset"]] = \
            df.loc[df.timezoneOffset > 840, ["timezoneOffset"]] - 1440

    while ((df.timezoneOffset < -720).sum() > 0):
        df.loc[df.timezoneOffset < -720, ["conversionOffset"]] = \
            df.loc[df.timezoneOffset < -720, ["conversionOffset"]] + \
            (1440 * 60 * 1000)

        df.loc[df.timezoneOffset < -720, ["timezoneOffset"]] = \
            df.loc[df.timezoneOffset < -720, ["timezoneOffset"]] + 1440

    return df



###################################### what was existing ###################################################



def round_time( df, timeIntervalMinutes=5, timeField="time", roundedTimeFieldName="roundedTime", verbose=False,):

    # A general purpose round time function that rounds the
    # "time" field to nearest <timeIntervalMinutes> minutes
    # INPUTS:
    #   * a dataframe (df) that contains a time field
    #   * timeIntervalMinutes defaults to 5 minutes given that most cgms output every 5 minutes
    #   * timeField defaults to UTC time "time"
    #   * verbose specifies whether the "TIB" and "TIB_cumsum" columns are returned

    df.sort_values(by=timeField, ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # calculate the time-in-between (TIB) consecutive records
    t = pd.to_datetime(df.time)
    t_shift = pd.to_datetime(df.time.shift(1))
    df["TIB"] = (
        round(
            (t - t_shift).dt.days * (86400 / (60 * timeIntervalMinutes))
            + (t - t_shift).dt.seconds / (60 * timeIntervalMinutes)
        )
        * timeIntervalMinutes
    )

    # separate the data into chunks if TIB is greater than <timeIntervalMinutes> minutes
    # so that rounding process can start over
    largeGaps = list(df.query("TIB > " + str(timeIntervalMinutes)).index)
    largeGaps.insert(0, 0)
    largeGaps.append(len(df))

    # loop through each chunk to get the cumulative sum and the rounded time
    for gIndex in range(0, len(largeGaps) - 1):

        df.loc[largeGaps[gIndex], "TIB"] = 0

        df.loc[largeGaps[gIndex] : (largeGaps[gIndex + 1] - 1), "TIB_cumsum"] = df.loc[
            largeGaps[gIndex] : (largeGaps[gIndex + 1] - 1), "TIB"
        ].cumsum()

        df.loc[
            largeGaps[gIndex] : (largeGaps[gIndex + 1] - 1), roundedTimeFieldName
        ] = pd.to_datetime(df.loc[largeGaps[gIndex], timeField]).round(
            str(timeIntervalMinutes) + "min"
        ) + pd.to_timedelta(
            df.loc[largeGaps[gIndex] : (largeGaps[gIndex + 1] - 1), "TIB_cumsum"],
            unit="m",
        )

    # sort descendingly by time and drop fieldsfields
    df.sort_values(by=timeField, ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    if verbose is False:
        df.drop(columns=["TIB", "TIB_cumsum"], inplace=True)

    return df


# OTHER
def temp_remove_fields(df, removeFields):
    tempRemoveFields = list(set(df) & set(removeFields))
    tempDf = df[tempRemoveFields]
    df = df.drop(columns=tempRemoveFields)

    return df, tempDf


def flatten_json(df, doNotFlattenList):
    # remove fields that we don't want to flatten
    df, hold_data = temp_remove_fields(df, doNotFlattenList)

    # get a list of data types of column headings
    column_headings = list(df)

    # loop through each columnHeading
    newDataFrame = pd.DataFrame()

    for colHead in column_headings:
        if any(isinstance(item, list) for item in df[colHead]):
            listBlob = df[colHead][df[colHead].astype(str).str[0] == "["]
            df.loc[listBlob.index, colHead] = df.loc[listBlob.index, colHead].str[0]

        # if the df field has embedded json
        if any(isinstance(item, dict) for item in df[colHead]):
            # grab the data that is in brackets
            jsonBlob = df[colHead][df[colHead].astype(str).str[0] == "{"]

            # replace those values with nan
            df.loc[jsonBlob.index, colHead] = np.nan

            # turn jsonBlob to dataframe
            newDataFrame = pd.concat(
                [
                    newDataFrame,
                    pd.DataFrame(jsonBlob.tolist(), index=jsonBlob.index).add_prefix(
                        colHead + "."
                    ),
                ],
                axis=1,
            )

    df = pd.concat([df, newDataFrame, hold_data], axis=1)

    df.sort_index(axis=1, inplace=True)

    return df
