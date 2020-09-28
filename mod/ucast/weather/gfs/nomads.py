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

from math import floor

import sys
import requests
import time

# GFS variables to be requested
variables = (
    "CLWMR", # Cloud liquid water mass mixing ratio [kg liquid / kg air]
    "ICMR",  # Cloud ice mass mixing ratio [kg liquid / kg air]
    "HGT",   # Geopotential height [m]
    "O3MR",  # Ozone mass mixing ratio [kg O3 / kg air]
    "RH",    # Relative Humidity [%]
    "TMP",   # Temperature [K]
)

# GFS grid levels [mbar]
levels = (
    1, 2, 3, 5, 7, 10, 20, 30, 50, 70, 100, 150, 200, 250, 300, 350, 400,
    450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 925, 950, 975, 1000,
)

def cgi_url(g):
    """URL for the CGI interface for getting GFS data.

    Args:
        g: grid spacing string defined below.

    """
    return f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_{g}_1hr.pl"

def product_query(c, g, f):
    """Query string for requesting the kind of data product.

    Args:
        c:  forecast production cycle (00, 06, 12, 18).
        g:  grid spacing string.  The available GFS lat,lon grid
            spacings are 0.25, 0.50, or 1.00 degrees.  In the GFS file
            names and CGI interface, this is coded as "0p25" for 0.25
            deg, etc.
        f:  forecast product, either "anl" for analysis at production
            time, or "fxxx" for forecast xxx hours in the future,
            where xxx ranges from 000 to 384 by 1-hour steps, by
            1-hour steps up to 120 hours, and by 3-hour steps
            thereafter.

    """
    return f"file=gfs.t{c:02d}z.pgrb2.{g}.{f}"

def variable_query(v):
    """Query string for adding GFS variables to the CGI request URL."""
    return f"var_{v}=on"

def level_query(l):
    """Query string used to add GFS grid level to the CGI request URL."""
    return f"lev_{l:d}_mb=on"

def subregion_query(lat, lon, grid_delta):
    """Query string for the grid subset request."""
    l = floor(lon / grid_delta) * grid_delta
    b = floor(lat / grid_delta) * grid_delta
    r = l + grid_delta
    t = b + grid_delta
    return f"subregion=&leftlon={l}&rightlon={r}&toplat={t}&bottomlat={b}"

def cycle_query(d, c):
    """Query string for requesting the specific data and production cycle
    within that date.

    Args:
        d:  date in the form YYYYMMDD.
        c:  forecast production cycle (00, 06, 12, 18).

    """
    return f"dir=%2Fgfs.{d}%2F{c:02d}"

def data_url(lat, lon, grid_delta, d, c, f):
    """Construct the full data request URL.

    These include the base URL for the NOMADS CGI, and various strings
    for formatting the arguments given to it.  Note that some
    information (e.g. grid, forecast production cycle) gets used more
    than once to construct the CGI request.

    """
    g = f"{grid_delta:.2f}".replace('.', 'p')
    query = '&'.join([
        product_query(c, g, f),
        '&'.join(level_query(l)    for l in levels),
        '&'.join(variable_query(v) for v in variables),
        subregion_query(lat, lon, grid_delta),
        cycle_query(d, c),
    ])
    return '?'.join([cgi_url(g), query])
