# script for different plots
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly_express as px
import plotly


def bar_plot(df, x_value, y_value, an_title, y_name, color_name, html_path):  # html_path ändrat inte vs code
    fig = px.bar(df, x=x_value, y=y_value, barmode='group', color=color_name,
                 labels={"variable": "", "value": y_name}, title=an_title)
    plotly.offline.plot(fig, filename=html_path)


def histogram_plot(df, x_value, y_value, an_title, y_name, color_name, html_path):
    fig = px.histogram(df, x=x_value, y=y_value, barmode='group', color=color_name,
                       labels={"variable": "", "value": y_name}, title=an_title)
    fig.update_xaxes(type='category')
    plotly.offline.plot(fig, filename=html_path)


def horizontal_bar_plot(df, x_value, y_value, an_title, y_name, color_name, html_path, reversed_y=False):
    fig = px.bar(df, x=x_value, y=y_value, barmode='stack', orientation='h', color=color_name,
                 labels={"variable": "", "value": y_name}, title=an_title)
    if reversed_y:
        fig.update_layout(yaxis=dict(autorange="reversed"))
    plotly.offline.plot(fig, filename=html_path)
