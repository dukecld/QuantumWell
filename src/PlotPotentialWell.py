# indep. well plotting class

import numpy as np
from matplotlib.patches import Rectangle


class PlotPotentialWell:
    """
    PlotPotentialWell class, uses potential well parameters from
    DataPotentialWell instance to make a plot of the well

    Methods
    Constructor: __init__(ax.dpw,infHeight=100.0)
           ax:  externally supplied axis reference
           dpw:  DataPotentialWell reference, contains well data
           infHeight=100.0 eV: height to plot infinite height barriers

    makeNormalPlot():  makes the plot, but not the energy lines

    addEnergyLine(e):  adds horizontal line at energy e, can be
                       called either before or after
                       calling makeNormalPlot
    """

    def __init__(self, ax, dpw1, infHeight=100.0):

        # graph axis
        self.ax = ax

        # dStatesPlot[int] = line pointer from plt.plot commands
        self.dStatesPlot = dict()

        self.barriers = dpw1.barriers
        self.infiniteHeight = infHeight
        self.dpw = dpw1
        self.lineH = list()

    # ------------- setupPlot -----------------
    def setupPlot(self):
        """
        fills various arrays and parameters from dpw to be
        used by the plotter later,
        internal use to this class only

        """

        self.wellHeightLeft = self.dpw.wellHeightLeft
        self.wellHeightRight = self.dpw.wellHeightRight
        self.wellWidth = self.dpw.wellWidth
        self.barriers = self.dpw.barriers

        # get plot limits, both in x and in V
        self.xmin = self.dpw.xmin
        self.xmax = self.dpw.xmax
        self.vmax = 0.0
        self.fractRt = self.dpw.fractRt
        self.fractLf = self.dpw.fractLf
        # set xlow and xhigh
        self.xlow = self.dpw.xlow
        self.xhigh = self.dpw.xhigh

        # axis labels
        self.xlabel = "well position in nanometers (nm)"
        self.ylabel = "electron energy in electron volts (eV)"
        self.title = "quantum mechanical potential well"

        debug = False
        if debug:
            print("  -- PlotPotentialWell::--init--")
            print("         barriers", self.barriers)
            print("         xlow,xmin,xmax,xhigh", self.xlow, self.xmin,
                  self.xmax, self.xhigh)
            print("         wellWidth", self.wellWidth)
            print("         wellHeightLeft/Right", self.wellHeightLeft,
                  self.wellHeightRight)

        # do we have a harmonic oscillator potential? look for x*x coeff.

        tt, = np.nonzero(self.barriers[0][2:])
        self.hoPot = tt.size
        # if hoPot=0, then no harmonic oscill potential has been added

        if debug:
            print("hoPot=0, no har.oscill. added. hoPOT = ", self.hoPot)

        self.vmax = self.getMaxHeight()
        self.dpw.vmax = self.vmax

        # set left/right vheight to infiniteHeight if necessary
        if not np.isfinite(self.wellHeightLeft):
            self.wellHeightLeft = self.infiniteHeight
            # add arrow and text to show infinite height
            self.ax.text(self.xlow * 0.9,
                         self.infiniteHeight * 0.95,
                         r'$\uparrow$ to $\infty$',
                         fontsize=16)

        if not np.isfinite(self.wellHeightRight):
            self.wellHeightRight = self.infiniteHeight
            self.ax.text(self.xhigh * 0.85, self.infiniteHeight * 0.95,
                         r'$\uparrow$ to $\infty$', fontsize=16)

        # find vertical scale, need to treat ho as special case later

        if self.hoPot == 0:
            lv = []
            lv.append(self.wellHeightLeft)
            lv.append(self.wellHeightRight)

            for bb in self.barriers:
                if (bb[3] == 0.0) and (bb[4] == 0.0):
                    # have horizontal surface
                    lv.append(bb[2])
                    if (bb[3] != 0.0) or (bb[4] != 0.0):
                        lv.append(bb[2])
                        x = np.linspace(0.0, bb[1] - bb[0])
                        v = bb[2] + bb[3] * x + bb[4] * x * x
                        lv.append(v)

        if debug:
            print("        wellHeightLeft/Right vmax", self.vmax,
                  self.wellHeightLeft, self.wellHeightRight,
                  self.wellWidth)

    # ---------------- getMaxHeight ------------------------
    def getMaxHeight(self):
        """
        internal use only
        """
        debug = False
        # find maxv, calculate infiniteHeight if necessary
        lv = [self.dpw.wellHeightLeft, self.wellHeightRight]
        vmaxTmp = max(lv)
        vminTmp = min(lv)
        if vmaxTmp != np.inf:
            maxHeight = vmaxTmp * 1.25
        else:
            if vminTmp == np.inf:
                maxHeight = self.infiniteHeight
            else:
                if vminTmp > self.infiniteHeight:
                    maxHeight = vminTmp * 1.25
                    self.infiniteHeight = maxHeight
                else:

                    maxHeight = self.infiniteHeight
        if debug:
            print("  -- in getMaxHeight")
            print("     lv  maxHeight", lv, maxHeight)
            print("     infiniteHeight ", self.infiniteHeight)

        return maxHeight

    # ------------------- makeNormalPlot -------------------------
    def makeNormalPlot(self, infHeight=100):
        """ Makes all potential energy plots

        """

        self.ax.clear()
        colorL = 'brown'
        alphaL = 0.3
        self.infiniteHeight = infHeight
        self.setupPlot()
        debug = False
        if debug:
            print("  -- makeNormalPlot")
            print("    vmax ", self.vmax)
        ax = self.ax
        ax.set_ylim(0.0, self.vmax)
        ax.set_xlim(self.xlow, self.xhigh)

        # add labels
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.set_title(self.title)

        # plot rectangles, maybe via a collection later
        if debug:
            print("       rectangle parameters")
            print("       self.xlow self.xmin, self.xmax, self.xhigh",
                  self.xlow, self.xmin, self.xmax, self.xhigh)
            print("       well heights left/right", self.wellHeightLeft,
                  self.wellHeightRight)

        rect = Rectangle((self.xlow, 0.0), self.xmin - self.xlow,
                         self.wellHeightLeft, ec="none", alpha=alphaL,
                         color=colorL)
        ax.add_patch(rect)
        rect = Rectangle((self.xmax, 0.0), self.xhigh - self.xmax,
                         self.wellHeightRight, ec="none",
                         alpha=alphaL, color=colorL)
        ax.add_patch(rect)

        for row in self.barriers:

            # plot additional square barriers (using Rectangle patches)
            if ((row[2] > 0.0) and (row[3] == 0.0) and (row[4] == 0.0)):
                rect = Rectangle((row[0], 0.0), row[1] - row[0],
                                 row[2], ec="none",
                                 alpha=alphaL, color=colorL)
                ax.add_patch(rect)
            # plot any sloping barriers
            if ((row[3] != 0.0) or (row[4] != 0.0)):
                xminb = row[0]
                xmaxb = row[1]
                ab = row[2]
                bb = row[3]
                cc = row[4]
                if debug:
                    print(xminb, xmaxb, ab, bb, cc)
                x = np.linspace(xminb, xmaxb, 500)

                v = ab + bb * (x - xminb) + cc * (x - xminb) * (x - xminb)
                if debug:
                    print(" in Plot xminb xmaxb ab bb cc ", xminb, xmaxb, ab,
                          bb, cc)

                self.ax.fill_between(x,
                                     v,
                                     where=v > 0,
                                     color=colorL,
                                     alpha=alphaL)

        ax.grid(axis='both')

    # ------------------ addEnergyLine ------------------------
    def addEnergyLine(self, e):
        """ Plot energy line at energy e

        """

        debug = False
        if debug:
            print("  -- addEnergyLine")
            print("         e, self.xmin, self.xmax, self.vmax", e, self.xmin,
                  self.xmax, self.vmax)
        # start with line at height e, from xmin to xmax
        if e < self.vmax:
            pt1 = [self.xlow, self.xhigh]
            pt2 = [e, e]
            self.lineH = self.ax.plot(pt1, pt2, 'k', linewidth=1.0)

    # ------------------- removeEnergyLine --------------------
    def removeEnergyLine(self):
        """ Remove energy line if lineM has value
        """
        if len(self.lineH) > 0:
            self.lineH.pop(0).remove()

    # ----------------------- addEnergyLinesFromDict ---------------------
    def addEnergyLinesFromDict(self):
        """ Adds energy lines for each stationary state,
            energies from dStates dictionary

        """

        debug = False
        if debug:
            print("  -- addEnergyLinesFromDict")
            print("         self.vmax", self.vmax)
            print("  dictionary from dpw")
            for i, v in self.dpw.dStates.items():
                print(i, v)

        # start with line at height e, from xmin to xmax
        if len(self.dStatesPlot) == 0:
            for i, e in self.dpw.dStates.items():
                if e < self.vmax:
                    pt1 = [self.xlow, self.xhigh]
                    pt2 = [e, e]
                    # just store the line reference rather than
                    # the list returned by plot
                    # for plotting one line, len(ax.plot(...)
                    # is always 1, nothing missed
                    self.dStatesPlot[i] = (self.ax.plot(pt1,
                                                        pt2,
                                                        'k',
                                                        linewidth=1.0))[0]
