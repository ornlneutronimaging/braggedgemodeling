API
===

The braggedgemodeling package provides tools to calculate neutron Bragg Edge
spectrum for a material.

.. note::

   The import package is ``braggedgemodeling``. Existing code that used the
   old ``bem`` name can add ``import braggedgemodeling as bem`` as a drop-in
   alias.

Atomic structure
----------------

.. autofunction:: braggedgemodeling.matter.loadCif
.. autofunction:: braggedgemodeling.matter.Structure

Cross section calculator
------------------------

.. autoclass:: braggedgemodeling.xscalc.XSCalculator
   :members:
   :special-members: __init__

Texture
-------

.. autoclass:: braggedgemodeling.xtaloriprobmodel.MarchDollase


Peak profile
------------
.. autoclass:: braggedgemodeling.peak_profile.Jorgensen
   :members:
   :special-members: __init__
