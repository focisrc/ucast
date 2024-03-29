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
import requests
import urllib
import pandas as pd

import gc
from math import floor

Site = namedtuple('Site', ['name', 'lat', 'lon', 'alt'])

ALMA = Site('ALMA', -23.029,  -67.755, 5070.4)
APEX = Site('APEX', -23.006,  -67.759, 5104.5)
GLT  = Site('GLT',   76.5312, -68.7039,  76.5)
JCMT = Site('JCMT',  19.823, -155.477, 4120.1)
KP   = Site('KP',    31.956, -111.612, 1902.0)
LMT  = Site('LMT',   18.985,  -97.315, 4600.0)
PDB  = Site('PDB',   44.634,    5.907, 2616.4)
PV   = Site('PV',    37.066,   -3.393, 2921.7)
SMA  = Site('SMA',   19.822, -155.476, 4110.3)
SMT  = Site('SMT',   32.702, -109.891, 3158.7)
SPT  = Site('SPT',  -90.000,   45.000, 2857.4)


# USGS Elevation Point Query Service
url = r'https://nationalmap.gov/epqs/pqs.php?'
def elevation_function(lat,lon):
    """Query service using lat, lon. add the elevation values as a new column."""
    lat=[lat]
    lon=[lon]
    for lat, lon in zip(lat,lon):
        # define rest query params
        params = {
            'output': 'json',
            'x': lon,
            'y': lat,
            'units': 'Meters'
        }
        # format query string and return query value
        result = requests.get((url + urllib.parse.urlencode(params)))
        return float(result.json()['USGS_Elevation_Point_Query_Service']['Elevation_Query']['Elevation'])




def get_sites(sites,stencil_size,grid_size=0.25):
    stencil_sites=[]
    for site in sites:
        stencil_sites.append(Site(f"{site.name}_{stencil_size}_E", site.lat,site.lon+0.25*stencil_size,elevation_function(site.lat,site.lon+0.25*stencil_size)))
        stencil_sites.append(Site(f"{site.name}_{stencil_size}_W", site.lat,site.lon-0.25*stencil_size,elevation_function(site.lat,site.lon-0.25*stencil_size)))
        stencil_sites.append(Site(f"{site.name}_{stencil_size}_S", site.lat-0.25*stencil_size,site.lon,elevation_function(site.lat-0.25*stencil_size,site.lon)))
        stencil_sites.append(Site(f"{site.name}_{stencil_size}_N",site.lat+0.25*stencil_size,site.lon,elevation_function(site.lat+0.25*stencil_size,site.lon)))
        stencil_sites.append(Site(f"{site.name}_{stencil_size}_SW",site.lat-0.25*stencil_size,site.lon-0.25*stencil_size,elevation_function(site.lat-0.25*stencil_size,site.lon+0.25*stencil_size)))
        stencil_sites.append(Site(f"{site.name}_{stencil_size}_SE",site.lat-0.25*stencil_size,site.lon+0.25*stencil_size,elevation_function(site.lat+0.25*stencil_size,site.lon+0.25*stencil_size)))
        stencil_sites.append(Site(f"{site.name}_{stencil_size}_NW",site.lat+0.25*stencil_size,site.lon-0.25*stencil_size,elevation_function(site.lat-0.25*stencil_size,site.lon+0.25*stencil_size)))
        stencil_sites.append(Site(f"{site.name}_{stencil_size}_NE",site.lat+0.25*stencil_size,site.lon+0.25*stencil_size,elevation_function(site.lat+0.25*stencil_size,site.lon-0.25*stencil_size)))
    return stencil_sites
