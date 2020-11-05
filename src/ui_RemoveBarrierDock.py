# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RemoveBarrierDock.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RemoveBarrierDock(object):
    def setupUi(self, RemoveBarrierDock):
        RemoveBarrierDock.setObjectName("RemoveBarrierDock")
        RemoveBarrierDock.resize(399, 381)
        RemoveBarrierDock.setMinimumSize(QtCore.QSize(296, 248))
        RemoveBarrierDock.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
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
        self.l_toplabel.setWordWrap(False)
        self.l_toplabel.setObjectName("l_toplabel")
        self.horizontalLayout_5.addWidget(self.l_toplabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.le_number = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.le_number.setObjectName("le_number")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_number)
        self.label = QtWidgets.QLabel(self.dockWidgetContents)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.verticalLayout.addLayout(self.formLayout)
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
        self.pb_ok = QtWidgets.QPushButton(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.pb_ok.setFont(font)
        self.pb_ok.setObjectName("pb_ok")
        self.horizontalLayout_4.addWidget(self.pb_ok)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.te_removebarrier = QtWidgets.QTextEdit(self.dockWidgetContents)
        self.te_removebarrier.setReadOnly(True)
        self.te_removebarrier.setObjectName("te_removebarrier")
        self.verticalLayout.addWidget(self.te_removebarrier)
        RemoveBarrierDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(RemoveBarrierDock)
        QtCore.QMetaObject.connectSlotsByName(RemoveBarrierDock)

    def retranslateUi(self, RemoveBarrierDock):
        _translate = QtCore.QCoreApplication.translate
        RemoveBarrierDock.setWindowTitle(_translate("RemoveBarrierDock", "RemoveAddedV Window"))
        self.l_toplabel.setText(_translate("RemoveBarrierDock", "Remove Added Potential"))
        self.le_number.setText(_translate("RemoveBarrierDock", "1"))
        self.label.setText(_translate("RemoveBarrierDock", "ID Number of Added Potential "))
        self.pb_ok.setText(_translate("RemoveBarrierDock", "Click to Remove Added PE"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RemoveBarrierDock = QtWidgets.QDockWidget()
    ui = Ui_RemoveBarrierDock()
    ui.setupUi(RemoveBarrierDock)
    RemoveBarrierDock.show()
    sys.exit(app.exec_())

