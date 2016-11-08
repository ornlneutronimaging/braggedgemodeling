# -*- Python -*-

import numpy as np
from danse.ins import matter
from .vogel import phi1


class AtomicScattering:

    def __init__(self, element):
        self.element = element
        return


    def theta(self, T):
        element = self.element
        from DebyeTemp import getT
        return 1.*T/getT(element)


    def B(self, T):
        element = self.element
        atom = matter.Atom(element)
        mass = atom.mass
        from DebyeTemp import getT
        T_D = getT(element)
        theta1 = self.theta(T)
        rt = 3*h*h*phi1(theta1)/(mass*amu*kB*T_D)
        # convert to AA
        return rt/AA/AA


h = 6.62607004e-34
kB = 1.38064852e-23
AA = 1e-10
amu = 1.660539040e-27

def test():
    assert np.isclose(AtomicScattering('Ni').B(300), 0.307, rtol=1e-2)


if __name__ == '__main__': test()

# End of file
