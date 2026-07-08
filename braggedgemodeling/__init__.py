# -*- Python -*-

"""
Bragg edge modeling

deps:
  * diffpy.Structure
  * periodictable
  * matplotlib, numpy
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("braggedgemodeling")
except PackageNotFoundError:  # package not installed (e.g. running from a source tree)
    __version__ = "unknown"

# config file
import yaml, os
conf_path = "bem.conf"
config = dict()
if os.path.exists(conf_path):
    config = yaml.safe_load(open(conf_path))

from . import matter

# End of file
