from dash import dcc, html
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from land_statistic import sort_france_medals, count_medals_per_sport, medals_per_os
from sort_data import athletes_by_sex_ratio, top_10_nations_medals, athletes_by_sex_ratio_over_time
from create_plot import pie_chart_dash, horizontal_bar_plot_dash, bar_plot_dash, histogram_plot_dash
from load_data import create_df

athlete_event, noc_regions = create_df()
medals_france = sort_france_medals(athlete_event)
medals_sport = count_medals_per_sport(medals_france)
medals_os = medals_per_os(medals_france)
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

dff_dict = dict(Age="age_os", Men="man_france", Women="female_france")
dff_dict_set_2 = dict(Overall_gender_ratio = "sex_ratio", Medals = "all_time_top_10", Gender_over_time = "sex_ratio_over_years")

dff_options_dropdown = [{"label": symbol, "value": name}
                          for symbol, name in dff_dict.items()]

dff_options_dropdown_all = [{"label": symbol, "value": name}
                          for symbol, name in dff_dict_set_2.items()]

season_options = [{"label": option , "value": option}
                for option in ["Summer", "Winter", "all"]]

app = dash.Dash(__name__, external_stylesheets=stylesheets,
                meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")])

server = app.server

app.layout = dbc.Container([
    dbc.Row([
        html.H1("Everything you ever wanted to know about Olympic Games"),
    ], style = {"margin-block-start": "1em", "margin-block-end" : "2em"}),

    dbc.Row([
        html.H2("France"),
        
        dbc.Col([
            dcc.Graph(id = "graph"),
            dcc.Store(id = "local-store")
        ], width=6, lg=10),

        dbc.Col([
            dbc.Card([
                html.H3("Figure", style={"font-size" : "1.45rem", "padding" : "0.4em"}),
                dcc.Dropdown(id = "os-dropdown", options=dff_options_dropdown, value="age_os"),
            ])
        ], width=6, lg=2)
    ]),

    
    dbc.Row([

        html.H2("All nations"),

        dbc.Col([
            dcc.Graph(id = "graph2"),
            dcc.Store(id = "local-store2")
        ], width=6, lg=10),

        dbc.Col([
            dbc.Card([
                html.H3("Figure", style={"font-size" : "1.45rem", "padding" : "0.4em"}),
                dcc.Dropdown(id = "leo-dropdown", options=dff_options_dropdown_all, value="sex_ratio")
            ], style={"margin-bottom": "1em"}),
            dbc.Card([
                html.H3("Options", style={"font-size" : "1.45rem", "padding" : "0.4em"}),
                dcc.RadioItems(id='season_radio', className="m-1",
                                    options=season_options,
                                    value='all',
                                    labelStyle={'margin-right' : '0.5em', 'display' : 'block'},
                                    inputStyle={'margin' : '0.2em'}
                                )
            ]),
        ], width=6, lg=2)  
    ]),

])


@app.callback(
    Output('graph', 'figure'),
    Input("os-dropdown", 'value'),
)
def update_graph_1(data):
    """
    :param data: DataFrames for France in the Olympics
    :return: plot to heroku
    """
    if data == "age_os":
        dff = medals_france     # age_os
        figure = histogram_plot_dash(dff, "Age", "Age", "Amount of medals per age for France in OS", "Amount", None)
    elif data == "man_france":
        dff = man_france
        figure = bar_plot_dash(dff, "Sport", "Amount M", "Medal per sport for Men, France in OS", "Amount", "Medal")
    elif data == "female_france":
        dff = female_france
        figure = bar_plot_dash(dff, "Sport", "Amount F", "Medal per sport for Women, France in OS", "Amount", "Medal")
    return figure


@app.callback(
    Output('graph2', 'figure'),
    Input("leo-dropdown", 'value'),
    Input("season_radio", 'value')
)
def update_graph_2(data, season):
    """
    :param data: DataFrames for alla nations in the olympics
    :param season: winter, summer or all
    :return: a plot to heroku
    """
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
