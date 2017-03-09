#!/usr/bin/env python
# Jiao Lin <jiao.lin@gmail.com>

interactive = False

import os, numpy as np
from bem import xscalc, peak_profile as pp, calc
from fccNi import fccNi

thisdir = os.path.dirname(__file__)

def test_fccNi():
    lambdas = np.arange(0.05, 5.5, 0.001)
    T = 300
    xs_calculator = xscalc.XSCalculator(fccNi, T)
    jorgensen = pp.Jorgensen(alpha=[1., 0.], beta=[2., 0], sigma=[0, 30e-3, 0])
    spectrum_calculator = calc.BraggEdgeSpectrumCalculator(xs_calculator, jorgensen)
    
    spectrum = spectrum_calculator('total', lambdas)
    xs = xs_calculator.xs(lambdas)
    
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
    test_fccNi()
    return

if __name__ == '__main__': main()

# End of file
