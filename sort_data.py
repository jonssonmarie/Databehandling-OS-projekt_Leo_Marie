import pandas as pd
from pandas.core.frame import DataFrame
from load_data import create_df

athlete_event, noc_regions = create_df()

def olympic_medals_by_season(athletes_dataframe: DataFrame, season = "Summer")-> DataFrame :
    """
    Takes in the athletes dataframe and returns it filtered by season, and with medalists only
    """
    df = athletes_dataframe.dropna(subset=['Medal'])
    df = df[df['Season'] == f'{season}']
    return df

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
    Returns a dictionary, with olympic years as keys and number of medal sets distributed as values.
    """
    olympic_medal_distributed = []
    for year in years:
        df = athletes_dataframe[athletes_dataframe["Year"] == year]
        df.drop_duplicates(subset ="Event", keep = 'first', inplace = True)
        olympic_medal_distributed.append(len(df["Medal"]))
    medals_per_year = pd.DataFrame(list(zip(years, olympic_medal_distributed)), columns = ["Year", "Total Medal sets"])
    return medals_per_year

summer_medalists = olympic_medals_by_season(athlete_event) #Summer as default season
winter_medalists = olympic_medals_by_season(athlete_event, "Winter")

olympic_summer_years = olympic_years(summer_medalists)
olympic_winter_years = olympic_years(winter_medalists)

medals_per_year_winter = medal_sets(winter_medalists, olympic_winter_years)
medals_per_year_summer = medal_sets(summer_medalists, olympic_summer_years)

print(medals_per_year_summer)
print(medals_per_year_winter)