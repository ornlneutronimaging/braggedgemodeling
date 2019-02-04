#!/usr/bin/env python

import pytest
pytest.importorskip("matlab")

import os

here = os.path.dirname(__file__)

infile = os.path.join(here, '..', 'data', 'vdrive_filename.txt')
interm = 'vulcan.intermediate'
rpffile = 'vulcan.rpf'
vpscfile = 'vpsc.txt'
hkls = [[1,1,1], [2,0,0], [2,2,0], [2,2,2]]


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
    mtex.polfig2VPSC(rpffile, hkls, vpscfile)
    return

def test3():
    # texture -> R
    from bem import matter
    # FCC
    atoms = [matter.Atom('Ni', (0,0,0)), matter.Atom('Ni', (0.5, 0.5, 0)),
             matter.Atom('Ni', (0.5,0,0.5)), matter.Atom('Ni', (0, 0.5, 0.5))]
    # a=3.5238
    a=3.60  # this is inferred from the d-spacing values in the original fortran file
    alpha = 90.
    lattice = matter.Lattice(a=a, b=a, c=a, alpha=alpha, beta=alpha, gamma=alpha)
    fccNi = matter.Structure(atoms, lattice, sgid=225)
    from bem.texture import texture2R
    texture2R.compute(
        fccNi,
        tex = vpscfile,
        N_RD = 36,
        N_HD = 144,
        out = 'R_samples.dat',
        max_hkl_index=5,
        )
    return


def main():
    test1()
    test2()
    test3()
    return


if __name__ == '__main__': main()
