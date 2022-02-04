# -*- Python -*-

"""
Bragg edge modeling

deps:
  * diffpy.Structure
  * periodictable
  * matplotlib, numpy
"""

from ._version import __version__

# config file
import yaml, os
conf_path = "bem.conf"
config = dict()
if os.path.exists(conf_path):
    config = yaml.safe_load(open(conf_path))

from . import matter

# End of file
