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

import sys
import time
import requests

# Timeouts and retries
CONN_TIMEOUT        = 6   # Initial server response timeout in seconds
READ_TIMEOUT        = 18  # Stalled download timeout in seconds
RETRY_DELAY         = 60  # Delay before retry (NOAA requests 60 s)
MAX_DOWNLOAD_TRIES  = 5

def errln(s):
    print(s, file=sys.stderr)

def err(s):
    print(s, file=sys.stderr, end='')

def request(url,
            ctime=CONN_TIMEOUT,
            rtime=READ_TIMEOUT,
            delay=RETRY_DELAY,
            retry=MAX_DOWNLOAD_TRIES):
    while True:
        retry -= 1

        try:
            r = requests.get(url, timeout=(ctime, rtime))
            if r.status_code == requests.codes.ok:
                return r
        except requests.exceptions.ConnectTimeout:
            err("Connection timed out.")
        except requests.exceptions.ReadTimeout:
            err("Data download timed out.")
        else:
            err(f"Download failed with status code {r.status_code}.")

        if retry:
            errln("  Retrying...")
            time.sleep(delay)
        else:
            errln("  Giving up.")
            break

    errln(f'Failed URL was: "{url}".')
    raise requests.exceptions.RetryError(
        f'Tried downloading "{url}" {retry} times but failed')
