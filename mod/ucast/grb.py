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

from tempfile import NamedTemporaryFile
import numpy as np
import pygrib

from .core import levels

grb_map = {
    'z'        : ("Geopotential Height", -99999.0),
    'T'        : ("Temperature",         -99999.0),
    'o3_vmr'   : ("Ozone mixing ratio",       0.0),
    'RH'       : ("Relative humidity",        0.0),
    'cloud_lmr': ("Cloud mixing ratio",       0.0),
    'cloud_imr': ("Ice water mixing ratio",   0.0),
}

def get_grb(r):

    M_AIR = 28.964 # average dry air mass [g / mole]
    M_O3  = 47.997 # O3 mass [g / mole]

    u = 0.5 #(lat/grid_delta) % 1
    v = 0.5 #(lon/grid_delta) % 1

    with NamedTemporaryFile() as t:
        with open(t.name, "wb") as f:
            f.write(r.content)

        idx = pygrib.index(t.name, "name", "level")

        def grid_interp(name, level, bad):
            try:
                a = idx.select(name=name, level=level)[0].values
            except:
                return bad
            else:
                return (a[0][0] * (1.0-u) * (1.0-v) + a[1][0] * u * (1.0-v) +
                        a[0][1] * (1.0-u) *      v  + a[1][1] * u *      v   )

        d = {'Pbase':np.array(levels)}
        for k, (name, bad) in grb_map.items():
            d[k] = np.array([grid_interp(name, l, bad) for l in levels])

    d['o3_vmr'] *= M_AIR / M_O3 # convert mass mixing ratio to volume
                                # mixing ratio
    return d
