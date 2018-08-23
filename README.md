[![Build Status](https://travis-ci.org/ornlneutronimaging/braggedgemodeling.svg?branch=master)](https://travis-ci.org/ornlneutronimaging/braggedgemodeling)
[![Coverage Status](https://coveralls.io/repos/github/ornlneutronimaging/braggedgemodeling/badge.svg?branch=master)](https://coveralls.io/github/ornlneutronimaging/braggedgemodeling?branch=master)
# Bragg Edge Modeling

This python package provides tools to model and help analyze neutron Bragg Edge imaging data.

**Main functionality:** given lattice structure of a material and optionally a texture model and
an instrument beam model,
calculate neutron Bragg Edge spectrum as a function of neutron wavelength.

## Features
* Cross section calculation from crystal structure specification
  - Calculate diffraction peaks data (d-spacing, form factors, etc.) according to sample crystal structure
  - Estimate inelastic scattering using incoherent approximation
* Modeling of texture:
  - March Dollase
* Modeling of peak profile:
  - Jorgensen model
* Flexible design to allow future extension to texture and peak profile models
* Enable easy fitting to measured Bragg Edge data

## Documentation

Please refer to https://ornlneutronimaging.github.io/braggedgemodeling for documentation
on installation, usage, and API.

## Community guidelines

**How to contribute**

Please clone the repository, make changes and make a pull request.

**How to report issues**

Please use [the github issues](https://github.com/ornlneutronimaging/braggedgemodeling/issues) to report issues or bug reports.

**Support**

Please either use [the github issues](https://github.com/ornlneutronimaging/braggedgemodeling/issues) to ask for support, or contact the authors directly using email.


## Known problems
* Debye temperatures are listed in a table, which is missing data for some elements.
  However, users can provide their own table in a [configuration file](tests/bem.conf).
