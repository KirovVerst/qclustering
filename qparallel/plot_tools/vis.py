__author__ = 'Maria Khodorchenko'

import plotly.graph_objs as go
from plotly.offline import plot
from plotly.plotly import image
import numpy as np
import pandas as pd
from scripts.config import RESULTS_DIR_PATH

path_to_figure = 'Figures\\'


def _parse_in(files):
    data = pd.read_csv(RESULTS_DIR_PATH + "\\" + files[0])
    if len(files) > 1:
        for i in range(1, len(files)):
            data_tmp = pd.read_csv(RESULTS_DIR_PATH + "\\" + files[i])
            data = data.append(data_tmp)
    return data


def plot_speedup(in_files):
    data = _parse_in(in_files)
    data["total_time"] = pd.to_datetime(data["total_time"])
    data["time"] = data["total_time"].dt.microsecond + (1000000 * data["total_time"].dt.second) + (60000000 * data["total_time"].dt.minute)
    ls_names = list(data["algorithm_name"].unique())
    print(ls_names)
    for i in ls_names:
        cpu = []
        seconds = []
        arr_tmp = data.query('algorithm_name == @i').copy()
        arr_tmp = arr_tmp.groupby('cpu_count')['time'].mean()
        print(arr_tmp)
        cpu = list(arr_tmp.index.values)
        for j in cpu:
            seconds += [arr_tmp[j]]
        print(cpu, seconds)
        seconds_sequential = seconds[0]
        for k in range(len(seconds)):
            seconds[k] = seconds_sequential / seconds[k]
        print(cpu, seconds)
        trace = go.Scatter(
            x=np.array(cpu),
            y=np.array(seconds),
            mode='lines+markers',
            line=dict(
                color=('rgb(205, 12, 24)')
            )
        )
        layout = dict(title=i,
                      xaxis=dict(title='Cpu count'),
                      yaxis=dict(title='Speedup')
                      )
        plot_data = [trace]
        fig = go.Figure(data=plot_data, layout=layout)
        image.save_as(fig, filename=path_to_figure + i + '.jpeg')
