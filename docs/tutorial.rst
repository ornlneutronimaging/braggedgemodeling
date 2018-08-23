.. _tutorial:

Tutorial
========

Please see :ref:`installation` before start here.

Cross section
-------------

Let us start by creating an atomic structure::

  from bem.matter import Atom, Lattice, Structure
  atoms = [Atom('Ni', (0,0,0)), Atom('Ni', (0.5, 0.5, 0)),
           Atom('Ni', (0.5,0,0.5)), Atom('Ni', (0, 0.5, 0.5))]
  a=3.5238
  alpha = 90.
  lattice = Lattice(a=a, b=a, c=a, alpha=alpha, beta=alpha, gamma=alpha)
  fccNi = Structure(atoms, lattice, sgid=225)

Then we can perform a simple Bragg Edge neutron cross section calculation and plot them::

  # define wavelength axis
  import numpy as np
  wavelengths = np.arange(0.05, 5.5, 0.005)
  T = 300
  # create calculator
  from bem import xscalc
  xscalculator = xscalc.XSCalculator(fccNi, T, max_diffraction_index=7)
  # compute various contributions
  # In neutron Bragg Edge data analysis, it may not be necessary to calculate all these
  # contributions, but it is useful to see them when exploring.
  coh_el_xs = xscalculator.xs_coh_el(wavelengths)
  inc_el_xs = xscalculator.xs_inc_el(wavelengths)
  abs_xs = xscalculator.xs_abs(wavelengths)
  coh_inel_xs = xscalculator.xs_coh_inel(wavelengths)
  inc_inel_xs = xscalculator.xs_inc_inel(wavelengths)
  # and the total cross section
  total = xscalculator.xs(wavelengths)
  # plot
  from matplotlib import pyplot as plt
  plt.plot(wavelengths, coh_el_xs, label='coh el')
  plt.plot(wavelengths, inc_el_xs, label='inc el')
  plt.plot(wavelengths, coh_inel_xs, label='coh inel')
  plt.plot(wavelengths, inc_inel_xs, label='inc inel')
  plt.plot(wavelengths, abs_xs, label='abs')
  plt.plot(wavelengths, total, label='total')
  plt.ylim(-0.2, None)
  plt.xlim(0,7)
  plt.legend()
  plt.show()


Texture
-------

To introduce texture into the sample, we can use a texture model::

  from bem import xtaloriprobmodel as xopm
  texture_model = xopm.MarchDollase()
  texture_model.r[(0,0,1)] = 2

Now we recreate the calculator using this texture model::
  
  xscalculator = xscalc.XSCalculator(fccNi, T, texture_model)

And replot::
    
  xscalculator.plotAll(wavelengths)
  plt.show()

The "plotAll" method simplifies plotting.


Peak profile
------------

To take instrument broadening into account::
  
  from bem import peak_profile as pp, calc
  jorgensen = pp.Jorgensen(alpha=[50, 0.], beta=[10, 0], sigma=[0, .003, 0])
  spectrum_calculator = calc.BraggEdgeSpectrumCalculator(xscalculator, jorgensen)
  # calculate total cross section convolved with peak profile
  spectrum = spectrum_calculator('total', wavelengths)
  # plot it
  plt.plot(wavelengths, spectrum)
  # also plot the cross sections
  xscalculator.plotAll(wavelengths)
  plt.show()
