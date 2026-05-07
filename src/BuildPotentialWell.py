import numpy as np
from numpy import isclose
from scipy import constants as cons


# utility function
def prS(floatVar):
    """
    function to format floats for printing with 6.3f format
    """
    return "{:6.3f}".format(floatVar)


class BuildPotentialWell:
    """
    class BuildPotentialWell first creates a simple square well, additional
    barriers added using the addBarrier method;  barrier types include
    square, linear, and quadratic shapes.
    A DataPotentialWell class reference must be passed in the constructor;
    BuildPotentialWell fills the DataPotentialWell instance used to carry all
    well parameters to other classes such as the plotter and solver classes.

    The fraction of the well width to the right and left of the well edges
    are set by attributes in this class and are stored in
    the DataPotentialWell instance.  Attribute names are:

    fractRt (default = 0.2)
    fractLf (default = 0.2)

    Methods:

    constructor: __init__(DataPotentialWell, well width(nm),
    well height left (eV), well height right (eV))

    setBasicWellParms(w_width,w_heightL, w_heightR):
           sets well width and left/right edge heights

    addBarrier(xmin1,xmax1,v0,vs,vss)
           xmin1/xmax1  (nm): barrier lower and upper limits (barrier range)
           v0,vs,vss:  v (eV) = v0 + vs*x + vxx*x*x
           where x is relative to the barrier not the potential well

    removeBarrier(barrierNum)
           removes barrier with barrier number, barrierNum.

    addHarmonOscillPotential(position,kho)
           position: either "Center" or "Left", sets minimum of the sho well
               relative to potential well
           kho:  defines harmonic oscillator, 1/2 kho x*x, x is with
               respect to minimum of sho well

    finishWell()
           complete filling DataPotentialWell instance. Must be called
           after completing well construction or making changes to an
           existing well described in the DataPotenetialWell instance.

    buildNewWell(wid, hgtL, hgtR)
        reset and build new simple well with these width and heights
    """

    def __init__(self, dpw, ww1=0.40, whl1=64., whr1=64.):
        """ init method for BuildPotentialWell

        Parameters:
            dpw:  DataPotenetialWell instance
            ww1 (default 0.40): Well width (nm)
            whl1 (default 64.): Well height on left (eV)
            whr1 (default 64.): Well height on right (eV)
        """
        debug = False
        self.dpw = dpw
        self.wellHeightLeft = whl1
        self.wellHeightRight = whr1
        self.dpw.barrierCt = 0  # no internal barriers yet
        self.wellWidth = ww1

        self.xlow = 0.0
        self.xhigh = 0.0
        # setup barrier np.array (xmin,xmax,v,vs,vss) for each element
        #    starting from left
        self.barriers = np.array([[0.0, ww1, 0.0, 0.0, 0.0]])
        self.fractRt = 0.2  # hard coded for now, can set externally ok
        self.fractLf = 0.2

        # set up constants for electron: 2*m/hbar**2, get values from scipy
        # may want to do the same for proton/neutron
        # change following to eliminate warning from scipy.constants:
        #    C.Duke 16March2022
        #hbarc = cons.value('Planck constant over 2 pi times c in MeV fm')
        hbarc = cons.value('reduced Planck constant times c in MeV fm')
        if (False):
            print('hbarc = ',hbarc)
        eEnergy = cons.value('electron mass energy equivalent in MeV')
        self.k2 = 2 * eEnergy * 1.0e+06 / (hbarc * hbarc)  # 26.25 1/(eV*nm*nm)

        if debug:
            print("-- in __init__")
            for r in self.barriers:
                print("barriers np.array", r)
                print("    barriers shape ", self.barriers.shape)
        # write default well to DataPotentialWell instance
        self.finishWell()
        if debug:
            print("at end of constructor")
            self.dpw.printData()

    ###########################################################################
    def setBasicWellParms(self, w_width, w_heightL, w_heightR):
        """
            setBasicWellParms: well width, well-height left and right
            Parameters:
                w_width:   well width
                w_heightL: well-height left
                w_heightR: well-height right

            Returns:
                None
        """
        debug = False
        self.barriers[0] = np.array([0.0, w_width, 0.0, 0.0, 0.0])
        self.wellHeightLeft = w_heightL
        self.wellHeightRight = w_heightR
        self.wellWidth = w_width
        self.finishWell()
        if debug:
            print("in setBasicWellParms")
            print("        wellHeightLeft/Right ", self.wellHeightLeft,
                  self.wellHeightRight)
            print("      barriers")
            for r in self.barriers:
                print("barriers np.array", r)
            print("    barriers shape ", self.barriers.shape)
            print("  printData end of setBasicWellParameters")
            self.dpw.printData()
        return

    ###########################################################################
    def addHarmonOscillPotential(self, centerFlag, vxmax):
        """  adds harmonic oscillator internal potential to well

        Parameters:
            centerFlag: either "Center" or "Left", sets minimum of the sho well
                        relative to potential well
            kho:  defines harmonic oscillator, 1/2 kho x*x, x is with
            respect to minimum of sho well

        Returns: None

        """
        debug = False
        if debug:
            print(" in addHarmonicOscillatorPotential")
            print("centerFlag vxmax ", centerFlag, vxmax)

        v0 = 0.0
        vs = 0.0
        vss = 0.0
        xmax1 = self.dpw.xmax
        xc = xmax1 / 2.0
        ksho = 0.0

        wellHL = vxmax
        wellHR = vxmax
        wellWidth = self.dpw.wellWidth

        if centerFlag:
            ksho = 2.0 * vxmax / (xc * xc)
            v0 = 0.5 * ksho * xc * xc
            vs = -ksho * xc
            vss = 0.5 * ksho

            wellHL = vxmax
            wellHR = vxmax
            if debug:
                print("wellHL wellHR wellWidth ", wellHL, wellHR,
                      self.dpw.wellWidth)
                print("      before setBasicWell ")
                self.dpw.printData()

        else:
            print("left ")
            ksho = 2.0 * vxmax / (xmax1 * xmax1)
            v0 = 0.0
            vs = 0.0
            wellHL = self.dpw.wellHeightLeft
            wellHR = vxmax
            vss = vxmax / (xmax1 * xmax1)
            # debug check at x = 0.0, xc, and xmax
            if debug:
                x = 0.0
                print(" x v ", x, v0 + vs * x + vss * x * x)
                x = xc
                print(" x v ", x, v0 + vs * x + vss * x * x)
                x = xmax1
                print(" x v ", x, v0 + vs * x + vss * x * x)
                print("wellHL wellHR wellWidth ", wellHL, wellHR,
                      self.dpw.wellWidth)
                print("      before setBasicWell ")
                self.dpw.printData()

        # remake well, set edges to vxmax, should put in calling method
        self.buildNewWell(wellWidth, wellHL, wellHR)

        if debug:
            print("      after setBasicWellParameters")
            self.dpw.printData()

        # add sho as internal barrier
        self.dpw.barriers[0][2] = v0
        self.dpw.barriers[0][3] = vs
        self.dpw.barriers[0][4] = vss
        self.dpw.barrierCt += 1

        self.dpw.updateBarrierDict()
        if False:
            print("after add sho barrier")
            print('ba')
            print(self.dpw.barriers)
            print('printData')

            self.dpw.printData()

        return

    ###########################################################################
    def addBarrier(self, xmin1, xmax1, v0, vs, vss):
        """ Adds internal barrier to well

        Parameters:
            xmin1/xmax1: barrier lower and upper limits (barrier range in nm)
            v0,vs,vss:  v (eV) = v0 + vs*x + vxx*x*x
                   where x is relative to the barrier not the potential well
        """
        debug = False
        if debug:
            print(" -- addBarrier", prS(xmin1), prS(xmax1), prS(v0), prS(vs),
                  prS(vss))

        # best to start with a copy since using vstack,insert,etc.
        # these np builtins create a new array that no longer references
        #     self.dpw.barrier
        ba = np.copy(self.dpw.barriers)

        # the next function arg is a list comprehension - iterable
        indexL = next(
            (i for i, v in enumerate(ba)
             if ((xmin1 >= v[0])
                 and (xmax1 <= v[1])
                 and isclose(v[2], 0.0)
                 and isclose(v[3], 0.0)
                 and isclose(v[4], 0.0))), None)

        if debug:
            print(" ba ")
            print(ba)
            print("indexL ", indexL)

        if indexL is None:
            if debug:
                print('incorrect new barrier limits')
                print('no new barrier added')
            return False
        self.dpw.barrierCt += 1
        # upper and lower edges of indexL row of ba np.array
        xminL = ba[indexL][0]
        xmaxL = ba[indexL][1]

        # import pdb; pdb.set_trace()

        # case 1:  xmin1 == xminL
        if isclose(xmin1, xminL):
            # can fill entire region
            row1 = [xmin1, xmax1, v0, vs, vss]
            ba[indexL] = row1

            # does not fill entire indexL region
            if not isclose(xmax1, xmaxL):
                ba[indexL] = row1
                row2 = [xmax1, xmaxL, 0.0, 0.0, 0.0]
                # append row1 and 2
                if isclose(xmaxL, self.dpw.xmax):
                    ba = np.vstack([ba, row2])
                # np.insert row2 before indexL+1
                else:
                    ba = np.insert(ba, indexL + 1, row2, axis=0)

        # xmin1 is not equal to xminL
        else:
            # xmax1 = xmaxL, fill upper region of indexL
            if isclose(xmax1, xmaxL):
                ba[indexL][1] = xmin1
                row2 = [xmin1, xmax1, v0, vs, vss]
                if isclose(xmaxL, self.dpw.xmax):
                    ba = np.vstack([ba, row2])
                # np.insert row2 before indexL+1
                else:
                    ba = np.insert(ba, indexL + 1, row2, axis=0)
            # xmax1 != xmaxL
            else:
                ba[indexL][1] = xmin1
                row1 = [xmin1, xmax1, v0, vs, vss]
                row2 = [xmax1, xmaxL, 0.0, 0.0, 0.0]
                if isclose(xmaxL, self.dpw.xmax):
                    ba = np.vstack([ba, row1])
                    ba = np.vstack([ba, row2])
                # np.insert rows before indexL+1
                else:
                    ba = np.insert(ba, indexL + 1, row1, axis=0)
                    ba = np.insert(ba, indexL + 1, row2, axis=0)

        # reset dpw.barriers
        self.dpw.barriers = np.copy(ba)
        # update the barrier Dictionary from self.dpw.barriers
        self.dpw.updateBarrierDict()
        if debug:
            print("after barrier addition")
            print(ba)
        return True

    ###########################################################################
    def removeBarrier(self, barrierNum):
        """ removes barrier with barrier number, barrierNum.

        Parameters:
            barrierNum: number of barrier to remove

        Returns:
            retFlag: False in all cases, currently not used

        """
        # notation used in this method
        #   iB, iP, iM:  record number in barriers np.array (iP / iM =-1
        #      if does't exist)
        #   iPFlag, iMFlag:  if True, records exist
        #   xmin, xmax:  limits on potential well
        #   xBmin/max,  xPmin/max, xMmin/max:  record x limits
        #   baPFlag, baMFlag:  if True, P/M are barrier records
        #       S(with one of the v's nonzero)
        #   ba dictB: self.dpw.barriers,  self.dpw.barrierDict
        #   baList: list of barrier record numbers that contain
        #      at least one non-zero v

        debug = False
        if debug:
            print("  -- removeBarrier: barrierNum ", barrierNum)
        retFlag = False

        # have to work with a copy since using np.insert,delete, etc.
        ba = np.copy(self.dpw.barriers)
        dictB = self.dpw.barrierDict

        # is iBnum in barrierDict
        if barrierNum not in dictB:
            if debug:
                print("barrier number not in barrierDict")
                print("barrier number  barrierDict ", barrierNum, dictB)
            return False

        # create indice list for barrier np.array records containing barriers
        baList = list(dictB.values())

        # get limits on barrier regions
        xmin = self.dpw.xmin
        xmax = self.dpw.xmax

        iB = dictB[barrierNum]
        xBmin = ba[iB][0]
        xBmax = ba[iB][1]

        # initialize these first
        xPmin = -1.0
        xPmax = -1.0
        xMmin = -1.0
        xMmax = -1.0
        iMFlag = False
        iPFlag = False
        iP = -1
        iM = -1
        baPFlag = False
        baMFlag = False

        # do barrier records above and below iBarrier exist
        # first, look below iBarrier
        if iB > 0:
            # ba record below iB exists
            iMFlag = True
            iM = iB - 1
            xMmin = ba[iM][0]
            xMmax = ba[iM][1]

        if not isclose(xmax, xBmax):
            # ba record above iB exists
            iPFlag = True
            iP = iB + 1
            xPmin = ba[iP][0]
            xPmax = ba[iP][1]

        # are the records above/below barrier records?
        if iM in baList:
            baMFlag = True
        if iP in baList:
            baPFlag = True

        # ready for logic to remove barrier, fix up ba, and recreate dataDict
        # no minus record (so barrier starts at xmin)
        if not iMFlag:
            # but with a plus record
            if iPFlag:
                if not baPFlag:
                    # plus record is not a barrier record
                    # resize plus record and delete barrier record
                    ba[iP][0] = xmin
                    ba = np.delete(ba, iB, axis=0)
                else:
                    # plus record is a barrier record, redo barrier record
                    row = [xBmin, xBmax, 0.0, 0.0, 0.0]
                    ba[iB] = row

            else:
                # there is no ipflag, so barrier covers entire region
                row = [xBmin, xBmax, 0.0, 0.0, 0.0]
                ba[iB] = row

        else:
            # so there is an iM record
            if not iPFlag:
                # no iP record, at top of region
                if not baMFlag:
                    ba[iM][1] = ba[iB][1]
                    ba = np.delete(ba, iB, axis=0)
                else:
                    ba[iB][2] = 0.0
                    ba[iB][3] = 0.0
                    ba[iB][4] = 0.0
            else:
                # there is an iP record and an iM record, 4 possibilities
                if baPFlag:
                    if baMFlag:
                        ba[iB][2] = 0.0
                        ba[iB][3] = 0.0
                        ba[iB][4] = 0.0
                    else:
                        ba[iM][1] = ba[iB][1]
                        ba = np.delete(ba, iB, axis=0)
                else:
                    if baMFlag:
                        ba[iP][0] = ba[iB][0]
                        ba = np.delete(ba, iB, axis=0)
                    else:
                        ba[iM][1] = ba[iP][1]
                        ba = np.delete(ba, iP, axis=0)
                        ba = np.delete(ba, iB, axis=0)

        self.dpw.barrierCt -= 1

        if debug:
            print("   variables")
            print(" ba ")
            for i, v in enumerate(ba):
                print("      ", i, "   ", v)
            print("barriers ", end=' ')
            for i, v in enumerate(self.dpw.barriers):
                print("     ", i, "     ", v)
            print(" dictB ", dictB)
            print(" iB, iP, iM ", iB, iP, iM)
            print(" iPFlag, iMFlag ", iPFlag, iMFlag)
            print(" xmin, xmax ", xmin, xmax)
            print(" xBmin xBmax ", xBmin, xBmax)
            print(" xPmin, xPmax ", xPmin, xPmax)
            print(" xMmin xMmax ", xMmin, xMmax)
            print(" baPFlag, baMFlag ", baPFlag, baMFlag)
            print("  baList ", baList)

        # reset dpw.barriers
        self.dpw.barriers = np.copy(ba)
        # update the barrier Dictionary from self.dpw.barriers
        self.dpw.updateBarrierDict()

        if debug:
            print("barrierCt ", self.dpw.barrierCt)
            print("barrierDict", self.dpw.barrierDict)
            print("barriers ", self.dpw.barriers)
            print("     end of removeBarrier")

        return retFlag

    ###########################################################################
    def finishWell(self):
        """ complete filling DataPotentialWell instance. Must be called
        after completing well construction or making changes to an
        existing well described in the DataPotenetialWell instance.

        """
        debug = False
        self.dpw.barriers = np.copy(self.barriers)
        self.dpw.xlow = self.xlow
        self.dpw.xhigh = self.xhigh
        self.dpw.wellWidth = self.wellWidth

        self.dpw.wellHeightLeft = self.wellHeightLeft
        self.dpw.wellHeightRight = self.wellHeightRight

        if not np.isfinite(self.wellHeightLeft) and not np.isfinite(
                self.wellHeightRight):
            self.dpw.infiniteWellFlag = True

        self.dpw.xmin = self.barriers[0][0]
        self.dpw.xmax = self.barriers[len(self.barriers) - 1][1]
        self.dpw.xlow = self.dpw.xmin - self.fractRt * self.wellWidth
        self.dpw.xhigh = self.dpw.xmax + self.fractLf * self.wellWidth
        self.dpw.k2 = self.k2
        self.dpw.fractRt = self.fractRt
        self.dpw.fractLf = self.fractLf

        if debug:
            print("  -- finishWell")
            print("xmin wellWidth ", self.dpw.xmin, self.wellWidth)
            print("dpw.xlow ", self.dpw.xlow)
            print("printData at end of finishWell")
            self.dpw.printData()

        return 0

# -------------- buildNewWell -----------------------------------------------

    def buildNewWell(self, wid, hgtL, hgtR):

        """ build a new well with these well parameters

        Parameters:
            wid:  well width (nm)
            hgtL: potential energy at left well edge (eV)
            hgtR: potential energy at right well edge (eV)

            method calls dpw.resetWEll and setBasicWellParms
        """
        debug = False
        if debug:
            print("in buildNewWell with BuildPotentialWell")
            # self.dpw.printData()

        # make sure that well is reset (may want to change this later)
        self.dpw.resetWell()

        self.setBasicWellParms(wid, hgtL, hgtR)

        if debug:
            print(" in buildNewWell after set new well parameters")
            self.dpw.printData()
