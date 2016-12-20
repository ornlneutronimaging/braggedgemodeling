#!/usr/bin/env python
# Jiao Lin <jiao.lin@gmail.com>

interactive = False

import numpy as np
from bem import xscalc, diffraction, matter

atoms = [
    matter.Atom('Ni', (0,0,0), occupancy=0.5), matter.Atom('Ni', (0.5, 0.5, 0), occupancy=0.5),
    matter.Atom('Ni', (0.5,0,0.5), occupancy=0.5), matter.Atom('Ni', (0, 0.5, 0.5), occupancy=0.5),
    matter.Atom('Cr', (0,0,0), occupancy=0.5), matter.Atom('Cr', (0.5, 0.5, 0), occupancy=0.5),
    matter.Atom('Cr', (0.5,0,0.5), occupancy=0.5), matter.Atom('Cr', (0, 0.5, 0.5), occupancy=0.5),
]
a=3.5238
alpha = 90.
lattice = matter.Lattice(a=a, b=a, c=a, alpha=alpha, beta=alpha, gamma=alpha)
NiCr = matter.Structure(atoms, lattice, sgid=225)

def test():
    lambdas = np.arange(0.05, 5.5, 0.001)
    T = 300
    calc = xscalc.XSCalculator(NiCr, T, max_diffraction_index=1)
    assert np.isclose(calc.coh_xs, ((10.3+3.635)/2)**2*4*np.pi/100)
    assert np.isclose(calc.inc_xs, 4*np.pi*((10.3**2+3.635**2)/2.-((10.3+3.635)/2.)**2)/100. + (5.2+1.83)/2)
    return

def main():
    global interactive
    interactive = True
    test()
    return

if __name__ == '__main__': main()

# End of file
