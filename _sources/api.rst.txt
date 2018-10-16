API
===

The braggedgemodeling package provides tools to calculate neutron Bragg Edge
spectrum for a material.

Atomic structure
----------------

.. autofunction:: bem.matter.loadCif
.. autofunction:: bem.matter.Structure

Cross section calculator
------------------------

.. autoclass:: bem.xscalc.XSCalculator
   :members:
   :special-members: __init__
		  
Texture
-------

.. autoclass:: bem.xtaloriprobmodel.MarchDollase


Peak profile
------------
.. autoclass:: bem.peak_profile.Jorgensen
   :members:
   :special-members: __init__
