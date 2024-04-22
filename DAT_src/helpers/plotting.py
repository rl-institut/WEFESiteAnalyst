import plotly.io as pio
import plotly.graph_objects as go
from plotly_resampler import FigureResampler


import matplotlib.pyplot as plt
import numpy as np

import pandas as pd

pd.options.plotting.backend = "plotly"
pio.renderers.default = "browser"


def plotly_df(figure, df, subplot_col=1, subplot_row=1, legend=None, legendgroup=None, showlegend=True, mode='lines', linestyle={}, color_palette=None, stackgroup=None, markerstyle=None, opacity=1, yaxis='y',
              prefix=""):
    """
    Plot every column of a passed dataframe into the passed plotly figure.

    - legend is (optional) prefix + column_name

    :param figure: Figure to plot into
    :param df: Dataframe to plot every column of
    :param col: subplot column to add this dataframe to
    :param row: subplot row to add this dataframe to
    :param legend: Legend for the passed data. If not passed, column names are used as legend. needs to provide legend for each column of df
    :param legendgroup
    :param showlegend
    :param mode: plotly go.Scatter mode: "lines" (default), "markers", "text" or combination e.g. "markers+text"
    :param linestyle: plotly line dict
    :param color_palette: plotly color palette to use for traces of passed df
    :param markerstyle: plotly marker dict
    :param opacity: opacity of passed df traces
    :param yaxis: specify, if further y-axis is to be used ("y2") (default='y' -> primary y-axis)
    :param prefix: optional prefix to add to legend for every column
    :return:
    """

    if prefix:
        df = df.add_prefix(prefix)

    if legend:  # Check if legend is passed
        if not len(legend) == df.shape[1]:  # check if legend is passed for every column
            raise Exception('Length of passed legend list does not match number of columns in passed df')

        i = 0
        for column_name, col in df.items():
            if color_palette:
                linestyle['color'] = color_palette[i]

            figure = figure.add_trace(go.Scatter(
                x=col.index,
                y=col,
                name=legend[i],
                opacity=opacity,
                line=linestyle,
                mode=mode,
                marker=markerstyle,
                yaxis=yaxis,
                stackgroup=stackgroup,
                legendgroup=legendgroup,
                showlegend=showlegend
            ),
                row=subplot_row,
                col=subplot_col
            )
            i = i + 1
    else:  # no legend passed

        i = 0
        for column_name, col in df.items():
            if color_palette:
                linestyle['color'] = color_palette[i]

            if prefix != "":
                name = prefix+' : '.join(column_name)
            else:
                name = column_name

            figure = figure.add_trace(go.Scatter(
                x=col.index,
                y=col,
                name=name,  # use df column_name as name for trace (displayed in legend), join tuples of multi-level columns
                opacity=opacity,
                line=linestyle,
                mode=mode,
                marker=markerstyle,
                yaxis=yaxis,
                stackgroup=stackgroup,
                legendgroup=legendgroup,
                showlegend=showlegend
            ),
                row=subplot_row,
                col=subplot_col
            )

            i = i + 1

    if yaxis != 'y':    # if secondary y-axis is specified
        # Create axis objects
        # create 2nd y axis
        figure.update_layout(
            yaxis2=dict(overlaying="y", anchor="x", side="right"),
            row=subplot_row,
            col=subplot_col
        )

    return figure

def plotly_high_res_df(figure, df, subplot_col=1, subplot_row=1, legend=None, legendgroup=None, showlegend=True, mode='lines', linestyle=None, markerstyle=None, opacity=1, yaxis='y',
              prefix=''):
    """
    Plot every column of a passed dataframe into the passed plotly figure.

    - legend is (optional) prefix + column_name

    :param figure: Figure to plot into
    :param df: Dataframe to plot every column of
    :param col: subplot column to add this dataframe to
    :param row: subplot row to add this dataframe to
    :param legend: Legend for the passed data. If not passed, column names are used as legend. needs to provide legend for each column of df
    :param legendgroup
    :param showlegend
    :param mode: plotly go.Scatter mode: "lines" (default), "markers", "text" or combination e.g. "markers+text"
    :param linestyle: plotly line dict
    :param markerstyle: plotly marker dict
    :param opacity: opacity of passed df traces
    :param yaxis: specify, if further y-axis is to be used ("y2") (default='y' -> primary y-axis)
    :param prefix: optional prefix to add to legend for every column
    :return:
    """

    # Use plotly resampler for better graph performance (https://github.com/predict-idlab/plotly-resampler)
    figure = FigureResampler(figure)

    if legend:  # Check if legend is passed
        if not len(legend) == df.shape[1]:  # check if legend is passed for every column
            raise Exception('Length of passed legend list does not match number of columns in passed df')

        i = 0
        for column_name, col in df.items():
            figure = figure.add_trace(
                go.Scattergl(
                    name=prefix+legend[i],
                    opacity=opacity,
                    line=linestyle,
                    mode=mode,
                    marker=markerstyle,
                    yaxis=yaxis,
                    legendgroup=legendgroup,
                    showlegend=showlegend
                ),
                hf_x=col.index,
                hf_y=col,
                row=subplot_row,
                col=subplot_col
            )
            i = i + 1
    else:  # no legend passed
        for column_name, col in df.items():
            if prefix != "":
                name = prefix+' : '.join(column_name)
            elif isinstance(column_name, str):
                name = column_name
            else:
                name = ' : '.join(column_name)

            figure = figure.add_trace(go.Scattergl(
                name=name,  # use df column_name as name for trace (displayed in legend)
                opacity=opacity,
                line=linestyle,
                mode=mode,
                marker=markerstyle,
                yaxis=yaxis,
                legendgroup=legendgroup,
                showlegend=showlegend
            ),
                hf_x=col.index,
                hf_y=col,
                row=subplot_row,
                col=subplot_col
            )

    if yaxis != 'y':    # if secondary y-axis is specified
        # Create axis objects
        # create 2nd y axis
        figure.update_layout(
            yaxis2=dict(overlaying="y", anchor="x", side="right"),
            row=subplot_row,
            col=subplot_col
        )

    return figure

