# -*- Python -*-

"""
Bragg edge modeling

deps:
  * diffpy.Structure
  * periodictable
  * matplotlib, numpy
"""

# config file
import yaml, os
conf_path = "bem.conf"
config = dict()
if os.path.exists(conf_path):
    config = yaml.load(open(conf_path))

from . import matter

# End of file
