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

import ucast as uc

def test_nomads():
    site         = uc.site.KP
    latest_cycle = uc.gfs.latest_cycle()

    url = uc.gfs.nomads.data_url(site, latest_cycle, None, 0.25)
    assert url is not None

def test_gfs():
    site         = uc.site.KP
    latest_cycle = uc.gfs.latest_cycle()

    gfs = uc.gfs.GFS(site, latest_cycle, 0)
    assert gfs is not None
