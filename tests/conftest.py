"""Pytest configuration for the braggedgemodeling test suite.

Register the Debye temperatures from ``tests/bem.conf`` directly into the
package table so tests that need them (e.g. NaCl → Cl) pass regardless of
import order or working directory.

``braggedgemodeling`` loads ``bem.conf`` only once, from the CWD at first
import. Under pytest the package may be imported (by another test) before the
NaCl test changes into ``tests/``, so the config would be missed and the run
would fail with ``ValueError: Debye temperature for 'Cl'``. Updating the table
here — at conftest import, before any test runs — makes it order-independent.
"""

import os

import yaml

from braggedgemodeling.DebyeTemp import table

_conf = os.path.join(os.path.dirname(__file__), "bem.conf")
with open(_conf) as _fh:
    _debye = (yaml.safe_load(_fh) or {}).get("DebyeTemperatures") or {}
table.update(_debye)
