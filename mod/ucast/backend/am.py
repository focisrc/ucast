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

import shutil
import subprocess
import re

from ..core import levels

class AM:

    # Column density units (cm^-2 equivalents)
    MM_PWV   = 3.3427e21
    KG_ON_M2 = 3.3427e21
    DU       = 2.6868e16

    cmap = {
        'pwv': (re.compile('^#.*h2o'             ), MM_PWV  ),
        'lwp': (re.compile('^#.*lwp_abs_Rayleigh'), KG_ON_M2),
        'iwp': (re.compile('^#.*iwp_abs_Rayleigh'), KG_ON_M2),
        'o3' : (re.compile('^#.*o3'              ), DU      ),
    }

    def __init__(self, path=None):
        if path is None:
            path = shutil.which('am')
        if path is None:
            raise OSError('Executable of `am` Atmospheric Model not found.')

        self.am = path

    def run(self, *args, **kwargs):
        return subprocess.run([self.am, *args], **kwargs)

    def solve(self, cfg):
        res = self.run('-', input=cfg, encoding='utf-8', capture_output=True)

        sol = {}

        l = res.stdout.split()
        sol['tau'] = float(l[1])
        sol['Tb' ] = float(l[2])

        for l in res.stderr.split('\n'):
            for k, (p, f) in self.cmap.items():
                if p.match(l):
                    sol[k] = float(l.split()[2]) / f
                    continue

        return sol


class AMC:

    G_STD               = 9.80665  # standard gravity [m / s^2]
    H2O_SUPERCOOL_LIMIT = 238.     # Assume ice below this temperature [K]

    @staticmethod
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

    @staticmethod
    def layer(Pbase, dP, alt, T, o3_vmr, RH, cloud_lmr, cloud_imr):
        return '\n'.join(filter(None, [
             "layer",
            f"Pbase {Pbase:.1f} mbar  # {alt:.1f} m",
            f"Tbase {T:.1f} K",
             "column dry_air vmr",
            AMC.column('o3 vmr', o3_vmr),
            AMC.column("h2o RH" if T > AMC.H2O_SUPERCOOL_LIMIT else "h2o RHi", RH),
            AMC.column("lwp_abs_Rayleigh", (dP / AMC.G_STD) * cloud_lmr),
            AMC.column("iwp_abs_Rayleigh", (dP / AMC.G_STD) * cloud_imr),
        ]))

    def __repr__(self,
                 Pbase, dP, z, T, o3_vmr, RH, cloud_lmr, cloud_imr,
                 gfsdate, gfscycle, product_str, lat, lon, alt):

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
#
"""]
        for i,lev in enumerate(levels):
            if z[i] < alt:
                break
            l.append(AMC.layer(
                Pbase[i], dP[i], z[i], T[i], o3_vmr[i], RH[i], cloud_lmr[i], cloud_imr[i]))

        if i == 0:
            raise ValueError("User-specified altitude exceeds top GFS level")

        if z[i] != alt:
            def interp(u, arr, min=None):
                return u * arr[i] + (1-u) * arr[i-1]

            def interp2(u, arr):
                a = u * arr[i] + (1-u) * arr[i-1]
                return 0.5 * ((a if a > 0 else 0) + arr[i-1])

            u = (alt - z[i-1]) / (z[i] - z[i-1])
            P_s = np.exp(interp(u, np.log(Pbase)))
            T_s = interp(u, T)

            u = (P_s - Pbase[i-1]) / (Pbase[i] - Pbase[i-1])
            l.append(AMC.layer(
                P_s, dP_s, alt, T_s,
                interp2(u, o3_vmr),
                interp2(u, RH),
                interp2(u, cloud_lmr),
                interp2(u, cloud_imr),
            ))

        return '\n'.join(l)
