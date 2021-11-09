import time
from land_statistic import anonymous, age_per_os, sort_france_medals, count_medals_per_sport, medals_per_os
from load_data import create_df
from create_plot import histogram_plot, bar_plot


def call_plot(df1, df2, df3):
    histogram_plot(df1, "Age", "Amount", "Amount of medals per age for France in OS", "Amount", None,
                   r"..\Visualizations\Amount_medals_per_age.html")
    bar_plot(df2, "Sport", "Amount", "Amount of medals per age for France in OS", "Amount", "Medal",
             r"..\Visualizations\Medals_per_sport.html")

    bar_plot(df3, "Game", "Amount", "Amount of medals per age for France in OS", "Amount", "Medal",
             r"..\Visualizations\Medals_os.html")


def main():
    start = time.time()
    athlete_event, noc_regions = create_df()

    # obs: anonymous name after here
    athlete_event = anonymous(athlete_event)
    medals_france = sort_france_medals(athlete_event)
    medals_sport = (count_medals_per_sport(medals_france))
    medals_os = medals_per_os(medals_france)
    age_os = age_per_os(medals_france)
    call_plot(age_os, medals_sport, medals_os)

    end = time.time()
    print("\nThe time of execution of above program is :", end - start)


if __name__ == '__main__':
    main()
    