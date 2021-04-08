from bokeh.models import Range1d, Column
from bokeh.plotting import figure, output_file, show, save

from bokeh.palettes import Category10_9 as palette
import itertools

colors = itertools.cycle(palette)
tools  = "pan,box_zoom,wheel_zoom,box_select,undo,redo,reset,save".split()

def static_vis(dfs, sites, fname, browser):
    output_file(fname+'.html')

    plots = []
    for var in "tau,pwv,lwp,iwp".split(","):
        if len(plots) == 0:
            kwargs = {}
        else:
            kwargs = {'x_range':plots[0].x_range}
        plots.append(create_plot(var, dfs, sites, **kwargs))

    c = Column(*plots)
    if browser:
        show(c)
    else:
        print(f'Save dashboard to "{fname}.html"')
        save(c)


def create_plot(var, dfs, sites, **kwargs):
    p = figure(title=var, x_axis_type="datetime",
               plot_width=1600,
               plot_height=500 if var == "tau" else 300,
               tools=tools,
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
               line_width=2,
               color=c, legend_label=sites[i],
               alpha=0.75, muted_alpha=0.25)

    p.legend.location = "top_right"
    p.legend.click_policy = "mute"

    return p
