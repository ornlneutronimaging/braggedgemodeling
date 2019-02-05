#!/usr/bin/env python

import pytest
pytest.importorskip("matlab")

import os, numpy as np

here = os.path.dirname(__file__)

infile = os.path.join(here, '..', 'data', 'vdrive_filename.txt')
interm = 'vulcan.intermediate'
rpffile = 'vulcan.rpf'
vpscfile = 'vpsc.txt'
hkls = [[1,1,1], [2,0,0], [2,2,0], [2,2,2]]
Rsamples_file = 'Rsamples.dat'
from bem import matter
# FCC
atoms = [matter.Atom('Ni', (0,0,0)), matter.Atom('Ni', (0.5, 0.5, 0)),
         matter.Atom('Ni', (0.5,0,0.5)), matter.Atom('Ni', (0, 0.5, 0.5))]
# a=3.5238
a=3.60  # this is inferred from the d-spacing values in the original fortran file
alpha = 90.
lattice = matter.Lattice(a=a, b=a, c=a, alpha=alpha, beta=alpha, gamma=alpha)
fccNi = matter.Structure(atoms, lattice, sgid=225)


def test1():
    # vdrive_filename.txt -> vulcan.rpf
    from bem.texture.preparation.vdrive_handler import VDriveHandler
    from bem.texture.preparation.vdrive_to_mtex import VDriveToMtex
    o_vdrive = VDriveHandler(filename = infile)
    o_vdrive.run()
    o_vdrive.export(filename = interm)

    o_handler = VDriveToMtex(interm)
    o_handler.run()
    o_handler.export(filename = rpffile)
    return

def test2():
    # vulcan.rpf -> vpsc.txt
    from bem.texture import mtex
    mtex.setup()
    mtex.polfig2VPSC(rpffile, vpscfile, hkls, Npoints=20000)
    return

def test3():
    # texture -> R
    from bem.texture import texture2R
    return texture2R.compute(
        fccNi,
        tex = vpscfile,
        N_RD = 36,
        N_HD = 144,
        out = Rsamples_file,
        max_hkl_index=5,
        )

def test4():
    # cross section from R
    wavelengths = np.arange(0.05, 5.5, 0.001)
    T = 300
    from bem import xscalc
    calc = xscalc.XSCalculator(fccNi, T, max_diffraction_index=3)
    coh_el_xs = [calc.xs_coh_el(l) for l in wavelengths]
    # add texture
    from bem.texture import texture2R
    lambdas, Rs = texture2R.read_results(Rsamples_file)
    hkls = [eval(l) for l in open('hkls.txt').readlines()]
    from bem.texture.InterpolatedXOPM import InterpolatedXOPM
    texture_model = InterpolatedXOPM(hkls, lambdas, Rs)
    calc2 = xscalc.XSCalculator(fccNi, T, texture_model, max_diffraction_index=3)
    coh_el_xs2 = [calc2.xs_coh_el(l) for l in wavelengths]    
    from matplotlib import pyplot as plt
    plt.figure()
    plt.plot(wavelengths, coh_el_xs, label='no texture')
    plt.plot(wavelengths, coh_el_xs2, label='with texture')
    plt.legend()
    plt.savefig("coh_el.png")
    plt.close()
    return


def main():
    test1()
    test2()
    test3()
    test4()
    return


if __name__ == '__main__': main()
