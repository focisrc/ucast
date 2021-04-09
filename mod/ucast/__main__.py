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

from os       import path
from glob     import glob
from datetime import datetime

import requests
import click

import ucast as uc
from ucast.utils import forced_symlink  as symlink
from ucast.utils import ucast_dataframe as mkdf
from ucast.utils import valid, regroup
from ucast.io    import dt_fmt
from ucast.io    import save_tsv as save
from ucast.io    import read_tsv as read
from ucast.plot  import plot_site, plot_all
from ucast.bokeh import static_vis


@click.group()
def ucast():
    """µcast: micro-weather forecasting for astronomy"""


@ucast.command()
@click.argument("site")
@click.option("--lag",     default=5.25,  help="Lag hour for weather forecast.")
@click.option("--data",    default=None,  help="Data archive directory.")
@click.option("--link",    default=None,  help="Directory with latest links.")
@click.option("--no-link", default=False, help="Disable latest links.",               is_flag=True)
@click.option("--test",    default=False, help="Pull two forecasts for fast testing", is_flag=True)
def mktab(lag, site, data, link, no_link, test):
    """Pull weather for telescope SITE, process with `am`, and make tables """

    if no_link and link is not None:
        raise click.UsageError(
            '"--link" should not be specified if "--no-link" is set')

    if data is None:
        data = site if path.isdir(site) else '.'

    if link is None:
        link = data

    site         = getattr(uc.site, site)
    latest_cycle = uc.gfs.latest_cycle(lag=lag)

    for hr_ago in range(0, 48+1, 6):
        cycle   = uc.gfs.relative_cycle(latest_cycle, hr_ago)
        outfile = path.join(data, cycle.strftime(dt_fmt)+'.tsv')

        if valid(outfile):
            print(f'Skip "{outfile}"', end='')
        else:
            print(f'Creating "{outfile}" ...', end='')
            save(outfile, mkdf(site, cycle, test))
            print(" DONE", end='')

        if no_link:
            print()
        else:
            target = path.join(link,
                "latest.tsv" if hr_ago == 0 else f"latest-{hr_ago:02d}.tsv")
            print(f'; linked as "{target}"')
            symlink(outfile, target)


@ucast.command()
@click.argument("site")
@click.option("--no-lag",  default=False, help="Do not use current time to name links.", is_flag=True)
@click.option("--lag",     default=None,  help="Lag hour for weather forecast.")
@click.option("--data",    default=None,  help="Data archive directory.")
@click.option("--link",    default=None,  help="Directory with latest links.")
def link(lag, no_lag, site, data, link):
    """(Re)link weather forecast tables"""

    if no_lag and lag is not None:
        raise click.UsageError(
            '"--lag" should not be specified if "--no-lag" is set')
    if lag is None:
        lag = 5.25

    if data is None:
        data = site if path.isdir(site) else '.'

    if link is None:
        link = data

    if no_lag:
        pattern = path.join(link, '????-??-??_??.??.??.tsv')
        sites = [p.split(path.sep)[-2] for p in sorted(glob(pattern))]

    else:
        latest_cycle = uc.gfs.latest_cycle(lag=lag)

    for hr_ago in range(0, 48+1, 6):
        cycle   = uc.gfs.relative_cycle(latest_cycle, hr_ago)
        outfile = path.join(data, cycle.strftime(dt_fmt)+'.tsv')

        if valid(outfile):
            target = path.join(link,
                "latest.tsv" if hr_ago == 0 else f"latest-{hr_ago:02d}.tsv")
            print(f'"{outfile}" linked as "{target}"')
            symlink(outfile, target)
        else:
            print(f'"{outfile}" is missing; skipped')


@ucast.command()
@click.argument("site")
@click.option("--link", default=None, help="Directory with latest links.")
@click.option("--out",  default=None, help="File name of the plot.")
def psite(site, link, out):
    """Read weather tables from SITE and create summary plot for one site"""

    if link is None:
        link = site if path.isdir(site) else '.'

    if out is None:
        out = path.join(link, 'latest')
    elif '/' not in out:
        out = path.join(link, out)

    site         = getattr(uc.site, site)
    latest_fname = path.basename(path.realpath(path.join(link, "latest.tsv")))
    latest_cycle = datetime.strptime(path.splitext(latest_fname)[0], dt_fmt)

    dfs = []
    for hr_ago in range(0, 48+1, 6):
        target = path.join(link,
            "latest.tsv" if hr_ago == 0 else f"latest-{hr_ago:02d}.tsv")
        dfs.append(read(target))

    title = f'{site.name} ({site.lat},{site.lon},{site.alt}) forecasted from {latest_cycle}'
    plot_site(dfs, title, fname=out, color='k')


@ucast.command()
@click.argument("sites", nargs=-1)
@click.option("--link", default=None, help="Directory with latest links.")
@click.option("--set",  default=None, help="Input dataset, e.g. latest, latest-06, ...")
@click.option("--out",  default=None, help="File name of the plot.")
def pall(sites, link, set, out):
    """Read weather tables from SITES and create summary plot for all sites"""

    if link is None:
        link = '.'

    if set is None:
        set = 'latest'

    if out is None:
        out = path.join(link, set)
    elif '/' not in out:
        out = path.join(link, out)

    if len(sites) == 0:
        pattern = path.join(link, "*", set+'.tsv')
        sites = [p.split(path.sep)[-2] for p in sorted(glob(pattern))]
        if len(sites) == 0:
            print('Weather table not found.')
            return 0

    latest_fname = path.basename(path.realpath(path.join(link, f"{sites[0]}/{set}.tsv")))
    latest_cycle = datetime.strptime(path.splitext(latest_fname)[0], dt_fmt)
    title = f'Full array forecasted from {latest_cycle}'

    sites = regroup(sites)
    dfs   = [read(f'{s}/{set}.tsv') for s in sites]
    sites = list(sites.values())
    plot_all(dfs, sites, title, fname=out)


@ucast.command()
@click.argument("sites", nargs=-1)
@click.option("--link", default=None, help="Directory with latest links.")
@click.option("--set",  default=None, help="Input dataset, e.g. latest, latest-06, ...")
@click.option("--out",  default=None, help="File name of the plot.")
@click.option('--browser/--no-browser',
                        default=True, help="Open visualization in a browser.")
def vis(sites, link, set, out, browser):
    """ Creates a bokeh html file containing forecast of all sites."""

    if link is None:
        link = '.'

    if set is None:
        set = 'latest'

    if out is None:
        out = path.join(link, set)
    elif '/' not in out:
        out = path.join(link, out)

    if len(sites) == 0:
        pattern = path.join(link, "*", set+'.tsv')
        sites = [p.split(path.sep)[-2] for p in sorted(glob(pattern))]
        if len(sites) == 0:
            print('Weather table not found.')
            return 0

    sites = regroup(sites)
    dfs   = [read(f'{s}/{set}.tsv') for s in sites]
    sites = list(sites.values())
    static_vis(dfs, sites, fname=out, browser=browser)


if __name__ == "__main__":
    ucast()
