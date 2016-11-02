# -*- Python -*-

import numpy as np
from danse.ins import matter


def theta(element, T):
    from DebyeTemp import getT
    return 1.*T/getT(element)


def phi1(theta1):
    def sum_series(theta1):
        n = np.arange(1., 35.)
        series = 1./np.exp(n/theta1)/n/n
        return np.sum(series)
    return 1./2+2*(theta1*np.log(1-np.exp(-1/theta1))+theta1**2*(np.pi**2/6 - sum_series(theta1)))

def B(element, T):
    atom = matter.Atom(element)
    mass = atom.mass
    from DebyeTemp import getT
    T_D = getT(element)
    theta1 = theta(element, T)
    rt = 3*h*h*phi1(theta1)/(mass*amu*kB*T_D)
    # convert to AA
    return rt/AA/AA

h = 6.62607004e-34
kB = 1.38064852e-23
AA = 1e-10
amu = 1.660539040e-27

def test():
    assert np.isclose(B('Ni', 300), 0.307, rtol=1e-2)


if __name__ == '__main__': test()

# End of file
