# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1408, 874)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_8.addWidget(self.label_6)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_8.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.verticalLayout_8)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.checkBox_conj = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_conj.setObjectName("checkBox_conj")
        self.horizontalLayout_4.addWidget(self.checkBox_conj)
        self.btn_clr_all = QtWidgets.QPushButton(self.centralwidget)
        self.btn_clr_all.setObjectName("btn_clr_all")
        self.horizontalLayout_4.addWidget(self.btn_clr_all)
        self.btn_clr_pole = QtWidgets.QPushButton(self.centralwidget)
        self.btn_clr_pole.setObjectName("btn_clr_pole")
        self.horizontalLayout_4.addWidget(self.btn_clr_pole)
        self.btn_clr_zero = QtWidgets.QPushButton(self.centralwidget)
        self.btn_clr_zero.setObjectName("btn_clr_zero")
        self.horizontalLayout_4.addWidget(self.btn_clr_zero)
        self.combx_zero_pole = QtWidgets.QComboBox(self.centralwidget)
        self.combx_zero_pole.setObjectName("combx_zero_pole")
        self.combx_zero_pole.addItem("")
        self.combx_zero_pole.addItem("")
        self.horizontalLayout_4.addWidget(self.combx_zero_pole)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_7.addWidget(self.label_4)
        self.grph_mag_response = PlotWidget(self.centralwidget)
        self.grph_mag_response.setObjectName("grph_mag_response")
        self.verticalLayout_7.addWidget(self.grph_mag_response)
        spacerItem = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem)
        self.horizontalLayout_6.addLayout(self.verticalLayout_7)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.grph_phase_response = PlotWidget(self.centralwidget)
        self.grph_phase_response.setObjectName("grph_phase_response")
        self.verticalLayout_2.addWidget(self.grph_phase_response)
        spacerItem1 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_6.addLayout(self.verticalLayout_2)
        self.horizontalLayout.addLayout(self.horizontalLayout_6)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 3, 0, 1, 1)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout.addWidget(self.doubleSpinBox, 0, 0, 1, 1)
        self.grph_4 = PlotWidget(self.groupBox)
        self.grph_4.setObjectName("grph_4")
        self.gridLayout.addWidget(self.grph_4, 4, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 1, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.grph_3 = PlotWidget(self.centralwidget)
        self.grph_3.setObjectName("grph_3")
        self.verticalLayout_3.addWidget(self.grph_3)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_3.addWidget(self.checkBox)
        spacerItem2 = QtWidgets.QSpacerItem(20, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.grph_1 = PlotWidget(self.centralwidget)
        self.grph_1.setObjectName("grph_1")
        self.verticalLayout_4.addWidget(self.grph_1)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_5.addWidget(self.label_2)
        self.grph_2 = PlotWidget(self.centralwidget)
        self.grph_2.setObjectName("grph_2")
        self.verticalLayout_5.addWidget(self.grph_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)
        self.slider_process_speed = QtWidgets.QSlider(self.centralwidget)
        self.slider_process_speed.setMaximum(100)
        self.slider_process_speed.setOrientation(QtCore.Qt.Horizontal)
        self.slider_process_speed.setObjectName("slider_process_speed")
        self.verticalLayout_6.addWidget(self.slider_process_speed)
        self.horizontalLayout_5.addLayout(self.verticalLayout_6)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1408, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_6.setText(_translate("MainWindow", "z plane"))
        self.checkBox_conj.setText(_translate("MainWindow", "add conjigate"))
        self.btn_clr_all.setText(_translate("MainWindow", "clear all "))
        self.btn_clr_pole.setText(_translate("MainWindow", "clear all poles"))
        self.btn_clr_zero.setText(_translate("MainWindow", "clear all zeros"))
        self.combx_zero_pole.setItemText(0, _translate("MainWindow", "add zero"))
        self.combx_zero_pole.setItemText(1, _translate("MainWindow", "add pole"))
        self.label_4.setText(_translate("MainWindow", "magnitude response"))
        self.label_5.setText(_translate("MainWindow", "frequency response"))
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox"))
        self.pushButton.setText(_translate("MainWindow", "Add"))
        self.label_3.setText(_translate("MainWindow", "padding area"))
        self.checkBox.setText(_translate("MainWindow", "CheckBox"))
        self.label.setText(_translate("MainWindow", "orignal signal"))
        self.label_2.setText(_translate("MainWindow", "filterd signal"))
from pyqtgraph import PlotWidget
