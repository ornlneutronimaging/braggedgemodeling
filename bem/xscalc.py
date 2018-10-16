# -*- Python -*-
# Jiao Lin <jiao.lin@gmail.com>

import numpy as np
from numpy import pi
from .xtaloriprobmodel import IsotropicXOPM

class XSCalculator:

    """Cross section calculator

    This class implements formulas in Chapter 3, section 2 of Sven Vogel's thesis,
    "A Rietveld-approach for the analysis of neutron time-of-flight transmission data"
    """

    example_code = """
    >>> xc = XSCalculator(structure, T, xopm=, size=, max_diffraction_index=)
    >>> xc.xs(wavelen)                         # compute total cross section
    >>> xc.diffpeaks                           # show diffraction peaks
    >>> xc.xopm(peak=, wavelen=)               # compute factor due to orientation distribution (texture)
    """

    def __init__(self, structure, T, xopm=None, max_diffraction_index=5, size=0):
        """constructor

        Parameters
        ----------
        structure : diffpy.structure
            lattice structure

        T : float
            temperature (Kelvin)

        max_diffraction_index : int, optional
            max integer for h,k, and l

        xopm : xtaloriprobmodel.XtalOriProbModel, optional
            crystal orientation probability model

        size : int, optional
            size of crystallites along beam (for extinction effect calculation)
        """
        self.name = structure.title
        occs = np.array([atom.occupancy for atom in structure])
        from .atomic_scattering import AtomicScattering as AS
        sctts = self.sctts = [AS(atom.element, occupancy=atom.occupancy) for atom in structure]
        bs = np.array([sc.b() for sc in sctts])
        inc_xss = np.array([sc.sigma_inc() for sc in sctts])
        abs_xss = np.array([sc.sigma_abs() for sc in sctts])
        def average(occs, qs):
            return np.sum(occs*qs)/np.sum(occs)
        self.coh_xs = average(occs, bs) **2*4*np.pi / 100
        self.inc_xs = average(occs, bs*bs)*4*np.pi/100 - self.coh_xs + average(occs, inc_xss)
        self.abs_xs_at2200 = np.sum(occs*abs_xss)
        self.uc_vol = structure.lattice.volume
        self.structure = structure
        # temperature dependent
        self.T = T
        from . import diffraction
        self.diffpeaks = list(diffraction.iter_peaks(structure, T, max_index=max_diffraction_index))
        self.xopm = xopm or IsotropicXOPM()
        self.size = size # size along beam. used for calculating extinction factor
        return

    def xs(self, wavelen):
        """calculate total cross section in barns

        Parameters
        ----------
        wavelen : float, floats
            wavelength or wavelengths. unit: angstrom
        """
        abs = self.xs_abs(wavelen)
        coh_el = self.xs_coh_el(wavelen)
        inc_el = self.xs_inc_el(wavelen)
        inel = self.xs_inel(wavelen)
        return abs+coh_el+inc_el+inel

    def xs_inel(self, wavelen):
        """calculate inelastic cross section in barns

        Parameters
        ----------
        wavelen : float, floats
            wavelength or wavelengths. unit: angstrom
        """
        S = self._S_inel(wavelen)
        return (self.coh_xs + self.inc_xs)*S

    def xs_coh_inel(self, wavelen):
        """calculate coherent inelastic cross section in barns

        Parameters
        ----------
        wavelen : float, floats
            wavelength or wavelengths. unit: angstrom
        """
        S = self._S_inel(wavelen)
        return self.coh_xs*S

    def xs_inc_inel(self, wavelen):
        """calculate incoherent inelastic cross section in barns

        Parameters
        ----------
        wavelen : float, floats
            wavelength or wavelengths. unit: angstrom
        """
        S = self._S_inel(wavelen)
        return self.inc_xs*S

    def xs_inc_el(self, wavelen):
        """calculate incoherent elastic cross section in barns

        Parameters
        ----------
        wavelen : float, floats
            wavelength or wavelengths. unit: angstrom
        """
        sctts = self.sctts
        Sarr = np.array([sc.S_el_inc(wavelen, self.T)*sc.occupancy for sc in sctts])
        if len(Sarr.shape) == 1:
            S = np.sum(Sarr)
        else:
            S = np.sum(Sarr, axis=0)
        return self.inc_xs * S

    def xs_coh_el(self, wavelen):
        """calculate coherent elastic cross section in barns

        Parameters
        ----------
        wavelen : float, floats
            wavelength or wavelengths. unit: angstrom
        """
        vs = [np.abs(p.F)**2*p.d*p.mult*self.xopm(p, wavelen)*self.extinction_factor(wavelen, p)*(p.d*2>wavelen) for p in self.diffpeaks]
        vs = np.array(vs) # unit fm^2
        vs[vs!=vs] = 0
        # print wavelen, vs * wavelen*wavelen/(2*self.uc_vol)
        if len(vs.shape) == 1:
            return np.sum(vs)/100 * wavelen*wavelen/(2*self.uc_vol) # unit: barn
        return np.sum(vs, axis=0)/100 * wavelen*wavelen/(2*self.uc_vol) # unit: barn

    def xs_coh_el__peak(self, wavelen, peak):
        """calculate coherent elastic cross section for one peak in barns

        Parameters
        ----------
        wavelen : float, floats
            wavelength or wavelengths. unit: angstrom

        peak : diffraction.DiffrPeak
            diffraction peak instance
        """
        v = np.abs(peak.F)**2*peak.d*peak.mult*self.xopm(peak, wavelen)*self.extinction_factor(wavelen, peak)*(peak.d*2>wavelen)
        return v/100 * wavelen*wavelen/(2*self.uc_vol) # unit: barn

    def xs_abs(self, wavelen):
        """calculate absorption cross section in barns

        Parameters
        ----------
        wavelen : float, floats
            wavelength or wavelengths. unit: angstrom
        """
        Q = 2*pi/wavelen
        from .constants import K2V
        v = K2V*Q
        return self.abs_xs_at2200/v*2200

    def extinction_factor(self, wavelen, pk):
        """
        compute extinction factor for given wavelength and diffraction peak
        """
        size = self.size
        if size == 0:
            return 1.
        sin_theta = wavelen / 2. / pk.d
        sin_theta_2 = sin_theta**2
        cos_theta_2 = 1 - sin_theta_2
        x = size*size * (wavelen*1e-10 * pk.F*1e-15 / self.uc_vol * 1e30)**2
        EB = 1/np.sqrt(1+x)
        EL = (1-x/2 + x*x/4 - 5*x**3/48)*(x<=1) + (np.sqrt(2/np.pi/x) * (1-1/8./x - 3./128/x/x - 15./1024/x**3))*(x>1)
        return EB*sin_theta_2 + EL*cos_theta_2

    def _S_inel(self, wavelen):
        Sarr = np.array([sc.S_inel_inc(wavelen, self.T)*sc.occupancy for sc in self.sctts])
        if len(Sarr.shape) == 1:
            S = np.sum(Sarr)
        else:
            S = np.sum(Sarr, axis=0)
        return S


    def plotAll(self, wavelen):
        """plot all cross sections w.r.t the given wavelength array

        Parameters
        ----------
        wavelen : floats
            wavelengths. unit: angstrom
        """
        coh_el_xs = self.xs_coh_el(wavelen)
        inc_el_xs = self.xs_inc_el(wavelen)
        abs_xs = self.xs_abs(wavelen)
        coh_inel_xs = self.xs_coh_inel(wavelen)
        inc_inel_xs = self.xs_inc_inel(wavelen)
        # and the total cross section
        total = self.xs(wavelen)
        # plot
        from matplotlib import pyplot as plt
        plt.plot(wavelen, coh_el_xs, label='coh el')
        plt.plot(wavelen, inc_el_xs, label='inc el')
        plt.plot(wavelen, coh_inel_xs, label='coh inel')
        plt.plot(wavelen, inc_inel_xs, label='inc inel')
        plt.plot(wavelen, abs_xs, label='abs')
        plt.plot(wavelen, total, label='total')
        plt.legend()
        return


# End of file
