from numpy import ndarray
import pandas as pd
from pandas.core.frame import DataFrame
from load_data import create_df


def possible_medals(athletes_dataframe)-> ndarray:
    """Extracts the possible medal options from the athletes dataframe"""
    medal_types = athletes_dataframe.dropna(subset=['Medal'])
    medal_types = medal_types['Medal'].unique()
    return medal_types

def seasonize(athletes_dataframe, season = "all")-> DataFrame :
    """
    Returns a dataframe according to olympic season, summer or winter
    """
    if season == "Summer" or season == "Winter":
        df = athletes_dataframe.loc[athletes_dataframe['Season'] == f'{season}']
    elif season == "all":
        df = athletes_dataframe
        print("No season given, all seasons still inculded, dataframe not seasonalized")
    else:
        raise ValueError(f"Season can either be Winter, SUmmer, or all, not {season}")
    return df


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

def athletes_by_sex_ratio(dataframe, season = "all") -> pd.DataFrame:
    df = seasonize(dataframe, season)
    count_M = len(df.loc[dataframe["Sex"] == "M"])
    count_F = len(df.loc[dataframe["Sex"] == "F"])
    output_df = pd.DataFrame({"Sex" : ["F", "M"], "Count" : [count_F, count_M]})
    return output_df

def athletes_by_sex_ratio_over_time(dataframe, season = "all") -> pd.DataFrame:
    df = seasonize(dataframe, season)
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


def olympic_medalists(athletes_dataframe: DataFrame, season = "all")-> DataFrame :
    """
    Takes in the athletes dataframe and returns it filtered with medalists only. A season can be passed as argument.
    """
    df = athletes_dataframe.dropna(subset=['Medal'])
    df = seasonize(df, season)
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
