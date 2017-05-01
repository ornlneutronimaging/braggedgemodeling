# -*- Python -*-
# Jiao Lin <jiao.lin@gmail.com>


# this is similar to resolution function
# Bragg edge curve should be convolved with the profile function computed here
# to model the experimental result


import numpy as np, scipy.special as sp
from matplotlib import pyplot as plt


class AbstractPeakProfile:

    def set_d_spacing(self, d):
        self.d = d
        return

    def convolve(self, x, f):
        raise NotImplementedError



class DeltaFunction(AbstractPeakProfile):

    def convolve(self, x, f):
        return f


class Jorgensen(AbstractPeakProfile):

    def __init__(self, alpha=None, beta=None, sigma=None):
        self.alpha = alpha if alpha is not None else [1., 0.]
        self.beta = beta if beta is not None else [1., 0.]
        self.sigma = sigma if sigma is not None else [0., 1., 0.]
        return


    def calc_profile(self, x, d):
        alpha = self.alpha[0] + self.alpha[1]/d
        # print "d=%s" % (d,)
        # print "alpha=%s" % alpha
        beta = self.beta[0] + self.beta[1]/d**4
        # print "beta=%s" % beta
        sigma2 = self.sigma[0]**2 + (self.sigma[1]*d)**2 + (self.sigma[2]*d*d)**2
        sigma = np.sqrt(sigma2)
        # print "sigma=%s" % sigma
        # print "x=%s" % x
        rt = Jorgensen_simple(x, sigma, alpha, beta)
        # print "rt=%s" % rt
        return rt


    def convolve(self, x, f):
        x0 = x[len(x)//2]
        x1 = x-x0
        profile = self.calc_profile(x1, self.d)
        profile/=np.sum(profile)
        return np.convolve(f, profile, 'same')


def Jorgensen_simple(x, sigma, alpha, beta):
    scale = alpha*beta/2/(alpha+beta)
    sigma2 = sigma*sigma
    sqrt2 = np.sqrt(2)
    u = alpha/2.*(alpha*sigma2 + 2*x)
    v = beta/2. * (beta*sigma2 - 2*x)
    y = (alpha*sigma2+x)/(sqrt2*sigma)
    z = (beta*sigma2 - x)/(sqrt2*sigma)
    # special treatment because exp(u) may goes to infinity
    term1 = np.exp(u)*sp.erfc(y)
    term1[sp.erfc(y)==0] = 0
    term2 = np.exp(v)*sp.erfc(z)
    term2[sp.erfc(z)==0] = 0
    return scale*(term1 + term2)


def test1():
    x = np.arange(-5, 5., 0.1)
    sigma = 1.
    alpha = 1.
    beta = 1.
    y = Jorgensen_simple(x, sigma, alpha, beta)
    plt.plot(x,y)
    plt.show()
    return


"""
old stuff
def test():
    x = np.arange(-20, 20., 0.1)
    alpha = 0.0252877
    beta0 = 0.0118713
    beta1 = 0.0123702
    sigma0 = 0
    sigma1 = 0.450648e3 # does not look right
    sigma1 = 30e-3
    sigma2 = 0
    d = 2.
    beta = beta0+beta1/d**4
    sigma_sq = sigma0**2 + sigma1**2 * d*d + sigma2**2 * d**4
    sigma = sigma_sq**.5
    print sigma, alpha, beta
    y = Jorgensen_simple(x, sigma, alpha, beta)
    plt.plot(x,y)
    plt.show()
    return
"""
def test2():
    x = np.arange(-20, 20., 0.1)
    j = Jorgensen(alpha=[1., 0.], beta=[2., 0], sigma=[0, 30e-3, 0])
    y = j.calc_profile(x, 1.)
    plt.plot(x,y)
    plt.show()
    return

def test():
    test2()
    return

if __name__ == '__main__': test()

# End of file
