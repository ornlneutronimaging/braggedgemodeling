# -*- Python -*-

import numpy as np
from danse.ins.matter import Lattice

def d(lattice, hkl):
    recbase = lattice.recbase # columns are rec base vectors
    recvec = np.dot(recbase, hkl)
    return 1./np.linalg.norm(recvec)

# End of file
