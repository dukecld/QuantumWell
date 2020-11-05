# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SolveWellDock.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SolveWellDock(object):
    def setupUi(self, SolveWellDock):
        SolveWellDock.setObjectName("SolveWellDock")
        SolveWellDock.resize(372, 387)
        SolveWellDock.setMinimumSize(QtCore.QSize(280, 261))
        SolveWellDock.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.l_toplabel = QtWidgets.QLabel(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.l_toplabel.setFont(font)
        self.l_toplabel.setObjectName("l_toplabel")
        self.horizontalLayout_5.addWidget(self.l_toplabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.dockWidgetContents)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.le_solve = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.le_solve.setObjectName("le_solve")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_solve)
        self.verticalLayout.addLayout(self.formLayout)
        self.line = QtWidgets.QFrame(self.dockWidgetContents)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.line_2 = QtWidgets.QFrame(self.dockWidgetContents)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(1)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.pb_solve = QtWidgets.QPushButton(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_solve.sizePolicy().hasHeightForWidth())
        self.pb_solve.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.pb_solve.setFont(font)
        self.pb_solve.setObjectName("pb_solve")
        self.horizontalLayout_4.addWidget(self.pb_solve)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.te_solvewell = QtWidgets.QTextEdit(self.dockWidgetContents)
        self.te_solvewell.setReadOnly(True)
        self.te_solvewell.setObjectName("te_solvewell")
        self.verticalLayout.addWidget(self.te_solvewell)
        SolveWellDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(SolveWellDock)
        QtCore.QMetaObject.connectSlotsByName(SolveWellDock)

    def retranslateUi(self, SolveWellDock):
        _translate = QtCore.QCoreApplication.translate
        SolveWellDock.setWindowTitle(_translate("SolveWellDock", "Solve Well Window"))
        self.l_toplabel.setText(_translate("SolveWellDock", "Potential Well Solver"))
        self.label.setText(_translate("SolveWellDock", "Energy (eV)"))
        self.le_solve.setText(_translate("SolveWellDock", "10.0"))
        self.pb_solve.setText(_translate("SolveWellDock", "Click to Find Psi "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SolveWellDock = QtWidgets.QDockWidget()
    ui = Ui_SolveWellDock()
    ui.setupUi(SolveWellDock)
    SolveWellDock.show()
    sys.exit(app.exec_())

