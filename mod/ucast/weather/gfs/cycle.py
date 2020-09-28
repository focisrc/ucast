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

def relative_cycle(ref, lag):
    """GFS forecast cycle time relative to another time.

    This function returns the datetime corresponding to a GFS forecast
    cycle time displaced by some number of hours relative to another
    GFS cycle time.  For example,

        relative_cycle(ref, 12)

    will return the GFS cycle time 12 hours before the cycle
    corresponding to `ref`

    Args:
        ref: Reference time
        lag: Lag time in hour

    Returns:
        The relative GFS cycle time.

    """
    last = ref - timedelta(hours=lag)
    return last.replace(hour=(last.hour//6)*6,
                        minute=0,
                        second=0,
                        microsecond=0)

def latest_cycle(lag=6):
    """The most recent GFS cycle time.

    Args:
        lag: The default GFS forecast production lag is 6 hours.  To
            get an earlier forecast, this might be set somewhat
            shorter, with due care taken to ensure it isn't set too
            short.

    Returns:
        The most recent GFS cycle time.

    """
    return relative_cycle(datetime.utcnow(), lag)
