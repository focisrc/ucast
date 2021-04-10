#!/usr/bin/env python3
#
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

from setuptools import setup, find_packages

setup(
    name='ucast',
    version='0.1.3',
    url='https://github.com/focisrc/ucast',
    author='Chi-kwan Chan',
    author_email='chanc@arizona.edu',
    description='Micro-weather forecasting for astronomy',
    packages=find_packages('mod'),
    package_dir={'': 'mod'},
    entry_points={
        'console_scripts': [
            'ucast = ucast.__main__:ucast',
        ],
    },
    python_requires='>=3.6', # `ucast` uses python3's f-string and typing
    install_requires=[
        'click>=7.1.2',
        'matplotlib>=3.2.2',
        'numpy>=1.18.5',
        'pandas>=1.0.5',
        'pygrib>=2.0.4',
        'requests>=2.24.0',
        'tqdm>=4.46.1',
        'bokeh>=2.3.0'
    ],
)
