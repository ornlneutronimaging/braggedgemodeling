[![Build Status](https://travis-ci.org/ornlneutronimaging/braggedgemodeling.svg?branch=master)](https://travis-ci.org/ornlneutronimaging/braggedgemodeling)
[![Coverage Status](https://coveralls.io/repos/github/ornlneutronimaging/braggedgemodeling/badge.svg?branch=master)](https://coveralls.io/github/ornlneutronimaging/braggedgemodeling?branch=master)
# Bragg Edge Modeling

This python package provides tools to model and help analyze neutron Bragg Edge imaging data.
** Main functionality: ** given lattice structure of a material and optionally a texture model and
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

## Installation

Conda installation

`$ conda install -c conda-forge braggedgemodeling`

Install from source:

* Check out the source repository or download and expand the source tar ball
* Run `python setup.py install`

## Known problems
* Debye temperature are listed a table, which is missing data for some elements. However, users can provide their
  own table in a configuration file.

