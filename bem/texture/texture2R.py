#!/usr/bin/env python


"""
A translation of QingGe's fortran code "BraggEdge.for".
This code should work with arbitrary materials.

The original code of QingGe hardcoded
* d_spacing
* hkl reflections
* integration parameters N_RD and N_HD
* input texture file name
* output filename

It takes 1 minute to run at heetuu.

Calculates Bragg Edge intensities from texture file.
A postprocessing step is needed to create histogram of computed data.

*** Known problems ***
* The method `compute` has a side effect of generating hkls.txt whi
"""

import numpy as np, os, sys

def compute(
        structure,
        tex = 'xqg.tex',
        N_RD = 36,
        N_HD = 144,
        out = 'int_samples.dat',
        hkls_out = 'hkls.txt',
        max_hkl_index=5,
        ):
    """
    It generates tuples of 
      (hkl_index+1, number_of_good_grains, 
       polar_angle_index+1, azimuthal_angle_index+1, 0???, wavelength)

    It also writes out a list of hkl in a text file: `hkls_out`
    """
    tolerance = 90./N_RD/2. # 90./36/2.
    # read euler angles from texture file
    texdata = np.loadtxt(tex, skiprows=4)
    N_grains = len(texdata)
    euler_matrices = np.zeros((N_grains, 3, 3), float)
    # convert euler angles to matrices
    for i in range(N_grains):
        line = texdata[i]
        fi1, PHI, fi2 = line[:3]
        euler_angles2matrix(fi1, PHI, fi2, euler_matrices[i])
        continue
    #
    euler_matrices = np.transpose(euler_matrices, (0, 2, 1))
    # compute diffraction peaks
    from bem.diffraction import iter_peaks
    peaks = list(iter_peaks(structure, T=300., max_index = max_hkl_index))
    peaks = sorted(peaks, key = lambda k: -k.d) # sort peaks by d spacing
    hkls = [p.hkl for p in peaks]
    # _hkls = [111, 200, 220, 311, 222, 400, 331, 420, 422, 511, 333, 440, 531]
    # d_spacing_list = [2.07793, 1.800787, 1.272775, 1.085376, 1.038812, 0.90032, 0.825621, 0.804956, 0.734553, 0.692623, 0.692623, 0.6356, 0.6082,]
    d_spacing_list = [p.d for p in peaks]
    print d_spacing_list
    #
    outstream = open(out, 'wt')
    hkls_outstream = open(hkls_out, 'wt')
    matched_min = np.cos(tolerance*np.pi/180.)
    
    RDs = np.arange(N_RD+1) * np.pi/2. / N_RD  # from 0 to pi/2
    betas = np.arange(N_HD) * np.pi*2 / N_HD  # from 0 to <2*pi
    # equiv_planes() calculates nfamily
    hkl_families = [normalized_equiv_planes(hkl, structure) for hkl in hkls]
    
    for ihkl, (hkl, d_spacing) in enumerate(zip(hkls, d_spacing_list)):
        print ihkl
        lambdas = 2.*d_spacing*np.sin( RDs )
        alfas = np.arccos(lambdas/2./d_spacing)
        sa_list = np.sin(alfas)
        hkl_family = hkl_families[ihkl]
        euler_dot_hkl_family = [np.dot(euler_matrices, hkl1) for hkl1 in hkl_family]
        for iRD, (lambda_, alfa, sa) in enumerate(zip(lambdas, alfas, sa_list)):
            # print iRD
            for iHD, beta in enumerate(betas):
                v = np.array([sa*np.cos(beta), sa*np.sin(beta), np.cos(alfa)])
                icounter = 0
                # print iRD, iHD, hkl_family
                for ipl, hkl1 in enumerate(hkl_family):
                    prodesc = np.dot(euler_dot_hkl_family[ipl], v)
                    prodesc = np.abs(prodesc)
                    # prodesc is close to 1 means a match
                    icounter+= np.sum(prodesc >= matched_min)
                    continue
                outstream.write("%6i%8i%8i%8i%8i%14.6f\n"  % (
                    ihkl+1, icounter, iRD+1, iHD+1, 0, lambda_
                ))
                continue # iHD
            continue #iRD
        hkls_outstream.write('%s\n' % (hkl,))
        continue #hkl
    return hkls


