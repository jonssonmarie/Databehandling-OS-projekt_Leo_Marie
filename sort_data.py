from numpy import ndarray
import pandas as pd
from pandas.core.frame import DataFrame
from load_data import create_df


def possible_medals(athletes_dataframe)-> ndarray:
    """Extracts the possible medal options from the athletes dataframe"""
    medal_types = athletes_dataframe.dropna(subset=['Medal'])
    medal_types = medal_types['Medal'].unique()
    return medal_types

def age_proofed_dataframe(athletes_dataframe)-> pd.DataFrame:
    """Returns a dataframe filtered from athletes without age given, and duplicate athletes names are erased """
    df = athletes_dataframe.dropna(subset=['Age'])
    df.drop_duplicates(subset ="Name", keep = 'first', inplace = True)#Hantera homonymer, ojoj ??
    return df

def age_stats(dataframe)-> pd.Series: #Utveckla funktionen så att statistiken kan delas mellan år ?
    """Takes in a dataframe and returns age statistics for Male and Female athletes as a pandas Series"""
    #Filter season argument if given
    stats = dataframe.groupby(['Sex']).Age.agg(['mean', 'median', 'min', 'max', 'std' ])
    return stats

def athletes_by_sex_ratio(dataframe) -> pd.DataFrame:
    #TODO
    pass

def athletes_by_sex_ratio_over_time(dataframe, season = "Summer") -> pd.DataFrame:
    df = dataframe[dataframe['Season'] == f'{season}']
    df.drop_duplicates(subset ="Name", keep = 'first', inplace = True)

    years = olympic_years(df)
    F_participants = []
    M_participants = []

    for year in years:
        daf = df[df["Year"] == year]
        F_count = len(daf[daf["Sex"] == "F"])
        M_count = len(daf[daf["Sex"] == "M"])
        F_participants.append(F_count)
        M_participants.append(M_count)
    
    output_df = pd.DataFrame(list(zip(years, F_participants, M_participants)), columns = ["Year", "Count F", "Count M"])
    output_df["Total"] = output_df["Count F"] + output_df["Count M"]
    output_df["Share M"] = output_df["Count M"] / output_df["Total"]
    output_df["Share F"] = output_df["Count F"] / output_df["Total"]
    return output_df


def olympic_medals_by_season(athletes_dataframe: DataFrame, season = "Summer")-> DataFrame :
    """
    Takes in the athletes dataframe and returns it filtered by season, and with medalists only
    """
    df = athletes_dataframe.dropna(subset=['Medal'])
    df = df[df['Season'] == f'{season}']
    return df

def top_10_nations_medals():
    #TODO
    pass

def olympic_years(seasonal_dataframe: DataFrame)-> list:
    """
    Takes in a seasonalized dataframe (Summer or Winter) and returns a list of years when olympic games took place
    """
    o_years = seasonal_dataframe["Year"].unique()
    o_years = list(o_years)
    o_years.sort()
    return o_years



def medal_sets(athletes_dataframe: DataFrame, years: list)-> DataFrame :
    """
    Returns a dataframe, with olympic years as keys and number of medal sets distributed as values.
    """
    olympic_medal_distributed = []
    for year in years:
        df = athletes_dataframe[athletes_dataframe["Year"] == year]
        df.drop_duplicates(subset ="Event", keep = 'first', inplace = True)
        olympic_medal_distributed.append(len(df["Medal"]))
    medals_per_year = pd.DataFrame(list(zip(years, olympic_medal_distributed)), columns = ["Year", "Total Medal sets"])
    return medals_per_year
