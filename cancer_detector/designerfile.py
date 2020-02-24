# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designerfile.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
import numpy as np
import pickle
import cv2
from backend import features

class Ui_MainWindow(QtWidgets.QMainWindow):

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1108, 782)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(130, 70, 381, 361))
        self.graphicsView.setObjectName("graphicsView")

        self.scene = QtWidgets.QGraphicsScene()

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(440, 520, 241, 51))
        self.pushButton.setObjectName("pushButton")

        self.pushButton.setStatusTip('Calculates cancerousness')
        self.pushButton.clicked.connect(self.calc)

        self.graphicsView_2 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_2.setGeometry(QtCore.QRect(620, 70, 391, 361))
        self.graphicsView_2.setObjectName("graphicsView_2")

        self.scene_2 = QtWidgets.QGraphicsScene()

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1108, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)

        self.actionOpen_Image = QtWidgets.QAction(MainWindow)
        self.actionOpen_Image.setObjectName("actionOpen_Image")
        self.menuFile.addAction(self.actionOpen_Image)
        self.menubar.addAction(self.menuFile.menuAction())
        self.actionOpen_Image.triggered.connect(self.showDialog)

        MainWindow.setWindowIcon(QtGui.QIcon('ribbon_n7C_12'))
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def showDialog(self):

        f,_ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '/home')
        self.image = cv2.imread(f)
        self.scene.clear()
        self.scene_2.clear()
        self.scene.addPixmap(QtGui.QPixmap(f))
        self.graphicsView.setScene(self.scene)

    def calc(self):

        image = self.image
        rFC = pickle.load(open('rFCfinal.sav', 'rb'))

        r, g, b = features.colorRatioMean(image)
        m, v = features.LBPmv(image)
        n, c, rat = features.areas(image)

        feat = np.array([r, g, b, features.roughnessIndex(image), features.variance(image), features.entropy(image),
                         features.imageMean(image), m, v, n, c, rat, features.perimeter(image)])

        feat = np.reshape(feat, [1, 13], 'C')
        prediction = rFC.predict(feat)

        if prediction == 1:
            self.scene_2.addPixmap(QtGui.QPixmap('./images/Cancerous.png'))
            self.graphicsView_2.setScene(self.scene_2)
        else:
            self.scene_2.addPixmap(QtGui.QPixmap('./images/Non-Cancerous.png'))
            self.graphicsView_2.setScene(self.scene_2)  


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Classify Image"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen_Image.setText(_translate("MainWindow", "Open Image"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
