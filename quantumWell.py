
# quantum potential well
#       Charlie Duke
#       Physics Department, Grinnell College
#       duke@grinnell.edu

import sys
import os
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import pickle

# add path to src and to Utilities
_pth = Path(sys.path[0])
_pthsrc = _pth / 'src'
_pthutil = _pth / 'Utilities'
sys.path.insert(0, str(_pthsrc))
# sys.path.insert(0,str(_pthutil))
# print(sys.path)

if sys.version_info[0] < 3:
    raise Exception("Must use Python 3")

#######################################################

# PyQt5 GUI modules
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, \
    QWidget, QVBoxLayout
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore

# set matplotlib backend for PyQt
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from MatplotlibWidget import MatplotlibWidget
from PlotPotentialWell import PlotPotentialWell
from DataPotentialWell import DataPotentialWell
from BuildPotentialWell import BuildPotentialWell
from SolvePotentialWell import SolvePotentialWell
from FindStationaryStates import FindStationaryStates
from plotPsi import plotPsi

from utilQt import sendMessageTE, BuildWellDock, SolveWellDock
from utilQt import MessageDock, printMessageTE, saveMessageTE
from utilQt import AddBarrierDock, RemoveBarrierDock, \
    FindStatesWellDock
from utilQt import AddSlopedPotentialDock, AddSHODock, MainDockWidget
from utilQt import AddMultiBarriersDock, InfoDock, AddVpeDock
from utilQt import stringToInt, stringToFloat

###############################################################
###############################################################


class PotentialWellWindow(QMainWindow):
    """  class for event loop, initiate in __main__
    """

    # ################## __init__ ###################################
    def __init__(self):

        super().__init__()

        # Name of visible floating window
        # initialize with None since yet to create windows
        self.openDockName = None

        # make dictionary connecting openDockName with close functions.
        # will go away after eliminating close buttons
        self.makeDockCloseDict()

        # error messages
        # message for non-floating point entry error
        self.errorMFloat = "One of your entries is not a floating \
            point number, try again"
        self.errorMInt = "One of your entries is not an integer, try again"

        # instantiate DataPotentialWell class
        self.dpwFileName = None
        self.dpw = DataPotentialWell()

        # create axis and fig variablesfor delSlope graph
        # (can be used in any method with self.)
        self.axDs = None
        self.figDelSlope = None

        # ==============================================================
        # ----------------- create MainWindow widget -------------

        # self inherits from QMainWindow and can thus use QtGui and
        #     QMainWindow methods
        # set window title
        self.setWindowTitle("Potential Well: Main Window")

        # instantiate main widget. It will be the main window
        # later self.setCentralWidget(self.main_widget) will place
        # self.main_widget into self, the QMainWindow.
        self.main_widget = QWidget()

        # set the focus on the main widget and set central widget
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        # get sizes of main window and dockwidgets
        self.setWindowSizes()

        # create a vertical box layout with main_widget as parent
        # this box will contain the matplotlib widget ane
        # the navigation toolbar widget previously created
        vbl = QVBoxLayout(self.main_widget)

        # ===============================================================
        # ============ create widgets for the main window ===============

        # ------------------- create matplotlib widget --------------
        # self.mpl_init creates self.mpl, self.axes, and self.axTwinx
        self.mpl_init()

        # make a navigation toolbar wizard tied to the mpl wizard
        # create self.vtoolbar. Connect print button to mpl.goPrinter
        self.mpl_toolbar_init()

        # add mpl widget and toolbar to the vertical box layout
        # reverse order to place toolbar above plot
        vbl.addWidget(self.mpl)
        vbl.addWidget(self.vtoolbar)

        # -------------------- create main dock widget -------------------
        # instantiate the main dock widget, add to the main window
        self.maindw = MainDockWidget()
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.maindw)

        # connect all maindock pushbuttons
        self.maindock_init()

        # ===================================================================

        # ==============create dock widgets ===========================
        # -------------------- create message dock widget ---------------

        self.mswd = MessageDock()
        leftm = int(self.swidth * 0.01)
        topm = int(self.qrt.height() * .8)
        sizemw = int(self.swidth / 4)
        sizehw = int(self.sheight / 2.8)
        if False:
            print("leftm topm sizemw sizehw: ", leftm, topm, sizemw, sizehw)
            sizemw = 200
            print(" new sizemw:", sizemw)

        self.mswd.setGeometry(leftm, topm, sizemw, sizehw)

        # signal/slots for MessageDock

        self.mswd.pb_save.clicked.connect(
            lambda: saveMessageTE(self.mswd.te_message))
        self.mswd.pb_print.clicked.connect(
            lambda: printMessageTE(self.mswd.te_message))

        self.mswd.show()

        # self.mswd.te_message.moveCursor(QtGui.QTextCursor.Start)

        str1 = "*************** log for potentialWell.py ***************"
        sendMessageTE(str1, self.mswd.te_message)

        # -------------- create BuildPotentialWell dock ---------------

        #  dpw defaults set in constructor
        self.sp = BuildPotentialWell(self.dpw)
        ssstr = "   Initial Well \n" + self.dpw.printBasicWellParms()
        sendMessageTE(ssstr, self.mswd.te_message)
        # sendMessageTE(self.dpw.printBasicWellParms(),self.mswd.te_message )

        # instantiate BuildWellDock, don't show it until called, \
        # set geometry here
        self.buildwd = BuildWellDock()

        if False:
            self.printWidPosSize(self.buildwd, "before setGeometry",
                                 self.buildwd.objectName())
            print("leftWid topWid widthWid heightWid ", self.leftWid,
                  self.topWid, self.widthWid, self.heightWid)

        self.buildwd.setGeometry(self.leftWid, self.topWid, self.widthWid,
                                 self.heightWid)

        if False:
            self.printWidPosSize(self.buildwd, "after setGeometry",
                                 self.buildwd.objectName())

        # signal/slots for BuildWellDock
        self.buildwd.pb_ok.clicked.connect(self.buildOK)
        # self.buildwd.te_message.clear()

        # ------------------- create AddBarrier dock ----------------------

        self.addwd = AddBarrierDock()

        if False:
            self.printWidPosSize(self.addwd, "before setGeometry",
                                 self.addwd.objectName())
            print("leftWid topWid widthWid heightWid ", self.leftWid,
                  self.topWid, self.widthWid, self.heightWid)

        self.addwd.setGeometry(self.leftWid, self.topWid, self.widthWid,
                               self.heightWid)

        if False:
            self.printWidPosSize(self.addwd, "after setGeometry",
                                 self.addwd.objectName())

        # signal/slots for AddBarrierDock
        self.addwd.pb_add.clicked.connect(self.addBarrierOK)

        # ------------------- create AddMultiBarriers dock -------------------
        # instantiate addbarrierdock
        self.addmultiwd = AddMultiBarriersDock()

        if False:
            self.printWidPosSize(self.addwd, "before setGeometry",
                                 self.addmultiwd.objectName())
            print("leftWid topWid widthWid heightWid ", self.leftWid,
                  self.topWid, self.widthWid, self.heightWid)

        self.addmultiwd.setGeometry(self.leftWid, self.topWid, self.widthWid,
                                    self.heightWid)

        if False:
            self.printWidPosSize(self.addwd, "after setGeometry",
                                 self.addmultiwd.objectName())

        # signal/slots for AddMultiBarrierDock
        self.addmultiwd.pb_addbarriers.clicked.connect(self.addMultiBarriersOK)

        # ---------------------- create RemoveBarrier dock------------------
        self.rembwd = RemoveBarrierDock()
        self.rembwd.setGeometry(self.leftWid, self.topWid, self.widthWid,
                                self.heightWid)

        # signal/slots for RemoveBarrierDock
        self.rembwd.pb_ok.clicked.connect(self.removeBarrierNum)

        # --------------------- create Add Sloped Base dock -------------------
        self.addspwd = AddSlopedPotentialDock()
        self.addspwd.setGeometry(self.leftWid, self.topWid, self.widthWid,
                                 self.heightWid)

        # signal/slots for AddSlopedPotentialDock
        self.addspwd.pb_ok.clicked.connect(self.addSlopedBaseOK)

        # --------------------- create Add Vpe dock -------------------
        self.addvpe = AddVpeDock()
        self.addvpe.setGeometry(self.leftWid, self.topWid, self.widthWid,
                                self.heightWid)

        # signal/slots for AddVpeDock
        self.addvpe.pb_add.clicked.connect(self.addVpeDockOK)

        # ------------------- create add Simple Harmonic Oscillator dock-------
        self.addshowd = AddSHODock()
        self.addshowd.setGeometry(self.leftWid, self.topWid, self.widthWid,
                                  self.heightWid)

        # signal/slots for AddSHODock
        self.addshowd.pb_ok.clicked.connect(self.addSHODockOK)

        # --------------------- create InfoDock ------------------------
        self.infodock = InfoDock()
        self.infodock.setGeometry(self.leftWid, self.topWid, self.widthWid,
                                  self.heightWid)
        # self.infodock.textEdit.clear()
        # signal/slots for InfoDock
        # self.infodock.pb_quit.clicked.connect(self.closeInfoDock)

        # ---------------------- create SolvePotentialWell dock --------- ----

        self.ws = SolvePotentialWell(self.dpw)
        # note: need to resetSolver after every change in dpw variables
        self.ws.resetSolver()
        if False:
            self.dpw.printXVArrays()
            exit()

        # instantiate SolveWellDock
        self.solvewd = SolveWellDock()
        self.solvewd.setGeometry(self.leftWid, self.topWid, self.widthWid,
                                 self.heightWid)

        # signal/slots for SolveWellDock
        self.solvewd.pb_solve.clicked.connect(self.solveSolve)

        # ----------------------- create FindStationaryStates dock ----------

        # instantiate FindStatStateDock
        self.findstate = FindStatesWellDock()
        self.findstate.setGeometry(self.leftWid, self.topWid, self.widthWid,
                                   self.heightWid)

        # instantiate FindStationaryStates
        interpolationFlag = True
        self.fss = FindStationaryStates(self.ws, interpolationFlag,
                                        self.findstate)

        # signal/slots for FindStatStates
        self.findstate.pb_findstates.clicked.connect(self.findStatesPb)
        self.findstate.pb_plotpsi.clicked.connect(self.findStatesPlotPsi)
        self.findstate.pb_savepsi.clicked.connect(self.findStatesSavePsi)

        # instantiate PlotPotentialWell and plot default well on main window
        self.pltt = PlotPotentialWell(self.axes, self.dpw)
        self.pltt.makeNormalPlot()
        # self.axes.grid()
        self.mpl.draw()

