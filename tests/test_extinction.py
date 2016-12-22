#!/usr/bin/env python
# Jiao Lin <jiao.lin@gmail.com>

interactive = False

import numpy as np
from bem import xscalc, diffraction
from fccNi import fccNi

def test_fccNi():
    lambdas = np.arange(0.05, 5.5, 0.001)
    T = 300
    calc = xscalc.XSCalculator(fccNi, T, size=10e-6)
    xs = [calc.xs(l) for l in lambdas]
    if interactive:
        from matplotlib import pyplot as plt
        plt.plot(lambdas, xs)
        plt.show()
    return

def main():
    global interactive
    interactive = True
    test_fccNi()
    return

if __name__ == '__main__': main()

# End of file
