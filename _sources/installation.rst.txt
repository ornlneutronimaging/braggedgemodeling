.. _installation:

Installation
============

Python
------
The `braggedgemodeling` package depends on python version 3 (3.5, 3.6).


Preferred: Install using conda
------------------------------

The preferred method for installation is to use `conda <https://conda.io/>`_.
Please use the following commands to install `braggedgemodeling`::

      $ conda config --add channels conda-forge
      $ conda install braggedgemodeling

Information on dependencies of this code can be found at `the conda recipe <https://github.com/conda-forge/braggedgemodeling-feedstock/blob/master/recipe/meta.yaml>`_.

      
Using setup.py
--------------

It is also possible to install `braggedgemodeling` using `setup.py` script,
but there are some hoops to jump through.

.. note:: The following instructions assume an ubuntu distribution. For other platforms, please make appropriate adjustments.

* First, please install `pip <https://pypi.org/project/pip/>`_ for python 3 (pip3) using `apt-get`::
	      
   $ sudo apt-get install python3-pip
	      
* Then, use pip3 to install some dependencies::

   $ pip3 install --user numpy pycifrw pyyaml scipy matplotlib periodictable

* Next, please install diffpy.structure (python 3 version) from source::
   
   $ git clone https://github.com/diffpy/diffpy.structure
   $ cd diffpy.structure
   $ git checkout python3  # Important! make sure to checkout the python3 branch
   $ python3 setup.py install --user

.. attention:: This step may fail if you have tried to install the python 2 version of diffpy.structure in the python 3 environment.
	       If so, you may need to remove the pip cache (which should be ~/.cache/pip) before trying this step again.
  
* Now you can install `braggedgemodeling` by::
     
  $ git clone https://github.com/ornlneutronimaging/braggedgemodeling.git
  $ cd braggedgemodeling && python setup.py install --user



