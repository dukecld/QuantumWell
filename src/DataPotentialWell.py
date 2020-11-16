
from numpy import isclose
import numpy as np
import pickle
import os


# a dictionary might be faster? Start with a class
class DataPotentialWell:
    """ Container class for all potential well parameters and data.

    This class contains all well parameters and
    data such as the array of x values,
    stationary state energies (if previously
    calculated), psi array, etc. The class
    has read and write methods using the python
    pickle method to read and write .dpw files.
    Thus, the class may be used to access
    wavefunction calculations from the quantum
    well solver for use in e.g. a jupyter
    notebook.

Methods:

    getBasicWellProperties()
        Returns (wellWidth,heightLeft,heightRight)

    printAddedVArray()
        prints array to screen. columns are:

        ID:  id number of addedV potential
        xmin: start energy for potential
        xmax: ending energy for potential
        a,b,c: polynomial coeffs,
               V = a + b*x + c*x*x

    get2mOverhbar2()
        2*m/(hbar*hbar) for electron in eV/(nm*nm)

    getXBinWidth()
        returns binWidth, the distance between adjacent x
        values

    getPotentialList():
        returns numpy array of all potential energy
        functions in the potential well.

        Each array row has the following fields:
            starting energy:
            ending energy:
            a,b,c: polynomial coefficients,
                   V = a + b*x + c*x*x

    getNumberOfAddedVPotentials():
        Returns number of added potentials

    getXArrayIndexWellEdges():
        Returns int numpy array:
        [left-edge index, right-edge index]

    getVArray():
        The V array includes a potential
        energy (eV) for each x in the x array.

    getXArray():
        The x-values in the x array include all
        points shown in the potential plot in the
        main window, including points outside of
        the potential well.
        The getXArrayIndexWellEdges() method
        returns the x-array indices between the
        well edges.

    readDpwFile(dpwfileName):
        reads a .dpw file into a DataPotentialWell
        class instance.

        This reader uses the python pickle.load
        method to read all DataPotentialWell
        attributes from a binary .dpw file into a
        DataPotentailWell instance.

    resetWell():
        set all well parameters to default values

    writeDpwFile(dpwFileName):
        writes DataPotentialWell class instance
        to a .dpw file.

        This writer uses the python pickle.dump
        method to write all attributes of the
        DataPotentailWell instance to a binary
        file with a .dpw extension.

    getPsiEnergy(self):
        return the energy of the last-plotted
        state in thefindStationaryStates
        window.

    getPsiArray()
        returns unnormalized stationary-state psi array, if available

    getPsiArrayNormalized():
        returns numpy normalized psi array, if available
        Normalization constant =
                   sqrt( sum(psi*psi) * deltaX ).

    getPsiPrimeArrayNormalized():
        returns first derivative of normalized-psi
        array as numpy array

    getPsiPrimeArray()
        returns first derivative of non-normalized psi array

    getStationaryStateEnergies():
        Returns numpy array

    printXVArrays()
        mislabeled, prints xLowMin and xMinMax arrays, fix later
        Not currently used

    printData()
        prints all well details to screen

    printBasicWellParms()
        string formatted for message box

    printAddedVArray()
        prints addedVArray to screen

    updateBarrierDictIO()
        use when adding a new barrier

    copyData(newdpw)
        copy all well parameters from newdpw into self.dpw
        used internally

    findPsiNorm()
        used internally

    """
    def __init__(self):

        #  resetWelll to default values, create dStates dictionary

        #      dStates dictionary used to store energies of
        #          stationary states, key = integer
        #      filled in potentialWell.py
        # dStates[integer key] = energy of stationary state
        self.dStates = dict()

        # clears well and set default values
        self.resetWell()

