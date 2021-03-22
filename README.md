[![Actions Status](https://github.com/focisrc/ucast/workflows/python-package/badge.svg)](https://github.com/focisrc/ucast/actions)

# µcast

µcast (Unix name `ucast` starts with the Roman letter "u") is a
toolkit for micro-weather forecast for astronomy.
It provides a high-level and developer-friendly interface to combine
weather data and radiative transfer models to enable accurate
micro-weather forecast at telescope sites.


## Weather Data and Forecast Systems

µcast supports different weather data and forecast systems.

### Global Forecast System (GFS)

[NOAA Operational Model Archive and Distribution System
(NOMADS)](https://nomads.ncep.noaa.gov/) addresses the need of remote
access to high-volume numerical weather prediction and global climate
models and data.
It is µcast's default service to pull weather data.


## Radaitive Transfer Backends

µcast supports multiple atmospherical model backend for radiative
transfer.

### *am* Atmospheric Model

[*am* Atmospheric Model](https://www.cfa.harvard.edu/~spaine/am) is a
tool for radiative transfer computations at microwave to submillimeter
wavelengths.
It is µcast's default model for radio astronomy.
