#!/usr/bin/env python

import os
from bem.texture.preparation.vdrive_handler import VDriveHandler
from bem.texture.preparation.vdrive_to_mtex import VDriveToMtex

here = os.path.dirname(__file__)

def test():
    infile = os.path.join(here, '..', 'data', 'vdrive_filename.txt')
    interm = 'vulcan.intermediate'
    outfile = 'vulcan.rpf'
    o_vdrive = VDriveHandler(filename = infile)
    o_vdrive.run()
    o_vdrive.export(filename = interm)

    o_handler = VDriveToMtex(interm)
    o_handler.run()
    o_handler.export(filename = outfile)
    return


if __name__ == '__main__': test()
