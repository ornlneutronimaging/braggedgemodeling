#!/usr/bin/env python
# Jiao Lin <jiao.lin@gmail.com>

interactive = False

import os, numpy as np
from bem import xscalc, peak_profile as pp
from bem.matter import fccNi

thisdir = os.path.dirname(__file__)

def test_fccNi_onepeak():
    lambdas = np.arange(0.05, 5.5, 0.001)
    T = 300
    calc = xscalc.XSCalculator(fccNi, T)

    pk = calc.diffpeaks[6]
    xs = calc.xs_coh_el__peak(lambdas, pk)
    jorgensen = pp.Jorgensen(alpha=[1., 0.], beta=[2., 0], sigma=[0, 30e-3, 0])
    jorgensen.set_d_spacing(pk.d)
    spectrum = jorgensen.convolve(lambdas, xs)
    
    if interactive:
        from matplotlib import pyplot as plt
        plt.plot(lambdas, xs, label='cross section')
        plt.plot(lambdas, spectrum, label='convolved')
        plt.legend()
        plt.show()
    return

def main():
    global interactive
    interactive = True
    test_fccNi_onepeak()
    return

if __name__ == '__main__': main()

# End of file
