import sys

if sys.version_info[0] < 3:
    from diffpy.Structure import Structure as _Structure, Lattice, Atom, SpaceGroups
    from diffpy.Structure.SpaceGroups import GetSpaceGroup as getSpaceGroup
else:
    from diffpy.structure import Structure as _Structure, Lattice, Atom, spacegroups as SpaceGroups
    from diffpy.structure.spacegroups import GetSpaceGroup as getSpaceGroup
    

def loadCif(path):
    """load CIF file from given path to create a Structure instance
    """
    if sys.version_info[0] < 3:
        from diffpy.Structure.Parsers import getParser
    else:
        from diffpy.structure.parsers import getParser
    p = getParser('cif')
    nacl = p.parseFile(path)
    nacl.sg = p.spacegroup
    return nacl


def Structure(*args, **kwds):
    """a wrapper for diffpy Structure method that injects "sg" data member.

    Structure(atoms, lattice, sgid=): create an atomic structure given the list of atoms, the lattice, and the space group id. This method is mainly for advanced users, and for testing and exploration purpose.
    
    Parameters
    ----------
    atoms : list
        list of atoms

    lattice : Lattice
    
    sgid : int
        space group id. For example 225 for FCC

    Examples
    --------
    >>> from bem.matter import Atom, Lattice, Structure
    >>> atoms = [Atom('Fe', (0,0,0)), Atom('Fe', (0.5, 0.5, 0.5))]
    >>> a=2.856
    >>> alpha = 90.
    >>> lattice = Lattice(a=a, b=a, c=a, alpha=alpha, beta=alpha, gamma=alpha)
    >>> astruct = Structure(atoms, lattice, sgid=229)

    For more details on Atom, Lattice, and Structure, please refer to http://www.diffpy.org/diffpy.structure/
    """
    if 'sgid' in kwds:
        sgid = kwds.pop('sgid')
    else:
        sgid = None
    s = _Structure(*args, **kwds)
    if sgid is not None:
        s.sg = getSpaceGroup(sgid)
    return s


# examples
def fccNi():
    atoms = [Atom('Ni', (0,0,0)), Atom('Ni', (0.5, 0.5, 0)),
             Atom('Ni', (0.5,0,0.5)), Atom('Ni', (0, 0.5, 0.5))]
    a=3.5238
    alpha = 90.
    lattice = Lattice(a=a, b=a, c=a, alpha=alpha, beta=alpha, gamma=alpha)
    return Structure(atoms, lattice, sgid=225)
fccNi = fccNi()

def fccAl():
    atoms = [Atom('Al', (0,0,0)), Atom('Al', (0.5, 0.5, 0)),
         Atom('Al', (0.5,0,0.5)), Atom('Al', (0, 0.5, 0.5))]
    a=4.046
    alpha = 90.
    lattice = Lattice(a=a, b=a, c=a, alpha=alpha, beta=alpha, gamma=alpha)
    return Structure(atoms, lattice, sgid=225)
fccAl = fccAl()

def bccFe():
    atoms = [Atom('Fe', (0,0,0)), Atom('Fe', (0.5, 0.5, 0.5))]
    a=2.856
    alpha = 90.
    lattice = Lattice(a=a, b=a, c=a, alpha=alpha, beta=alpha, gamma=alpha)
    return Structure(atoms, lattice, sgid=229)
bccFe = bccFe()
