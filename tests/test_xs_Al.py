#!/usr/bin/env python
# Jiao Lin <jiao.lin@gmail.com>

interactive = False

import os, numpy as np
from bem import xscalc, diffraction
from fccAl import fccAl

thisdir = os.path.dirname(__file__)

def test_fccAl():
    lambdas = np.arange(0.05, 5.5, 0.001)
    T = 300
    # if max_diffraction_index is too small, the low wavelength portion will be a bit off
    calc = xscalc.XSCalculator(fccAl, T, max_diffraction_index=15)
    coh_el_xs = calc.xs_coh_el(lambdas)
    # data = np.array([lambdas, coh_el_xs])
    # expected = np.load(os.path.join(thisdir, 'fccAl-coh-el-xs.npy'))
    # assert np.isclose(data, expected).all()

    inc_el_xs = calc.xs_inc_el(lambdas)
    inel_xs = calc.xs_inel(lambdas)
    abs_xs = calc.xs_abs(lambdas)
    coh_inel_xs = calc.xs_coh_inel(lambdas)
    inc_inel_xs = calc.xs_inc_inel(lambdas)
    if interactive:
        from matplotlib import pyplot as plt
        plt.plot(lambdas, coh_el_xs, label='coh el')
        plt.plot(lambdas, inc_el_xs, label='inc el')
        plt.plot(lambdas, coh_inel_xs, label='coh inel')
        plt.plot(lambdas, inc_inel_xs, label='inc inel')
        # plt.plot(lambdas, inel_xs, label='inel')
        plt.plot(lambdas, abs_xs, label='abs')
        plt.plot(lambdas, abs_xs+coh_el_xs+inc_el_xs+inel_xs, label='sum')
        plt.ylim(-0.2, None)
        plt.xlim(0,7)
        plt.legend()
        plt.show()
    return

def main():
    global interactive
    interactive = True
    test_fccAl()
    return

if __name__ == '__main__': main()

# End of file
