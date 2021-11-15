# här skriver i ett utkast innan in i main.py

import pandas as pd
from dash import dcc, html
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input


from land_statistic import anonymous, age_per_os, sort_france_medals, count_medals_per_sport, medals_per_os

from create_plot import histogram_plot, bar_plot, pie_chart, horizontal_bar_plot, bar_plot_dash, histogram_plot_dash
#from sort_data import athletes_by_sex_ratio, athletes_by_sex_ratio_over_time, top_10_nations_medals
import os

#path = r"Data/"

path = r"C:\Users\trull\PycharmProjects\ITHS_Python_utb\databehandling\Projekt_OS\Data"
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

dff_dict = dict(df1 = "age_os", df2 = "man_france", df3 = "female_france")

dff_options_dropdown = [{"label": symbol, "value": name}
                          for symbol, name in dff_dict.items()]

app = dash.Dash(__name__)   # skapar server

app.layout = dbc.Container([
    html.H1("Test"),
    dcc.Dropdown(id = "os-dropdown", options=dff_options_dropdown, value="age_os"),
    dcc.Graph(id = "graph"),
    dcc.Store(id = "local-store")
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


if __name__ == '__main__':
    app.run_server(debug=True)
