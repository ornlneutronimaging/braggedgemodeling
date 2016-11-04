# -*- Python -*-

import numpy as np
import periodictable as pt


def iter_peaks(structure, T, max_index=5):
    for h in range(max_index):
        for k in range(max_index):
            for l in range(max_index):
                if h+k+l==0: continue
                q1 = h,k,l
                F1 = F(structure, q1, T)
                d1 = d(structure.lattice, q1)
                mult1 = multiplicity(q1, structure.sg)
                if np.abs(F1) > 1e-7:
                    yield DiffrPeak(q1, F1, d1, mult1)
    return


class DiffrPeak:
    
    def __init__(self, hkl, F, d, mult):
        self.hkl = hkl
        self.F = F
        self.d = d
        self.mult = mult
        return

    def __repr__(self):
        return "DiffrPeak(%s, F=%r, d=%r, mult=%r)" % (self.hkl, self.F, self.d, self.mult)


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
