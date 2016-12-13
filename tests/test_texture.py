#!/usr/bin/env python
# Jiao Lin <jiao.lin@gmail.com>

interactive = False

import numpy as np
from bem import xscalc, diffraction, xtaloriprobmodel as xopm
from fccNi import fccNi

def test_fccNi():
    lambdas = np.arange(0.05, 5.5, 0.001)
    T = 300
    texture_model = xopm.MarchDollase()
    texture_model.r[(0,0,1)] = 2
    calc = xscalc.XSCalculator(fccNi, T, texture_model)
    coh_el_xs = [calc.xs_coh_el(l) for l in lambdas]
    data = np.array([lambdas, coh_el_xs])
    # expected = np.load('fccNi-coh-el-xs.npy')
    # assert np.isclose(data, expected).all()

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

def main():
    global interactive
    interactive = True
    test_fccNi()
    return

if __name__ == '__main__': main()

# End of file
