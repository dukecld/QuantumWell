# plotPsi function to plot solver wavefunction after extending to x < 0 region

import numpy as np
from extendPsi import extendPsi


def plotPsi(ax, psi, e, dpw, plotFlagLower, plotFlagUpper, color='r'):
    """
        PlotPsi function:  plots psi function, might need to extend to
        lower region with call to extendPsi

        PlotPsi(ax,psie,dpw,plotFlagLower,plotFlagUpper)
             ax:   axis reference for plot
             psi:  psi array from solver
             dpw: DataPotentialWell reference, contains well details
             plotFlagLower: extends psi to x values < 0.0
             plotFlagUpper: extends psi to x values > xmax (NOT IMPLEMENTED)

             need to make sure that psi is within +- 10 from xmin to xmax.

    """
    debug = False
    if debug:
        print("  -- in plotPsi ------------------")

    # make a copy so I can more easily translate/normalize psi
    psiT = np.copy(psi)
    indxmax = np.where(np.isclose(psiT[:, 2], dpw.xmax))
    imax = indxmax[0][0]

    absPsi = np.abs(psiT[:, 0])
    absPsi1 = absPsi[:imax]

    maxPsi = np.max(absPsi1)

    fTrans = (20.0 / dpw.vmax) * e
    fNorm = 1.5 / maxPsi

    ax.plot(psiT[:, 2], (fNorm * psiT[:, 0] + fTrans), color)
    ax.set_axis_off()
    # extend to lower region if necessary
    # set to zero if wellHeightLeft = inf

    if plotFlagLower:
        psiLow = extendPsi(psiT, dpw, e)
        if (0):
            print("    psiLow ")
            print(psiLow)
            exit()
        ax.plot(psiLow[:, 2], (fNorm * psiLow[:, 0] + fTrans), color)

    ymax = 10.0
    ymin = -10.0
    fract = e / dpw.vmax
    delta = fract * (ymax - ymin)
    alpha = -ymin - delta
    yminNew = -delta
    ymaxNew = ymax + alpha
    if debug:
        print("   new ylimits for psi plot")
        print("            yminOld, ymaxOld ", ymax, ymin)
        print("            e,f ", e, fract)
        print("            yminNew, ymaxNew ", yminNew, ymaxNew)
    ax.set_ylim([yminNew, ymaxNew])
    ax.set_xlim([dpw.xlow, dpw.xhigh])
    ax.set_ylim([0.0, 20.0])
    ax.set_xlim([dpw.xlow, dpw.xhigh])

    # set up array to dump to a file
    if plotFlagLower:
        psidump = psiLow[:, (0, 1, 2)]
        psidump = np.delete(psidump, len(psidump) - 1, axis=0)

        psiTT = np.copy(psiT[:, (0, 1, 2)])
        psiAll = np.vstack((psidump, psiTT))
    else:
        psiAll = psiT[:, (0, 1, 2)]

    dpw.psiArray = psiAll
    if (0):
        print("psiAll.shape ", psiAll.shape)
        print("dpw.dStates ", dpw.dStates)
        dpw.printData()
        print("leaving plotPsi")
    return psiAll
