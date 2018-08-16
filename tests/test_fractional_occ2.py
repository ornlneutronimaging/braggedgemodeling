#!/usr/bin/env python
# Jiao Lin <jiao.lin@gmail.com>

interactive = False

import os, numpy as np
from bem import xscalc, diffraction, matter
thisdir = os.path.dirname(__file__)

atoms = [
    matter.Atom('Ni', (0,0,0), occupancy=0.5444), matter.Atom('Ni', (0.5, 0.5, 0), occupancy = 0.5444),
    matter.Atom('Ni', (0.5,0,0.5), occupancy = 0.5444), matter.Atom('Ni', (0, 0.5, 0.5), occupancy = 0.5444),
    matter.Atom('Fe', (0,0,0), occupancy=0.20685), matter.Atom('Fe', (0.5, 0.5, 0), occupancy=0.20685),
    matter.Atom('Fe', (0.5,0,0.5), occupancy=0.20685), matter.Atom('Fe', (0, 0.5, 0.5), occupancy=0.20685),
    matter.Atom('Cr', (0,0,0), occupancy=0.22925), matter.Atom('Cr', (0.5, 0.5, 0), occupancy=0.22925),
    matter.Atom('Cr', (0.5,0,0.5), occupancy=0.22925), matter.Atom('Cr', (0, 0.5, 0.5), occupancy=0.22925),
    matter.Atom('Mo', (0,0,0), occupancy=0.01953), matter.Atom('Mo', (0.5, 0.5, 0), occupancy=0.01953),
    matter.Atom('Mo', (0.5,0,0.5), occupancy=0.01953), matter.Atom('Mo', (0, 0.5, 0.5), occupancy=0.01953)
]
a=3.61
alpha = 90.
lattice = matter.Lattice(a=a, b=a, c=a, alpha=alpha, beta=alpha, gamma=alpha)
mat = matter.Structure(atoms, lattice, sgid=225)

def test():
    lambdas = np.arange(0.05, 5.5, 0.001)
    T = 300
    calc = xscalc.XSCalculator(mat, T)
    xs = [calc.xs(l) for l in lambdas]
    # np.save('expected/NiFeCrMo-xs.npy', np.array([lambdas, xs]).T)
    expected = np.load(os.path.join(thisdir, 'expected', 'NiFeCrMo-xs.npy'))
    assert np.allclose(expected[:, 1], xs)
    if interactive:
        from matplotlib import pyplot as plt
        plt.plot(lambdas, xs)
        plt.show()
    return

def main():
    global interactive
    interactive = True
    test()
    return

if __name__ == '__main__': main()

# End of file