# ################### end of __init__ #############################
# #################################################################

# ====================== printWidPosSize ================================

    def printWidPosSize(self, widgg, titl, name):
        print("\n    name ", name)
        print("printWidPosSize ", titl, widgg.geometry(), "\n")

# ======================= mpl_init  ==========================================

    def mpl_init(self):

        # ---- instantiate matplotlib widget, make axes for later use  -------
        # Note that its parent is self.main_widget
        self.mpl = MatplotlibWidget(parent=self.main_widget,
                                    xlabel="Well Position (nm)",
                                    ylabel="Energy (eV)")
        self.axes = self.mpl.axes

        # create axis for plotPsi plots, create color list for these plots
        # will cycle through these colors for multiple psi plots.
        # twinx() produces axis with same x-axis details as on original plot.
        # turning the axis off makes it invisible.
        # axTwinx created from a self.axes method (they share the same x axis)
        self.axTwinx = self.axes.twinx()
        self.axTwinx.set_axis_off()

        # color list for multi-plotPsi plots, will be used by axTwinx axes
        self.colorIndex = 0
        self.colorList = ['r', 'b', 'g', 'c', 'm', 'k']

# =====================end of mpl_init =================================

# ============== mpl_toolbar_init ======================================

    def mpl_toolbar_init(self):

        # make a toolbar and tie it to the mpl widget
        self.vtoolbar = NavigationToolbar(self.mpl, self.main_widget)

        # add print button to navigation toolbar, include connection
        self.print_button = QPushButton()
        self.print_button.setText("Print")
        # add the print button to the navigation toolbar
        self.vtoolbar.addWidget(self.print_button)

        # connect the print button click to the goPrinter method.
        # now printing from mpl method, may move to a utility function
        self.print_button.clicked.connect(self.mpl.goPrinter)

