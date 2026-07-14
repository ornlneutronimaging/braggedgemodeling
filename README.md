[![CI](https://github.com/ornlneutronimaging/braggedgemodeling/actions/workflows/CI.yml/badge.svg)](https://github.com/ornlneutronimaging/braggedgemodeling/actions/workflows/CI.yml)
[![codecov](https://codecov.io/gh/ornlneutronimaging/braggedgemodeling/graph/badge.svg)](https://codecov.io/gh/ornlneutronimaging/braggedgemodeling)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.00973/status.svg)](https://doi.org/10.21105/joss.00973)

# Bragg Edge Modeling

This python package provides tools to model and help analyze neutron Bragg Edge imaging data.

**Main functionality:** given lattice structure of a material and optionally a texture model and
an instrument beam model,
calculate neutron Bragg Edge spectrum as a function of neutron wavelength.

## Features
* Calculation of basic Bragg Edge spectrum from crystal structure specification, assuming an isotropic powder sample, and accounting for various contributions to neutron scattering including, for example, diffraction and inelastic scattering (using incoherent approximation)
* Modeling of texture:
  - March Dollase
* Modeling of peak profile:
  - Jorgensen model
* Flexible design to allow future extension to texture and peak profile models
* Allow easy fitting to measured Bragg Edge data

## Installation

`braggedgemodeling` requires Python 3.12+.

```bash
# from PyPI
pip install braggedgemodeling

# or from conda (our anaconda.org neutronimaging channel)
conda install neutronimaging::braggedgemodeling
```

The distribution is named `braggedgemodeling` (the short name `bem` is already taken on PyPI) and the **import package is also `braggedgemodeling`**. Code written against the old `bem` module can add a one-line alias as a drop-in stop-gap:

```python
import braggedgemodeling as bem
```

For development, the project uses [pixi](https://pixi.sh/):

```bash
git clone https://github.com/ornlneutronimaging/braggedgemodeling.git
cd braggedgemodeling
pixi run test   # build the environment and run the test suite
```

## Documentation

Please refer to https://braggedge.readthedocs.io for documentation
on installation, usage, and API.

## Community guidelines

**How to contribute**

Please clone the repository, make changes and make a pull request.

**How to report issues**

Please use [the github issues](https://github.com/ornlneutronimaging/braggedgemodeling/issues) to report issues or bug reports.

**Support**

Please either use [the github issues](https://github.com/ornlneutronimaging/braggedgemodeling/issues) to ask for support, or contact the authors directly using email.


## Known problems
* Debye temperatures are listed in a [table](braggedgemodeling/DebyeTemp.py), which is missing data for some elements.
  However, users can provide their own table in a [configuration file](tests/bem.conf).
