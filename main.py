import time

from land_statistic import  sort_france_medals, count_medals_per_sport, medals_per_os
from load_data import create_df
from create_plot import bar_plot, histogram_plot, bar_plot_dash, pie_chart_dash, horizontal_bar_plot_dash
#from sort_data import athletes_by_sex_ratio, athletes_by_sex_ratio_over_time, top_10_nations_medals


# call_plot skall bort senare när olympic_app är klar
def call_plot(df7, df8,df9, df10, df11, df12):  # tillfällig att det är df1, df2 ... df6
    pie_chart_dash(df7, "Count", "Sex", "Historical ratio males-females")

    bar_plot_dash(df8, "Nation", "Total", "Top 10 Nations, total medals, winter-summer olympics", "count medals", None)
    
    bar_plot_dash(df9, "Nation", "Total", "Top 10 Nations, total medals, summer olympics", "count medals", None)
        
    bar_plot_dash(df10, "Nation", "Total", "Top 10 Nations, total medals, winter olympics", "count medals", None)

    horizontal_bar_plot_dash(df11, ['Share M','Share F'], 'Year', "Historical repartition of athletes by gender under winter olympics", "Share", None, True)

    horizontal_bar_plot_dash(df12, ['Share M','Share F'], 'Year', "Historical repartition of athletes by gender under summer olympics", "Share", None, True)



def offline_plot(df1, df2, df3, df4):
    bar_plot(df1, "Sport", "Amount", "Amount of medals per sport for France in OS", "Amount", "Medal",
             r"..\Visualizations\France_medals_per_sport.html")
    bar_plot(df2, "Game", "Amount", "Amount of medals per game for France in OS", "Amount", "Medal",
             r"..\Visualizations\France_amount_of_medals_per_game.html")
    bar_plot(df3, "Sport", ["Sex"], "Amount of medals per sex in OS", "Sex", "Medal",
             r"..\Visualizations\France_summery_of_all_medals_per_sex.html")
    histogram_plot(df4, "Age", "Age", "Amount of medals for Athletics", "Amount", None,
                   r"..\Visualizations\age_summery_per_athletics.html")


def main():
    start = time.time()
    athlete_event, noc_regions = create_df()

    # Leos variabler -ta bort när app är klar
    """sex_ratio = athletes_by_sex_ratio(athlete_event)
    all_time_top_10 = top_10_nations_medals(athlete_event)
    winter_top_10 = top_10_nations_medals(athlete_event, "Winter")
    summer_top_10 = top_10_nations_medals(athlete_event, "Summer")
    sex_years_winter = athletes_by_sex_ratio_over_time(athlete_event, "Winter")
    sex_years_summer = athletes_by_sex_ratio_over_time(athlete_event, "Summer")"""

 
    # Note: anonymous name
    medals_france = sort_france_medals(athlete_event)
    medals_sport = count_medals_per_sport(medals_france)
    medals_os = medals_per_os(medals_france)
    athletics = athlete_event[athlete_event["Sport"] == "Athletics"]
    offline_plot(medals_sport, medals_os, medals_france, athletics)

    end = time.time()
    print("\nThe time of execution of above program is :", end - start)

    end = time.time()
    print("\nThe time of execution of above program is :", end - start)


if __name__ == '__main__':
    main()
 