# ====================== end of mpl_toolbar_init =========================

# ===================== maindock_init =====================================

    def maindock_init(self):
        # create maindock widget and add to main window

        # self.maindw = MainDockWidget()
        # self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,self.maindw)

        # set signals/slots for main widget
        self.maindw.pb_buildwell.clicked.connect(self.openBuildWellDock)
        self.maindw.pb_addbarrier.clicked.connect(self.openAddBarrierDock)
        self.maindw.pb_addmultibarriers.clicked.connect(
            self.openAddMultiBarriersDock)
        self.maindw.pb_removebarrier.clicked.connect(
            self.openRemoveBarrierDock)
        self.maindw.pb_solvepotwell.clicked.connect(self.openSolveWellDock)
        self.maindw.pb_findstatstates.clicked.connect(
            self.openFindStatStatesDock)
        self.maindw.pb_addslopedbase.clicked.connect(
            self.openAddSlopedBaseDock)
        self.maindw.pb_addsimharosc.clicked.connect(self.openSHOBaseDock)
        self.maindw.pb_readfile.clicked.connect(self.readDpwFile)
        self.maindw.pb_writefile.clicked.connect(self.writeDpwFile)
        self.maindw.pb_info.clicked.connect(self.openInfoDock)
        self.maindw.pb_addvpe.clicked.connect(self.openAddVpeDock)

        self.maindw.pb_quit.clicked.connect(QApplication.instance().quit)

# ==================== end of maindock_init ==========================

# ================== setWindowSizes ==================================

    def setWindowSizes(self):
        # set sizes of windows and dockwidgets
        debug = False
        if debug:
            print("  -- in setWindowSizes")

        # set location of main window on screen,
        #      should be independent of resolution
        # get width and height of screen
        # looks circular,but takes care of multiple open desktops (I think)
        primaryScreen = QApplication.desktop()
        rScr = QApplication.desktop().screenGeometry(primaryScreen)
        # get width and height of screen
        self.swidth = rScr.width()
        self.sheight = rScr.height()
        if debug:
            print("swidth sheight ", self.swidth, self.sheight)

        # widget widths
        self.leftWid = int(self.swidth * 0.01)
        self.topWid = int(self.swidth * 0.01)
        self.widthWid = int(self.swidth / 4)
        self.heightWid = int(self.sheight / 2.5)
        if debug:
            print("leftWid topWid widthWid heightWid ", self.leftWid,
                  self.topWid, self.widthWid, self.heightWid)

        # set Geometry:  left = pixels of left edge from screen left
        #                top  = pixels of top edge from screen top

        left = int(self.swidth / 3.5)
        top = int(self.sheight / 10)
        sizew = int(self.swidth / 1.5)
        sizeh = int(self.sheight / 1.4)
        if debug:
            print("main window left top sizew sizeh ", left, top, sizew, sizeh)

        # set geometry of main window
        self.setGeometry(left, top, sizew, sizeh)
        # to get size and location information of self window
        # returns QRect class: .x(),.y(),.width(),.height()
        self.qrt = self.geometry()

# ===================== end of setWindowSizes ============================

# ########################################################################
# ###################### Main window pushbutton handler methods ##########

#  close eventhandler for main window (red x in upper-right hand corner)

    def closeEvent(self, event):
        quit()
        # or ignore the closeEvent for main window (and closes all others)
        # event.ignore()

# ------------ makeDockCloseDict -----------------------------

    def makeDockCloseDict(self):
        """ Dict connects openDocName string to dock close function.
        """
        debug = False
        if debug:
            print("  in makeDockCloseDict")

        self.dockCloseDict = {
            "buildWell": self.closeBuildWellDock,
            "addBarrier": self.closeAddBarrierDock,
            "removeBarrier": self.closeRemoveBarrierDock,
            "slopedBase": self.closeAddSlopedBaseDock,
            "shoBase": self.closeAddSHOBaseDock,
            "solveWell": self.closeSolveWellDock,
            "findStates": self.closeFindStatStatesDock,
            "addMultiBarriers": self.closeAddMultiBarriersDock,
            "infoDock": self.closeInfoDock,
            "vpeDock": self.closeVpeDock
        }

# ---------------------- closeOpenDock ---------------------

    def closeOpenDock(self):
        """ make open dock invisible.
        """
        debug = False
        if debug:
            print(" in closeOpenDock")
            print("  self.openDockName: ", self.openDockName)
            if self.openDockName in self.dockCloseDict:
                print("in dictionary ok")

        if self.openDockName is not None:
            # execute the close function for the open window
            # and set the open dock name to None.
            self.dockCloseDict[self.openDockName]()
            self.openDockName = None

# ===================== MainDockWidget Handlers =================

# -------------- openBuildWellDock ------------------------------

    def openBuildWellDock(self):
        debug = False
        if debug:
            print("  in openBuildWellDock(")

        self.closeOpenDock()

        # sendMessageTE(self.dpw.printBasicWellParms(),self.buildwd.te_message)
        self.buildwd.setVisible(True)
        self.openDockName = "buildWell"

# ----------- openAddBarrierDock ----------------------------

    def openAddBarrierDock(self):
        debug = False
        if debug:
            print("  in openAddBarrierDock")

        self.closeOpenDock()

        # sendMessageTE(self.dpw.printAddedVArray(),self.addwd.te_addbarrier)
        self.addwd.setVisible(True)
        self.openDockName = "addBarrier"

# --------------- openAddMultiBarriersDock ------------------------

    def openAddMultiBarriersDock(self):
        debug = False
        if debug:
            print("  in openAddMultiBarriersDock")

        self.closeOpenDock()

        # sendMessageTE(self.dpw.printAddedVArray(), \
        # self.addmultiwd.te_multibarriers)
        self.addmultiwd.setVisible(True)
        self.openDockName = "addMultiBarriers"

