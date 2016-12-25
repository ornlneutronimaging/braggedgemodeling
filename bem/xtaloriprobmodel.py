# -*- Python -*-
# Jiao Lin <jiao.lin@gmail.com>


class XtalOriProbModel:

    "Crystal orientation probability model"

    def __call__(self, peak, wavelen):
        raise NotImplementedError


class IsotropicXOPM(XtalOriProbModel):

    def __call__(self, peak, wavelen):
        return 1.


class MarchDollase(XtalOriProbModel):

    class Texture(dict):

        def __call__(self, hkl):
            if hkl in self: return self[hkl]
            for hkl1 in self:
                div = np.array(hkl, float)/np.array(hkl1, float)
                div = div[div==div][0]
                if np.allclose(hkl, np.array(hkl1)*div):
                    return self[hkl1]
                continue
            return 1.
    

    def __init__(self, r=None, beta=None):
        self.r = r or self.Texture()
        self.beta = beta or self.Texture()
        return


    def __call__(self, peak, wavelen):
        hkl = tuple(peak.hkl)
        r = self.r(hkl)
        if np.isclose(r, 1.):
            return 1.
        alpha = np.pi/2 - np.arcsin(wavelen/2./peak.d)
        beta = self.beta(hkl)
        delta = np.pi/100.
        phi = np.arange(-np.pi/2, np.pi/2-delta/2., delta)
        # array
        if isinstance(wavelen, np.ndarray):
            integral = (r*r - 1./r)*((np.cos(alpha)*np.cos(beta))[:, np.newaxis]
                                     - (np.sin(alpha)*np.sin(beta))[:, np.newaxis] * np.sin(phi))**2
            integral += 1./r
            integral = 1./(np.sqrt(integral)*integral)
            ret = np.sum(integral, axis=-1)*delta/np.pi
            ret[ret!=ret] = 0
            return ret
        # number
        integral = (r*r - 1./r)*(np.cos(alpha)*np.cos(beta)
                                 - np.sin(alpha)*np.sin(beta)*np.sin(phi))**2
        integral += 1./r
        integral = 1./(np.sqrt(integral)*integral)
        return np.sum(integral)*delta/np.pi

import numpy as np

# End of file
