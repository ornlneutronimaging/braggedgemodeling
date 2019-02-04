#!/usr/bin/env python

import pytest
pytest.importorskip("matlab")

import os

here = os.path.dirname(__file__)

def test():
    # vdrive_filename.txt -> vulcan.rpf
    infile = os.path.join(here, '..', 'data', 'vdrive_filename.txt')
    interm = 'vulcan.intermediate'
    rpffile = 'vulcan.rpf'
    from bem.texture.preparation.vdrive_handler import VDriveHandler
    from bem.texture.preparation.vdrive_to_mtex import VDriveToMtex
    o_vdrive = VDriveHandler(filename = infile)
    o_vdrive.run()
    o_vdrive.export(filename = interm)

    o_handler = VDriveToMtex(interm)
    o_handler.run()
    o_handler.export(filename = rpffile)

    # vulcan.rpf -> vpsc.txt
    vpscfile = 'vpsc.txt'
    hkls = [[1,1,1], [2,0,0], [2,2,0], [2,2,2]]
    from bem.texture import mtex
    mtex.setup()
    mtex.polfig2VPSC(rpffile, hkls, vpscfile)
    return


if __name__ == '__main__': test()
