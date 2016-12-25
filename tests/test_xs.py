#!/usr/bin/env python
# Jiao Lin <jiao.lin@gmail.com>

interactive = False

import numpy as np
from bem import xscalc, diffraction
from fccNi import fccNi

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
    print Fe.xs(2200)
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
    expected = np.load('fccNi-coh-el-xs.npy')
    assert np.isclose(data, expected).all()

    inc_el_xs = [calc.xs_inc_el(l) for l in lambdas]
    inel_xs = [calc.xs_inel(l) for l in lambdas]
    abs_xs = np.array([calc.xs_abs(l) for l in lambdas])
    if interactive:
        from matplotlib import pyplot as plt
        plt.plot(lambdas, coh_el_xs)
        plt.plot(lambdas, inc_el_xs)
        plt.plot(lambdas, inel_xs)
        plt.plot(lambdas, abs_xs)
        plt.plot(lambdas, abs_xs+coh_el_xs+inc_el_xs+inel_xs)
        plt.show()
    return

def test_fccNi2():
    lambdas = np.arange(0.05, 5.5, 0.001)
    T = 300
    calc = xscalc.XSCalculator(fccNi, T)
    # coherent
    coh_el_xs = calc.xs_coh_el(lambdas)
    data = np.array([lambdas, coh_el_xs])
    expected = np.load('fccNi-coh-el-xs.npy')
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
    # test_Fe()
    test_fccNi()
    test_fccNi2()
    return

if __name__ == '__main__': main()

# End of file
