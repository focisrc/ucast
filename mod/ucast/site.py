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

from collections import namedtuple

Site = namedtuple('Site', ['name', 'lat', 'lon', 'alt'])

ALMA = Site('ALMA', -23.029,  -67.755, 5070.4)
APEX = Site('APEX', -23.006,  -67.759, 5104.5)
GLT  = Site('GLT',   72.579,  -38.454, 3204.9)
JCMT = Site('JCMT',  19.823, -155.477, 4120.1)
KP   = Site('KP',    31.956, -111.612, 1902.0)
LMT  = Site('LMT',   18.985,  -97.315, 4600.0)
PDB  = Site('PDB',   44.634,    5.907, 2616.4)
PV   = Site('PV',    37.066,   -3.393, 2921.7)
SMA  = Site('SMA',   19.822, -155.476, 4110.3)
SMT  = Site('SMT',   32.702, -109.891, 3158.7)
SPT  = Site('SPT',  -90.000,   45.000, 2857.4)
