import time


def offline_plot(df1, df2, df3, df4):
    """ Plot and save the html-plot to a folder
    :param df1: medals_sport
    :param df2: medals_os
    :param df3: medals_france
    :param df4: athletics
    :return: None
    """
    bar_plot(df1, "Sport", "Amount", "Amount of medals per sport for France in OS", "Amount", "Medal",
             "Visualizations/France_medals_per_sport.html")
    bar_plot(df2, "Game", "Amount", "Amount of medals per game for France in OS", "Amount", "Medal",
             "Visualizations/France_amount_of_medals_per_game.html")
    bar_plot(df3, "Sport", ["Sex"], "Amount of medals per sex in OS", "Sex", "Medal",
             "Visualizations/France_summery_of_all_medals_per_sex.html")
    histogram_plot(df4, "Age", "Age", "Amount of medals for Athletics", "Amount", None,
                   "Visualizations/Age_summery_per_athletics.html")


def main():
    start = time.time()
    athlete_event, noc_regions = create_df()

    # Note: anonymous name
    medals_france = sort_france_medals(athlete_event)
    medals_sport = count_medals_per_sport(medals_france)
    medals_os = medals_per_os(medals_france)
    athletics = athlete_event[athlete_event["Sport"] == "Athletics"]
    offline_plot(medals_sport, medals_os, medals_france, athletics)

    end = time.time()
    print("\nThe time of execution of above program is :", end - start)


if __name__ == '__main__':
    from land_statistic import sort_france_medals, count_medals_per_sport, medals_per_os
    from load_data import create_df
    from create_plot import bar_plot, histogram_plot
    main()
else:
    import olympic_app
    olympic_app
