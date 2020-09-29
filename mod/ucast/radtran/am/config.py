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

from ...weather.gfs.nomads import levels

G_STD               = 9.80665  # standard gravity [m / s^2]
H2O_SUPERCOOL_LIMIT = 238.     # Assume ice below this temperature [K]

def column(name, value):
    fu_map = {
        'o3 vmr'          :('.3e', ''        ),
        'h2o RH'          :('.2f', '%'       ),
        'h2o RHi'         :('.2f', '%'       ),
        'lwp_abs_Rayleigh':('.3e', ' kg*m^-2'),
        'iwp_abs_Rayleigh':('.3e', ' kg*m^-2'),
    }
    if value > 0:
        fmt, unit = fu_map[name]
        return f"column {name} {value:{fmt}}{unit}"
    else:
        return None

def layer(Pbase, dP, alt, T, o3_vmr, RH, cloud_lmr, cloud_imr):
    return '\n'.join(filter(None, [
        "layer",
       f"Pbase {Pbase:.1f} mbar  # {alt:.1f} m",
       f"Tbase {T:.1f} K",
        "column dry_air vmr",
        column('o3 vmr', o3_vmr),
        column("h2o RH" if T > H2O_SUPERCOOL_LIMIT else "h2o RHi", RH),
        column("lwp_abs_Rayleigh", (dP / G_STD) * cloud_lmr),
        column("iwp_abs_Rayleigh", (dP / G_STD) * cloud_imr),
    ]))

def config(gfs):

    M_AIR = 28.964  # average dry air mass [g / mole]
    M_O3  = 47.997  # O3 mass [g / mole]

    Pbase     = gfs.Pbase
    z         = gfs.z
    T         = gfs.T
    o3_vmr    = gfs.o3_vmr * (M_AIR / M_O3)
    RH        = gfs.RH
    cloud_lmr = gfs.cloud_lmr
    cloud_imr = gfs.cloud_imr

    alt       = 1
    dP        = Pbase

    l = ["""#
# Layer data below were derived from NCEP GFS model data obtained
# from the NOAA Operational Model Archive Distribution System
# (NOMADS).  See http://nomads.ncep.noaa.gov for more information.
#
#         Production date: {gfsdate}
#                   Cycle: {gfscycle:02d} UT
#                 Product: {product_str}
#
# Interpolated to
#
#                latitude: {lat} deg. N
#               longitude: {lon} deg. E
#   Geopotential altitude: {alt} m
#"""]
    for i,lev in enumerate(levels):
        if z[i] < alt:
            break
        l.append(layer(
            Pbase[i], dP[i], z[i], T[i], o3_vmr[i], RH[i], cloud_lmr[i], cloud_imr[i]))

    if i == 0:
        raise ValueError("User-specified altitude exceeds top GFS level")

    if z[i] != alt:
        def interp(u, arr, min=None):
            return u * arr[i] + (1-u) * arr[i-1]

        def interp2(u, arr):
            a = u * arr[i] + (1-u) * arr[i-1]
            return 0.5 * ((a if a > 0 else 0) + arr[i-1])

        u   = (alt - z[i-1]) / (z[i] - z[i-1])
        P_s = np.exp(interp(u, np.log(Pbase)))
        T_s = interp(u, T)

        dP_s = P_s

        u = (P_s - Pbase[i-1]) / (Pbase[i] - Pbase[i-1])
        l.append(layer(
            P_s, dP_s, alt, T_s,
            interp2(u, o3_vmr),
            interp2(u, RH),
            interp2(u, cloud_lmr),
            interp2(u, cloud_imr),
        ))

    return '\n\n'.join(l)
