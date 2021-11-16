# här skriver i ett utkast innan in i main.py

import pandas as pd
from dash import dcc, html
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input


from land_statistic import anonymous, age_per_os, sort_france_medals, count_medals_per_sport, medals_per_os
from sort_data import athletes_by_sex_ratio, top_10_nations_medals, athletes_by_sex_ratio_over_time

from create_plot import histogram_plot, bar_plot, pie_chart_dash, horizontal_bar_plot_dash, bar_plot_dash, histogram_plot_dash
#from sort_data import athletes_by_sex_ratio, athletes_by_sex_ratio_over_time, top_10_nations_medals
import os

path = r"/Users/leolassarade/GitHub-project/Databehandling-OS-projekt_Leo_Marie/Data/"

#path = r"C:\Users\trull\PycharmProjects\ITHS_Python_utb\databehandling\Projekt_OS\Data"
os.chdir(path)


def create_df():
    """ read files with tail .csv from a specified folder and create dataframes
    file extensions typ csv
    :return: dataframes
    """
    file_list = []
    for file in sorted(os.listdir()):
        if file.endswith(".csv"):
            file_path = f"{path}/{file}"
            file_list.append(file_path)
    athlete_event = pd.read_csv(file_list[0])
    noc_regions = pd.read_csv(file_list[1])
    return athlete_event, noc_regions

athlete_event, noc_regions = create_df()
athlete_event = anonymous(athlete_event)
medals_france = sort_france_medals(athlete_event)
medals_sport = count_medals_per_sport(medals_france)
medals_os = medals_per_os(medals_france)
age_os = age_per_os(medals_france)
man_france = medals_sport[medals_sport["Amount M"] > 0]
female_france = medals_sport[medals_sport["Amount F"] > 0]
sex_ratio = athletes_by_sex_ratio(athlete_event)
all_time_top_10 = top_10_nations_medals(athlete_event)
all_time_top_10_summer = top_10_nations_medals(athlete_event, "Summer")
all_time_top_10_winter = top_10_nations_medals(athlete_event, "Winter")
sex_ratio_over_years = athletes_by_sex_ratio_over_time(athlete_event)
sex_ratio_over_years_summer = athletes_by_sex_ratio_over_time(athlete_event, "Summer")
sex_ratio_over_years_winter = athletes_by_sex_ratio_over_time(athlete_event, "Winter")



stylesheets = [dbc.themes.MATERIA]

dff_dict = dict(df1 = "age_os", df2 = "man_france", df3 = "female_france")
dff_dict_set_2 = dict(df4 = "sex_ratio", df5 = "all_time_top_10", df6 = "sex_ratio_over_years")

dff_options_dropdown = [{"label": symbol, "value": name}
                          for symbol, name in dff_dict.items()]

dff_options_dropdown_all = [{"label": symbol, "value": name}
                          for symbol, name in dff_dict_set_2.items()]

season_options = [{"label": option , "value": option}
                for option in ["Summer", "Winter", "all"]]

app = dash.Dash(__name__, external_stylesheets=stylesheets,
                meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")])

app.layout = dbc.Container([
    dbc.Row([
        html.H1("Frankrike"),
        dcc.Dropdown(id = "os-dropdown", options=dff_options_dropdown, value="age_os"),
        dcc.Graph(id = "graph"),
        dcc.Store(id = "local-store")
    ]),

    
    dbc.Row([

        html.H2("All nations"),

        dbc.Col([
            dcc.Dropdown(id = "leo-dropdown", options=dff_options_dropdown_all, value="sex_ratio"),
        ], width=6, lg=3), #xs="12", sm="12", md="12", lg='4', xl="3"),

        dbc.Col([
            dbc.Card([
            dcc.RadioItems(id='season_radio', className="m-1",
                                options=season_options,
                                value='all'
                            ),
            ])
        ], width=6, lg=3)  #xs="12", sm="12", md="12", lg='4', xl="3")      
    ]),

    dbc.Row([
    dcc.Graph(id = "graph2"),
    dcc.Store(id = "local-store2")
    ])
])


@app.callback(
    Output('graph', 'figure'),
    Input("os-dropdown", 'value'),
)
def update_graph_1(data):
    if data == "age_os":
        dff = age_os
        figure = histogram_plot_dash(dff, "Age", "Amount", "Amount of medals per age for France in OS", "Amount", None)
    elif data == "man_france":
        dff = man_france
        figure = bar_plot_dash(dff, "Sport", "Amount M", "Male medal per sport, France in OS", "Amount", "Medal")
    elif data == "female_france":
        dff = female_france
        figure = bar_plot_dash(dff, "Sport", "Amount F", "Female medal per sport, France in OS", "Amount", "Medal")
    return figure

@app.callback(
    Output('graph2', 'figure'),
    Input("leo-dropdown", 'value'),
    Input("season_radio", 'value')
)
def update_graph_2(data, season):
    if data == "sex_ratio":
        dff = sex_ratio
        figure =  pie_chart_dash(dff, "Count", "Sex", "Historical ratio males-females")
    elif data == "all_time_top_10":
        if season == "all":
            dff = all_time_top_10
            figure = bar_plot_dash(dff, "Nation", "Total", "Top 10 Nations, total medals, winter-summer olympics", "count medals", None)
        elif season == "Summer":
            dff = all_time_top_10_summer
            figure = bar_plot_dash(dff, "Nation", "Total", "Top 10 Nations, total medals, summer olympics", "count medals", None)
        elif season == "Winter":
            dff = all_time_top_10_winter
            figure = bar_plot_dash(dff, "Nation", "Total", "Top 10 Nations, total medals, winter olympics", "count medals", None)
    elif data == "sex_ratio_over_years":
        if season == "all":
            dff = sex_ratio_over_years
            figure = horizontal_bar_plot_dash(dff, ['Share M','Share F'], 'Year', "Historical repartition of athletes by gender under all olympics", "Share", None, True)
        elif season == "Summer":
            dff = sex_ratio_over_years_summer
            figure = horizontal_bar_plot_dash(dff, ['Share M','Share F'], 'Year', "Historical repartition of athletes by gender under summer olympics", "Share", None, True)
        elif season =="Winter":
            dff = sex_ratio_over_years_winter
            figure = horizontal_bar_plot_dash(dff, ['Share M','Share F'], 'Year', "Historical repartition of athletes by gender under winter olympics", "Share", None, True)



    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
