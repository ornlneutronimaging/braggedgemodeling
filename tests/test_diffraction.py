#!/usr/bin/env python

import numpy as np
from bem import diffraction
from danse.ins import matter

from fccNi import fccNi


def test_F_i():
    assert np.isclose(diffraction.F_i(0, fccNi, (1,1,1), 300), 10.11, rtol=0.002)
    return

def test_F():
    assert np.isclose(diffraction.F(fccNi, (1,1,1), 300), 40.44, rtol=0.002)
    assert np.isclose(diffraction.F(fccNi, (2,0,0), 300), 40.19, rtol=0.002)
    assert np.isclose(diffraction.F(fccNi, (4,4,4), 300), 30.6, rtol=0.002)
    return

def test_d():
    assert np.isclose(diffraction.d(fccNi.lattice, (1,1,1)), 2.03447)
    return

def test_peaks():
    for pk in diffraction.iter_peaks(fccNi, 300):
        print pk
    return


def main():
    test_F_i()
    test_F()
    test_d()
    test_peaks()
    return


if __name__ == '__main__': main()


# End of file
