import pandas as pd


def possible_medals(athletes_dataframe):
    """ Extracts the possible medal options from the athletes dataframe
    :param athletes_dataframe:
    :return: serie
    """
    medal_types = athletes_dataframe.dropna(subset=['Medal'])
    medal_types = medal_types['Medal'].unique()
    return medal_types


def seasonize(athletes_dataframe, season="all"):
    """ Returns a dataframe according to olympic season, summer or winter
    :param athletes_dataframe: dataframe
    :param season: str 'Winter' or 'Summer', default 'all'
    :return: dataframe
    """
    if season == "Summer" or season == "Winter":
        df = athletes_dataframe.loc[athletes_dataframe['Season'] == f'{season}']
    elif season == "all":
        df = athletes_dataframe
    else:
        raise ValueError(f"Season can either be Winter, SUmmer, or all, not {season}")
    return df


def age_proofed_dataframe(athletes_dataframe):
    """ Returns a dataframe filtered from athletes without age given, and duplicate athletes names are erased
    :param athletes_dataframe: dataframe
    :return: dataframe
    """
    df = athletes_dataframe.dropna(subset=['Age'])
    df.drop_duplicates(subset="Name", keep='first', inplace=True)
    return df


def age_stats(dataframe, season="all"):  # Utveckla funktionen så att statistiken kan delas mellan år ?
    """ Takes in a dataframe and returns age statistics for Male and Female athletes as a pandas Series
    :param dataframe: dataframe
    :param season: str 'Winter' or 'Summer', default 'all'
    :return: pandas series
    """
    df = age_proofed_dataframe(dataframe)
    df = seasonize(df, season)
    stats = df.groupby(['Sex']).Age.agg(['mean', 'median', 'min', 'max', 'std'])
    return stats


def athletes_by_sex_ratio(dataframe, season="all"):
    """
    :param dataframe: dataframe
    :param season: str 'Winter' or 'Summer', default 'all'
    :return: dataframe
    """
    df = seasonize(dataframe, season)
    count_M = len(df[df["Sex"] == "M"])
    count_F = len(df[df["Sex"] == "F"])
    output_df = pd.DataFrame({"Sex": ["F", "M"], "Count": [count_F, count_M]})
    return output_df


def athletes_by_sex_ratio_over_time(dataframe, season="all"):
    """
    :param dataframe:
    :param season: str 'Winter' or 'Summer', default 'all'
    :return: dataframe
    """
    df = seasonize(dataframe, season)
    df.drop_duplicates(subset="Name", keep='first', inplace=True)

    years = olympic_years(df)
    female_participants = []
    male_participants = []

    for year in years:
        daf = df[df["Year"] == year]
        female_count = len(daf[daf["Sex"] == "F"])
        male_count = len(daf[daf["Sex"] == "M"])
        female_participants.append(female_count)
        male_participants.append(male_count)

    output_df = pd.DataFrame(list(zip(years, female_participants, male_participants)),
                             columns=["Year", "Count F", "Count M"])
    output_df["Total"] = output_df["Count F"] + output_df["Count M"]
    output_df["Share M"] = output_df["Count M"] / output_df["Total"]
    output_df["Share F"] = output_df["Count F"] / output_df["Total"]
    return output_df


def olympic_medalists(athletes_dataframe):
    """ Takes in the athletes dataframe and returns it filtered with medalists only. A season can be passed as argument.
    :param athletes_dataframe: dataframe
    :return: dataframe
    """
    df = athletes_dataframe.dropna(subset=['Medal'])
    return df


def top_10_nations_medals(dataframe, season="all"):
    """
    :param dataframe: dataframe
    :param season: str 'Winter' or 'Summer', default 'all'
    :return: dataframe
    """
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

    output_df = pd.DataFrame({"Nation": nations, "Gold": gold_medals, "Silver": silver_medals, "Bronze": bronze_medals})
    output_df.eval("Total = Gold + Silver + Bronze", inplace=True)
    output_df.sort_values(by=['Total'], ascending=False, inplace=True)
    return output_df.head(10)

def top_5_nations_medals_per_sport(dataframe, sport = "Cross Country Skiing"):
    """
    :param dataframe: 
    :param sport: str, valid input is sport in Sport-column in athlete_events
    :return: dataframe
    """
    nations = dataframe["NOC"].unique()
    df = dataframe.dropna(subset=['Medal'])
    df = df.drop_duplicates(subset=["Event", "Games", "Medal", "NOC"])
    df = df.query(f"Sport == '{sport}'")
    gold_medals = []
    silver_medals = []
    bronze_medals = []
    for nation in nations:
        gold_medals.append(df.query(f"NOC == '{nation}' & Medal == 'Gold'").shape[0])
        silver_medals.append(df.query(f"NOC == '{nation}' & Medal == 'Silver'").shape[0])
        bronze_medals.append(df.query(f"NOC == '{nation}' & Medal == 'Bronze'").shape[0])

    output_df = pd.DataFrame({"Nation": nations, "Gold": gold_medals, "Silver": silver_medals, "Bronze": bronze_medals})
    output_df.eval("Total = Gold + Silver + Bronze", inplace=True)
    output_df.sort_values(by=['Total'], ascending=False, inplace=True)
    return output_df.head(5)

def olympic_years(dataframe):
    """  Takes in a seasonalized dataframe (Summer or Winter) and returns a list of years when olympic games took place
    :param seasonal_dataframe: dataframe
    :return: list
    """
    o_years = dataframe["Year"].unique()
    o_years = list(o_years)
    o_years.sort()
    return o_years


def medal_sets(athletes_dataframe, season="all"):
    """ Returns a dataframe, with olympic years and number of medal sets distributed as columns.
    :param athletes_dataframe: dataframe
    :param season: str 'Winter' or 'Summer', default 'all'
    :return: dataframe
    """
    df = seasonize(athletes_dataframe, season)
    years = olympic_years(df)
    df = df.dropna(subset=['Medal'])
    df = df.drop_duplicates(subset=["Event", "Games", "Medal", "NOC"])

    olympic_medal_distributed = []
    for year in years:
        dataframe = df[df["Year"] == year]
        olympic_medal_distributed.append(len(dataframe["Medal"]))

    medals_per_year = pd.DataFrame(list(zip(years, olympic_medal_distributed)), columns=["Year", "Total Medal sets"])
    return medals_per_year
