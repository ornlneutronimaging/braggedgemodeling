from diffpy.Structure import Structure as _Structure, Lattice, Atom, SpaceGroups
from diffpy.Structure.SpaceGroups import GetSpaceGroup as getSpaceGroup

def Structure(*args, **kwds):
    """a wrapper for Structure method that injects "sg" data member"""
    if 'sgid' in kwds:
        sgid = kwds.pop('sgid')
    else:
        sgid = None
    s = _Structure(*args, **kwds)
    if sgid is not None:
        s.sg = getSpaceGroup(sgid)
    return s
