import time

from land_statistic import anonymous, age_per_os, sort_france_medals, count_medals_per_sport, medals_per_os
from load_data import create_df
from create_plot import histogram_plot, bar_plot
from sort_data import possible_medal, age_proofed_dataframe, age_stats, athletes_by_sex_ratio 
from sort_data import athletes_by_sex_ratio_over_time, medal_sets


def call_plot(df1, df2, df3, df4, df5, df6):  # tillfällig att det är df1, df2 ... df6
    histogram_plot(df1, "Age", "Amount", "Amount of medals per age for France in OS", "Amount", None,
                   r"..\Visualizations\France_amount_medals_per_age.html")

    bar_plot(df2, "Sport", "Amount", "Amount of medals per sport for France in OS", "Amount", "Medal",
             r"..\Visualizations\France_medals_per_sport.html")

    bar_plot(df3, "Game", "Amount", "Amount of medals per game for France in OS", "Amount", "Medal",
             r"..\Visualizations\France_amount_of_medals_per_game.html")

    bar_plot(df4, "Sport", ["Sex"], "Amount of medals per sex in OS", "Sex", "Medal",
             r"..\Visualizations\France_summer_of_all_medals_per_sex.html")

    bar_plot(df5,"Sport", ["Amount M"], "Male medal per sport, France in OS", "Amount", "Medal",
             r"..\Visualizations\France_medals_per_man_sport.html")

    bar_plot(df6, "Sport", ["Amount F"], "Female medal per sport, France in OS", "Amount", "Medal",
             r"..\Visualizations\France_medals_per_female_sport.html")


def main():
    start = time.time()
    athlete_event, noc_regions = create_df()



    # Note: anonymous name                                  # ändrat obs to Note
    athlete_event = anonymous(athlete_event)
    medals_france = sort_france_medals(athlete_event)
    medals_sport = count_medals_per_sport(medals_france)   # ändrat
    medals_os = medals_per_os(medals_france)
    age_os = age_per_os(medals_france)
    man_france = medals_sport[medals_sport["Amount M"] > 0]   # ändrat
    female_france = medals_sport[medals_sport["Amount F"] > 0]    # ändrat
    call_plot(age_os, medals_sport, medals_os, medals_france, man_france, female_france)    # ändrat

    end = time.time()
    print("\nThe time of execution of above program is :", end - start)


if __name__ == '__main__':
    main()
