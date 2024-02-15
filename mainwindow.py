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
        MainWindow.resize(1034, 818)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.grph_3 = PlotWidget(self.groupBox_3)
        self.grph_3.setObjectName("grph_3")
        self.verticalLayout_3.addWidget(self.grph_3)
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_3.addWidget(self.checkBox)
        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.grph_input_sig = PlotWidget(self.groupBox_3)
        self.grph_input_sig.setObjectName("grph_input_sig")
        self.verticalLayout_4.addWidget(self.grph_input_sig)
        self.verticalLayout_6.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_5.addWidget(self.label_2)
        self.grph_output_sig = PlotWidget(self.groupBox_3)
        self.grph_output_sig.setObjectName("grph_output_sig")
        self.verticalLayout_5.addWidget(self.grph_output_sig)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.slider_process_speed = QtWidgets.QSlider(self.groupBox_3)
        self.slider_process_speed.setMaximum(100)
        self.slider_process_speed.setOrientation(QtCore.Qt.Horizontal)
        self.slider_process_speed.setObjectName("slider_process_speed")
        self.verticalLayout_6.addWidget(self.slider_process_speed)
        self.horizontalLayout_3.addLayout(self.verticalLayout_6)
        spacerItem = QtWidgets.QSpacerItem(13, 655, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.horizontalLayout_3.addItem(spacerItem)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_3, 0, 1, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.grph_phase_response = PlotWidget(self.groupBox_2)
        self.grph_phase_response.setObjectName("grph_phase_response")
        self.gridLayout_2.addWidget(self.grph_phase_response, 5, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 4, 0, 1, 1)
        self.grph_mag_response = PlotWidget(self.groupBox_2)
        self.grph_mag_response.setObjectName("grph_mag_response")
        self.gridLayout_2.addWidget(self.grph_mag_response, 3, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
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
        self.horizontalLayout.addLayout(self.verticalLayout_8)
        spacerItem1 = QtWidgets.QSpacerItem(0, 440, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_clr_zero = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_clr_zero.setObjectName("btn_clr_zero")
        self.verticalLayout.addWidget(self.btn_clr_zero)
        self.btn_clr_pole = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_clr_pole.setObjectName("btn_clr_pole")
        self.verticalLayout.addWidget(self.btn_clr_pole)
        self.btn_clr_all = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_clr_all.setObjectName("btn_clr_all")
        self.verticalLayout.addWidget(self.btn_clr_all)
        self.combx_zero_pole = QtWidgets.QComboBox(self.groupBox_2)
        self.combx_zero_pole.setObjectName("combx_zero_pole")
        self.combx_zero_pole.addItem("")
        self.combx_zero_pole.addItem("")
        self.verticalLayout.addWidget(self.combx_zero_pole)
        self.checkBox_conj = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_conj.setObjectName("checkBox_conj")
        self.verticalLayout.addWidget(self.checkBox_conj)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setStyleSheet("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_add_coeff = QtWidgets.QPushButton(self.groupBox)
        self.btn_add_coeff.setObjectName("btn_add_coeff")
        self.gridLayout.addWidget(self.btn_add_coeff, 4, 0, 1, 1)
        self.tbl_allpass_list = QtWidgets.QTableWidget(self.groupBox)
        self.tbl_allpass_list.setObjectName("tbl_allpass_list")
        self.tbl_allpass_list.setColumnCount(0)
        self.tbl_allpass_list.setRowCount(0)
        self.gridLayout.addWidget(self.tbl_allpass_list, 5, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)
        self.input_real = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.input_real.setMinimum(-100.0)
        self.input_real.setObjectName("input_real")
        self.gridLayout.addWidget(self.input_real, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)
        self.input_imag = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.input_imag.setMinimum(-100.0)
        self.input_imag.setObjectName("input_imag")
        self.gridLayout.addWidget(self.input_imag, 3, 0, 1, 1)
        self.grph_4 = PlotWidget(self.groupBox)
        self.grph_4.setObjectName("grph_4")
        self.gridLayout.addWidget(self.grph_4, 7, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 6, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1034, 26))
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
        self.groupBox_3.setTitle(_translate("MainWindow", "signal "))
        self.label_3.setText(_translate("MainWindow", "padding area"))
        self.checkBox.setText(_translate("MainWindow", "enable mouse genration"))
        self.label.setText(_translate("MainWindow", "orignal signal"))
        self.label_2.setText(_translate("MainWindow", "filterd signal"))
        self.groupBox_2.setTitle(_translate("MainWindow", "zeros poles"))
        self.label_5.setText(_translate("MainWindow", "frequency response"))
        self.label_6.setText(_translate("MainWindow", "z plane"))
        self.btn_clr_zero.setText(_translate("MainWindow", "clear all zeros"))
        self.btn_clr_pole.setText(_translate("MainWindow", "clear all poles"))
        self.btn_clr_all.setText(_translate("MainWindow", "clear all "))
        self.combx_zero_pole.setItemText(0, _translate("MainWindow", "add zero"))
        self.combx_zero_pole.setItemText(1, _translate("MainWindow", "add pole"))
        self.checkBox_conj.setText(_translate("MainWindow", "add conjigate"))
        self.label_4.setText(_translate("MainWindow", "magnitude response"))
        self.groupBox.setTitle(_translate("MainWindow", "all pass filter"))
        self.btn_add_coeff.setText(_translate("MainWindow", "Add"))
        self.label_8.setText(_translate("MainWindow", "add imag"))
        self.label_7.setText(_translate("MainWindow", "add real"))
        self.label_9.setText(_translate("MainWindow", "allpass response"))
from pyqtgraph import PlotWidget
