import pandas as pd
from load_data import create_df

noc_regions, athlete_event = create_df()

medalists = athlete_event.dropna(subset=['Medal'])

winter = medalists[medalists['Season'] == 'Winter']
summer = medalists[medalists['Season'] == 'Summer']

olympic_summer_years = summer["Year"].unique()
olympic_summer_years = list(olympic_summer_years)
olympic_summer_years.sort()

olympic_winter_years = winter["Year"].unique()
olympic_winter_years = list(olympic_winter_years)
olympic_winter_years.sort()

def medal_sets(dataframe, years: list)-> dict :
    olympic_medal_distributed = []
    for year in years:
        df = dataframe[dataframe["Year"] == year]
        df.drop_duplicates(subset ="Event", keep = 'first', inplace = True)
        olympic_medal_distributed.append(len(df["Medal"]))
    medals_per_year = dict(zip(years, olympic_medal_distributed))
    return medals_per_year

medals_per_year_winter = medal_sets(winter, olympic_winter_years)
medals_per_year_summer = medal_sets(summer, olympic_summer_years)

print(medals_per_year_summer)
print(medals_per_year_winter)