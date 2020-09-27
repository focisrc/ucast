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

from datetime import datetime, timedelta

def relative_gfs_cycle_time(ref, lag):
    """GFS forecast cycle time relative to another time.

    This function returns the datetime corresponding to a GFS forecast
    cycle time displaced by some number of hours relative to another
    GFS cycle time.  For example,

        relative_gfs_cycle_time(ref, 12)

    will return the GFS cycle time 12 hours before the cycle
    corresponding to `ref`

    Args:
        ref: Reference time
        lag: Lag time in hour

    Returns:
        The relative GFS cycle time.

    """
    gfs = ref - timedelta(hours=lag)
    return gfs.replace(hour=gfs.hour//6*6,
                       minute=0,
                       second=0,
                       microsecond=0)

def latest_gfs_cycle_time(lag=6):
    """The most recent GFS cycle time.

    Args:
        lag: The default GFS forecast production lag is 6 hours.  To
            get an earlier forecast, this might be set somewhat
            shorter, with due care taken to ensure it isn't set too
            short.

    Returns:
        The most recent GFS cycle time.

    """
    return relative_gfs_cycle_time(datetime.utcnow(), lag)

def cgi_url(g):
    """URL for the CGI interface.

    Args:
        g: grid spacing string defined below.

    """
    return f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_{g}_1hr.pl"

def product_query(c, g, f):
    """Query string for requesting the kind of data product.

    Args:
        c:  forecast production cycle (00, 06, 12, 18).
        g:  grid spacing string.
        f:  forecast product, either "anl" for analysis at production
            time, or "fxxx" for forecast xxx hours in the future,
            where xxx ranges from 000 to 384 by 1-hour steps, by
            1-hour steps up to 120 hours, and by 3-hour steps
            thereafter.

    """
    return f"file=gfs.t{c:02d}z.pgrb2.{g}.{f}"

# GFS variables to be requested
variables = (
    "CLWMR", # Cloud liquid water mass mixing ratio [kg liquid / kg air]
    "ICMR",  # Cloud ice mass mixing ratio [kg liquid / kg air]
    "HGT",   # Geopotential height [m]
    "O3MR",  # Ozone mass mixing ratio [kg O3 / kg air]
    "RH",    # Relative Humidity [%]
    "TMP",   # Temperature [K]
)

def variable_query(v):
    """Query string for adding GFS variables to the CGI request URL."""
    return f"var_{v}=on"

# GFS grid levels [mbar]
levels = (
    1, 2, 3, 5, 7, 10, 20, 30, 50, 70, 100, 150, 200, 250, 300, 350, 400,
    450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 925, 950, 975, 1000)

def level_query(l):
    """Query string used to add GFS grid level to the CGI request URL."""
    return f"lev_{l:d}_mb=on"

def subregion_query(l, r, t, b):
    """Query string for the grid subset request."""
    return f"subregion=&leftlon={l}&rightlon={r}&toplat={t}&bottomlat={b}"

def cycle_query(d, c):
    """Query string for requesting the specific data and production cycle
    within that date.

    Args:
        d:  date in the form YYYYMMDD.
        c:  forecast production cycle (00, 06, 12, 18).

    """
    return f"dir=%2Fgfs.{d}%2F{c:02d}"