def plot_timeseries_segments(figure, df, column, subplot_col=1, subplot_row=1, start_date='1-1', end_date='12-31', group_dur='day', mode='lines', linestyle=None, markerstyle=None, opacity=1):
    """

    :param df: data to plot
    :param column: column of passed dataframe to plot
    :param start_date:
    :param end_date:
    :param group_dur: duration of segments to be plotted
    :param show_legend:
    :return:
    """
    # create copy to avoid pointer horseshit -> otherwise input df is manipulated
    data = df.copy()
    if group_dur == 'day':
        # Create time column with hour and minute of day (HH:mm) to pivot series into df
        data['time'] = data.index.strftime('%H:%M')
        data.set_index(data.index.date, inplace=True)

        # Create 2D df from series where rows are days and columns are datapoints of the according rows day
        data_pivot = data.pivot_table(columns='time', values=column).T

        # Select days to plot
        mask = (data_pivot.index > pd.to_datetime('2019-' + start_date)) & (
                data_pivot.index <= pd.to_datetime('2019-' + end_date))
        data_pivot = data_pivot.loc[mask]

    elif group_dur == 'week':
        # Create time column with day (short), hour and minute (ddd:HH:mm) to pivot series into df
        data['time'] = data.index.strftime('%a:%H:%M')
        data.set_index(data.index.strftime('%U'), inplace=True)

        # Create 2D df from series where rows are days and columns are datapoints of the according rows day
        data_pivot = data.pivot(columns='time', values=column)

        # Select weeks to plot
        mask = (data_pivot.index > pd.to_datetime('2019-' + start_date)).strftime('%U') & (
                data_pivot.index <= pd.to_datetime('2019-' + end_date).strftime('%U'))
        data_pivot = data_pivot.loc[mask]

    # Select days to plot
    # mask = (data.index > pd.to_datetime('2019-'+start_date)) & (data.index <= pd.to_datetime('2019-'+end_date))
    # data = data.loc[mask]

    # Plot segments

    for column_name, col in data_pivot.T.items():
        figure = figure.add_trace(go.Scatter(
            x=col.index,
            y=col,
            name=column_name,  # use df column_name as name for trace (displayed in legend)
            opacity=opacity,
            line=linestyle,
            mode=mode,
            marker=markerstyle,
        ),
            row=subplot_row,
            col=subplot_col
        )

    return figure

def plot_timeseries_heatmaps(df, column, group_dur='day', wide=False, zmin=None, zmax=None):
    """
    Takes Dataframe and column name of column to be segmented and pivoted.
    Plot pivoted data and return it.
    :param df: Dataframe of which column is to be plotted as heatmap
    :param column: Column of the dataframe to be segmented and plotted as heatmap
    :param group_dur: Duration of segments in which timeseries will be split and plotted (day or week)
    :param wide: if True, segmented data is pivoted -> segments on y-axis and year on x-axis
    :param zmin: lower limit of color scale -> default None -> lower limit is min of data
    :param zmax: upper limit of color scale -> default None -> upper limit is max of data
    :return: heatmap figure
    """

    # create copy to avoid pointer horseshit -> otherwise input df is manipulated
    data = df.copy()
    data.replace(np.inf, np.nan, inplace=True)  # replace infinite values with NaN

    # Check if data is boolean -> turn into 0 and 1 to make plottable
    if data[column].dtype == 'bool':
        data.replace([True, False], [1, 0], inplace=True)

    if group_dur == 'day':
        # Create time column with hour and minute of day (HH:mm) to pivot series into df
        data['time'] = data.index.strftime('%H:%M')
        data.set_index(data.index.date, inplace=True)

        # Create 2D df from series where rows are days and columns are datapoints of the according rows day
        data_pivot = data.pivot(columns='time', values=column)

    elif group_dur == 'week':
        # Create time column with day (short), hour and minute (ddd:HH:mm) to pivot series into df
        data['time'] = data.index.strftime('%a:%H:%M')

        data.set_index(data.index.strftime('%U'), inplace=True)

        # Create 2D df from series where rows are days and columns are datapoints of the according rows day
        data_pivot = data.pivot(columns='time', values=column)
        print(data_pivot.head())

    if wide:
        data_pivot = data_pivot.T  # transpose to plot heatmap wide

    # Create heatmap figure
    fig = go.Figure(
        data=go.Heatmap(
            z = data_pivot.values.tolist(),
            x = data_pivot.columns.tolist(),
            y = data_pivot.index.tolist(),
            zmin=zmin, zmax=zmax
        )
    )

    return fig