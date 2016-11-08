# -*- Python -*-
# Jiao Lin <jiao.lin@gmail.com>

import numpy as np
from numpy import pi

class XSCalculator:

    def __init__(self, structure, T):
        self.name = structure.description
        occs = np.array([atom.occupancy for atom in structure])
        from atomic_scattering import AtomicScattering as AS
        sctts = [AS(atom.symbol) for atom in structure]
        bs = np.array([sc.b() for sc in sctts])
        inc_xss = np.array([sc.sigma_inc() for sc in sctts])
        abs_xss = np.array([sc.sigma_abs() for sc in sctts])
        self.coh_xs = (occs * bs).sum()**2*4*np.pi
        self.inc_xs = (occs*bs*bs).sum()*4*np.pi - self.coh_xs + (occs*inc_xss).sum()
        self.abs_xs_at2200 = abs_xss.sum()
        self.uc_vol = structure.lattice.getVolume()
        self.structure = structure
        # temperature dependent
        self.T = T
        from . import diffraction
        self.diffpeaks = list(diffraction.iter_peaks(structure, T, max_index=5))
        return

    def xs(self, wavelen):
        """wavelen: angstom
        """
        abs = self.xs_abs(wavelen)
        coh = self.xs_coh(wavelen)
        inc = self.xs_inc(wavelen)
        return abs+coh+inc

    def xs_inc(self, wavelen):
        return self.xs_inc_el(wavelen) + self.xs_inc_inel(wavelen)

    def xs_coh(self, wavelen):
        return self.xs_coh_el(wavelen) + self.xs_coh_inel(wavelen)

    def xs_coh_inel(self, wavelen):
        return 0

    def xs_inc_inel(self, wavelen):
        return 0

    def xs_inc_el(self, wavelen):
        DW = self.B/wavelen/wavelen
        return self.inc_xs * (1./(2*DW))* (1-np.exp(-2*DW))

    def xs_coh_el(self, wavelen):
        "unit: barn"
        vs = [np.abs(p.F)**2*p.d*p.mult for p in self.diffpeaks if p.d*2>wavelen]
        vs = np.array(vs) # unit fm^2
        # print wavelen, vs * wavelen*wavelen/(2*self.uc_vol)
        return np.sum(vs)/100 * wavelen*wavelen/(2*self.uc_vol) # unit: barn

    def xs_abs(self, wavelen):
        Q = 2*pi/wavelen
        from mcni.utils.conversion import K2V
        v = K2V*Q
        return self.abs_xs_at2200/v*2200


if __name__ == '__main__': test()


# End of file