# ----------------------- resetWell -------------------

    def resetWell(self):
        # xlow/xhigh are the limits of the well as seen on the screen
        self.xlow = 0.0
        self.xhigh = 0.0
        # xmin/xmax are the lower and upper edges of the well
        self.xmin = 0.0
        self.xmax = 0.0

        # should have an easier way of setting the number of bins
        # set in solver, but may need a setter here?
        # self.numX = 50
        self.numX = 500  # number of bins, xlow to xhigh, default 500
        # self.numX = 1000

        self.xMinMax = np.array([])  # xarray from xmin to xmax
        self.xMinHigh = np.array([])  # xarray from xmin to xhigh

        # array from xlow to xmin
        self.xLowMin = np.array([])
        # array from xmax to xhigh (may be overkill, ueed in solver)
        self.xMaxHigh = np.array([])

        self.binW = 0.0  # binwidth of x array
        self.vA = np.array([])  # rows are [x,v] for all x array values

        self.barrierCt = 0

        self.updateBarrierDict()
        self.barriers = np.array([])

        self.wellWidth = 0.0
        self.wellHeightLeft = 0.0
        self.wellHeightRight = 0.0
        self.vmax = 0.0
        self.fractRt = 0.2
        self.fractLf = 0.2

        # filled following stationary state plot, otherwise empty
        # array row: psi  psi'  x  V
        self.psiArray = np.array([])

        # psiEnergy is the energy associated with psiArray
        self.psiEnergy = 0.0

        # normalization constant for psi, only used in getters
        self.psiNorm = 0.0

        # 2m/hbar*hbar, set in buildPotentialWell
        self.k2 = 0.0

        # clear dictionary of stationary states
        self.dStates.clear()
        # stationary state chosen by plot button.
        self.statStateNumber = 0

        # minimum/maximum energy in dStates energy range
        self.minEStates = 0.0
        self.maxEStates = 0.0
        # energy from solver (will use to scale graph in infinite square well)
        # may want this easier to change?
        self.maxESolve = 100.0
        self.infiniteWellFlag = False  # true for infinite well.

    # ------------------ printXVArrays -----------------------
    def printXVArrays(self):
        """
        print method, misnamed - currently prints
        xLowMin and xMinMax
        Not currently used
        """

        print("  -- DataPotentialWell::printSVArrays")

        # print "      vA array, all x and V "
        # for r in self.vA:
        #    print r[0],r[1]
        # print "\n"

        print("      xLowMin array")
        for r in self.xLowMin:
            print(r)
        print("\n")

        print("     xMinMax array ")
        for r in self.xMinMax:
            print(r)

