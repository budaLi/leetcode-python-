# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.toolButton = QtWidgets.QToolButton(Dialog)
        self.toolButton.setGeometry(QtCore.QRect(180, 40, 47, 21))
        self.toolButton.setObjectName("toolButton")
        self.toolBox = QtWidgets.QToolBox(Dialog)
        self.toolBox.setGeometry(QtCore.QRect(50, 60, 85, 145))
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 85, 85))
        self.page.setObjectName("page")
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 100, 30))
        self.page_2.setObjectName("page_2")
        self.toolBox.addItem(self.page_2, "")
        self.columnView = QtWidgets.QColumnView(Dialog)
        self.columnView.setGeometry(QtCore.QRect(160, 80, 151, 161))
        self.columnView.setObjectName("columnView")

        self.retranslateUi(Dialog)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.toolButton.setText(_translate("Dialog", "..."))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("Dialog", "Page 1"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("Dialog", "Page 2"))


def main():
    """
    主函数，用于运行程序
    :return: None
    """
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
