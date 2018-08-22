.. _tutorial:

Tutorial
========

Please see :ref:`installation` before start here.


Let us start by create an atomic structure::

  from bem.matter import Atom, Lattice, Structure
  atoms = [Atom('Al', (0,0,0)), Atom('Al', (0.5, 0.5, 0)),
           Atom('Al', (0.5,0,0.5)), Atom('Al', (0, 0.5, 0.5))]
  a=4.046
  alpha = 90.
  lattice = Lattice(a=a, b=a, c=a, alpha=alpha, beta=alpha, gamma=alpha)
  fccAl = Structure(atoms, lattice, sgid=225)

Then we can perform a simple Bragg Edge neutron cross section calculation and plot them::

  # define wavelength axis
  import numpy as np
  lambdas = np.arange(0.05, 5.5, 0.005)
  T = 300
  # create calculator
  from bem import xscalc
  calc = xscalc.XSCalculator(fccAl, T, max_diffraction_index=7)
  # compute various contributions
  # In neutron Bragg Edge data analysis, it may not be necessary to calculate all these
  # contributions, but it is useful to see them when exploring.
  coh_el_xs = calc.xs_coh_el(lambdas)
  inc_el_xs = calc.xs_inc_el(lambdas)
  abs_xs = calc.xs_abs(lambdas)
  coh_inel_xs = calc.xs_coh_inel(lambdas)
  inc_inel_xs = calc.xs_inc_inel(lambdas)
  # and the total cross section
  total = calc.xs(lambdas)
  # plot
  from matplotlib import pyplot as plt
  plt.plot(lambdas, coh_el_xs, label='coh el')
  plt.plot(lambdas, inc_el_xs, label='inc el')
  plt.plot(lambdas, coh_inel_xs, label='coh inel')
  plt.plot(lambdas, inc_inel_xs, label='inc inel')
  plt.plot(lambdas, abs_xs, label='abs')
  plt.plot(lambdas, total, label='total')
  plt.ylim(-0.2, None)
  plt.xlim(0,7)
  plt.legend()
  plt.show()
