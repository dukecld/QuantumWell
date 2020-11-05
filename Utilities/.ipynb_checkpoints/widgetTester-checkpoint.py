# illustrates use of QuantumWell widgets and can be used to test
# new widgets. 
# edit last __main__ section to select widgets to open
# close python using red close button on MainDockWidget window
# otherwise, will have to close terminal window to exit python.
# or use os force quit option.

import sys
import os

import numpy as np
import matplotlib.pyplot as plt
import datetime
import pickle

#######################################################

# PyQt5 GUI modules
try:
   import PyQt5
   from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QVBoxLayout, QDockWidget
   from PyQt5.QtWidgets import QApplication, qApp, QFileDialog, QDialog, QLabel
   from PyQt5.QtGui import QIcon, QPainter
   from PyQt5 import Qt, QtWidgets
   from PyQt5.QtCore import QCoreApplication
   from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
   from PyQt5 import QtGui, QtCore

except ImportError:
   print("    IMPORT ERROR ")
   print("PyQt5 NOT INSTALLED")
   print("  note that PyQt5 is included with anaconda3 installation")

# set matplotlib backend for PyQt
from matplotlib.backends.backend_qt5agg \
import NavigationToolbar2QT as NavigationToolbar

# add path to QuantumWell/src directory
from getPath import setPath
setPath(sys.path)

from MatplotlibWidget import MatplotlibWidget

from PlotPotentialWell import *
from DataPotentialWell import *
from BuildPotentialWell import *
from SolvePotentialWell import *
from FindStationaryStates import *
from plotPsi import *

from utilQt import sendMessageTE, BuildWellDock, SolveWellDock, MessageDock
from utilQt import AddBarrierDock, RemoveBarrierDock, FindStatesWellDock
from utilQt import AddSlopedPotentialDock, AddSHODock, MainDockWidget

###############################################################
class WidgetTester():
    """ test class for dock widgets in potentialWell project
    """
    ################### __init__ ###################################
    def __init__(self, widgt,name = ""):
        """ widgt must be a qwidget or inherit from widgt"""
        debug = False
        self.wd = widgt
        self.leftm = 50
        self.topm = 50
        self.sizemw = 415
        self.sizehw = 381
        if debug:
            print("leftm topm sizemw sizehw: ",self.leftm,self.topm,  \
                self.sizemw,self.sizehw)
            print("")

        self.printWidPosSize(self.wd,"before setGeometry",name)

        self.wd.setGeometry(self.leftm,self.topm,self.sizemw,self.sizehw)
        self.printWidPosSize(self.wd,"after setGeometry",name)

        self.wd.show()

    def printWidPosSize(self,widgg,titl,name):
        print("    name ",name)
        print("printWidPosSize ", titl,widgg.geometry(),"\n")

if __name__ == "__main__":
    # execute the following with: python widgetTester.py
    
    app = QtWidgets.QApplication(sys.argv)

    mswd1 = BuildWellDock()
    mswd2 =  SolveWellDock()
    mswd3 = MessageDock()

    mswd4 = AddBarrierDock()
    name = mswd4.objectName()

    mswd5 = RemoveBarrierDock()
    mswd6 = FindStatesWellDock()
    mswd7 = AddSlopedPotentialDock()
    mswd8 = AddSHODock()
    mswd9  = MainDockWidget()

    # remove comment to show widget, 
    # the QuantumWell dock widgets will overlap
    # on the monitor 
    #wgt1 = WidgetTester(mswd1,mswd1.objectName())
    #wgt2 = WidgetTester(mswd2, mswd2.objectName())
    #wgt3 = WidgetTester(mswd3, mswd3.objectName())
    wgt4 = WidgetTester(mswd4, mswd4.objectName())
    #wgt5 = WidgetTester(mswd5, mswd5.objectName())
    #wgt6 = WidgetTester(mswd6, mswd6.objectName())
    #wgt7 = WidgetTester(mswd7, mswd7.objectName())
    wgt8 = WidgetTester(mswd8, mswd8.objectName())
    wgt9 = WidgetTester(mswd9,mswd9.objectName())
    
    # start the application
    sys.exit(app.exec_())
    
    # to exit this application, close the MainDockWidget window
    # or close your terminal window or use your os force quit
    # option

    
