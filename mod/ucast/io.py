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

import numpy  as np
import pandas as pd

names   = [             'date',    'tau',       'Tb',      'pwv',  'lwp',       'iwp',             'o3']
heading = "#            date       tau225        Tb[K]      pwv[mm] lwp[kg*m^-2] iwp[kg*m^-2]       o3[DU]\n"
out_fmt = "%16s %12.4e %12.4e %12.4e %12.4e %12.4e %12.4e"
dt_fmt  = "%Y-%m-%d_%H.%M.%S"


def save_txt(fname, df):
    with open(fname, "w") as f:
        f.write(heading)
        np.savetxt(f, df.fillna(0).values, fmt=out_fmt)

def read_txt(fname):
    d = pd.read_csv(fname, delim_whitespace=True, skiprows=1, names=names)
    d.date = pd.to_datetime(d.date, format=dt_fmt)
    return d


def save_csv(fname, df):
    df.to_csv(fname, index=False)

def read_csv(fname):
    d = pd.read_csv(fname)
    d.date = pd.to_datetime(d.date, format=dt_fmt)
    return d


def save_tsv(fname, df):
    df.to_csv(fname, index=False, sep='\t')

def read_tsv(fname):
    d = pd.read_csv(fname, sep='\t')
    d.date = pd.to_datetime(d.date, format=dt_fmt)
    return d
