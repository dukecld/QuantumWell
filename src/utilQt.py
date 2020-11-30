#  utilities for potentialWell.py PyQt5 classes

import numpy as np
import datetime
import os

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QDockWidget, QDialog, QFileDialog
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

# All ui modules built with Qt-Designer
from ui_MainDockWidget import Ui_MainDockWidget
from ui_BuildWellDock import Ui_BuildWellDock
from ui_SolveWellDock import Ui_SolveWellDock
from ui_FindStatesWellDock import Ui_FindStatesWellDock
from ui_MessageDock import Ui_MessageDock
from ui_AddBarrierDock import Ui_AddBarrierDock
from ui_RemoveBarrierDock import Ui_RemoveBarrierDock
from ui_AddSlopedPotentialDock import Ui_AddSlopedPotentialDock
from ui_AddSHODock import Ui_AddSHODock
from ui_AddMultiBarriersDock import Ui_AddMultiBarriersDock
from ui_InfoDock import Ui_InfoDock
from ui_AddVpeDock import Ui_AddVpeDock


def sendMessageTE(message, texted, dateFlag=True, endFlag=True):
    """ Send a message to a QTextEdit instance.

    Parameters:
        message:  message string
        texted:   QTextEdit instance
        dateFlag: if True, include date and time with message
        endFlag:  if True, move cursor to bottom of window

    Returns:
        pstr: complete message string

   """
    debug = False
    if debug:
        print("in sendMessageTE")
        print("dateFlag: ", dateFlag)
        print("endFlag: ", endFlag)
        print("message: ", message)

    if endFlag:
        texted.moveCursor(QtGui.QTextCursor.End)

    # initial text line includes data and time
    pstr = " "
    if dateFlag:
        strDateTime = datetime.datetime.now().strftime("%x       %X")
        pstr = "-------------------- " + strDateTime + "\n"

    pstr = pstr + message + "\n"
    # insert text at the end
    texted.insertPlainText(pstr)

    if endFlag:
        # to always see the inserted text, move the scroll bar
        # to its maximum value
        texted.verticalScrollBar().setValue(
            texted.verticalScrollBar().maximum())

    # return the full string added to the textedit box
    if debug:
        print("full message: ", pstr)
    return pstr


# ----------------------------------------------------------------
def printMessageTE(textEd):
    """ Print qtextedit or global widget,
        Uses QPrintDialog
    """

    debug = False
    if debug:
        print("  -- in printLog")

    printer = QPrinter()

    printer.Letter
    printer.HighResolution
    printer.Color

    anotherWidget = QPrintDialog(printer)
    if (anotherWidget.exec_() == QDialog.Accepted):
        textEd.document().print_(anotherWidget.printer())


# -------------------------------------------------------------
# ----------------------------------------------------
def saveMessageTE(textEd):
    """ write qtextedit or global widget
        to a file, uses QFileDialog
    """

    debug = False
    if debug:
        print("  -- in saveLog")
        # print("self.mswd.te_message", self.mswd.te_message.toPlainText())

    # get filename
    filenameTuple = QFileDialog.getSaveFileName(caption="write log file",
                                                filter="*.log")
    filename = filenameTuple[0]

    if filename:
        fname = str(filename)
        fbase, fext = os.path.splitext(fname)
        if fext != '.log':
            fname += '.log'

        f = open(fname, 'w')
        f.write(str(textEd.toPlainText()))
        f.close()

    return


# ---------------- stringToFloat -------------------
def stringToFloat(string, numD=6):
    """ Convert string to float type

    Returns: tuple stringFloat, okfloat

    """
    okfloat = True
    try:
        stringFloat = float(string)
    except ValueError:
        okfloat = False
        stringFloat = 0.0

    if okfloat:
        if np.isfinite(stringFloat):
            stringFloat = np.around(stringFloat, numD)

    return stringFloat, okfloat


# ----------------- stringToInt ---------------------------------
def stringToInt(string):
    """ convert string to integer type

    Returns: tuple stringint, okint

    """
    okint = True
    try:
        stringint = int(string)
    except ValueError:
        okint = False
        stringint = 0
    return stringint, okint


# =====================  setup ui files =====================
#  rename closeEvent for dock to ignore red close button
#       closeEvent is a method in QDockWidget


class MainDockWidget(QDockWidget, Ui_MainDockWidget):
    """ Inherit from Ui_MainDockWidget
    """

    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QDockWidget.__init__(self, parent, f)
        self.setupUi(self)


class BuildWellDock(QDockWidget, Ui_BuildWellDock):
    """ Inherit from Ui_MainDockWidget
    """

    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QDockWidget.__init__(self, parent, f)
        self.setupUi(self)


class AddMultiBarriersDock(QDockWidget, Ui_AddMultiBarriersDock):
    """ Inherit from Ui_MainDockWidget
    """

    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QDockWidget.__init__(self, parent, f)
        self.setupUi(self)


class SolveWellDock(QDockWidget, Ui_SolveWellDock):
    """ Inherit from Ui_MainDockWidget
    """

    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QDockWidget.__init__(self, parent, f)
        self.setupUi(self)


class MessageDock(QDockWidget, Ui_MessageDock):
    """ Inherit from Ui_MessageDock
    """

    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QDockWidget.__init__(self, parent, f)
        self.setupUi(self)


class AddBarrierDock(QDockWidget, Ui_AddBarrierDock):
    """ Inherit from Ui_AddBarrierDock
    """

    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QDockWidget.__init__(self, parent, f)
        self.setupUi(self)


class RemoveBarrierDock(QDockWidget, Ui_RemoveBarrierDock):
    """ Inherit from Ui_RemoveBarrierDock
    """

    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QDockWidget.__init__(self, parent, f)
        self.setupUi(self)


class FindStatesWellDock(QDockWidget, Ui_FindStatesWellDock):
    """ Inherit from Ui_FindStatesWellDock
    """

    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QDockWidget.__init__(self, parent, f)
        self.setupUi(self)


class AddSlopedPotentialDock(QDockWidget, Ui_AddSlopedPotentialDock):
    """ Inherit from Ui_AddSlopedPotentialDock
    """

    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QDockWidget.__init__(self, parent, f)
        self.setupUi(self)


class AddSHODock(QDockWidget, Ui_AddSHODock):
    """ Inherit from Ui_AddSHODock
    """

    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QDockWidget.__init__(self, parent, f)
        self.setupUi(self)


class InfoDock(QDockWidget, Ui_InfoDock):
    """ Inherit from Ui_InfoDock
    """

    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QDockWidget.__init__(self, parent, f)
        self.setupUi(self)


class AddVpeDock(QDockWidget, Ui_AddVpeDock):
    """ Inherit from Ui_AddVpeDock
    """

    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QDockWidget.__init__(self, parent, f)
        self.setupUi(self)
