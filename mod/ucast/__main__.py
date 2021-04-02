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

from os import path

import requests
import click

import ucast as uc
from ucast.utils import forced_symlink  as symlink
from ucast.utils import ucast_dataframe as mkdf
from ucast.utils import forecasts
from ucast.io    import dt_fmt, save


@click.command()
@click.option("--lag",     default=5.2,  help="Lag hour for weather forecast.")
@click.option("--site",    default='KP', help="Telescope site.")
@click.option("--archive", default='.',  help="Archive data directory.")
@click.option("--latest",  default=None, help="Latest data directory.")
def ucast(lag, site, archive, latest):
    """µcast: micro-weather forecasting for astronomy"""

    site         = getattr(uc.site, site)
    latest_cycle = uc.gfs.latest_cycle(lag=lag)

    for hr_ago in range(0, 48+1, 6):
        cycle   = uc.gfs.relative_cycle(latest_cycle, hr_ago)
        outfile = path.join(archive, cycle.strftime(dt_fmt))

        if path.isfile(outfile) and len(open(outfile).readlines()) == len(forecasts)+1:
            print(f'Skip "{outfile}"; ', end='')
        else:
            print(f'Creating "{outfile}" ...', end='')
            save(outfile, mkdf(site, cycle))
            print(" DONE; ", end='')

        if latest is not None:
            target = "latest" if hr_ago == 0 else f"latest-{hr_ago:02d}"
            print(f'link as "{target}"')
            symlink(path.realpath(outfile),
                    path.join(latest, target))
        else:
            print()


if __name__ == "__main__":
    ucast()
