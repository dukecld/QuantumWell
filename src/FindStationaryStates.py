import numpy as np
from PyQt5 import QtCore

class FindStationaryStates:
    def __init__(self, ws, interpolationFlag, stDock):
        """ Initializes variablesfo

        Parameters:
            ws: SolvePotentialWell(self.dpw) instance,
                dpw instance is ws.dpwFileNam
            interpolationFlag: if True, interpolate for zero
                               crossing
        """
        self.stDock = stDock
        self.dpw = ws.dpw
        self.ws = ws
        self.interpolationFlag = interpolationFlag
        debug = False
        if debug:
            print("  -- FindStationaryStates")

    def findStates(self, emin, emax, delE):
        """ find the stationary states between emin and emax.

            delE is the distance in eV between solution points
        """
        debug = False
        psiLast = np.array([])
        psiSlopeLast = np.array([])
        self.emin = emin
        self.emax = emax
        # create energy array
        self.eA = np.arange(emin, emax, delE)
        if False:
            for row in self.eA:
                print(row)
                print("eA[0] ", self.eA[0])

        # make initial conditions array, add infinite well ic's later
        wellH0 = self.dpw.wellHeightLeft
        wellH1 = self.dpw.wellHeightRight
        k2 = self.dpw.k2

        y0 = 1.0

        if debug:
            print("k2, wellH0, self.eA[0] ", k2, wellH0, self.eA[0])

        y01A = np.sqrt(k2 * (wellH0 - self.eA)) * y0

        # create constant array (for all energies)
        KA = np.sqrt(k2 * (wellH1 - self.eA))

        if debug:
            print("     eA[0]     KA[0], y01A[0] ", self.eA[0], KA[0], y01A[0])

        self.ws.resetSolver()

        if np.isfinite(self.dpw.wellHeightRight):
            # x = self.dpw.xMinMax # don't need xsolve
            x = self.dpw.xMinHigh
            # don't need xsolve, fitting over entire region
        else:
            # for wellHeightRight = inf
            x = self.dpw.xMinMax

        if not np.isfinite(self.dpw.wellHeightLeft):
            # for wellHeightLeft = inf
            y0 = 0.0
            y01Inf = 40. * (0.4 / self.dpw.wellWidth)

        if debug:
            print(
                "      after resetSolver() in FindStationaryStates::findStates"
            )
            self.dpw.printData()
            psi = self.ws.solveQuantumWell(self.eA[0], y0, y01A[0], x)
            for row in psi:
                print(row)

        self.stDock.proBar.reset()

        NE = len(self.eA)
        skip = 10
        delNE = NE / skip
        self.stDock.proBar.setMinimum(0)
        self.stDock.proBar.setMaximum(NE)
        self.stDock.proBar.reset()
        QtCore.QCoreApplication.processEvents()

        for i in np.arange(len(self.eA)):
            e = self.eA[i]
            if True:
                if (i % delNE == 0):
                    self.stDock.proBar.setValue(i)
                    QtCore.QCoreApplication.processEvents()

            if np.isfinite(self.dpw.wellHeightLeft):
                # for wellHeightLeft = finite
                y01i = y01A[i]
            else:
                # for wellHeightLeft = inf, new boundary conditions
                y01i = y01Inf

            # solve Schro.Eq for this energy between x=0 and x=wellWidth
            psi = self.ws.solveQuantumWell(e, y0, y01i, x)

            # extract wavefunction and slope of wave function for all x
            wfunc = psi[:, 0]
            wslope = psi[:, 1]
            # extract last value and last slope, accumulate in arrays
            psiLast = np.append(psiLast, wfunc[len(wfunc) - 1])
            psiSlopeLast = np.append(psiSlopeLast, wslope[len(wslope) - 1])

        self.stDock.proBar.reset()
        QtCore.QCoreApplication.processEvents()
        # get difference between calculated slope and slope if stationary state
        # determine where the sign of delSlope changes to get stationary states
        if np.isfinite(self.dpw.wellHeightRight):
            # for wellHeightRight finite, create slope difference
            self.delSlope = psiSlopeLast + KA * psiLast
        else:
            # for wellHeightRight infinite, use sign change in psi
            self.delSlope = psiLast

        delSign, = np.where(((np.sign(self.delSlope[1:]))
                             != (np.sign(self.delSlope[:-1]))))

        statE = self.eA[delSign]

        if self.interpolationFlag:
            # include interpolation
            statE = statE + ((self.eA[delSign + 1] - self.eA[delSign])
                             / (self.delSlope[delSign]
                             - self.delSlope[delSign + 1])) * \
                self.delSlope[delSign]

        return statE

    def plotStatStates(self, ax):
        """ Plot slope difference vs energy using ax as axes
            Write energy_slope.txt file
        """

        ax.plot(self.eA, self.delSlope, 'r.')
        ax.grid()
        ax.set_title(
            "slope difference, stationary state energies at zero crossings")
        ax.set_xlabel("electron energy (eV)")
        ax.set_ylabel("meas.slope - calc.slope at upper well edge")

        eA_delSlope = np.vstack((self.eA, self.delSlope)).transpose()
        np.savetxt("energy_slope.txt", eA_delSlope)
