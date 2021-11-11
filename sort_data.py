
def olympic_medalists(athletes_dataframe: DataFrame, season="all") -> object:
    """ Takes in the athletes dataframe and returns it filtered with medalists only. A season can be passed as argument.
    :param athletes_dataframe: 
    :param season: 
    :return: 
    """
    df = athletes_dataframe.dropna(subset=['Medal'])
    df = seasonize(df, season)
    return df


def top_10_nations_medals():
    # TODO
    pass


def olympic_years(seasonal_dataframe: object) -> list:
    """  Takes in a seasonalized dataframe (Summer or Winter) and returns a list of years when olympic games took place
    :param seasonal_dataframe: 
    :return: 
    """
    o_years = seasonal_dataframe["Year"].unique()
    o_years = list(o_years)
    o_years.sort()
    return o_years


def medal_sets(athletes_dataframe: DataFrame, years: list) -> object:
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
    