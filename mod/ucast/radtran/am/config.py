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

# Physical constants
G_STD               = 9.80665  # standard gravity [m / s^2]
M_AIR               = 28.964   # average dry air mass [g / mole]
M_O3                = 47.997   # O3 mass [g / mole]
H2O_SUPERCOOL_LIMIT = 238.     # Assume ice below this temperature [K]
PASCAL_ON_MBAR      = 100.     # conversion from mbar (hPa) to Pa

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

def layer(Pbase, zbase, Tbase, o3_vmr, RH, ctw, cti):
    return '\n'.join(filter(None, [
        "layer",
       f"Pbase {Pbase:.1f} mbar  # {zbase:.1f} m",
       f"Tbase {Tbase:.1f} K",
        "column dry_air vmr",
        column('o3 vmr', o3_vmr),
        column("h2o RH" if Tbase > H2O_SUPERCOOL_LIMIT else "h2o RHi", RH),
        column("lwp_abs_Rayleigh", ctw),
        column("iwp_abs_Rayleigh", cti),
    ]))

def config(gfs):

    z      = gfs.site.alt

    Pb     = gfs.P
    zb     = gfs.z
    Tb     = gfs.T

    dP     = Pb
    o3_vmr = gfs.o3_vmr * (M_AIR / M_O3)
    RH     = gfs.RH
    ctw    = gfs.cloud_lmr * (dP / G_STD)
    cti    = gfs.cloud_imr * (dP / G_STD)

    l = [f"""#
# Layer data below were derived from NCEP GFS model data obtained
# from the NOAA Operational Model Archive Distribution System
# (NOMADS).  See http://nomads.ncep.noaa.gov for more information.
#
#         Production date: {gfs.cycle:%Y%m%d}
#                   Cycle: {gfs.cycle:%H} UT
#                 Product: {gfs.product}
#
# Interpolated to
#
#                latitude: {gfs.site.lat} deg. N
#               longitude: {gfs.site.lon} deg. E
#   Geopotential altitude: {gfs.site.alt} m
#"""]
    for i,lev in enumerate(levels):
        if zb[i] < z:
            break
        l.append(layer(
            Pb[i], zb[i], Tb[i],
            o3_vmr[i], RH[i], ctw[i], cti[i]))

    if i == 0:
        raise ValueError("User-specified altitude exceeds top GFS level")

    if zb[i] != z:
        def interp(u, arr, min=None):
            return u * arr[i] + (1-u) * arr[i-1]

        def interp2(u, arr):
            a = u * arr[i] + (1-u) * arr[i-1]
            return 0.5 * ((a if a > 0 else 0) + arr[i-1])

        u  = (z - zb[i-1]) / (zb[i] - zb[i-1])
        Ps = np.exp(interp(u, np.log(Pb)))
        Ts = interp(u, Tb)
        dPs = Ps

        u  = (Ps - Pb[i-1]) / (Pb[i] - Pb[i-1])
        l.append(layer(
            Ps, z, Ts,
            interp2(u, o3_vmr),
            interp2(u, RH),
            interp2(u, ctw),
            interp2(u, cti),
        ))

    return "\n\n".join(l)
