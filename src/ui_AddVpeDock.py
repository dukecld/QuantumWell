# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddVpeDock.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddVpeDock(object):
    def setupUi(self, AddVpeDock):
        AddVpeDock.setObjectName("AddVpeDock")
        AddVpeDock.resize(331, 374)
        AddVpeDock.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label_4 = QtWidgets.QLabel(self.dockWidgetContents)
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
        self.le_vleft = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.le_vleft.setObjectName("le_vleft")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.le_vleft)
        self.label_3 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.le_vright = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.le_vright.setObjectName("le_vright")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.le_vright)
        self.le_xzero = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.le_xzero.setObjectName("le_xzero")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_xzero)
        self.horizontalLayout.addLayout(self.formLayout)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout)
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
        self.te_addvpe = QtWidgets.QTextEdit(self.dockWidgetContents)
        self.te_addvpe.setObjectName("te_addvpe")
        self.verticalLayout.addWidget(self.te_addvpe)
        AddVpeDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(AddVpeDock)
        QtCore.QMetaObject.connectSlotsByName(AddVpeDock)

    def retranslateUi(self, AddVpeDock):
        _translate = QtCore.QCoreApplication.translate
        AddVpeDock.setWindowTitle(_translate("AddVpeDock", "DockWidget"))
        self.label_4.setText(_translate("AddVpeDock", "Add V-shaped potential"))
        self.label.setText(_translate("AddVpeDock", "PE Zero in Well (nm)"))
        self.label_2.setText(_translate("AddVpeDock", "PE Left Edge (eV)"))
        self.le_vleft.setText(_translate("AddVpeDock", "20.0"))
        self.label_3.setText(_translate("AddVpeDock", "PE Right Edge (eV)"))
        self.le_vright.setText(_translate("AddVpeDock", "20.0"))
        self.le_xzero.setText(_translate("AddVpeDock", "0.20"))
        self.pb_add.setText(_translate("AddVpeDock", "Add V PE"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddVpeDock = QtWidgets.QDockWidget()
    ui = Ui_AddVpeDock()
    ui.setupUi(AddVpeDock)
    AddVpeDock.show()
    sys.exit(app.exec_())

