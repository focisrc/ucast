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

import numpy as np
import pygrib

from .nomads import levels

BADVAL = -99999.0  # placeholder for missing or undefined data

load_map = {
    'z'        : ("Geopotential Height", BADVAL),
    'T'        : ("Temperature",         BADVAL),
    'o3_mmr'   : ("Ozone mixing ratio",     0.0),
    'RH'       : ("Relative humidity",      0.0),
    'cloud_lmr': ("Cloud mixing ratio",     0.0),
    'cloud_imr': ("Ice water mixing ratio", 0.0),
}

def load(path, site, grid_delta=0.25):

    u = (site.lat/grid_delta) % 1
    v = (site.lon/grid_delta) % 1

    idx = pygrib.index(path, "name", "level")

    def grid_interp(name, level, bad):
        try:
            a = idx.select(name=name, level=level)[0].values
        except:
            return bad
        else:
            return (a[0][0] * (1.0-u) * (1.0-v) + a[1][0] * u * (1.0-v) +
                    a[0][1] * (1.0-u) *      v  + a[1][1] * u *      v   )

    d = {'P':np.array(levels)}
    for k, (name, bad) in load_map.items():
        d[k] = np.array([grid_interp(name, l, bad) for l in levels])

    return d
