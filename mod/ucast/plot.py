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

    fig, axes = plt.subplots(6, 1, figsize=(8,8), sharex=True)

    columns = dfs[0].columns
    for j, ax in enumerate(axes):
        ax.tick_params(axis='x',direction="in",top=True)
        ax.tick_params(axis='y',direction="in",right=True)
        ax.set_ylabel(f'{columns[j+1]}')
        #ax.grid(axis='y')

    for i, df in enumerate(dfs):
        alpha = 1.0 if i == 0 else (1 - i/len(dfs)) / 3
        for j, ax in enumerate(axes):
            ax.plot(df.date, df.iloc[:,j+1], alpha=alpha, **kwargs)

    if title is not None:
        axes[0].set_title(title)

    axes[5].set_xlabel('Date')
    axes[5].set_xlim(dfs[-1].date[0], None)
    plt.xticks(rotation=45, ha='right')

    fig.tight_layout()
    fig.subplots_adjust(wspace=0, hspace=0.05)

    if name is not None:
        fig.savefig(name)
