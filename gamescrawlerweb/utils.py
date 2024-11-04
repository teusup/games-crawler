import numpy as np


def calculate_average_score(dataframe):
    total_score = 0
    not_nan = 0

    if not np.isnan(dataframe["Meta_score"]):
        total_score += dataframe["Meta_score"] / 100
        not_nan += 1
    if not np.isnan(dataframe["User_score_x"]):
        total_score += dataframe["User_score_x"] / 10
        not_nan += 1
    if not np.isnan(dataframe["Ign_score"]):
        total_score += dataframe["Ign_score"] / 10
        not_nan += 1
    if not np.isnan(dataframe["User_score_y"]):
        total_score += dataframe["User_score_y"] / 10
        not_nan += 1
    if not np.isnan(dataframe["Score"]):
        total_score += dataframe["Score"] / 5
        not_nan += 1
    if not np.isnan(dataframe["OpenCritic_average"]):
        total_score += dataframe["OpenCritic_average"] / 100
        not_nan += 1
    if not np.isnan(dataframe["OpenCritic_recommended"]):
        total_score += dataframe["OpenCritic_recommended"] / 100
        not_nan += 1
    if not_nan > 0:
        average_score = "{:.2f}".format(total_score / not_nan * 100)
    else:
        average_score = '-'

    return average_score
