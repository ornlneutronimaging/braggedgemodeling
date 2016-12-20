# -*- Python -*-
# Jiao Lin <jiao.lin@gmail.com>

import numpy as np
from numpy import pi
from .xtaloriprobmodel import IsotropicXOPM

class XSCalculator:

    def __init__(self, structure, T, xopm=None, max_diffraction_index=5):
        self.name = structure.description
        occs = np.array([atom.occupancy for atom in structure])
        from atomic_scattering import AtomicScattering as AS
        sctts = self.sctts = [AS(atom.symbol) for atom in structure]
        bs = np.array([sc.b() for sc in sctts])
        inc_xss = np.array([sc.sigma_inc() for sc in sctts])
        abs_xss = np.array([sc.sigma_abs() for sc in sctts])
        def average(occs, qs):
            return np.sum(occs*qs)/np.sum(occs)
        self.coh_xs = average(occs, bs) **2*4*np.pi / 100
        self.inc_xs = average(occs, bs*bs)*4*np.pi/100 - self.coh_xs + average(occs, inc_xss)
        self.abs_xs_at2200 = np.sum(occs*abs_xss)
        self.uc_vol = structure.lattice.getVolume()
        self.structure = structure
        # temperature dependent
        self.T = T
        from . import diffraction
        self.diffpeaks = list(diffraction.iter_peaks(structure, T, max_index=max_diffraction_index))
        self.xopm = xopm or IsotropicXOPM()
        return

    def xs(self, wavelen):
        """wavelen: angstom
        return: cross section in barns
        """
        abs = self.xs_abs(wavelen)
        coh_el = self.xs_coh_el(wavelen)
        inc_el = self.xs_inc_el(wavelen)
        inel = self.xs_inel(wavelen)
        return abs+coh_el+inc_el+inel

    def xs_inel(self, wavelen):
        ss = [sc.S_inel_inc(wavelen, self.T) for sc in self.sctts]
        return (self.coh_xs + self.inc_xs)*np.sum(ss)

    def xs_inc_el(self, wavelen):
        sctts = self.sctts
        S = np.sum([sc.S_el_inc(wavelen, self.T) for sc in sctts])
        return self.inc_xs * S

    def xs_coh_el(self, wavelen):
        "unit: barn"
        vs = [np.abs(p.F)**2*p.d*p.mult*self.xopm(p, wavelen) for p in self.diffpeaks if p.d*2>wavelen]
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
