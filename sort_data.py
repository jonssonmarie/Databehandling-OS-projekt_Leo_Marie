
import pandas as pd
import numpy as np
from load_data import create_df


def possible_medals(athletes_dataframe) -> object:
    """ Extracts the possible medal options from the athletes dataframe
    :param athletes_dataframe:
    :return:
    """
    medal_types = athletes_dataframe.dropna(subset=['Medal'])
    medal_types = medal_types['Medal'].unique()
    return medal_types


def seasonize(athletes_dataframe, season="all") -> object:
    """ Returns a dataframe according to olympic season, summer or winter
    :param athletes_dataframe:
    :param season:
    :return:
    """
    if season == "Summer" or season == "Winter":
        df = athletes_dataframe.loc[athletes_dataframe['Season'] == f'{season}']
    elif season == "all":
        df = athletes_dataframe
        print("No season given, all seasons still inculded, dataframe not seasonalized")
    else:
        raise ValueError(f"Season can either be Winter, SUmmer, or all, not {season}")
    return df


def age_proofed_dataframe(athletes_dataframe) -> object:
    """ Returns a dataframe filtered from athletes without age given, and duplicate athletes names are erased
    :param athletes_dataframe:
    :return:
    """
    df = athletes_dataframe.dropna(subset=['Age'])
    df.drop_duplicates(subset="Name", keep='first', inplace=True)  # Hantera homonymer, ojoj ??
    return df


def age_stats(dataframe) -> object:  # Utveckla funktionen så att statistiken kan delas mellan år ?
    """ Takes in a dataframe and returns age statistics for Male and Female athletes as a pandas Series
    :param dataframe:
    :return:
    """
    # Filter season argument if given
    stats = dataframe.groupby(['Sex']).Age.agg(['mean', 'median', 'min', 'max', 'std'])
    return stats


def athletes_by_sex_ratio(dataframe, season="all") -> object:
    """
    :param dataframe:
    :param season:
    :return:
    """
    df = seasonize(dataframe, season)
    count_M = np.sum(df.loc[dataframe["Sex"] == "M"])
    count_F = np.sum(df.loc[dataframe["Sex"] == "F"])
    output_df = pd.DataFrame({"Sex": ["F", "M"], "Count": [count_F, count_M]})
    return output_df


def athletes_by_sex_ratio_over_time(dataframe, season="all") -> object:
    """
    :param dataframe:
    :param season:
    :return:
    """
    df = seasonize(dataframe, season)
    df.drop_duplicates(subset="Name", keep='first', inplace=True)

    years = olympic_years(df)
    F_participants = []
    M_participants = []

    for year in years:
        daf = df[df["Year"] == year]
        F_count = np.sum(daf[daf["Sex"] == "F"])
        M_count = np.sum(daf[daf["Sex"] == "M"])
        F_participants.append(F_count)
        M_participants.append(M_count)

    output_df = pd.DataFrame(list(zip(years, F_participants, M_participants)), columns=["Year", "Count F", "Count M"])
    output_df["Total"] = output_df["Count F"] + output_df["Count M"]
    output_df["Share M"] = output_df["Count M"] / output_df["Total"]
    output_df["Share F"] = output_df["Count F"] / output_df["Total"]
    return output_df


def olympic_medalists(athletes_dataframe: object, season="all") -> object:
    """ Takes in the athletes dataframe and returns it filtered with medalists only. A season can be passed as argument.
    :param athletes_dataframe:
    :param season:
    :return:
    """
    df = athletes_dataframe.dropna(subset=['Medal'])
    df = seasonize(df, season)
    return df


def top_10_nations_medals(dataframe: object, season ="all") -> object:
    nations = dataframe["NOC"].unique()
    df = dataframe.dropna(subset=['Medal'])
    df = seasonize(df, season)
    df = df.drop_duplicates(subset=["Event", "Games", "Medal", "NOC"])
    gold_medals = []
    silver_medals = []
    bronze_medals = []
    for nation in nations:
        gold_medals.append(df.query(f"NOC == '{nation}' & Medal == 'Gold'").shape[0])
        silver_medals.append(df.query(f"NOC == '{nation}' & Medal == 'Silver'").shape[0])
        bronze_medals.append(df.query(f"NOC == '{nation}' & Medal == 'Bronze'").shape[0])

    output_df = pd.DataFrame({"Nation" : nations, "Gold" : gold_medals, "Silver" : silver_medals,  "Bronze" : bronze_medals})
    output_df.eval("Total = Gold + Silver + Bronze", inplace = True)
    output_df.sort_values(by=['Total'], ascending=False, inplace=True)
    return output_df.head(10)


def olympic_years(seasonal_dataframe: object) -> list:
    """  Takes in a seasonalized dataframe (Summer or Winter) and returns a list of years when olympic games took place
    :param seasonal_dataframe:
    :return:
    """
    o_years = seasonal_dataframe["Year"].unique()
    o_years = list(o_years)
    o_years.sort()
    return o_years


def medal_sets(athletes_dataframe: object, years: list) -> object:
    """ Returns a dataframe, with olympic years as keys and number of medal sets distributed as values.
    :param athletes_dataframe:
    :param years:
    :return:
    """
    olympic_medal_distributed = []
    for year in years:
        df = athletes_dataframe[athletes_dataframe["Year"] == year]
        df.drop_duplicates(subset="Event", keep='first', inplace=True)
        olympic_medal_distributed.append(len(df["Medal"]))
    medals_per_year = pd.DataFrame(list(zip(years, olympic_medal_distributed)), columns=["Year", "Total Medal sets"])
    return medals_per_year
