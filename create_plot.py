# script for different plots
import seaborn as sns
import plotly_express as px
import plotly


def bar_plot(df, x_value, y_value, an_title, y_name, color_name, file_path):
    fig = px.bar(df, x=x_value, y=y_value, barmode='group', color=color_name,
                 labels={"variable": "", "value": y_name}, title=an_title)
    plotly.offline.plot(fig, filename=file_path)


def histogram_plot(df, x_value, y_value, an_title, y_name, color_name, file_path):
    fig = px.histogram(df, x=x_value, y=y_value, barmode='group', color=color_name,
                       labels={"variable": "", "value": y_name}, title=an_title)
    fig.update_xaxes(type='category')
    plotly.offline.plot(fig, filename=file_path)
