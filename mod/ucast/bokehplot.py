from bokeh.models import Range1d, Column
from bokeh.plotting import figure, output_file, show

def bokeh_static(dfs, sites, fname):
    colors = ['navy', 'red', 'blue', 'green', 'pink', 'purple',
              'violet', 'darkcyan', 'royalblue', 'seagreen', 'gold']

    output_file(fname+'.html')
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
        p2.line(dfs[i]['date'], dfs[i][var].fillna(0),
                color=colors[i], alpha=0.5, legend_label=sites[i])
    # Enable line hide toggle
    p2.legend.location = "top_left"
    p2.legend.click_policy = "hide"
    return p2
