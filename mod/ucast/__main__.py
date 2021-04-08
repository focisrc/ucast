# Copyright (C) 2020 Chi-kwan Chan
# Copyright (C) 2020 Steward Observatory
#
# This file is part of `ucast`.
#
# `Ucast` is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# `Ucast` is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with `ucast`.  If not, see <http://www.gnu.org/licenses/>.

from os   import path
from glob import glob

import requests
import click

import ucast as uc
from ucast.utils import forced_symlink  as symlink
from ucast.utils import ucast_dataframe as mkdf
from ucast.utils import forecasts
from ucast.io    import dt_fmt, save, read
from ucast.plot  import plot_latest, plot_sites
from ucast.bokehplot import bokeh_static


@click.group()
def ucast():
    """µcast: micro-weather forecasting for astronomy"""


@ucast.command()
@click.argument("site")
@click.option("--lag",  default=5.25, help="Lag hour for weather forecast.")
@click.option("--data", default='.',  help="Data archive directory.")
@click.option("--link", default='.',  help="Directory contains links to the latest data.")
def mktab(lag, site, data, link, plot):
    """Pull weather data for telescope SITE, process with `am`, and make tables"""

    site         = getattr(uc.site, site)
    latest_cycle = uc.gfs.latest_cycle(lag=lag)

    for hr_ago in range(0, 48+1, 6):
        cycle   = uc.gfs.relative_cycle(latest_cycle, hr_ago)
        outfile = path.join(data, cycle.strftime(dt_fmt))

        if path.isfile(outfile) and len(open(outfile).readlines()) == len(forecasts)+1:
            print(f'Skip "{outfile}"; ', end='')
        else:
            print(f'Creating "{outfile}" ...', end='')
            save(outfile, mkdf(site, cycle))
            print(" DONE; ", end='')

        if link is None:
            print()
        else:
            target = path.join(link,
                "latest" if hr_ago == 0 else f"latest-{hr_ago:02d}")
            print(f'link as "{target}"')
            symlink(outfile, target)


@ucast.command()
@click.argument("sites", nargs=-1)
@click.option("--out", default='ucast', help="Output file name (no extension)")
@click.option("--plot", default='latest', help="File name of the plot; inside `link` if '/' is not in the name.")
def mkplot(sites, out, plot):
    """Read weather tables from the directories SITES and create a summary plot"""

    dfs = []
    for hr_ago in range(0, 48+1, 6):
        target = path.join(link,
            "latest" if hr_ago == 0 else f"latest-{hr_ago:02d}")
        dfs.append(read(target))

    if link is not None and plot is not None:
        title = f'{site.name}: ({site.lat}, {site.lon}, {site.alt}) from {latest_cycle}'
        if '/' not in plot:
            plot = path.join(link, plot)
        plot_latest(dfs, title, plot, color='k')

    if len(sites) == 0:
        sites = [p[:-7] for p in glob("*/latest")]
        if len(sites) == 0:
            print('Weather table not found.')
            return 0

    dfs = [read(f'{s}/latest') for s in sites]
    plot_sites(dfs, sites, name=out)


@ucast.command()
@click.option("--data", default='.',      help="Data archive directory.")
@click.option("--version",default="latest", help="version of dataset. Eg : latest, latest-06...")
def mkbokeh(data,version):
    """ Creates a bokeh html file containing forecast of all sites."""
    bokeh_static(data,version)


if __name__ == "__main__":
    ucast()
