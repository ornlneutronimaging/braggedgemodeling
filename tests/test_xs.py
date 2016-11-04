#!/usr/bin/env python
# Jiao Lin <jiao.lin@gmail.com>

import numpy as np
from bem import xscalc, diffraction
from fccNi import fccNi

def test_Fe():
    d = laz.read("Fe.laz")
    peaks = [
        xscalc.DiffrPeak(hkl, F, d, mult)
        for hkl, F, d, mult in zip(d['hkl'], d['F'], d['d'], d['mult'])
        ]
    # "An experimental determination of the Debye-Waller factor for iron by neutron diffraction" S K Mohanlal
    # Journal of Physics C: Solid State Physics, Volume 12, Number 17
    B = 0.35
    Fe = xscalc.XSCalculator('Fe', 11.22, 0.4, 2.56, 2.886**3, peaks, B)
    print Fe.xs(2200)
    lambdas = np.arange(0.05, 5.5, 0.001)
    xs = [Fe.xs_coh(l) for l in lambdas]
    from matplotlib import pyplot as plt
    plt.plot(lambdas, xs)
    plt.show()
    return


def test_fccNi():
    peaks = list(diffraction.iter_peaks(fccNi, 300, max_index=5))
    import periodictable as pt
    Ni_xs = pt.Ni.neutron
    Ni = xscalc.XSCalculator(
        'Ni',
        Ni_xs.coherent, Ni_xs.incoherent, Ni_xs.absorption,
        fccNi.lattice.getVolume(), peaks, B=0.5)
    print Ni.xs(2200)
    lambdas = np.arange(0.05, 5.5, 0.001)
    xs = [Ni.xs_coh(l) for l in lambdas]
    from matplotlib import pyplot as plt
    plt.plot(lambdas, xs)
    plt.show()
    return

def test():
    # test_Fe()
    test_fccNi()
    return

if __name__ == '__main__': test()

# End of file