# ---------------- openRemoveBarrierDock -------------------------

    def openRemoveBarrierDock(self):
        debug = False
        if debug:
            print("in openRemoveBarrierDock")

        self.closeOpenDock()

        self.rembwd.setVisible(True)
        sendMessageTE(self.dpw.printAddedVArray(),
                      self.rembwd.te_removebarrier)
        self.openDockName = "removeBarrier"

# --------------- openAddSlopedBaseDock ----------------------------

    def openAddSlopedBaseDock(self):
        debug = False
        if debug:
            print(" in openAddSlopedBaseDock")

        self.closeOpenDock()

        self.addspwd.setVisible(True)
        # sendMessageTE(self.dpw.printAddedVArray(),self.addspwd.te_addslope)
        self.openDockName = "slopedBase"

# --------------- openAddVpeDock ----------------------------

    def openAddVpeDock(self):
        debug = False
        if debug:
            print(" in openAddVpeDock")

        self.closeOpenDock()

        self.addvpe.setVisible(True)
        # sendMessageTE(self.dpw.printAddedVArray(),self.addvpe.te_addvpe)
        self.openDockName = "vpeDock"

# ------------------ openSHOBaseDock -----------------------------

    def openSHOBaseDock(self):
        debug = False
        if debug:
            print(" in openSHOBaseDock")

        self.closeOpenDock()

        self.addshowd.setVisible(True)
        # sendMessageTE(self.dpw.printAddedVArray(),self.addshowd.te_addsho)
        self.openDockName = "shoBase"

# ----------------- openSolveWellDock -------------------------------

    def openSolveWellDock(self):
        debug = False
        if debug:
            print("  -- openSolveWellDock")

        self.closeOpenDock()

        self.solvewd.setVisible(True)
        self.openDockName = "solveWell"

# ------------------- openInfoDock -----------------------------

    def openInfoDock(self):
        debug = False
        if debug:
            print("  -- openInfoDock")

        self.closeOpenDock()

        self.infodock.setVisible(True)
        self.openDockName = "infoDock"

# --------------- openFindStatStatesDock ----------------------------------

    def openFindStatStatesDock(self):
        debug = False
        if debug:
            print("  -- openFindStatStatesDock")

        self.closeOpenDock()

        self.findstate.setGeometry(self.leftWid, self.topWid, self.widthWid,
                                   self.heightWid)
        self.findstate.setVisible(True)
        self.openDockName = "findStates"

# #####################################################################
# ##################### Dock Handlers ########################

# ---------------- buildOK -----------------------------

    def buildOK(self):
        debug = False
        if debug:
            print("in buildOK")

        # start with a new basic well
        self.dpw.resetWell()

        # get numbers from textedit boxes
        qwidth = self.buildwd.le_width.text()
        width, okW = stringToFloat(qwidth)

        qheightL = self.buildwd.le_heightleft.text()
        heightL, okL = stringToFloat(qheightL)

        qheightR = self.buildwd.le_heightright.text()
        heightR, okR = stringToFloat(qheightR)

        # see if all boxes contain numbers
        if not all([okW, okL, okR]):
            strre = self.errorMFloat
            sendMessageTE(strre, self.buildwd.te_message, False)
        else:

            self.sp.setBasicWellParms(width, heightL, heightR)

            # bring solver up to date (dpw has possibly changed)
            self.ws.resetSolver()

            # plot the well
            self.pltt.makeNormalPlot()

            self.mpl.draw()
            if False:
                self.dpw.printXVArrays()

            msg = self.dpw.printBasicWellParms()
            sendMessageTE(msg, self.buildwd.te_message)

# ---------------- end of buildOK --------------------------

# ------------------ closeBuildWellDock -------------------------

    def closeBuildWellDock(self):
        debug = False
        if debug:
            print("in closeBuildWellDock")
        self.buildwd.setVisible(False)

        # send results to message board
        strr = "BuildWell\n"
        msg = strr + str(self.dpw.printBasicWellParms())
        sendMessageTE(msg, self.mswd.te_message)

# ------------------ end of closeBuildWellDock -------------------------

# ############## addBarrier Handlers ######################

# ------------ AddBarrierOK -------------------------------

    def addBarrierOK(self):
        debug = True
        if debug:
            print("in addBarrierOK")
        qxmin = self.addwd.le_xmin.text()
        xmin, okMi = stringToFloat(qxmin)

        qxmax = self.addwd.le_xmax.text()
        xmax, okMa = stringToFloat(qxmax)
        qbarrierv = self.addwd.le_barrierv.text()
        barrierv, okBa = stringToFloat(qbarrierv)

        if not all([okMi, okMa, okBa]):
            strre = self.errorMFloat
            sendMessageTE(strre, self.addwd.te_addbarrier, False)
        else:
            addBarrierFlag = self.sp.addBarrier(xmin, xmax, barrierv, 0.0, 0.0)

            if not addBarrierFlag:
                strb = "nothing added: do limits overlap other barriers"
                sendMessageTE(strb, self.addwd.te_addbarrier)
            else:
                sendMessageTE(self.dpw.printAddedVArray(),
                              self.addwd.te_addbarrier)

                # bring solver up to date (dpw has possibly changed)
                self.ws.resetSolver()

                # plot the well
                self.pltt.makeNormalPlot()
                self.mpl.draw()

# ------------ end ofAddBarrierOK -------------------------------

# ------------------ closeAddBarrierDock ------------------------

    def closeAddBarrierDock(self):
        debug = False
        if debug:
            print("in closeAddBarrierDock")
        self.addwd.setVisible(False)
        sss = "addBarrier\n" + self.dpw.printAddedVArray()
        sendMessageTE(sss, self.mswd.te_message)

# ################### AddMultiBarriersDock handlers  ############

