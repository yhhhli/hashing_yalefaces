# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from skimage import io
import get_nearest

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(989, 704)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(170, 570, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openimg)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 130, 301, 301))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(580, 90, 101, 111))
        self.label_2.setObjectName("label_2")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(830, 90, 101, 111))
        self.label_6.setObjectName("label_7")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(690, 300, 101, 111))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(580, 520, 101, 111))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(820, 520, 101, 111))
        self.label_5.setObjectName("label_5")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(50, 20, 72, 15))
        self.label_7.setObjectName("label_6")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(710, 20, 72, 15))
        self.label_8.setObjectName("label_8")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def openimg(self):
        imgName, imgType = QFileDialog.getOpenFileName(self.pushButton, 'ChooseImg', 'C:\\', 'Image files(*.jpg *.gif *.png *.bmp)')
        shown_jpg = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())
        self.label.setPixmap(shown_jpg)
        jpg=QtGui.QPixmap(imgName)
        jpg.save('sample.bmp')
        im = io.imread("sample.bmp", as_gray=True)
        list=get_nearest.get_five(im)
        sim_shown_jpg=QtGui.QPixmap(list[0][0]).scaled(self.label_2.width(), self.label_2.height())
        self.label_2.setPixmap(sim_shown_jpg)
        sim_shown_jpg = QtGui.QPixmap(list[1][0]).scaled(self.label_3.width(), self.label_3.height())
        self.label_3.setPixmap(sim_shown_jpg)
        sim_shown_jpg = QtGui.QPixmap(list[2][0]).scaled(self.label_4.width(), self.label_4.height())
        self.label_4.setPixmap(sim_shown_jpg)
        sim_shown_jpg = QtGui.QPixmap(list[3][0]).scaled(self.label_5.width(), self.label_5.height())
        self.label_5.setPixmap(sim_shown_jpg)
        sim_shown_jpg = QtGui.QPixmap(list[4][0]).scaled(self.label_6.width(), self.label_6.height())
        self.label_6.setPixmap(sim_shown_jpg)




    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "上传图片"))
        self.label.setText(_translate("Dialog", "TextLabel"))
        self.label_2.setText(_translate("Dialog", "TextLabel"))
        self.label_6.setText(_translate("Dialog", "TextLabel"))
        self.label_3.setText(_translate("Dialog", "TextLabel"))
        self.label_4.setText(_translate("Dialog", "TextLabel"))
        self.label_5.setText(_translate("Dialog", "TextLabel"))
        self.label_7.setText(_translate("Dialog", "被测图片"))
        self.label_8.setText(_translate("Dialog", "相似图片"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

