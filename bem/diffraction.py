# -*- Python -*-

import numpy as np
import periodictable as pt


def F(structure, hkl, T):
    fs = [F_i(i, structure, hkl, T) 
          for i in range(len(structure))]
    return sum(fs)

def F_i(i, structure, hkl, T):
    from .DebyeWaller import B
    atom = structure[i]
    B = B(atom.symbol, T)
    d1 = d(structure.lattice, hkl)
    position = atom.xyz
    o = atom.occupancy
    b = getattr(pt, atom.symbol).neutron.b_c
    return o*b*np.exp(2*np.pi*1j*np.dot(hkl, position) - B/4/d1/d1)


def d(lattice, hkl):
    recbase = lattice.recbase # columns are rec base vectors
    recvec = np.dot(recbase, hkl)
    return 1./np.linalg.norm(recvec)


def multiplicity(hkl, sg):
    vs = []
    for symop in sg.symop_list:
        v1 = np.dot(symop.R, hkl)
        added=False
        for v2 in vs:
            if np.isclose(v1, v2, atol=1e-7).all():
                added=True
                break
            continue
        if not added:
            vs.append(v1)
        continue
    return len(vs)


# End of file
