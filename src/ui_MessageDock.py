# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MessageDock.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MessageDock(object):
    def setupUi(self, MessageDock):
        MessageDock.setObjectName("MessageDock")
        MessageDock.resize(415, 381)
        MessageDock.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.te_message = QtWidgets.QTextEdit(self.dockWidgetContents)
        self.te_message.setReadOnly(True)
        self.te_message.setObjectName("te_message")
        self.verticalLayout.addWidget(self.te_message)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.pb_print = QtWidgets.QPushButton(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pb_print.setFont(font)
        self.pb_print.setObjectName("pb_print")
        self.horizontalLayout_3.addWidget(self.pb_print)
        self.pb_save = QtWidgets.QPushButton(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pb_save.setFont(font)
        self.pb_save.setObjectName("pb_save")
        self.horizontalLayout_3.addWidget(self.pb_save)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        MessageDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(MessageDock)
        QtCore.QMetaObject.connectSlotsByName(MessageDock)

    def retranslateUi(self, MessageDock):
        _translate = QtCore.QCoreApplication.translate
        MessageDock.setWindowTitle(_translate("MessageDock", "Message box"))
        self.pb_print.setText(_translate("MessageDock", "Print"))
        self.pb_save.setText(_translate("MessageDock", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MessageDock = QtWidgets.QDockWidget()
    ui = Ui_MessageDock()
    ui.setupUi(MessageDock)
    MessageDock.show()
    sys.exit(app.exec_())

