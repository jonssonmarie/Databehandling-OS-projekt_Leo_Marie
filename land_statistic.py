import pandas as pd
import numpy as np
import hashlib as hl


def anonymous(df):
    """
    Anonymous the competitor names
    :param df: with data of the OS
    :return: df with Name anonymize
    """
    df["Name"] = df["Name"].astype(str)
    df["Name"] = df["Name"].apply(lambda x: hl.sha256(x.encode()).hexdigest())
    return df


def sort_france_medals(df):
    """
    Sort the medals that France has won
    :param df: dataframe with Name anonymize
    :return: df sorted on France and medals
    """
    df = df.drop_duplicates(subset=["Event", "Games", "Medal"])
    df = df[['ID', 'Name', 'Sex', 'Age', 'NOC', 'Games', 'Sport', 'Medal']]     # collect the labels needed further on
    df['Medal'] = df['Medal'].astype(str)
    medals_fra = df.query("NOC == 'FRA' & Medal != 'nan'")
    return medals_fra


def count_medals_per_sport(df):
    """ Count number of medals per Sport for France
    :param df: dataframe with Name anonymize
    :return: DataFrame with Sport, Medal, amount of medals for Gold, Silver and Bronze
    """
    sports = df['Sport'].unique()
    medal_value = df["Medal"].unique()
    count_medals = []
    for sport in sports:
        for medal in medal_value:
            fra_medal = df.query("Sport == @sport & Medal == @medal")
            count = np.sum(fra_medal['Medal'] == medal)
            count_man = np.sum(fra_medal["Sex"] == 'M')
            count_female = np.sum(fra_medal["Sex"] == 'F')
            summary = [sport, medal, count, count_man, count_female]
            count_medals.append(summary)
    count_medal = pd.DataFrame(count_medals, columns=['Sport', 'Medal', 'Amount', "Amount M", "Amount F"]) \
        .sort_values(by='Amount', ascending=False)
    return count_medal


def medals_per_os(df):
    """ Count number of medals per Game for France
    :param df: dataframe with Name anonymize
    :return: DataFrame with Game, Medal, amount of medals for Gold, Silver and Bronze
    """
    medal_value = df["Medal"].unique()
    games = df["Games"].unique()
    medal_per_os = []
    for game in games:
        for medal in medal_value:
            olympic_game = df.query("Games == @game")
            count = np.sum(olympic_game["Medal"] == medal)
            summary = [game, medal, count]
            medal_per_os.append(summary)
    count_os = (pd.DataFrame(medal_per_os, columns=["Game", "Medal", "Amount"])).sort_values(by="Game", ascending=True)
    return count_os


def age_per_os(df):
    """
    Count how many participants there are per age for France
    :param df: dataframe with Name anonymize
    :return: DataFrame with Age, amount of ages per Age
    """
    all_ages = []
    ages = df["Age"].dropna().unique()
    for age in ages:
        count = np.sum(df["Age"] == age)
        summary = [age, count]
        all_ages.append(summary)
    count_age = pd.DataFrame(all_ages, columns=["Age", "Amount"]).sort_values(by="Age", ascending=True)
    return count_age
