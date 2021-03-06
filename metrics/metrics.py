import numpy as np
from typing import Tuple
import pandas as pd


def get_cv_of_glucose(bg_values, round_val=2):
    """
        Calculate the average within a set of glucose values

        Arguments:
        values -- numpy array contains a list of bg values.
        round_val -- the number of digits to round the result to.

        Output: Calculated Average
    """
    std_dev = get_std_deviation(bg_values, round_val)
    avg_glu = get_avg_glucose(bg_values, round_val)
    return round(std_dev/avg_glu * 100, round_val)


def get_gmi(bg_values, round_val=2):
    """
        Calculate the average within a set of glucose values

        Arguments:
        values -- numpy array contains a list of bg values.
        round_val -- the number of digits to round the result to.

        Output: Calculated Average

        GMI(mmol / mol) = 12.71 + 4.70587 x[mean glucose in mmol / L]
        GMI( %) = 3.31 + 0.02392 x[mean glucose in mg / dL]
        #For example, if the SD is 50 mg/dl, and the average glucose is 150 mg/dl,
        # then you divide 50 by 150, multiply by 100, and you get a CV of 33%.
    """
    gmi = 3.31 + (0.02392 * get_mean_glucose(bg_values))
    return round(gmi, round_val)

def get_mean_glucose(bg_values, round_val=2):
    """
        Calculate the mean within a set of glucose values

        Arguments:
        values -- numpy array contains a list of bg values.
        round_val -- the number of digits to round the result to.

        Output: Calculated Mean
    """
    return round(np.mean(bg_values), round_val)

def get_avg_glucose(bg_values, round_val=2):
    """
        Calculate the average within a set of glucose values

        Arguments:
        values -- numpy array contains a list of bg values.
        round_val -- the number of digits to round the result to.

        Output: Calculated Average
    """
    return round(np.average(bg_values), round_val)

def get_std_deviation(bg_values, round_val=2):
    """
            Calculate the standard deviation within a set of glucose values

            Arguments:
            values -- numpy array contains a list of bg values.
            round_val -- the number of digits to round the result to.

            Output: Calculated standard deviation
    """
    return round(np.std(bg_values), round_val)

def get_percent_values_by_range(bg_values, lower_threshold: int, upper_threshold: int, round_val=2):
    """
        Calculate the percent of values that match has a bg within the lower and upper threshold.
        The lower and upper values will be included in the range to calculate on.

        Arguments:
        bg_values -- numpy array contains a list of bg values.
        lower_threshold -- The the lower value in the range to calculate on.
        upper_threshold -- The the upper value in the range to calculate on.
        round_val -- the number of digits to round the result to.

        Output:
        Percent value
    """
    calc_low_thresh, calc_upper_thresh = _validate_input(lower_threshold, upper_threshold)
    results = round(np.where((bg_values <= calc_upper_thresh) & (bg_values >= calc_low_thresh), 1, 0).sum()/bg_values.size*100, round_val)
    return results

def get_percent_time_in_range(bg_values, lower_threshold: int, upper_threshold: int, round_val=2, time_delta=5 ):
    """
        Calculate the number of minutes the bg was within the lower and upper range.
        The lower and upper values will be included in the range to calculate on.

        Arguments:
        bg_values -- Panda Dataframe with a column named values that contains a list of bg values and a column named date
        containing a python datetime value.
        lower_threshold -- The the lower value in the range to calculate on.
        upper_threshold -- The the upper value in the range to calculate on.
        round_val -- the number of digits to round the result to.

        Output:
        Percent of bg values in range
    """
    calc_low_thresh, calc_upper_thresh = _validate_input(lower_threshold, upper_threshold)
    bg_df = bg_values['bg_values']
    bg_np = bg_df.to_numpy()
    in_range = np.count_nonzero((bg_np > calc_low_thresh) & (bg_np < calc_upper_thresh))
    val_count = bg_df.count()
    return round(in_range/val_count*100, round_val)

#todo:need to finish this and create test
"""  
def get_episodes(
        df,
        episode_criterion="cgm",
        min_duration=5,
):
    # TODO: deal with case where there are nan's in the middle of an episode
    # it probably makes sense to interpolate between values iff the gap is
    # <= 1 to 6 points (5 to 30 minutes)
    print("test")
    # put consecutive data that matches in groups
    df["tempGroups"] = ((
        df[episode_criterion] != df[episode_criterion].shift()
    ).cumsum())

    df["episodeId"] = (
        df["tempGroups"] * df[episode_criterion]
    )

    # group by the episode groups
    episode_groups = df.groupby("episodeId")
    episodes = episode_groups["roundedUtcTime"].count().reset_index()
    episodes["duration"] = episodes["roundedUtcTime"] * 5
    episodes.rename(columns={"roundedUtcTime": "episodeCounts"}, inplace=True)

    df = pd.merge(df, episodes, on="episodeId", how="left")
    df["episodeDuration"] = (
        df["duration"] * df[episode_criterion]
    )

    # mark record as belonging to an episode
    df["isEpisode"] = (
        df["episodeDuration"] >= min_duration
    )

    # get the hypo episode starts so we only count each episode once
    df["episodeStart"] = (
        (df[episode_criterion])
        & (~df[episode_criterion].shift(1).fillna(False))
    )

    # calculate the total duration and attach to start record
    # which is needed to get the average duration per episode
    df["episodeTotalDuration"] = (
        df["episodeStart"] * df["episodeDuration"]
    )
    df["episodeTotalDuration"].replace(0, np.nan, inplace=True)

    episode_prefix = (
        "episode." + episode_criterion
        + ".durationThreshold=" + str(min_duration) + "."
    )

    df = df[[
        "isEpisode", "episodeId", "episodeStart", "episodeTotalDuration"
    ]].add_prefix(episode_prefix)

    return df
"""

def get_bgri(bg_values, round_val=2):
    """
            Calculate the LBGI, HBGI and BRGI within a set of glucose values

            Arguments:
            values -- numpy array contains a list of bg values.
            round_val -- the number of digits to round the result to.

            Output: Calculated standard deviation
    """

    # Calculate LBGI and HBGI using equation from
    # Clarke, W., & Kovatchev, B. (2009)
    ###bgs = bg_df.copy()
    bg_values[bg_values < 1] = 1  # this is added to take care of edge case BG <= 0
    transformed_bg = 1.509*((np.log(bg_values)**1.084)-5.381)
    risk_power = 10*(transformed_bg)**2
    low_risk_bool = transformed_bg < 0
    high_risk_bool = transformed_bg > 0
    rlBG = risk_power * low_risk_bool
    rhBG = risk_power * high_risk_bool
    LBGI = round(np.mean(rlBG), round_val)
    HBGI = round(np.mean(rhBG), round_val)
    BGRI = round(LBGI + HBGI, round_val)

    return LBGI[0], HBGI[0], BGRI[0]


def _validate_input(lower_threshold: int, upper_threshold: int) -> Tuple[int, int]:
    if any(num < 0 for num in [lower_threshold, upper_threshold]):
        raise Exception("lower and upper thresholds must be a non-negative number")
    if upper_threshold == 0:
        upper_threshold = 1000
    if lower_threshold > upper_threshold:
        raise Exception("lower threshold is higher than the upper threshold.")
    return lower_threshold, upper_threshold