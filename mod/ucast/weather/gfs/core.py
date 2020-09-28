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

from ...request import request
from .nomads    import data_url
from .grib      import load

M_AIR = 28.964 # average dry air mass [g / mole]
M_O3  = 47.997 # O3 mass [g / mole]

class GFS:

    def __init__(self, site, cycle, product):
        # Step 1: download data from NOMADS
        r = request(data_url(site.lat, site.lon, cycle, product))

        # Step 2: save data to temporary file; load it back with `pygrib`
        with NamedTemporaryFile() as t:
            with open(t.name, "wb") as f:
                f.write(r.content)
            d = load(t.name, site)

        # Step 3: convert mass mixing ratio to volume mixing ratio
        d['o3_vmr'] *= M_AIR / M_O3

        # Step 4: set the instance attributes
        for k, v in d.items():
            setattr(self, k, v)
