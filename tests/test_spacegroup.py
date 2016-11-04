#!/usr/bin/env python
# Jiao Lin <jiao.lin@gmail.com>

import numpy as np
from danse.ins.matter import SpaceGroups as sg

def test():
    test1()
    test2()
    return


def test1():
    sg225 = sg.sg225
    v0 = [1,1,1]
    vs = []
    for symop in sg225.symop_list:
        v1 = np.dot(symop.R, v0)
        added=False
        for v2 in vs:
            if np.isclose(v1, v2, atol=1e-7).all():
                added=True
                break
            continue
        if not added:
            vs.append(v1)
        continue
    # for v in vs:
    #    print v
    assert len(vs)==8
    return


def test2():
    sg225 = sg.sg225
    assert calc_multiplicity([1,1,1], sg225) == 8
    assert calc_multiplicity([2,0,0], sg225) == 6
    assert calc_multiplicity([2,2,0], sg225) == 12
    assert calc_multiplicity([3,1,1], sg225) == 24
    assert calc_multiplicity([2,2,2], sg225) == 8
    assert calc_multiplicity([4,0,0], sg225) == 6
    assert calc_multiplicity([3,3,1], sg225) == 24
    assert calc_multiplicity([4,2,0], sg225) == 24
    assert calc_multiplicity([4,2,2], sg225) == 24
    assert calc_multiplicity([5,1,1], sg225) == 24
    assert calc_multiplicity([3,3,3], sg225) == 8
    assert calc_multiplicity([4,4,0], sg225) == 12
    assert calc_multiplicity([5,3,1], sg225) == 48
    return


def calc_multiplicity(v0, sg):
    vs = []
    for symop in sg.symop_list:
        v1 = np.dot(symop.R, v0)
        added=False
        for v2 in vs:
            if np.isclose(v1, v2, atol=1e-7).all():
                added=True
                break
            continue
        if not added:
            vs.append(v1)
        continue
    return len(vs)


if __name__ == '__main__': test()

# End of file
