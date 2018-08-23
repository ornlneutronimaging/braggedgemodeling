#!/usr/bin/env python
# Jiao Lin <jiao.lin@gmail.com>

interactive = False

import os, numpy as np
from bem import xscalc, diffraction, xtaloriprobmodel as xopm
from bem.matter import bccFe

thisdir = os.path.dirname(__file__)

def test_bccFe():
    lambdas = np.arange(0.05, 5, 0.01)
    T = 300
    texture_model = xopm.MarchDollase()
    calc = xscalc.XSCalculator(bccFe, T, texture_model, max_diffraction_index=5)
    xs_0 = calc.xs(lambdas)
    # r = 2, beta = 60.
    texture_model.r[(0,1,1)] = 2
    texture_model.beta[(0,1,1)] = 60./180.*np.pi
    xs_60 = calc.xs(lambdas)
    # r = 1.2, beta = 30
    texture_model.r[(0,1,1)] = 1.2
    texture_model.beta[(0,1,1)] = 30./180.*np.pi
    xs_30 = calc.xs(lambdas)
    # r = 1.2, beta = 30
    texture_model.r[(0,1,1)] = 1.2
    texture_model.beta[(0,1,1)] = 90./180.*np.pi
    xs_90 = calc.xs(lambdas)
    data = np.array([lambdas, xs_0, xs_30, xs_60, xs_90])
    # np.save(os.path.join(thisdir, 'expected', 'bccFe-texture-xs.npy'), data)
    expected = np.load(os.path.join(thisdir, 'expected', 'bccFe-texture-xs.npy'))
    assert np.isclose(data, expected).all()
    
    if interactive:
        from matplotlib import pyplot as plt
        plt.plot(lambdas, xs_0, label='r=1, isotropic')
        plt.plot(lambdas, xs_30, label='r=1.2, $\\beta=30^\\circ$')
        plt.plot(lambdas, xs_60, label='r=2.0, $\\beta=60^\\circ$')
        plt.plot(lambdas, xs_90, label='r=1.2, $\\beta=90^\\circ$')
        plt.legend(loc='upper left')
        plt.show()
    return

def main():
    global interactive
    interactive = True
    test_bccFe()
    return

if __name__ == '__main__': main()

# End of file
