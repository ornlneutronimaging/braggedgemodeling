#!/usr/bin/env python
# Jiao Lin <jiao.lin@gmail.com>

from __future__ import print_function

interactive = False

import os, sys, numpy as np
from bem import xscalc, diffraction
from bem.matter import fccNi
thisdir = os.path.abspath(os.path.dirname(__file__))


def _test_Fe():
    d = laz.read("Fe.laz")
    peaks = [
        xscalc.DiffrPeak(hkl, F, d, mult)
        for hkl, F, d, mult in zip(d['hkl'], d['F'], d['d'], d['mult'])
        ]
    # "An experimental determination of the Debye-Waller factor for iron by neutron diffraction" S K Mohanlal
    # Journal of Physics C: Solid State Physics, Volume 12, Number 17
    B = 0.35
    Fe = xscalc.XSCalculator('Fe', 11.22, 0.4, 2.56, 2.886**3, peaks, B)
    print(Fe.xs(2200))
    lambdas = np.arange(0.05, 5.5, 0.001)
    xs = [Fe.xs_coh(l) for l in lambdas]
    from matplotlib import pyplot as plt
    plt.plot(lambdas, xs)
    plt.show()
    return


def test_fccNi():
    lambdas = np.arange(0.05, 5.5, 0.001)
    T = 300
    calc = xscalc.XSCalculator(fccNi, T)
    coh_el_xs = [calc.xs_coh_el(l) for l in lambdas]
    data = np.array([lambdas, coh_el_xs])
    expected = np.load(os.path.join(thisdir, 'expected', 'fccNi-coh-el-xs.npy'))
    assert np.isclose(data, expected).all()

    if not interactive:
        import matplotlib as mpl
        mpl.use('Agg')
    from matplotlib import pyplot as plt        
    calc.plotAll(lambdas)
    if interactive:
        plt.show()
    return

def test_fccNi_onepeak():
    lambdas = np.arange(0.05, 5.5, 0.001)
    T = 300
    calc = xscalc.XSCalculator(fccNi, T)

    xs = calc.xs_coh_el__peak(lambdas, calc.diffpeaks[6])
    if interactive:
        from matplotlib import pyplot as plt
        plt.plot(lambdas, xs)
        plt.show()
    return

def test_fccNi2():
    lambdas = np.arange(0.05, 5.5, 0.001)
    T = 300
    calc = xscalc.XSCalculator(fccNi, T)
    # coherent
    coh_el_xs = calc.xs_coh_el(lambdas)
    data = np.array([lambdas, coh_el_xs])
    expected = np.load(os.path.join(thisdir, 'expected', 'fccNi-coh-el-xs.npy'))
    # total
    assert np.isclose(data, expected).all()
    xs = calc.xs(lambdas)
    if interactive:
        from matplotlib import pyplot as plt
        plt.plot(lambdas, xs)
        plt.show()
    return

def main():
    global interactive
    interactive = True
    # _test_Fe()
    test_fccNi()
    test_fccNi_onepeak()
    test_fccNi2()
    return

if __name__ == '__main__': main()

# End of file
