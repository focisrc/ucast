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
from os       import symlink, rename, path
from datetime import timedelta
from math     import sqrt

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


def valid(fname):
    if path.isfile(fname):
        with open(fname) as f:
            return len(f.readlines()) == len(forecasts)+1
    return False


def forced_symlink(src, dst):
    r   = randrange(1000000)
    tmp = f"{dst}-tmp{r:06d}"
    symlink(path.relpath(src, path.dirname(tmp)), tmp)
    rename(tmp, dst)


def regroup(sites):

    def d(s1, s2):
        dlat = s1.lat - s2.lat
        dlon = s1.lon - s2.lon
        return sqrt(dlat * dlat + dlon * dlon)

    ss = [getattr(uc.site, s) for s in sites]

    m = {}
    for i, curr in enumerate(ss):
        added = False
        for prev in ss[:i]:
            if d(curr, prev) < 0.1:
                added = True
                m[prev.name] = ','.join((m[prev.name], curr.name))
                break
        if not added:
            m[curr.name] = curr.name

    return m
