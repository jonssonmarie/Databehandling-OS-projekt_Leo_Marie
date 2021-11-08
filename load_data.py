# -*- coding: utf-8 -*-
import os
import pandas as pd

path = r"Data/"
os.chdir(path)

file_list = []
for file in os.listdir():
    if file.endswith(".csv"):
        file_path = f"../{path}{file}"
        file_list.append(file_path)


def create_df(lst):
    athlete_event = pd.read_csv(lst[0])
    noc_regions = pd.read_csv(lst[1])
    #print(athlete_event.head())


# TO BE DONE set in next py file ex statistic
athlete, noc = create_df(file_list)




