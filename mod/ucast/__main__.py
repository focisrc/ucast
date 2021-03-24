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

from os        import path
from os        import symlink
from itertools import chain
from datetime  import timedelta
from tqdm      import tqdm

import numpy  as np
import pandas as pd
import requests
import click

import ucast as uc

columns   = ['date', 'tau', 'Tb', 'pwv', 'lwp', 'iwp', 'o3']
dt_fmt    = "%Y%m%d_%H:%M:%S"
forecasts = list(range(120+1)) + list(range(123, 384+1, 3))
heading   = "#            date       tau225        Tb[K]      pwv[mm] lwp[kg*m^-2] iwp[kg*m^-2]       o3[DU]\n"
out_fmt   = "%16s %12.4e %12.4e %12.4e %12.4e %12.4e %12.4e"

am = uc.am.AM()

def mktable(site, cycle):
    df = pd.DataFrame(columns=columns)

    for hr_forecast in tqdm(forecasts, desc=cycle.strftime(dt_fmt)):
        try:
            gfs = uc.gfs.GFS(site, cycle, hr_forecast)
        except requests.exceptions.RetryError as e:
            continue # skip a row

        sol  = am.solve(gfs)
        date = (gfs.cycle + timedelta(hours=hr_forecast)).strftime(dt_fmt)
        df   = df.append({'date':date, **sol}, ignore_index=True)

    return df


@click.command()
@click.option("--lag",  default=5.2,  help="default lag")
@click.option("--site", default='KP', help="Kitt Peak")
@click.option("--run",  default='.',  help="Run directory")
@click.option("--data", default=None, help="Data directory")
def ucast(lag, site, run, data):
    """µcast: micro-weather forecasting for astronomy"""

    site         = getattr(uc.site, site)
    latest_cycle = uc.gfs.latest_cycle(lag=lag)

    for hr_ago in range(0, 48+1, 6):
        cycle   = uc.gfs.relative_cycle(latest_cycle, hr_ago)
        outfile = path.join(run, cycle.strftime(dt_fmt))

        if path.isfile(outfile) and len(open(outfile).readlines()) == len(forecasts)+1:
            print(f'Skip "{outfile}"')
        else:
            print(f'Creating "{outfile}" ...', end='')
            df = mktable(site, cycle)
            with open(outfile, "w") as f:
                f.write(heading)
                np.savetxt(f, df.fillna(0).values, fmt=out_fmt)
            print(" DONE")

        if data is not None:
            target="latest" if hr_ago == 0 else f"latest-{hr_ago:02d}"
            symlink(path.realpath(outfile),
                    path.join(data, target))


if __name__ == "__main__":
    ucast()
