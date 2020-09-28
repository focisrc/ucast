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
    450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 925, 950, 975, 1000)