# --------------- addMultiBarriersOK -------------------

    def addMultiBarriersOK(self):
        debug = False
        if debug:
            print("in addMultiBarriersOK")

        # read lineEdits for number of barriers and width/height
        brNum = self.addmultiwd.le_numbarriers.text()
        bNum, okNum = stringToInt(brNum)
        brWidth = self.addmultiwd.le_width.text()
        bWidth, okWidth = stringToFloat(brWidth)
        barrHeight = self.addmultiwd.le_barheight.text()
        barHeight, okBarHeight = stringToFloat(barrHeight)
        barrWidth = self.addmultiwd.le_barwidth.text()
        barWidth, okBarWidth = stringToFloat(barrWidth)

        if debug:
            print("   number of barriers, ok", bNum, okNum)
            print("   subWell width, ok", bWidth, okWidth)
            print("   barrier height, ok", barHeight, okBarHeight)
            print("   barrier width,  ok", barWidth, okBarWidth)

        if okNum is False:
            strre = self.errorMInt
            sendMessageTE(strre, self.addmultiwd.te_multibarriers, False)
            return

        if (okWidth and okBarHeight and okBarWidth) is False:
            strre = self.errorMFloat
            sendMessageTE(strre, self.addmultiwd.te_multibarriers, False)
            return

        # get current well width and heights
        currentWell = self.dpw.getBasicWellProperties()

        # build well after determining well width
        totalWidth = bWidth * (bNum + 1) + bNum * barWidth
        if debug:
            print("totalWidth", totalWidth)

        # buildNewWell will reset the well and dpw instance
        self.sp.buildNewWell(totalWidth, currentWell[1], currentWell[2])

        # bring solver up to date (dpw has possibly changed)
        self.ws.resetSolver()

        for i in np.arange(1, bNum + 1):
            startb = bWidth * i + (i - 1) * barWidth
            endb = startb + barWidth
            if debug:
                print("loop", i, startb, endb)
            addMultiBarrierFlag = self.sp.addBarrier(startb, endb, barHeight,
                                                     0, 0)
            if addMultiBarrierFlag:
                sendMessageTE(self.dpw.printAddedVArray(),
                              self.addmultiwd.te_multibarriers)

        # add barriers

        # plot the well after removing previous plot
        # self.axes.clear()
        self.pltt.makeNormalPlot()
        # self.axes.grid()

        self.mpl.draw()
        if False:
            self.dpw.printXVArrays()

        msg = self.dpw.printBasicWellParms()
        sendMessageTE(msg, self.buildwd.te_message)
# --------------- end of addMultiBarriersOK -------------------

# ------------------- closeAddMultiBarriersDock -----------------------

    def closeAddMultiBarriersDock(self):
        debug = False
        if debug:
            print("in closeAddMultiBarriersDock")
        self.addmultiwd.setVisible(False)
        sss = "addMultiBarriers\n" + self.dpw.printAddedVArray()
        sendMessageTE(sss, self.mswd.te_message)

# ################## RemoveBarrierDock handlers ################

# ------------ removeBarrierNum -----------------------------

    def removeBarrierNum(self):
        debug = False
        if debug:
            print("  removeBarrierNum")

        # get barrier number
        qbarnum = self.rembwd.le_number.text()
        barnum, okBn = stringToInt(qbarnum)
        if okBn is False:
            strre = self.errorMInt
            sendMessageTE(strre, self.rembwd.te_removebarrier, False)
        else:

            if debug:
                print("barrier number entered ", barnum)
            self.sp.removeBarrier(barnum)

            sendMessageTE(self.dpw.printAddedVArray(),
                          self.rembwd.te_removebarrier)

            # bring solver up to date (dpw has possibly changed)
            self.ws.resetSolver()

            # plot the well after removing previous plot
            # self.axes.clear()
            self.pltt.makeNormalPlot()
            # self.axes.grid()
            if debug:
                print("       post makeNormalPlot")
                self.dpw.printData()

            self.mpl.draw()
# ------------ end of removeBarrierNum -----------------------------

# --------------- closeRemoveBarrierDock ------------------------

    def closeRemoveBarrierDock(self):
        debug = False
        if debug:
            print(" closeRemoveBarrierDock")
        self.rembwd.setVisible(False)
        sss = "removeAddedV\n" + self.dpw.printAddedVArray()
        sendMessageTE(sss, self.mswd.te_message)

# #################### AddSlopedBase handlers #######################

# ----------------------- addSlopedBaseOK -------------------

    def addSlopedBaseOK(self):
        """ addSlopedBase Potential within potential well

        Parameters from dock widget
            location and PE of left edge of sloping  PE: xmin, vxmin
            location and PE of right edge of sloping PE: xmax, vxmax
        """

        debug = False
        if debug:
            print(" in addSlopedBaseOK")

        # get lineedit entries, make sure of float format
        qxmin = self.addspwd.le_xmin.text()
        xmin, okMi = stringToFloat(qxmin)

        qvxmin = self.addspwd.le_vxmin.text()
        vxmin, okVMi = stringToFloat(qvxmin)

        qxmax = self.addspwd.le_xmax.text()
        xmax, okMa = stringToFloat(qxmax)

        qvxmax = self.addspwd.le_vxmax.text()
        vxmax, okVMa = stringToFloat(qvxmax)

        if not all([okMi, okMa, okVMi, okVMa]):
            strre = self.errorMFloat
            sendMessageTE(strre, self.addspwd.te_addslope, False)
        else:
            # get current well heights and widths
            (ww, whl, whr) = self.dpw.getBasicWellProperties()

            # See if xmin or xmax fall outside of the well
            if (xmin < 0.0) or (xmin > ww) or (xmax < 0.0) or (xmax > ww):
                strr = "linear potential endpoints fall outside the well"
                sendMessageTE(strr, self.addspwd.te_addslope, True)
                return

            # determine slope of line for addBarrier method entry
            v0 = vxmin
            vs = (vxmax - vxmin) / (xmax - xmin)
            vss = 0.0

            # sp is an instance of the BuildPotentialWell class
            addBarrierFlag = self.sp.addBarrier(xmin, xmax, v0, vs, vss)

            if not addBarrierFlag:
                strb = "nothing added: do limits overlap other barriers"
                # sendMessageTE(strb, self.addwd.te_addbarrier)
                sendMessageTE(strb, self.addspwd.te_addslope)
            else:
                sendMessageTE(self.dpw.printAddedVArray(),
                              self.addspwd.te_addslope)

                # bring solver up to date (dpw has possibly changed)
                self.ws.resetSolver()

                # plot the well
                self.pltt.makeNormalPlot()

                self.mpl.draw()

# ----------------------- end of addSlopedBaseOK -------------------

