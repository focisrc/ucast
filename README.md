[![Actions Status](https://github.com/focisrc/ucast/workflows/python-package/badge.svg)](https://github.com/focisrc/ucast/actions)
[![PyPI version](https://badge.fury.io/py/ucast.svg)](https://badge.fury.io/py/ucast)

# µcast

µcast (Unix name `ucast` starts with the Roman letter "u") is a
toolkit for micro-weather forecast for astronomy.
It provides a high-level and developer-friendly interface to combine
weather data and radiative transfer models to enable accurate
micro-weather forecast at telescope sites.
It is built on top of other projects including *am* for atmospheric
modeling.


## Usage

µcast is a pure python package that can easily be installed by `pip
install ucast`.
However, in order to use *am* Atmospheric Model, the `am` needs to be
in your `$PATH`.
After installation, one can simply `import ucast` to use µcast inside
python.
µcast also comes with a command line tool `ucast` to automatically
pull GFS data, create summary tables of atmospheric properties, and
plot the results:

    $ ucast mktab KP # create weather forecast table
    $ ucast psite KP # create summary plot for one site
    $ ucast pall     # create summary plot for all sites
    $ ucast vis      # create a bokeh visualization

Use `ucast mktab --help`, `ucast psite --help`, etc to see the
detailed usages.


## Backend Tools

### Weather Data and Forecast Systems

µcast supports different weather data and forecast systems.

* **Global Forecast System (GFS)**

  [NOAA Operational Model Archive and Distribution System
  (NOMADS)](https://nomads.ncep.noaa.gov/) addresses the need of
  remote access to high-volume numerical weather prediction and global
  climate models and data.
  It is µcast's default service to pull weather data.


### Radaitive Transfer Backends

µcast supports multiple atmospherical model backend for radiative
transfer.

* ***am* Atmospheric Model**

  [*am* Atmospheric Model](https://www.cfa.harvard.edu/~spaine/am) is
  a tool for radiative transfer computations at microwave to
  submillimeter wavelengths.
  It is µcast's default model for radio astronomy.