def read_results(path):
    "parse output file from compute method and reformat"
    # implementation here is mostly copy of "calculate R.ipynb"
    # read
    samples = np.loadtxt(path)
    hkl_indices = samples[:, 0]
    counts = samples[:, 1]
    polar_indices = samples[:, 2]
    azimuthal_indices = samples[:, 3]
    lambdas = samples[:, -1]
    # reformat
    Npolar = np.max(polar_indices)
    assert Npolar == int(Npolar)
    Npolar = int(Npolar)
    Nazimuthal = np.max(azimuthal_indices)
    assert Nazimuthal == int(Nazimuthal)
    Nazimuthal = int(Nazimuthal)
    nhkl = np.max(hkl_indices)
    assert nhkl == int(nhkl)
    nhkl = int(nhkl)
    ncols = samples.size/(nhkl*Npolar*Nazimuthal)
    assert nhkl*Npolar*Nazimuthal*ncols == samples.size
    lambdas.shape = counts.shape = nhkl, Npolar, Nazimuthal
    # wave length does not depend on azimuthal angle
    lambdas1 = lambdas[:, :, 0]
    for i in range(Nazimuthal):
        assert (lambdas[:, :, i] == lambdas1).all()
    lambdas = lambdas1
    # for each hkl, normalize counts
    norm_counts = np.zeros(counts.shape, dtype=float)
    for i in range(nhkl):
        ave = np.average(counts[i])
        norm_counts[i, :] = counts[i] / ave
    # Calculate R as a function of polar angle and hkl
    R = np.average(norm_counts, axis=-1)
    assert R.shape == (nhkl, Npolar)
    # both have shape (nhkl, Npolar)
    return lambdas, R


def euler_angles2matrix(fi1, PHI, fi2, T):
    COS = np.cos; SIN = np.sin
    DEG2RAD = np.deg2rad(1)
    fi1 *= DEG2RAD
    PHI *= DEG2RAD
    fi2 *= DEG2RAD
    C1=COS(fi1)
    C= COS(PHI)
    C2=COS(fi2)
    S1=SIN(fi1)
    S= SIN(PHI)
    S2=SIN(fi2)
    T[0,0]=C1*C2-S1*S2*C
    T[0,1]=S1*C2+C1*S2*C
    T[0,2]=S2*S
    T[1,0]=-C1*S2-S1*C2*C
    T[1,1]=-S1*S2+C1*C2*C
    T[1,2]=C2*S
    T[2,0]=S1*S
    T[2,1]=-C1*S
    T[2,2]=C
    return


def equiv_planes(hkl, structure):
    from bem import diffraction
    candidates = [tuple(map(int, _)) for _ in diffraction.equivalent_hkls(hkl, structure.sg)]
    res = [hkl]
    for c in candidates:
        if not isDuplicate(c, res):
            res.append(c)
        continue
    return res

def equiv_planes0(hkl):
    h, k, l = hkl
    all = [(h, k, l)]
    candidates = [ (-h, k, l), (h, -k, l), (h,k, -l), (-h, -k, l), (-h, k, -l), (h, -k, -l), (-h, -k, -l)]
    from itertools import permutations
    for c in candidates:
        for p in permutations(c):
            if not isDuplicate(p, all):
                all.append(p)
        continue
    return all

def isDuplicate(hkl, collection):
    if hkl in collection: return True
    h,k,l = hkl; nhkl = -h,-k,-l
    if nhkl in collection: return True
    return False

def normalized_equiv_planes(hkl, structure):
    hkls0 = equiv_planes0(hkl)
    hkls = equiv_planes(hkl, structure)
    assert len(hkls)==len(hkls0)
    norm = lambda x: x/np.linalg.norm(x)
    norma = lambda x: norm(np.array(x))
    return map(norma, hkls)


def main():
    from bem import matter
    # FCC
    atoms = [matter.Atom('Ni', (0,0,0)), matter.Atom('Ni', (0.5, 0.5, 0)),
             matter.Atom('Ni', (0.5,0,0.5)), matter.Atom('Ni', (0, 0.5, 0.5))]
    # a=3.5238
    a=3.60  # this is inferred from the d-spacing values in the original fortran file
    alpha = 90.
    lattice = matter.Lattice(a=a, b=a, c=a, alpha=alpha, beta=alpha, gamma=alpha)
    fccNi = matter.Structure(atoms, lattice, sgid=225)
    compute(
        fccNi,
        tex = 'xqg.tex',
        N_RD = 36,
        N_HD = 144,
        out = 'int_samples.dat',
        max_hkl_index=5,
        )
    return

if __name__ == '__main__': main()
