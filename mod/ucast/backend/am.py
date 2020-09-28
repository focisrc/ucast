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
