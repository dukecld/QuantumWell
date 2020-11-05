# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddBarrierDock.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddBarrierDock(object):
    def setupUi(self, AddBarrierDock):
        AddBarrierDock.setObjectName("AddBarrierDock")
        AddBarrierDock.resize(472, 427)
        AddBarrierDock.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label_4 = QtWidgets.QLabel(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.dockWidgetContents)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.le_xmax = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.le_xmax.setObjectName("le_xmax")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.le_xmax)
        self.label_3 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.le_barrierv = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.le_barrierv.setObjectName("le_barrierv")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.le_barrierv)
        self.le_xmin = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.le_xmin.setObjectName("le_xmin")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_xmin)
        self.horizontalLayout.addLayout(self.formLayout)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(self.dockWidgetContents)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(1)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.pb_add = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pb_add.setObjectName("pb_add")
        self.horizontalLayout_2.addWidget(self.pb_add)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.te_addbarrier = QtWidgets.QTextEdit(self.dockWidgetContents)
        self.te_addbarrier.setObjectName("te_addbarrier")
        self.verticalLayout.addWidget(self.te_addbarrier)
        AddBarrierDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(AddBarrierDock)
        QtCore.QMetaObject.connectSlotsByName(AddBarrierDock)

    def retranslateUi(self, AddBarrierDock):
        _translate = QtCore.QCoreApplication.translate
        AddBarrierDock.setWindowTitle(_translate("AddBarrierDock", "Add Barrier"))
        self.label_4.setText(_translate("AddBarrierDock", "Add Potential Barrier"))
        self.label.setText(_translate("AddBarrierDock", "Left Edge of Barrier (nm)"))
        self.label_2.setText(_translate("AddBarrierDock", "Right Edge of Barrier (nm)"))
        self.le_xmax.setText(_translate("AddBarrierDock", "0.22"))
        self.label_3.setText(_translate("AddBarrierDock", "Barrier Potential Energy (eV)"))
        self.le_barrierv.setText(_translate("AddBarrierDock", "64.0"))
        self.le_xmin.setText(_translate("AddBarrierDock", "0.18"))
        self.pb_add.setText(_translate("AddBarrierDock", "Click to Add Barrier"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddBarrierDock = QtWidgets.QDockWidget()
    ui = Ui_AddBarrierDock()
    ui.setupUi(AddBarrierDock)
    AddBarrierDock.show()
    sys.exit(app.exec_())

