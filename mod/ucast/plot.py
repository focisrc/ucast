# Copyright (C) 2021 Chi-kwan Chan
# Copyright (C) 2021 Steward Observatory
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

from matplotlib import pyplot as plt

def plot_latest(dfs, title=None, name=None, **kwargs):

    fig, ax = plt.subplots(figsize=(10.5,4.5))

    for i, df in enumerate(dfs):
        alpha = 1.0 if i == 0 else (1 - i/len(dfs)) / 3
        ax.plot(df.date, df.tau, alpha=alpha, **kwargs)

    ax.set_xlabel('Date')
    ax.set_ylabel(r'$\tau_{255}$')

    ax.set_xlim(dfs[-1].date[0], None)
    ax.set_ylim(0, None)

    ax.grid(axis='y')
    plt.xticks(rotation=45, ha='right')

    if title is not None:
        ax.set_title(title)

    fig.tight_layout()

    if name is not None:
        fig.savefig(name)