# ---------------- closeAddSlopedBaseDock ---------------------------

    def closeAddSlopedBaseDock(self):
        debug = False
        if debug:
            print(" in closeAddSlopedBaseDock")
        self.addspwd.setVisible(False)
        sss = "addSlopedBase\n" + self.dpw.printAddedVArray()
        sendMessageTE(sss, self.mswd.te_message)

# ################### AddVpeDock handlers ##################

# ------------------ addVpeDockOK -----------------

    def addVpeDockOK(self):
        """ add v-shaped potential energy within well
        """
        debug = False
        if debug:
            print("  -- in addVpeDockOK")

        # get lineedit entries, make sure of float format
        qxzero = self.addvpe.le_xzero.text()
        xzero, okMi = stringToFloat(qxzero)

        qvleft = self.addvpe.le_vleft.text()
        vleft, okMj = stringToFloat(qvleft)

        qvright = self.addvpe.le_vright.text()
        vright, okMk = stringToFloat(qvright)

        # get current well heights and widths
        (ww, whl, whr) = self.dpw.getBasicWellProperties()

        if (okMi and okMj and okMk) is False:
            strre = self.errorMFloat
            sendMessageTE(strre, self.addvpe.te_addvpe, False)

        # does xzero fall within the well
        elif (xzero < 0.0) or (xzero > ww):
            strr = "zero point of V potential falls outside the well"
            sendMessageTE(strr, self.addvpe.te_addvpe, True)

        # are the left and right heights within the well
        elif (vleft < 0.0) or (vleft > whl) or \
             (vright < 0.0) or (vright > whr):
            strr = "V potential left or right height(s) outside well"
            sendMessageTE(strr, self.addvpe.te_addvpe, True)

        else:

            # buildNewWell will reset the well and set
            # the basic well parameters
            self.sp.buildNewWell(ww, whl, whr)

            # bring solver up to date (dpw has possibly changed)
            self.ws.resetSolver()

            xminL = [0.0, xzero]
            xmaxL = [xzero, ww]
            v0L = [vleft, 0.0]
            vs0 = (0.0 - vleft) / (xmaxL[0] - xminL[0])
            vs1 = (vright - 0.0) / (xmaxL[1] - xminL[1])
            vsL = [vs0, vs1]
            vssL = [0.0, 0.0]

            for i in [0, 1]:
                self.sp.addBarrier(xminL[i], xmaxL[i], v0L[i], vsL[i], vssL[i])
                sendMessageTE(self.dpw.printAddedVArray(),
                              self.addvpe.te_addvpe)

            # bring solver up to date (dpw has possibly changed)
            self.ws.resetSolver()

            # plot the well after removing previous plot
            self.pltt.makeNormalPlot()
            self.mpl.draw()

# ------------------ end of addVpeDockOK -----------------

# ------------------ closeAddVpeDock -----------------

    def closeVpeDock(self):
        """ set Visibility off, write log message """

        self.addvpe.setVisible(False)
        sss = "addVpe\n" + self.dpw.printAddedVArray()
        sendMessageTE(sss, self.mswd.te_message)

# ------------------ end of closeAddVpeDock -----------------

# ################### AddSHODock handlers ##################

# ------------------ addSHODockOK -----------------

    def addSHODockOK(self):
        debug = False
        if debug:
            print(" in addSHODockOK")

        if False:
            if len(self.dpw.barriers) > 1:
                qstr0 = "\nCan not add simple harmonic oscillator "
                qstr1 = "over an internal barrier"
                qstr2 = "    Remove the barrier(s) first\n"
                qstr = qstr0 + qstr1 + qstr2

                # use message method....
                self.addshowd.te_addsho.insertPlainText(qstr)

                return

        centerFlag = self.addshowd.rb_center.isChecked()
        if debug:
            print("center is checked flag ", centerFlag)

        qvmax = self.addshowd.le_vxmax.text()
        vxmax, okV = stringToFloat(qvmax)

        if okV is False:
            sendMessageTE(self.errorMFloat, self.addshowd.te_addsho)

        else:
            if False:
                # if self.dpw.barrierCt > 0:
                sendMessageTE(self.dpw.printAddedVArray(),
                              self.addshowd.te_addsho, False)
            else:
                # print('****calling addHarmonicOscillatorPotential')
                self.sp.addHarmonOscillPotential(centerFlag, vxmax)

                sendMessageTE(self.dpw.printAddedVArray(),
                              self.addshowd.te_addsho)
                # bring solver up to date (dpw has possibly changed)
                self.ws.resetSolver()

                # plot the well

                self.pltt.makeNormalPlot()

                self.mpl.draw()

# -------------- end of addSHODockOK ---------------

# -------------------- closeAddSHOBaseDock ------------------

    def closeAddSHOBaseDock(self):
        debug = False
        if debug:
            print(" in closeAddSHOBaseDock")
        self.addshowd.setVisible(False)
        sss = "addSimHarOsc\n" + self.dpw.printAddedVArray()
        sendMessageTE(sss, self.mswd.te_message)

# ################## SolveWellDock handlers ########################

# ---------------- solveSolve -------------------------

    def solveSolve(self):

        okE = True
        qsolve = self.solvewd.le_solve.text()
        try:
            energy = float(qsolve)
        except ValueError:
            okE = False

        if okE is False:
            strre = self.errorMFloat
            sendMessageTE(strre, self.solvewd.te_solvewell, False)

        else:
            wellH0 = self.dpw.wellHeightLeft
            wellH1 = self.dpw.wellHeightRight

            # set xsolve region,don't solve if inf  potential
            if np.isfinite(wellH1):
                xsolve = self.dpw.xMinHigh
            else:
                xsolve = self.dpw.xMinMax
            # set initial conditions
            # have to set choice for infinite well, do this later
            if np.isfinite(wellH0):
                y0 = 1.0
                y01 = np.sqrt((self.dpw.k2) * (wellH0 - energy)) * y0
                extrapolateLeft = True
            else:
                y0 = 0.0
                y01 = 40. * (0.4 / self.dpw.wellWidth)
                extrapolateLeft = False

            psi = self.ws.solveSquareWell(energy, y0, y01, xsolve)

            self.axTwinx.cla()
            self.pltt.removeEnergyLine()

            plotPsi(self.axTwinx, psi, energy, self.dpw, extrapolateLeft,
                    False, 'r')

            self.pltt.addEnergyLine(energy)
            self.mpl.draw()

