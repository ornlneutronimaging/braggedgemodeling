#!/usr/bin/env python
# Jiao Lin <jiao.lin@gmail.com>

import os, numpy as np
from bem import xscalc, diffraction
from bem import xtaloriprobmodel as xopm
from bem.matter import fccAl

thisdir = os.path.dirname(__file__)

def test1():
    lambdas = np.arange(0.05, 5.5, 0.005)
    T = 300
    # if max_diffraction_index is too small, the low wavelength portion will be a bit off
    calc = xscalc.XSCalculator(fccAl, T, max_diffraction_index=8)
    calc.xs_coh_el(1.5)
    coh_el_xs = calc.xs_coh_el(lambdas)
    inc_el_xs = calc.xs_inc_el(lambdas)
    inel_xs = calc.xs_inel(lambdas)
    abs_xs = calc.xs_abs(lambdas)
    coh_inel_xs = calc.xs_coh_inel(lambdas)
    inc_inel_xs = calc.xs_inc_inel(lambdas)
    total = calc.xs(lambdas)
    for i,l in enumerate(lambdas):
        assert np.isclose(calc.xs_coh_el(l), coh_el_xs[i])
        assert np.isclose(calc.xs_inc_el(l), inc_el_xs[i])
        assert np.isclose(calc.xs_inel(l), inel_xs[i])
        assert np.isclose(calc.xs_abs(l), abs_xs[i])
        assert np.isclose(calc.xs_coh_inel(l), coh_inel_xs[i])
        assert np.isclose(calc.xs_inc_inel(l), inc_inel_xs[i])
        assert np.isclose(calc.xs(l), total[i])
        continue
    return


def test2():
    lambdas = np.arange(0.05, 5.5, 0.005)
    T = 300
    texture_model = xopm.MarchDollase()
    texture_model.r[(0,1,1)] = 2
    texture_model.beta[(0,1,1)] = np.deg2rad(60.)

    calc = xscalc.XSCalculator(fccAl, T, texture_model, max_diffraction_index=8)
    calc.xs_coh_el(1.5)
    coh_el_xs = calc.xs_coh_el(lambdas)
    inc_el_xs = calc.xs_inc_el(lambdas)
    inel_xs = calc.xs_inel(lambdas)
    abs_xs = calc.xs_abs(lambdas)
    coh_inel_xs = calc.xs_coh_inel(lambdas)
    inc_inel_xs = calc.xs_inc_inel(lambdas)
    total = calc.xs(lambdas)
    for i,l in enumerate(lambdas):
        assert np.isclose(calc.xs_coh_el(l), coh_el_xs[i])
        assert np.isclose(calc.xs_inc_el(l), inc_el_xs[i])
        assert np.isclose(calc.xs_inel(l), inel_xs[i])
        assert np.isclose(calc.xs_abs(l), abs_xs[i])
        assert np.isclose(calc.xs_coh_inel(l), coh_inel_xs[i])
        assert np.isclose(calc.xs_inc_inel(l), inc_inel_xs[i])
        assert np.isclose(calc.xs(l), total[i])
        continue
    return


def main():
    test1()
    test2()
    return

if __name__ == '__main__': main()

# End of file
