# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainDockWidget.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainDockWidget(object):
    def setupUi(self, MainDockWidget):
        MainDockWidget.setObjectName("MainDockWidget")
        MainDockWidget.resize(403, 616)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pb_readfile = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pb_readfile.setObjectName("pb_readfile")
        self.verticalLayout.addWidget(self.pb_readfile)
        self.pb_writefile = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pb_writefile.setObjectName("pb_writefile")
        self.verticalLayout.addWidget(self.pb_writefile)
        self.line_3 = QtWidgets.QFrame(self.dockWidgetContents)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.pb_buildwell = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pb_buildwell.setObjectName("pb_buildwell")
        self.verticalLayout.addWidget(self.pb_buildwell)
        self.pb_addbarrier = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pb_addbarrier.setObjectName("pb_addbarrier")
        self.verticalLayout.addWidget(self.pb_addbarrier)
        self.pb_addslopedbase = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pb_addslopedbase.setObjectName("pb_addslopedbase")
        self.verticalLayout.addWidget(self.pb_addslopedbase)
        self.pb_addsimharosc = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pb_addsimharosc.setObjectName("pb_addsimharosc")
        self.verticalLayout.addWidget(self.pb_addsimharosc)
        self.pb_addmultibarriers = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pb_addmultibarriers.setObjectName("pb_addmultibarriers")
        self.verticalLayout.addWidget(self.pb_addmultibarriers)
        self.pb_addvpe = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pb_addvpe.setObjectName("pb_addvpe")
        self.verticalLayout.addWidget(self.pb_addvpe)
        self.pb_removebarrier = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pb_removebarrier.setObjectName("pb_removebarrier")
        self.verticalLayout.addWidget(self.pb_removebarrier)
        self.line_2 = QtWidgets.QFrame(self.dockWidgetContents)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.pb_solvepotwell = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pb_solvepotwell.setObjectName("pb_solvepotwell")
        self.verticalLayout.addWidget(self.pb_solvepotwell)
        self.pb_findstatstates = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pb_findstatstates.setObjectName("pb_findstatstates")
        self.verticalLayout.addWidget(self.pb_findstatstates)
        self.line = QtWidgets.QFrame(self.dockWidgetContents)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.pb_info = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pb_info.setObjectName("pb_info")
        self.verticalLayout.addWidget(self.pb_info)
        self.pb_quit = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pb_quit.setObjectName("pb_quit")
        self.verticalLayout.addWidget(self.pb_quit)
        MainDockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(MainDockWidget)
        QtCore.QMetaObject.connectSlotsByName(MainDockWidget)

    def retranslateUi(self, MainDockWidget):
        _translate = QtCore.QCoreApplication.translate
        MainDockWidget.setWindowTitle(_translate("MainDockWidget", "SteeringOptions"))
        self.pb_readfile.setText(_translate("MainDockWidget", "ReadDpwFile"))
        self.pb_writefile.setText(_translate("MainDockWidget", "WriteDpwFile"))
        self.pb_buildwell.setText(_translate("MainDockWidget", "BuildWell"))
        self.pb_addbarrier.setText(_translate("MainDockWidget", "AddBarrierPE"))
        self.pb_addslopedbase.setText(_translate("MainDockWidget", "AddLinearPE"))
        self.pb_addsimharosc.setText(_translate("MainDockWidget", "AddSimHarOscPE"))
        self.pb_addmultibarriers.setText(_translate("MainDockWidget", "AddMultipleBarrierPE"))
        self.pb_addvpe.setText(_translate("MainDockWidget", "AddVshapedPE"))
        self.pb_removebarrier.setText(_translate("MainDockWidget", "RemoveAddedPE"))
        self.pb_solvepotwell.setText(_translate("MainDockWidget", "SolveSchrodingerEq"))
        self.pb_findstatstates.setText(_translate("MainDockWidget", "FindStationaryStates"))
        self.pb_info.setText(_translate("MainDockWidget", "Info"))
        self.pb_quit.setText(_translate("MainDockWidget", "Quit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainDockWidget = QtWidgets.QDockWidget()
    ui = Ui_MainDockWidget()
    ui.setupUi(MainDockWidget)
    MainDockWidget.show()
    sys.exit(app.exec_())

