# -*- Python -*-
# Jiao Lin <jiao.lin@gmail.com>


class BraggEdgeSpectrumCalculator:


    def __init__(self, xscalc, peak_profile):
        self.xscalc = xscalc
        self.peak_profile = peak_profile
        return


    def __call__(self, kind, wavelen):
        if hasattr(self, 'calc_%s' % kind):
            return getattr(self, 'calc_%s' % kind)(wavelen)
        return getattr(self.xscalc, 'xs_%s' % kind)(wavelen)

    def calc_total(self, wavelen):
        abs = self('abs', wavelen)
        coh_el = self('coh_el', wavelen)
        inc_el = self('inc_el', wavelen)
        inel = self('inel', wavelen)
        return abs+coh_el+inc_el+inel

    def calc_coh_el(self, wavelen):
        "wavelen has to be a numpy array"
        pf = self.peak_profile
        xscalc = self.xscalc
        sum = 0
        for peak in xscalc.diffpeaks:
            pf.set_d_spacing(peak.d)
            xs = xscalc.xs_coh_el__peak(wavelen, peak)
            spectrum = pf.convolve(wavelen, xs)
            sum = sum + spectrum
            continue
        return sum


# End of file