# ---------------- end of solveSolve -------------------------

# ------------------- closeSolveWellDock -----------------------------

    def closeSolveWellDock(self):
        debug = False
        if debug:
            print("  -- in closeSolveWellDock")
        self.axTwinx.cla()  # remove psi plot
        self.axTwinx.set_axis_off()
        self.pltt.removeEnergyLine()
        self.mpl.draw()
        self.solvewd.setVisible(False)

    # ##################### InfoDock handlers ###############

# ---------------- closeInfoDock ---------------------

    def closeInfoDock(self):
        debug = False
        if debug:
            print("      -- in closeInfoDock")
        self.infodock.setVisible(False)

# ##################### Find Stationary States handlers ####################

# --------------- findStatesPb ---------------------

    def findStatesPb(self):

        for i, v in self.pltt.dStatesPlot.items():
            self.axes.lines.remove(v)
        self.mpl.draw()
        self.pltt.dStatesPlot.clear()
        self.dpw.dStates.clear()

        # next three lines, new 2/1/15
        self.axTwinx.cla()
        self.axTwinx.set_axis_off()
        self.mpl.draw()

        self.colorIndex = 0
        debug = False
        if debug:
            print(" -- findStatesPb")
        qnumx = self.findstate.le_numx.text()

        numX, okNum = stringToInt(qnumx)
        qdele = self.findstate.le_dele.text()
        dele, okD = stringToFloat(qdele)
        qemin = self.findstate.le_emin.text()
        emin, okMi = stringToFloat(qemin)
        qemax = self.findstate.le_emax.text()
        emax, okMa = stringToFloat(qemax)

        if debug:
            print("numX delE emin emax ", numX, dele, emin, emax)
            # print("okNum, okD okMi okMa", okNumokD, okMi, okMa)

        if (okD and okMi and okMa) is False:
            strre = self.errorMFloat
            sendMessageTE(strre, self.findstate.te_findstates, False)

        if okNum is False:
            strre = "numX is not an integer, try again"
            sendMessageTE(strre, self.findstate.te_findstates, False)

        else:
            # check emax against barrier heights,
            # can't be above min edge height
            emaxMax = min(self.dpw.wellHeightLeft, self.dpw.wellHeightRight)
            if emax > emaxMax:
                emax = emaxMax

            # store emax and numX in DataPotentialWell
            self.dpw.maxESolve = emax
            self.dpw.numX = numX

            statE = self.fss.findStates(emin, emax, dele)
            strlabel = "  ID   Stationary State Energies " + "\n"

            i = 0
            strSS = strlabel
            for e in statE:
                i = i + 1
                self.dpw.dStates[i] = e
                strSS += "  " + str(i) + "     " + "{:7.4f}".format(e) + "\n"

            if len(self.dpw.dStates) > 0:
                sendMessageTE(strSS, self.findstate.te_findstates, False)

            if self.dpw.infiniteWellFlag:
                # plot the well after removing previous plot
                # self.axes.clear()
                self.pltt.makeNormalPlot(emax)
                # self.axes.grid()

                self.mpl.draw()

            self.pltt.addEnergyLinesFromDict()
            self.mpl.draw()

            if debug:
                print("    after Find states")
                self.dpw.printData()

            if self.findstate.cb_figure.isChecked():
                if self.figDelSlope is not None:
                    plt.close(self.figDelSlope)
                self.figDelSlope = plt.figure(5)
                self.axDs = self.figDelSlope.add_subplot(111)
                self.fss.plotStatStates(self.axDs)
                self.figDelSlope.show()
                self.figDelSlope.canvas.draw()

# --------------- end of findStatesPb ---------------------

# ----------------- closeFindStatStatesDock --------------------------------

    def closeFindStatStatesDock(self):
        debug = False
        if debug:
            print("  -- closeFindStatStatesDock")
        self.findstate.setVisible(False)

        for i, v in self.pltt.dStatesPlot.items():
            self.axes.lines.remove(v)
        self.pltt.dStatesPlot.clear()
        # self.dpw.dStates.clear()
        self.findstate.te_findstates.clear()
        self.axTwinx.cla()
        self.axTwinx.set_axis_off()
        self.mpl.draw()
        plt.close(5)

        strlabel = "  ID   Stationary State Energies " + "\n"

        i = 0
        strSS = strlabel
        for i, e in self.dpw.dStates.items():
            strSS += "  " + str(i) + "     " + "{:7.4f}".format(e) + "\n"

        if len(self.dpw.dStates) > 0:
            sendMessageTE(strSS, self.mswd.te_message)

        # new
        self.dpw.dStates.clear()

# ----------------- end of closeFindStatStatesDock ---------------------------

# ------------------- findStatesSavePsi ------------------------------

    def findStatesSavePsi(self):
        debug = False
        if debug:
            print(" -- findStatesSavePsi")
        qstatNum = self.findstate.le_statenum.text()
        statNum, okS = stringToInt(qstatNum)

        if okS is False:
            sendMessageTE(self.errorMInt, self.findstate.te_findstates)
        else:
            if statNum not in self.dpw.dStates:
                strM = "this is not a valid energy stationary state number "
                sendMessageTE(strM, self.findstate.te_findstates)
                return False

        energy = self.dpw.dStates[statNum]
        wellH0 = self.dpw.wellHeightLeft
        if np.isfinite(self.dpw.wellHeightRight):
            xsolve = self.dpw.xMinHigh
        else:
            xsolve = self.dpw.xMinMax

        if np.isfinite(wellH0):
            y0 = 1.0
            y01 = np.sqrt((self.dpw.k2) * (wellH0 - energy)) * y0
        else:
            y0 = 0.0
            y01 = 40. * (0.4 / self.dpw.wellWidth)

        psi = self.ws.solveSquareWell(energy, y0, y01, xsolve)

        self.axTwinx.set_axis_on()

        if np.isinf(self.dpw.wellHeightLeft):
            extendLeft = False
        else:
            extendLeft = True

        psiAll = plotPsi(self.axTwinx, psi, energy, self.dpw, extendLeft,
                         False, self.colorList[self.colorIndex])

        v = [self.ws.getV(x) for x in psiAll[:, 2]]
        varray = np.array(v)
        psiAll = np.hstack((psiAll, varray[:, None]))

        filenameTuple = QFileDialog.getSaveFileName(caption="write text file",
                                                    filter="*.txt")
        filename = filenameTuple[0]

        if filename:
            fname = str(filename)
            fbase, fext = os.path.splitext(fname)
            if fext != '.txt':
                fname += '.txt'
            if debug:
                print("filename: ", filename, type(filename))
                print("filename str ", fname)
                print("writing ", fname, " to text file")

            np.savetxt(fname, psiAll)

        return True

