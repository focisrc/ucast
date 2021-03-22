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

from itertools import chain
from datetime  import timedelta

import pandas as pd
import ucast  as uc

import click

dt_fmt = "%Y%m%d_%H:%M:%S"

@click.command()
@click.option("--lag",  default=5.2,  help="default lag")
@click.option("--site", default='KP', help="Kitt Peak")
def ucast(lag, site):
    """µcast: micro-weather forecasting for astronomy"""

    site         = getattr(uc.site, site)
    latest_cycle = uc.gfs.latest_cycle(lag=lag)
    am           = uc.am.AM()

    for hr_ago in range(0, 48+1, 6):
        cycle   = uc.gfs.relative_cycle(latest_cycle, hr_ago)
        outfile = cycle.strftime(dt_fmt)
        print(outfile)

        df = pd.DataFrame()
        for hr_forecast in chain(range(120+1), range(123, 384+1, 3)):
            gfs  = uc.gfs.GFS(site, cycle, hr_forecast)
            date = (gfs.cycle + timedelta(hours=hr_forecast)).strftime(dt_fmt)
            sol  = am.solve(gfs)
            df   = df.append({'date':date, **sol}, ignore_index=True)

        print(df)


if __name__ == "__main__":
    ucast()
