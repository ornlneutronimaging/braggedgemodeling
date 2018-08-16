#!/usr/bin/env python

from bem import matter

atoms = [matter.Atom('Al', (0,0,0)), matter.Atom('Al', (0.5, 0.5, 0)),
         matter.Atom('Al', (0.5,0,0.5)), matter.Atom('Al', (0, 0.5, 0.5))]
a=4.046
alpha = 90.
lattice = matter.Lattice(a=a, b=a, c=a, alpha=alpha, beta=alpha, gamma=alpha)
fccAl = matter.Structure(atoms, lattice, sgid=225)

# End of file
