from ucast.io import read_tsv as read

from bokeh.models import Range1d, Column
import pandas as pd
from bokeh.plotting import figure, output_file, show

def bokeh_static(link, input):
    # All the relevant variables to be plotted.
    sites  = ["ALMA", "APEX", "GLT", "JCMT", "KP",
              "LMT", "PDB", "PV", "SMA", "SMT", "SPT"]
    colors = ['navy', 'red', 'blue', 'green', 'pink', 'purple',
              'violet', 'darkcyan', 'royalblue', 'seagreen', 'gold']
    # Read files
    dfs = [read(f'{link}/{s}/{input}') for s in sites]

    output_file("forecast.html")
    plot_list = [create_plot(var, dfs, colors, sites)
                 for var in "tau,pwv,lwp,iwp".split(",")]
    p = Column(*plot_list)
    show(p)

def create_plot(var, dfs, colors, sites):
    p2 = figure(title=var, plot_width=1600, plot_height=500, x_axis_type="datetime",
                tools="pan,box_zoom,box_select,lasso_select,undo,wheel_zoom,redo,reset,save".split())
    if var == "tau":
        p2.y_range = Range1d(0, 1)
    elif var == "pwv":
        p2.y_range = Range1d(0, 15)
    elif var == "lwp":
        p2.y_range = Range1d(0, 1)
    elif var == "iwp":
        p2.y_range = Range1d(0, 2)
    for i in range(11):
        p2.line(dfs[i]['date'], dfs[i][var], color=colors[i],
                alpha=0.5, legend_label=sites[i])
    # Enable line hide toggle
    p2.legend.location = "top_left"
    p2.legend.click_policy = "hide"
    return p2
