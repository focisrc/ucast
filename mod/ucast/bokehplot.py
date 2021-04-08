from bokeh.models import Range1d, Column
from bokeh.plotting import figure, output_file, show

from bokeh.palettes import Category10_10 as palette
import itertools

colors = itertools.cycle(palette)

def bokeh_static(dfs, sites, fname):
    output_file(fname+'.html')

    plots = []
    for var in "tau,pwv,lwp,iwp".split(","):
        if len(plots) == 0:
            kwargs = {}
        else:
            kwargs = {'x_range':plots[0].x_range}
        plots.append(create_plot(var, dfs, sites, **kwargs))

    show(Column(*plots))

def create_plot(var, dfs, sites, **kwargs):
    p = figure(title=var, plot_width=1600, plot_height=500, x_axis_type="datetime",
               tools="pan,box_zoom,box_select,lasso_select,undo,wheel_zoom,redo,reset,save".split(),
               **kwargs)
    if var == "tau":
        p.y_range = Range1d(0, 1)
    elif var == "pwv":
        p.y_range = Range1d(0, 15)
    elif var == "lwp":
        p.y_range = Range1d(0, 2)
    elif var == "iwp":
        p.y_range = Range1d(0, 2)
    for i, (df, c) in enumerate(zip(dfs, colors)):
        p.line(df['date'], df[var].fillna(0),
               color=c, alpha=0.5, legend_label=sites[i])
    # Enable line hide toggle
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    return p
