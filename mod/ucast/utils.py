# Copyright (C) 2021 Chi-kwan Chan
# Copyright (C) 2021 Steward Observatory
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

from random   import randrange
from os       import symlink, rename
from datetime import timedelta

import requests
import pandas as pd
from tqdm import tqdm

import ucast  as uc
from ucast.io import dt_fmt

columns   = ['date', 'tau', 'Tb', 'pwv', 'lwp', 'iwp', 'o3']
forecasts = list(range(120+1)) + list(range(123, 384+1, 3))


am = uc.am.AM()


def ucast_dataframe(site, cycle):
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


def forced_symlink(src, dst):
    r   = randrange(1000)
    tmp = f"{dst}-{r:03d}"
    symlink(src, tmp)
    rename(tmp, dst)
