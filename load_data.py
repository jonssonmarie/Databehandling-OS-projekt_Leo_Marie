# -*- coding: utf-8 -*-
import os
import pandas as pd

path = r"Data/"
os.chdir(path)


def create_df() -> object:
    """ read all files with end ".csv" from a specified folder and create dataframes
    :return: dataframes
    """
    file_list = []
    for file in sorted(os.listdir()):
        if file.endswith(".csv"):
            file_path = f"../{path}{file}"
            file_list.append(file_path)

    athlete_event = pd.read_csv(file_list[0])
    noc_regions = pd.read_csv(file_list[1])
    return athlete_event, noc_regions