# ----------------------- printData --------------

    def printData(self):
        """ Print all well properties to screen. """
        print("    -- DataPotentialWell::printData")
        print("       xmin, xmax, xlow, xhigh ", self.xmin, self.xmax,
              self.xlow, self.xhigh)
        print("       numX,  len(xMinMax), len(xMinHigh) ", self.numX,
              len(self.xMinMax), len(self.xMinHigh))
        print("       binW,  ", self.binW)
        print("       wellWidth, wellHeightLeft, wellHeightRight ",
              self.wellWidth, self.wellHeightLeft, self.wellHeightRight)
        print("       vmax set in Plotter, fractRt, fractLf ", self.vmax,
              self.fractRt, self.fractLf)
        print("       k2 ", self.k2)
        print("       AddedVCt ", self.barrierCt)
        print("       AddedVDict ", self.barrierDict)
        print("       AddedV array ")
        if len(self.barriers) > 0:
            for row in self.barriers:
                print(row)
        else:
            print("         length of AddedV array is zero")
        if len(self.dStates) > 0:
            print("         table of stationary states")
            for key, v in self.dStates.items():
                print("          ", key, v)
        print("psiArray.shape ", self.psiArray.shape)
        print("self.statStateNumber ", self.statStateNumber)
        print("self.psiEnergy ", self.psiEnergy)

    # --------------------- printBasicWellParms --------------
    def printBasicWellParms(self):
        """
        returns string formatted for message box of basic well parameters
        """
        cr = "\n"
        sp = "  "
        dataB = "Basic Well Parameters " + cr
        l10 = "     width  " + "{:6.3f}".format(self.wellWidth)
        l11 = "  nm" + cr
        l1 = l10 + l11
        # l1 = "     width  " + "{:6.3f}".format(self.wellWidth) + "  nm" + cr
        l20 = "     heightLeft  heightRight  "
        l21 = "{:6.3f}".format(self.wellHeightLeft) + sp
        l22 = "{:6.3f}".format(self.wellHeightRight) + "  eV" + cr
        l2 = l20 + l21 + l22
        # l2 = "     heightLeft  heightRight  "
        # + "{:6.3f}".format(self.wellHeightLeft) + sp \
        #  + "{:6.3f}".format(self.wellHeightRight) + "  eV" + cr
        dataB = dataB + l1 + l2
        return dataB

    # ---------------------- printAddedVArray ------------------------
    def printAddedVArray(self):
        """ prints addedV array to screen.

            The printout labels each column of the addedV array.
            The columns are:
                ID:  identification number of addedV potential
                xmin: start energy for potential
                xmax: ending energy for potential
                a,b,c: polynomial coeffs, V = a + b*x + c*x*x
        """
        sp = "  "
        strR = "Current AddedPE list" + "\n"

        if self.barrierCt > 0:
            strR0 = "    ID            lo         hi          "
            strR1 = "polynomial coeffs" + "\n"
            strR = strR0 + strR1
            # strR += "    ID            lo         hi
            # polynomial coeffs" + "\n"
            for i, v in self.barrierDict.items():
                xminS = "{:6.3f}".format(self.barriers[v][0])
                xmaxS = "{:6.3f}".format(self.barriers[v][1])
                v0S = "{:6.3f}".format(self.barriers[v][2])
                vsS = "{:6.3f}".format(self.barriers[v][3])
                vssS = "{:6.3f}".format(self.barriers[v][4])
                bar = xminS + sp + xmaxS + sp + v0S + sp + vsS + sp + vssS

                strR += "     " + str(i) + "          " + bar + "\n"
        else:
            strR += "     There are no internal potentials" + "\n"

        return strR

    # --------------------------- updateBarrierDict ------------------
    def updateBarrierDict(self):
        """used when adding new barrier, see calls from BuildPotentialWell
        """
        debug = False
        if debug:
            print("  -- updateAddedVDict")
        # import pdb; pdb.set_trace()
        barrDict = dict()
        if self.barrierCt > 0:
            count = 1
            for i, v in enumerate(self.barriers):
                if not (isclose(v[2], 0.0)
                        and isclose(v[3], 0.0)
                        and isclose(v[4], 0.0)):
                    # either v0,vs,or vss is nonzero
                    # so this v is a barrier row
                    barrDict[count] = i
                    count += 1

        self.barrierDict = barrDict.copy()

        if debug:
            print("count, self.barrierCt ", count, self.barrierCt)
            print("self.barrierDict ", self.barrierDict)
            print(" end of updateAddedVDict")

        return

    # --------------------------- pickleDpw ------------------------
    def writeDpwFile(self, dpwFileName):
        """ writes DataPotentialWell class instance to a .dpw file.

            This writer uses the python pickle.dump method to write
            all attributes of the DataPotentailWell instance to a
            binary file with a .dpw extension. Similarly, a reader,
            readDpwFile(), can read the attributes into a
            DataPotentialWell instance. A .dpw file is thus a means
            of saving all parameters of a  specific potential
            well for later use.

            Parameters:
                dpwFileName: string-typ

        """
        debug = False

        # check for .dpw file extension
        fbase, fext = os.path.splitext(dpwFileName)
        if fext != '.dpw':
            dpwFileName += '.dpw'

        if debug:
            print("  -- pickleDpw ")
            print(" ready to open file for writing: ", dpwFileName)
        f = open(dpwFileName, 'wb')
        if debug:
            print(" after open f")
        pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

        f.close()

    # --------------------------- unpickleDpw ------------------------
    def readDpwFile(self, fileName):
        """ reads .dpw file into a DataPotentialWell instance.

            This reader uses the python pickle.load method to read
            all DataPotentialWell attributes from a binary .dpw file
            into a DataPotentailWell instance. The writeDpwFile()
            method previously created the binary file with a .dpw
            extension using the python pickle.store method.  A .dpw
            file is thus a means of saving all parameters of a
            specific potential well for later use.

            Parameters:
                dpwFileName: string-type

        """
        debug = False
        if debug:
            print("  -- unpickleDpw ")
            print("  ready to open a fle for reading: ", fileName)

        f = open(fileName, 'rb')
        if debug:
            print("after opening file ")
        newDpw = pickle.load(f)
        f.close()

        if debug:
            newDpw.printData()

        # copy all well parameters from newDpw into self.dpw
        self.copyData(newDpw)

        # probably need to
        return newDpw

    # --------------------------- copyData ------------------------
    def copyData(self, newdpw):
        """ copy all well parameters from newdpw into self.dpw
        used internally

            Parameters:
                newdpw: DataPotentialWell instance
        """
        debug = False
        if debug:
            print("  -- copyData")
            print("      newdpw instance variable")
            print(newdpw)

        self.resetWell()
        self.barrierCt = newdpw.barrierCt
        self.numX = newdpw.numX
        self.barriers = np.copy(newdpw.barriers)
        self.xlow = newdpw.xlow
        self.xhigh = newdpw.xhigh
        self.wellWidth = newdpw.wellWidth
        self.wellHeightLeft = newdpw.wellHeightLeft
        self.wellHeightRight = newdpw.wellHeightRight

        self.xmin = newdpw.barriers[0][0]
        self.xmax = newdpw.barriers[len(self.barriers) - 1][1]
        self.xlow = newdpw.xlow
        self.xhigh = newdpw.xhigh
        self.binW = newdpw.binW
        self.k2 = newdpw.k2
        self.fractRt = newdpw.fractRt
        self.fractLf = newdpw.fractLf
        self.statStateNumber = newdpw.statStateNumber
        self.updateBarrierDict()
        self.dStates = newdpw.dStates

        self.psiArray = newdpw.psiArray
        self.psiEnergy = newdpw.psiEnergy
        if debug:
            print("       new dpw from read file ")
            self.printData()

    # --------------------------- getPsi ------------------------
    def getPsiArray(self):
        """ return non-normalized stationary state psi array.

            The stationary state psi array, calculated in the
            potential well solver, is the last psi array plotted
            in the findStationaryStates window. The array is empty
            if no stationary state wavefunction is plotted
            on the main window.

            Returns:
                non-normalized psi-array: float numpy array-type
        """
        debug = False
        if debug:
            print("starting getPsi ")
        return self.psiArray[:, 0]

    # --------------------------- getPsiArrayNormalized --------------
    def getPsiArrayNormalized(self):
        """ returns normalized stationary state psi array.

            The normalized stationary state psi array, calculated
            in the potential well solver, is the last psi array
            plotted in the findStationaryStates window. The array
            is empty if no stationary state wavefunction is
            plotted on the main window.
            Normalization constant =  sqrt( sum(psi*psi) * deltaX ).

            Returns:
                normalized psi-array: float numpy array-type

         """
        debug = False
        if debug:
            print("starting getPsiArrayNormalized")
        if np.isclose(self.psiEnergy, 0.0):
            return 0.0
        else:
            if np.isclose(self.psiNorm, 0.0):
                self.findPsiNorm()
            psi = self.psiArray[:, 0]
            return psi / self.psiNorm

    # --------------------------- findPsiNorm ------------------------
    def findPsiNorm(self):
        """ find normalization constant for normalizing
        psi and psiPrime arrays.
        """
        debug = False
        if debug:
            print("starting findPsiNorm")
        psi = self.psiArray[:, 0]
        sumForIntegral = np.sum(psi * psi) * self.binW
        self.psiNorm = np.sqrt(sumForIntegral)
        if debug:
            print("self.psiNorm ", self.psiNorm)

    # --------------------------- getPsiPrime ------------------------
    def getPsiPrimeArray(self):
        """ return non-normalized stationary state first
        derivative of psi array.

            The stationary state psi array, calculated
            in the potential well solver, is the last psi
            array plotted in the findStationaryStates window.
            The array is empty if no stationary state
            wavefunction is plotted on the main window.

            Returns:
                non-normalized first derivative of psi-array:
                float numpy array-type
        """

        debug = False
        if debug:
            print("starting getPsiPrime ")
        return self.psiArray[:, 1]

    # -------------- getPsiPrimeArrayNormalized -------------------
    def getPsiPrimeArrayNormalized(self):
        """ returns first derivative of normalized-psi array.

            Uses normalization constant determined from normalizing
            psi-array

            Returns:
                first derivative: float numpy array-type
        """
        debug = False
        if debug:
            print("starting getPsiPrimeArrayNormalized ")
        if np.isclose(self.psiEnergy, 0.0):
            return 0.0
        else:
            if np.isclose(self.psiNorm, 0.0):
                self.findPsiNorm()
            psiPrime = self.psiArray[:, 1]
            return psiPrime / self.psiNorm

    # --------------------------- getXArrau ------------------
    def getXArray(self):
        """ return array of x values used in solver

            The x-values in the x array include all points shown
            in the potential plot in the main window, including
            points outside of the potential well.
            The getXArrayIndexWellEdges() method returns the
            x-array indices corresponding to the well edges.

            Returns:
                array of x values: float numpy array-type

        """
        debug = False
        if debug:
            print("starting getX ")
        return self.psiArray[:, 2]

    # --------------------------- getVArray --------------------
    def getVArray(self):
        """ return array of potential energies used in solver.

        The V array includes a potential energy (eV) for each x
        in the x array.

        Returns:
            array of V values: float numpy array-type
        """

        debug = False
        if debug:
            print("starting getV ")
        return self.psiArray[:, 3]

    # --------------------------- getPsiEnergy --------------------
    def getPsiEnergy(self):
        """ returns the energy of last plotted wavefunction..

            The energy of the last plotted stationary state
            wavefunction in the findStationaryStates solver
            window.

            Returns: float-type
        """
        debug = False
        if debug:
            print("starting getPsiEnergy")
        return self.psiEnergy

    # --------------------- getBasicWellProperties -----------
    def getBasicWellProperties(self):
        """ return tuple (wellWidth, wellHeightLeft, wellHeightRight). """

        debug = False
        if debug:
            print("starting getBasicWellProperties")
            print("returning tuple: (width, VLeft, VRight) ")
        return (self.wellWidth, self.wellHeightLeft, self.wellHeightRight)

    # -------------- getXArrayIndexWellEdges ------------------------
    def getXArrayIndexWellEdges(self):
        """ returns indices of well edges in the x array.

            Returns: int numpy array: [left-edge index,
            right-edge index]
        """
        debug = False
        if debug:
            print("starting getXArrayIndexWellEdges")
        x = self.getXArray()
        i_min = np.where(np.isclose(x, self.xmin))[0][0]
        i_max = np.where(np.isclose(x, self.xmax))[0][0]

        return np.array([i_min, i_max])

    # ----------------- getNumberOfAddedVPotentials -----------------
    def getNumberOfAddedVPotentials(self):
        """ returns the number of internal added potentials
        in potential well.

            Returns:
               Number of added potentials: int-type
        """
        return self.barrierCt

    # ----------------------- getBarriersArray ----------------
    def getPotentialList(self):
        """ array of all potential energy functions
        used in potential well.

            Each row in the array has the following fields:
                starting energy:
                ending energy:
                three polynomial coefficients, a,b,c where
                   V = a + b*x + c*x*x

            Returns:
               numpy float array
        """
        return self.barriers

    # ---------------------- getXBinWidth ------------------
    def getXBinWidth(self):
        """ return width of each x bin.

            Returns:
                bin width: float
        """
        return self.binW

    # ----------------- get2mOverhbar2 ------------------
    def get2mOverhbar2(self):
        """ 2*m/(hbar^hbar) for electron in eV/(nm*nm)
            This is set in BuildPotential well,
            sorry for rhe confusion

            Returns:
                float-type
        """
        return self.k2

    # ---------------- getStationaryStateEnergies ---------
    def getStationaryStateEnergies(self):
        """ Returns: numpy array float-type """
        if len(self.dStates) == 0:
            return 0
        return np.array(list(self.dStates.values()))
