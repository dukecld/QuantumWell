#  extendPsi function to calculate values of wavefunction within lower barrier
#  no extension within upper barrier (this region included in solver)

import numpy as np


def extendPsi(psi, dbw, energy):
    """ function to extend the square well wavefunction in x < 0 barrier region
        psi:  array of psi values from solver
        dbw:  DataPotentialWell reference, contains well details
        energy: particle energy

        return:   [psi,x] array
    """

    debug = False
    if debug:
        print("  -- extendPsi ")

    # get well parameters and bin width for extension
    # get initial conditions, left and right
    y0 = psi[0, 0]
    y01 = psi[0, 1]

    ind = np.searchsorted(psi[:, 2], dbw.xmax)

    y1 = psi[ind][0]
    y11 = psi[ind][1]
    v0 = dbw.wellHeightLeft
    v1 = dbw.wellHeightRight
    if debug:
        print("    left: y0 y01 v0", y0, y01, v0)
        print("    right: y1,y11,v1,ind, phi[ind]", y1, y11, v1, ind, psi[ind])

    # assumes electron in 2m/hbar*hbar, in eV/nm*nm
    kk = dbw.k2
    # find k's: k for v0 and K for v1
    if v0 < np.inf:
        k = np.sqrt(kk * (v0 - energy))
    else:
        k = 0.0

    if v1 < np.inf:
        K = np.sqrt(kk * (v1 - energy))
    else:
        K = 0

    if debug:
        print("k K", k, K)

    # extend in lower barrier
    xA = dbw.xLowMin
    xA = np.append(xA, 0.0)

    if debug:
        print("")

    # calculate psi and its derivative, set to zero for infinite barrier
    if debug:
        print("v0 ", v0)
    if v0 < np.inf:
        psiL = y0 * np.exp(k * xA)
        psiLDeriv = k * psiL
    else:
        psiL = 0.0 * xA
        psiLDeriv = 0.0 * xA

    # concatenate arrays, psiL, psiLDeriv, xA1
    psiL = psiL[:, None]
    psiLDeriv = psiLDeriv[:, None]
    xA = xA[:, None]

    # horizontally stack the three columns into a single array,
    # 3 columns, psi, psiDeriv, x
    psiLX = np.hstack((psiL, psiLDeriv, xA))

    if debug:
        # print("psiLX ", psiLX)
        print("psiLX.shape ", psiLX.shape)
        # exit()

    return psiLX
