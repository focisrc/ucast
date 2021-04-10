from bokeh.models import Range1d, Column
from bokeh.plotting import figure, output_file, show, save

from bokeh.palettes import Category10_9 as palette
import itertools

colors = itertools.cycle(palette)
tools  = "pan,box_zoom,wheel_zoom,box_select,undo,redo,reset,save"

vars   = [   'tau',        'Ts',     'RHs',    'pwv',       'lwp',                'iwp'              ]
labels = [r'$\tau_{255}$', 'T [C°]', 'RH [%]', 'pwv [mm]', r'lwp [kg m$^{-2}$]', r'iwp [kg m$^{-2}$]']
ylims  = [   (0, 1.1),     (-55, 22), (0, 110), (0, 16.5),   (0, 2.2),             (0., 2.2)         ]


def static_vis(dfs, sites, fname, browser):

    output_file(fname+'.html')

    plots = []
    for i, var in enumerate(vars):
        if i == 0:
            kwargs = {}
        else:
            kwargs = {'x_range':plots[0].x_range}

        p = figure(title=labels[i],
                   x_axis_type="datetime",
                   plot_width=1600,
                   plot_height=500 if i == 0 else 300,
                   tools=tools,
                   **kwargs)

        for j, (df, c) in enumerate(zip(dfs, colors)):
            p.line(df['date'], df[var].fillna(0),
                   line_width=2,
                   color=c, legend_label=sites[j],
                   alpha=0.75, muted_alpha=0.25)

        p.y_range = Range1d(*ylims[i])
        p.legend.location     = "top_right"
        p.legend.click_policy = "mute"

        plots.append(p)

    c = Column(*plots)
    if browser:
        show(c)
    else:
        print(f'Save dashboard to "{fname}.html"')
        save(c)
