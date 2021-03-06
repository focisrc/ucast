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

from datetime import datetime
from os.path  import splitext

from matplotlib import pyplot as plt
from matplotlib import dates  as mdates

vars   = [   'tau',        'Ts',      'RHs',    'pwv',       'lwp',                'iwp'              ]
labels = [r'$\tau_{255}$', 'T [°C]',  'RH [%]', 'pwv [mm]', r'lwp [kg m$^{-2}$]', r'iwp [kg m$^{-2}$]']
ylims  = [   (0, 1.1),     (-55, 22), (0, 110), (0, 16.5),   (0, 2.2),             (0., 2.2)          ]

def plot_site(dfs, title=None, fname=None, **kwargs):

    fig, axes = plt.subplots(len(vars), 1, figsize=(12,8), sharex=True)

    for i, df in enumerate(dfs):
        alpha = 1.0 if i == 0 else (1 - i/len(dfs)) / 3
        width = 1.0 if i == 0 else 0.5
        for j, ax in enumerate(axes):
            try:
                ax.plot(df.date, df[vars[j]].fillna(0),
                        alpha=alpha, linewidth=width, **kwargs)
            except:
                pass
            ax.axvline(x=datetime.utcnow(), linestyle=':', color='k')

    for j, ax in enumerate(axes):
        ax.grid(alpha=0.25)
        ax.tick_params(axis='x',direction="in",top=True)
        ax.tick_params(axis='y',direction="in",right=True)
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.autoscale(enable=True, axis='x', tight=True)
        ax.set_ylabel(labels[j])
        ax.set_ylim(*ylims[j])

    if title is not None:
        axes[0].set_title(title)

    axes[5].set_xlabel('Date')
    axes[5].set_xlim(dfs[-1].date[0], None)
    plt.xticks(rotation=45, ha='right')

    fig.tight_layout()
    fig.subplots_adjust(wspace=0, hspace=0.05)

    if fname is not None:
        _, ext = splitext(fname)
        if ext[1:] in plt.gcf().canvas.get_supported_filetypes():
            fig.savefig(fname)
        else:
            fig.savefig(fname+'.pdf')
            fig.savefig(fname+'.png')


def plot_all(dfs, sites, title=None, fname=None, **kwargs):

    fig, axes = plt.subplots(len(vars), 1, figsize=(12,8), sharex=True)

    for i, df in enumerate(dfs):
        if i == 0:
            kwa = {**kwargs, 'color':'dimgray'}
        else:
            kwa = kwargs
        for j, ax in enumerate(axes):
            try:
                ax.plot(df.date, df[vars[j]].fillna(0),
                        label=sites[i], **kwargs)
            except:
                pass
            ax.axvline(x=datetime.utcnow(), linestyle=':', color='k')

    for j, ax in enumerate(axes):
        ax.grid(alpha=0.25)
        ax.tick_params(axis='x',direction="in",top=True)
        ax.tick_params(axis='y',direction="in",right=True)
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.autoscale(enable=True, axis='x', tight=True)
        ax.set_ylabel(labels[j])
        ax.set_ylim(*ylims[j])

    if title is not None:
        axes[0].set_title(title)

    axes[5].legend(loc='upper right', bbox_to_anchor=(0.99,2))

    axes[5].set_xlabel('Date')
    axes[5].set_xlim(dfs[-1].date[0], None)
    plt.xticks(rotation=45, ha='right')

    fig.tight_layout()
    fig.subplots_adjust(wspace=0, hspace=0.05)

    if fname is not None:
        _, ext = splitext(fname)
        if ext[1:] in plt.gcf().canvas.get_supported_filetypes():
            fig.savefig(fname)
        else:
            fig.savefig(fname+'.pdf')
            fig.savefig(fname+'.png')
