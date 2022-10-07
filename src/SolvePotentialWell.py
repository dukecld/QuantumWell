# SolvePotentialWell class
# C. Duke, Grinnell College,ver. 07Oct2022

import numpy as np
from scipy.integrate import odeint

class SolvePotentialWell:
    """ SolvePotentialWell: solves Schroedinger's equation.

    methods:

    constructor:__init__(dpw,numX)
          dpw: DataPotentialWell reference, carriers all well parameters
          numX: number of x values for the solved region
                used to create several arrays in DataPotentialWell that
                can be usedin odeint.  This is somewhat circular, but
                is more flexible

    solveQuantumWell(e,y0,y01,x)
          e: energy (eV)
          y0:  psi initial condition
          y01: initial condition for derivative of psi
          x:   array of x values used in odeint,
               can come from DataPotentialWell

    getV(x)
          returns value of potential energy at position x

    getVFast(x):  quickly return value of potential energy at
                  position x, x values restricted to those in the
                  x array specified in solveQuantumWell method

                  Not currently used and is untested

    makeVArray():  create array of V values for each value of x in the x array

    makeXArray():  create x arrays for storage in DataPotentialWell
    """
    def __init__(self, dpw):
        """ constructor

        Parameters:
            dpw: DataPotentialWell reference, carriers all well parameters
            numX: number of x values for the solved region
                  used to create several arrays in DataPotentialWell that
                  can be usedin odeint.  This is somewhat circular, but
                  is more flexible

        """

        self.debug = False
        debug = False
        if debug:
            print("  -- SolvePotentialWell")
        self.dpw = dpw
        self.resetSolver()

    # call this method if change well details after instantiating the solver
    def resetSolver(self):
        """ Resets solver to default values

        """

        debug = False
        if debug:
            print(" in resetSolver")
        self.binW = 0.0

        self.wellHeightLeft = self.dpw.wellHeightLeft
        self.wellHeightRight = self.dpw.wellHeightRight
        self.barrierCt = 0
        self.wellWidth = self.dpw.wellWidth
        self.barriers = self.dpw.barriers

        self.xlow = self.dpw.xlow
        self.xhigh = self.dpw.xhigh
        self.xmin = self.dpw.xmin
        self.xmax = self.dpw.xmax

        self.x = np.array([])
        self.xMinMax = np.array([])
        self.xMinHigh = np.array([])

        self.xLowMin = np.array([])
        self.xMaxHigh = np.array([])

        # schro.eq; D2Y/DX2 = K2*(V-E)Y, where K2 = 26.25/(eV*nm*nm)
        # K = sqrt(26.25)
        self.k2 = self.dpw.k2
        self.barrierDict = dict()

        if debug:
            print("-- reset solver")
            print("        barriers")
            for r in self.barriers:
                print("      ", r)

        # always recalculate these arrays, have to reset x array
        self.dpw.x = np.array([])
        if (len(self.dpw.x) == 0):
            self.makeXArray()
            # self.makeVArray()

    def solveQuantumWell(self, e, y0, y01, x):
        """ Solve Schrodinger equation for energy # -*- coding: utf-8 -*-

        Parameters:
            e: energy (eV)
            y0:  psi initial condition
            y01: initial condition for derivative of psi
            x:   array of x values used in odeint,
                       can come from DataPotentialWell
        Returns:
            psiX array: 3 columns, psi   psiDeriv   x

        """
        debug = False

        self.e = e
        self.y0 = y0
        self.y01 = y01
        if debug:
            print("-- in solveQuantumWell")
            print("   dpw ")
            self.dpw.printData()
            print("       e ", self.e)
            print("       self.y0,self.y01", self.y0, self.y01)

        psi = odeint(self.deriv, (self.y0, self.y01), x)

        # add x column and return
        lenx = len(x)
        xnew = x.reshape((lenx, 1))
        psiX = np.append(psi, xnew, axis=1)

        if debug:
            print("  following odeint: psi")
            for row in psiX:
                print(row)
            print("shape of psiX ", psiX.shape)
            exit()

        #  psiX row, 3 columns: psi   psiDeriv   x
        return psiX

    def getV(self, x):
        """ Returns value of potential energy at position x
            for constant, linear, and quadratic potentials

        """

        if (not np.isfinite(self.dpw.wellHeightRight)) and (x > self.xmax):
            x = self.xmax
        v = -1.0

        # import pdb; pdb.set_trace()
        # if ( (self.xlow <= x) and (x <= self.xmin) ):

        # if ( (self.xlow <= x) and (x < self.xmin) ):
        if (x < self.xmin):
            v = self.wellHeightLeft

        elif (self.xmax < x):
            v = self.wellHeightRight

        else:
            for bar in self.barriers:
                if ((bar[0] <= x) and (x <= bar[1])):
                    v = bar[2] + bar[3] * (x - bar[0]) + bar[4] * (
                        x - bar[0]) * (x - bar[0])
                    break

        if v < 0.0:
            print(" in getV( x)  v<0.0, x = ", x)
            print("  v = ", v)
            print("( self.xmax < x )  ", (self.xmax < x))
            print("(x <= self.xhigh) ", (x <= self.xhigh))
            print(" ( ( self.xmax < x ) and (x <= self.xhigh)) ",
                  ((self.xmax < x) and (x <= self.xhigh)))
            print("x self.xmax del ", x, self.xmax, x - self.xmax)
            print(" not np.isclose(self.xmax,x) ",
                  not np.isclose(self.xmax, x, rtol=1e-04))
            self.dpw.printData()
            exit()

            if False:
                print("self.barriers ", self.barriers)
                print("                         in getV ", x)
                v = [(bar[2] + bar[3] * (x - bar[0])
                      + bar[4] * (x - bar[0]) * (x - bar[0])) for bar in
                     self.barriers if (bar[0] <= x) and (x <= bar[1])][0]
                print(" in getV ", x, v)
                exit()

        return v

    # only use when x values are restricted to those in the x array!!!!!!
    def getVFast(self, x):
        """ Quickly return value of potential energy at
            position x, x values restricted to those in the
            x array specified in solveQuantumWell method

            Not currently used and is untested
        """
        ind = np.searchsorted(self.vA[:, 0], x)
        print("x,ind ", x, ind)
        v = self.vA[ind, 1]

        return v

        # assumes x in the x array (for exact retrieval from the x/v array)
        if ((self.xlow < x) and (x <= self.xmin)):
            v = self.wellHeightLeft
        elif (self.xmax < x):
            v = self.wellHeightRight
        else:
            ind = np.searchsorted(self.vA[:, 0], x)
            v = self.vA[ind, 1]

        return v

    def makeVArray(self):
        """ Create array of V values for each value
            of x in the x array

        """

        # can I do this using an array directly
        vA = [[xi, self.getV(xi)] for xi in self.x]
        vAA = np.array(vA)

        debug = False
        if debug:
            print("  -- makeVArray")
            print("       vAA.shape", vAA.shape)
            print("     vAA")
            for r in vAA:
                print(r)

        self.dpw.vA = vAA
        self.vA = vAA

    def deriv(self, y, x):
        debug = False
        v = self.getV(x)
        if debug:
            print(" deriv v ", x, v)
        kk = self.k2 * (v - self.e)
        dret = [y[1], kk * y[0]]
        return dret

    def makeXArray(self):
        """ create x arrays for storage in DataPotentialWell

        """
        debug = False
        if debug:
            print("  -- makeXArray")
        N = self.dpw.numX

        # x array from xmin to xmax, bin edge falls on xmin and xmax
        xminmax = np.linspace(self.xmin, self.xmax, N)

        # make and store subarray
        self.xMinMax = xminmax
        self.dpw.xMinMax = self.xMinMax

        # determine binwidth and store
        binW = (self.xmax - self.xmin) / (N - 1)
        self.dpw.binW = binW
        self.binW = binW

        # get x values from xlow to xmin, bins have to line up!
        xlo = np.arange(-binW, self.xlow, -binW)
        xlo = xlo[::-1]  # have to reverse order for correct appending

        self.xLowMin = xlo
        self.dpw.xLowMin = xlo

        # get x values from xmax to xhigh, bins have to line up
        xup = np.arange(self.xmax + binW, self.xhigh, binW)

        self.xMaxHigh = xup
        self.dpw.xMaxHigh = xup

        # final arrays
        # full array
        self.x = np.append(np.append(xlo, xminmax), xup)

        # probably not needed
        self.dpw.x = self.x

        # xmin to xhigh
        xminhigh = np.append(xminmax, xup)
        self.xMinHigh = xminhigh
        self.dpw.xMinHigh = xminhigh

        return 0
