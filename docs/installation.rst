.. _installation:

Installation
============

Python
------
``braggedgemodeling`` requires **Python 3.12 or newer**.

.. note::

   The distribution is named ``braggedgemodeling`` (the short name ``bem`` is
   already taken on PyPI), and the **import package is also**
   ``braggedgemodeling``. Code written against the old ``bem`` module can add a
   one-line alias as a drop-in stop-gap::

      import braggedgemodeling as bem


Install from PyPI (pip)
-----------------------

::

   $ pip install braggedgemodeling


Install from conda (anaconda.org)
----------------------------------

Conda packages are published to the ``neutronimaging`` channel::

   $ conda install -c conda-forge -c neutronimaging braggedgemodeling


From source (pixi)
------------------

The project uses `pixi <https://pixi.sh/>`_ for reproducible environments.
To work from a clone::

   $ git clone https://github.com/ornlneutronimaging/braggedgemodeling.git
   $ cd braggedgemodeling
   $ pixi run test        # build the environment and run the test suite

Individual environments and tasks are defined in ``pyproject.toml`` (for
example ``pixi run -e docs build-docs`` to build these docs).

.. note::

   The optional ``texture`` subpackage additionally requires an external
   MATLAB + mtex + VPSC toolchain, which cannot be installed from PyPI or
   conda and is not exercised in CI. See :doc:`api` and issue `#40
   <https://github.com/ornlneutronimaging/braggedgemodeling/issues/40>`_.