# ------------------- end of findStatesSavePsi ------------------------------

# ------------------- findStatesPlotPsi --------------------------------------

    def findStatesPlotPsi(self):

        debug = False
        if debug:
            print(" -- findStatesPlotPsi")
            print("self.dpw.dStates", self.dpw.dStates)
        qstatNum = self.findstate.le_statenum.text()
        statNum, okS = stringToInt(qstatNum)

        if okS is False:
            sendMessageTE(self.errorMInt, self.findstate.te_findstates)
        else:
            if statNum not in self.dpw.dStates:
                strM = "this is not a valid energy stationary state number "
                sendMessageTE(strM, self.findstate.te_findstates)
                return False
            self.dpw.statStateNumber = statNum

        energy = self.dpw.dStates[statNum]
        self.dpw.psiEnergy = energy

        wellH0 = self.dpw.wellHeightLeft
        if np.isfinite(self.dpw.wellHeightRight):
            xsolve = self.dpw.xMinHigh
        else:
            xsolve = self.dpw.xMinMax

        if np.isfinite(wellH0):
            y0 = 1.0
            y01 = np.sqrt((self.dpw.k2) * (wellH0 - energy)) * y0
        else:
            y0 = 0.0
            y01 = 40. * (0.4 / self.dpw.wellWidth)

        psi = self.ws.solveSquareWell(energy, y0, y01, xsolve)

        self.axTwinx.set_axis_on()

        if np.isinf(self.dpw.wellHeightLeft):
            extendLeft = False
        else:
            extendLeft = True

        plotPsi(self.axTwinx, psi, energy, self.dpw, extendLeft, False,
                self.colorList[self.colorIndex])
        self.colorIndex += 1
        if self.colorIndex == len(self.colorList):
            self.colorIndex = 0

        self.mpl.draw()

        return True

# ------------------- end of findStatesPlotPsi ------------------------------

# #################  read/write dpw file handlers ######################

# ------------- readDpwFile --------------------------

    def readDpwFile(self):
        debug = False
        if debug:
            print("  -- readDpwFile")
        # get filename
        filenameT = QFileDialog.getOpenFileName(caption="read dpw file",
                                                filter="*.dpw")
        filename = filenameT[0]

        if filename:
            if debug:
                print("filename: ", filename, type(filename))
                print("filename str ", str(filename))
            strfile = str(filename)

            newDpw = self.unpickleDpw(strfile)
            if debug:
                newDpw.printData()
                print(newDpw)

            self.dpw.copyData(newDpw)

            # bring solver up to date (dpw has possibly changed)
            self.ws.resetSolver()

            # plot the well
            self.pltt.makeNormalPlot()

            self.mpl.draw()

            msg = "Reading from file: " + strfile + '\n' + str(
                self.dpw.printBasicWellParms()) + str(
                    self.dpw.printAddedVArray())
            sendMessageTE(msg, self.mswd.te_message)

            if debug:
                print("new self.dpw.printData() ")
                self.dpw.printData()

# ------------- end of readDpwFile --------------------------

# --------------- pickleDpw ----------------------------------------

    def pickleDpw(self, dpwFileName):
        debug = False
        if debug:
            print("  -- pickleDpw ")
            print(" ready to open file for writing: ", dpwFileName)
        f = open(dpwFileName, 'wb')
        if debug:
            print(" after open f")
        pickle.dump(self.dpw, f, pickle.HIGHEST_PROTOCOL)

        f.close()

# --------------- end of pickleDpw ----------------------------------------

# --------------- unpickleDpw --------------------------------------------

    def unpickleDpw(self, fileName):

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

        return newDpw

# --------------- end of unpickleDpw ----------------------------------------

# ------------------ writeDpwFile ------------------------------------

    def writeDpwFile(self):
        debug = False
        if debug:
            print("  -- writeDpwFile")

        # get filename
        filenameT = QFileDialog.getSaveFileName(caption="write dpw file",
                                                filter="*.dpw")
        filename = filenameT[0]

        # filename =
        # QtGui.QFileDialog.getSaveFileName(caption="write dpw file")
        if filename:
            fname = str(filename)
            fbase, fext = os.path.splitext(fname)
            if fext != '.dpw':
                fname += '.dpw'
            if debug:
                print("filename: ", filename, type(filename))
                print("filename str ", fname)

            if self.dpw.psiArray.size:
                v = [self.ws.getV(x) for x in self.dpw.psiArray[:, 2]]
                varray = np.array(v)
                self.dpw.psiArray = np.hstack(
                    (self.dpw.psiArray, varray[:, None]))

            print("psiArray ", self.dpw.psiArray.shape)

            self.pickleDpw(fname)

            self.dpw.psiArray = np.array([])
            msg = "writing file " + fname
            self.dpw.printData()
            sendMessageTE(msg, self.mswd.te_message)

# ------------------ end of writeDpwFile ------------------------------------

# ########################## Utility methods #####################

# ################# end of potentialWell class ############################


# #####################################################

# the following creates and runs the event loop, as required by the PyQt Gui.
# create the GUI application

# instantiate the ApplicationWindow widget
qAppM = QApplication(sys.argv)

# instantiate the above class
aw = PotentialWellWindow()

# show and raise required for osx, linux and windows don't need these
#  but they don't mind them either.
# raise_ since raise is a reserved word: QWidget::raise_()
aw.show()
aw.raise_()
aw.mswd.raise_()

# start the Qt main loop execution
sys.exit(qAppM.exec_())
