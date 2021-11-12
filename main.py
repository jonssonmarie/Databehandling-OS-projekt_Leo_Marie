import time

from land_statistic import anonymous, age_per_os, sort_france_medals, count_medals_per_sport, medals_per_os
from load_data import create_df
from create_plot import histogram_plot, bar_plot, pie_chart, horizontal_bar_plot
from sort_data import possible_medals, age_proofed_dataframe, age_stats, athletes_by_sex_ratio 
from sort_data import athletes_by_sex_ratio_over_time, top_10_nations_medals


def call_plot(df1, df2, df3, df4, df5, df6, df7, df8,df9, df10, df11, df12):  # tillfällig att det är df1, df2 ... df6
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
    
    pie_chart(df7, "Count", "Sex", "Historical ratio males-females",
             "../Visualizations/sex_pie.html")

    bar_plot(df8, "Nation", "Total", "Top 10 Nations, total medals, winter-summer olympics", "count medals", None, 
            "../Visualizations/All_nations_all_seasons_medal_top10" )
    
    bar_plot(df9, "Nation", "Total", "Top 10 Nations, total medals, summer olympics", "count medals", None, 
            "../Visualizations/All_nations_summer_medal_top10" )
        
    bar_plot(df10, "Nation", "Total", "Top 10 Nations, total medals, winter olympics", "count medals", None, 
            "../Visualizations/All_nations_winter_medal_top10" )

    horizontal_bar_plot(df11, ['Share M','Share F'], 'Year', "Historical repartition of athletes by gender under winter olympics", "Share", None, 
            "../Visualizations/Athletes_by_gender_winter_years.html", True)

    horizontal_bar_plot(df12, ['Share M','Share F'], 'Year', "Historical repartition of athletes by gender under summer olympics", "Share", None,
     "../Visualizations/Athletes_by_gender_summer_years.html", True)







def main():
    start = time.time()
    athlete_event, noc_regions = create_df()
    #Leos variabler
    sex_ratio = athletes_by_sex_ratio(athlete_event)
    all_time_top_10 = top_10_nations_medals(athlete_event)
    winter_top_10 = top_10_nations_medals(athlete_event, "Winter")
    summer_top_10 = top_10_nations_medals(athlete_event, "Summer")
    sex_years_winter = athletes_by_sex_ratio_over_time(athlete_event, "Winter")
    sex_years_summer = athletes_by_sex_ratio_over_time(athlete_event, "Summer")


    # Note: anonymous name                                  # ändrat obs to Note
    athlete_event = anonymous(athlete_event)
    medals_france = sort_france_medals(athlete_event)
    medals_sport = count_medals_per_sport(medals_france)   # ändrat
    medals_os = medals_per_os(medals_france)
    age_os = age_per_os(medals_france)
    man_france = medals_sport[medals_sport["Amount M"] > 0]   # ändrat
    female_france = medals_sport[medals_sport["Amount F"] > 0]    # ändrat
    call_plot(age_os, medals_sport, medals_os, medals_france, man_france, female_france, sex_ratio, all_time_top_10, winter_top_10, summer_top_10,sex_years_winter, sex_years_summer)    # ändrat

    end = time.time()
    print("\nThe time of execution of above program is :", end - start)


if __name__ == '__main__':
    main()
