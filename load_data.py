# -*- coding: utf-8 -*-
import os
import pandas as pd

path = r"Data/"
os.chdir(path)


def create_df():
    file_list = []
    for file in os.listdir():
        if file.endswith(".csv"):
            file_path = f"../{path}{file}"
            file_list.append(file_path)

    athlete_event = pd.read_csv(file_list[0])
    noc_regions = pd.read_csv(file_list[1])
    return athlete_event, noc_regions


# to be set in next py file
athlete, noc = create_df()

print(athlete.head())
