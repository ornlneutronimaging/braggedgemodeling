#!/usr/bin/env python

from bem import diffraction
from danse.ins import matter


atoms = [matter.Atom('Ni', (0,0,0)), matter.Atom('Ni', (0.5, 0.5, 0)),
         matter.Atom('Ni', (0.5,0,0.5)), matter.Atom('Ni', (0, 0.5, 0.5))]
a=3.5238
alpha = 90.
lattice = matter.Lattice(a=a, b=a, c=a, alpha=alpha, beta=alpha, gamma=alpha)
fccNi = matter.Structure(atoms, lattice, sgid=225)


def test_F_i():
    print diffraction.F_i(0, fccNi, (1,1,1), 300)
    return

def test_F():
    print diffraction.F(fccNi, (1,1,1), 300)
    print diffraction.F(fccNi, (2,0,0), 300)
    return


def main():
    test_F_i()
    test_F()
    return


if __name__ == '__main__': main()


# End of file
