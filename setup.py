#!/usr/bin/env python

import os
from setuptools import setup, find_packages

here = os.path.dirname(__file__)
version_ns = {}
with open(os.path.join(here, 'bem', '_version.py')) as f:
    exec(f.read(), {}, version_ns)

# define distribution
setup(
    name = "bem",
    version = version_ns['__version__'],
    packages = find_packages(".", exclude=['tests', 'notebooks', 'docs']),
    package_dir = {'': "."},
    data_files = [],
    test_suite = 'tests',
    install_requires = [
        'pyyaml', 'numpy', 'scipy', 'matplotlib',
        'diffpy.structure', 'periodictable'
    ],
    dependency_links = [
    ],
    author = "ORNL neutron imaging team",
    description = "Bragg Edge modeling",
    license = 'BSD',
    keywords = "instrument, neutron, imaging, Bragg Edge",
    url = "https://github.com/ornlneutronimaging/braggedgemodeling",
    # download_url = '',
)

# End of file
