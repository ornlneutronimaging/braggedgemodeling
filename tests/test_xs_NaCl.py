#!/usr/bin/env python
# Jiao Lin <jiao.lin@gmail.com>

interactive = False

import os, numpy as np
from bem import xscalc, diffraction, matter

thisdir = os.path.dirname(__file__)
NaCl = matter.loadCif(os.path.join(thisdir, 'NaCl.cif'))


def test_NaCl():
    lambdas = np.arange(1.5, 7, 0.01)
    T = 300
    # if max_diffraction_index is too small, the low wavelength portion will be a bit off
    calc = xscalc.XSCalculator(NaCl, T, max_diffraction_index=7)
    coh_el_xs = calc.xs_coh_el(lambdas)
    inc_el_xs = calc.xs_inc_el(lambdas)
    inel_xs = calc.xs_inel(lambdas)
    abs_xs = calc.xs_abs(lambdas)
    coh_inel_xs = calc.xs_coh_inel(lambdas)
    inc_inel_xs = calc.xs_inc_inel(lambdas)
    total = calc.xs(lambdas)
    data = np.array([lambdas, total])
    # np.save(os.path.join(thisdir, 'expected', 'NaCl-total-xs.npy'), data)
    expected = np.load(os.path.join(thisdir, 'expected', 'NaCl-total-xs.npy'))
    assert np.isclose(data, expected).all()

    if interactive:
        from matplotlib import pyplot as plt
        plt.figure(figsize=(9,4))
        # *4 to match what is done in "nxs" paper
        plt.plot(lambdas, coh_el_xs*4, label='coh el')
        plt.plot(lambdas, inc_el_xs*4, label='inc el')
        plt.plot(lambdas, coh_inel_xs*4, label='coh inel')
        plt.plot(lambdas, inc_inel_xs*4, label='inc inel')
        # plt.plot(lambdas, inel_xs, label='inel')
        plt.plot(lambdas, abs_xs, label='abs')
        plt.plot(lambdas, total, label='total')
        plt.ylim(-0.2, None)
        plt.xlim(2,9)
        plt.legend()
        plt.show()
    return

def main():
    global interactive
    interactive = True
    test_NaCl()
    return

if __name__ == '__main__': main()

# End of file
