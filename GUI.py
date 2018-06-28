# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from compare1 import Compare1 
from compare import Compare
import os

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(500, 400)

        self.ans = QtGui.QLabel(Dialog)
        self.ans.setGeometry(QtCore.QRect(80, 50, 350, 200))
        self.ans.setObjectName(_fromUtf8("ans"))
        self.vecButton = QtGui.QRadioButton(Dialog)
        self.vecButton.setGeometry(QtCore.QRect(90, 60, 151, 22))
        self.vecButton.setObjectName(_fromUtf8("vecButton"))
        self.finButton = QtGui.QRadioButton(Dialog)
        self.finButton.setGeometry(QtCore.QRect(90, 100, 151, 22))
        self.finButton.setObjectName(_fromUtf8("finButton"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(80, 20, 200, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.okButton = QtGui.QPushButton(Dialog)
        self.okButton.setGeometry(QtCore.QRect(250, 240, 85, 27))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.okButton.clicked.connect(self.btnstate)



        self.fileDialog = QtGui.QFileDialog(Dialog)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.vecButton.setText(_translate(
            "Dialog", "Vector Space Model", None))
        self.finButton.setText(_translate("Dialog", "Fingerprinting", None))
        self.label.setText(_translate(
            "Dialog", "Choose Plagirism Engine", None))
        self.okButton.setText(_translate("Dialog", "OK", None))


    def btnstate(self):
        if self.vecButton.isChecked():
            print("Vector Selected")
            fileName = self.fileDialog.getOpenFileName()
            
            baby = Compare(fileName)

            self.vecButton.deleteLater()
            self.vecButton = None

            self.finButton.deleteLater()
            self.finButton = None

            self.okButton.deleteLater()
            self.okButton = None

            f = open('compare.txt','r')
            sr = f.read()
            self.label.setText("Top 5 Closest Documents")
            self.ans.setText(sr)
            os.remove("compare.txt")
            self.ans.setFont(QtGui.QFont("Coic", 13, QtGui.QFont.Bold) )

        elif self.finButton.isChecked():

            print("Fingerprinting Selected")
            fileName = self.fileDialog.getOpenFileName()
            baby = Compare1(fileName)


            self.vecButton.deleteLater()
            self.vecButton = None

            self.finButton.deleteLater()
            self.finButton = None

            self.okButton.deleteLater()
            self.okButton = None
            f = open('compare1.txt','r')
            sr = f.read()
            self.label.setText("Top 5 Closest Documents")
            self.ans.setText(sr)
            os.remove("compare1.txt")
            self.ans.setFont(QtGui.QFont("Coic", 13, QtGui.QFont.Bold) )
        else:
            print("Please select a method")


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)

    Dialog.show()
    sys.exit(app.exec_())

