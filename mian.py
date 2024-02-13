from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog, QShortcut
from scipy import signal
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene

import pandas as pd
from PyQt5.QtWidgets import QInputDialog  ,  QApplication, QMainWindow, QShortcut, QFileDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtCore, QtGui
import pyqtgraph as pg
from scipy import signal

from PyQt5.QtCore import Qt


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PyQt5.QtWidgets import  QApplication, QMainWindow, QShortcut, QMenu 
from scipy.signal import spectrogram
from scipy.signal import resample
import sys
from PyQt5.QtGui import  QKeySequence , QCursor
from mainwindow import Ui_MainWindow  

import numpy as np
from PyQt5.QtCore import pyqtSlot
import sounddevice as sd
import librosa

class DraggablePoint:
    def __init__(self, ax , parent , x, y , marker):
        self.x = x
        self.y = y
        self.ax = ax
        self.parent = parent
        self.marker = marker
        self.point, = ax.plot(x, y, marker, markersize=7, color='r', markeredgewidth=1)
        self.cpid = self.point.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cmid = self.point.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.ceid = self.point.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.crid = self.point.figure.canvas.mpl_connect('button_release_event', self.on_right_click)
        self.conj = None
        self.press = None
        
    def create_conjgate(self):
        self.conj = DraggablePoint(self.ax , self.parent, self.x , -self.y , self.marker)
        self.conj.conj = self
        self.conj.draw_point(self.conj.x , self.conj.y)

    def on_press(self, event):
        if event.inaxes == self.ax:
            contains, _ = self.point.contains(event)
            if contains:
                self.press = self.point.get_data(), event.xdata, event.ydata

    def on_right_click(self, event):
        if event.inaxes == self.ax and event.button == 3: 
            contains, _ = self.point.contains(event)
            if contains:
                self.delete_point()
        self.parent.response_plot()
                

    def on_motion(self, event):
        if self.press is None:
            return
        if event.inaxes == self.ax:
            prev_data, xpress, ypress = self.press
            dx = event.xdata - xpress
            dy = event.ydata - ypress
            # self.x , self.y = (prev_data[0] + dx, prev_data[1] + dy)
            self.x , self.y = ((prev_data[0] + dx)[0], (prev_data[1] + dy)[0])
            self.point.set_data([self.x] , [self.y])
            self.point.figure.canvas.draw()
            if self.conj != None:
                self.conj.x, self.conj.y = self.x, -self.y
                self.conj.point.set_data([self.conj.x], [self.conj.y])
                self.conj.point.figure.canvas.draw()
        self.parent.response_plot()

    def on_release(self, event):
        self.press = None
        self.parent.circle.figure.canvas.draw()

    def draw_point(self, x, y):
        self.point.set_data([x], [y])
        self.point.figure.canvas.draw()

    def delete_point(self):
        self.parent.delete_point(self)

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=1, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class CustomGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.points_x = []
        self.points_y = []
        
    def mouseDoubleClickEvent(self, event):
        # Call your function here
        print("Double click event occurred")
        
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            pos = event.pos()
            scene_pos = self.mapToScene(pos)
            self.points_x.append(scene_pos.x())
            self.points_y.append(scene_pos.y())
            print(f"X: {scene_pos.x()}, Y: {scene_pos.y()}")
        super().mouseMoveEvent(event)

class MyWindow(QMainWindow):   
    
    def __init__(self ):
        super(MyWindow , self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  
        # self.padding_area = CustomGraphicsView()
        # self.ui.verticalLayout_3.addWidget(self.padding_area)
        
        self.c = MplCanvas(self)
        
        self.zeros = []
        self.poles = []
        self.zeros_conj = []
        self.poles_conj = []

        # self.ui.checkBox_conj.stateChanged.connect(self.handle_checkbox_change)
        self.current_index = 0

        QShortcut(QKeySequence("Ctrl+z"), self).activated.connect(lambda: self.combo_switch(0))
        QShortcut(QKeySequence("Ctrl+p"), self).activated.connect(lambda: self.combo_switch(1))
        QShortcut(QKeySequence("Ctrl+c"), self).activated.connect(self.check_switch)

        self.circle = self.c.axes.add_patch(plt.Circle((0, 0), 1, color='b', fill=False))
        self.c.axes.axhline(0, color='black',linewidth=0.5)
        self.c.axes.axvline(0, color='black',linewidth=0.5)

        self.ui.horizontalLayout_2.addWidget(self.c)
        self.c.axes.set_xlim(-1.5, 1.5)
        self.c.axes.set_ylim(-1.5, 1.5)
        
        self.ui.btn_clr_zero.clicked.connect(self.clear_all_zeros)
        self.ui.btn_clr_pole.clicked.connect(self.clear_all_poles)
        self.ui.btn_clr_all.clicked.connect(self.clear_all)
        QShortcut(QKeySequence("Ctrl+o"), self).activated.connect(self.open_file)
        self.ui.grph_3.scene().sigMouseMoved.connect(self.genrate_signal_with_mouse)
        self.ui.checkBox.stateChanged.connect(self.handle_gen_checkbox)

        # self.

        self.animation_timer = QTimer()
        # self.animation_timer.timeout.connect(self.update_plot_with_time)
        
        self.c.mpl_connect('button_press_event', self.on_double_click)

        # coeff_item = QTableWidgetItem("x1")
        # coeff_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
        # coeff_item.setCheckState(Qt.CheckState.Checked)
        # # Insert the item into the table widget
        # self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
        # self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1, 0, coeff_item)

        # self.ui.tableWidget.add
        self.ui.tableWidget.setColumnCount(1)  # Set column count to 1 for a single column
        self.ui.tableWidget.setRowCount(1) 
        item =  QTableWidgetItem('Item')
        item.setFlags(item.flags() | 2)  # Enable ItemIsUserCheckable
        item.setCheckState(1)  # Set default state to unchecked
        self.ui.tableWidget.setItem(0, 0, item)
        # self.ui.tableWidget.setItem(2, 0, item)
        # self.ui.tableWidget.setItem(3, 0, item)

        self.animation_speed = 1

        self.x_positions = []
        self.y_positions = []
        self.counter = 1
        self.gen_data = []
        self.data_y = None
        self.data_x = None
        
        self.ui.slider_process_speed.valueChanged.connect(self.handle_slider_speed)
        
    def handle_slider_speed(self):
          self.animation_speed = int(self.ui.slider_process_speed.value())
          
    def handle_gen_checkbox(self):
        if  self.ui.checkBox.isChecked():
            self.animation_timer.stop()
            self.data_x = 0
            self.data_y = []
            self.ui.grph_1.clear()     
            
    def genrate_signal_with_mouse(self , event):
        if self.ui.checkBox.isChecked():
            x = event.x()
            y = event.y()
            self.x_positions.append(x)
            self.y_positions.append(y)
            self.ui.grph_1.clear()
            self.counter += 1
            self.gen_data.append(self.counter)
            self.data_y = self.x_positions
            self.ui.grph_1.plot(self.gen_data , self.x_positions)
            self.ui.grph_1.autoRange()
            print(self.x_positions)
            self.create_filter_from_z_p()
            self.ui.grph_2.plot(self.gen_data , self.filtered_signal)
            self.ui.grph_2.autoRange()

        print("_____")
    
    def create_filter_from_z_p(self):
        zeros , poles = self.get_zeros_poles()
        a, b = signal.zpk2tf(zeros, poles, 1)
        self.filtered_signal = np.real(signal.lfilter(b, a, self.data_y))
        # pass

    def combo_switch(self , index):
        self.ui.combx_zero_pole.setCurrentIndex(index)
    
    def check_switch(self ):
        if self.ui.checkBox_conj.isChecked():
            self.ui.checkBox_conj.setChecked(False)
        else:
            self.ui.checkBox_conj.setChecked(True)
        
    def remove_all_cong(self):
        # pass
        for zero in self.zeros:
            if zero.conj != None:
                zero.conj.point.remove()
                zero.conj = None
        for pole in self.poles:
            if pole.conj != None:
                pole.conj.point.remove()
                pole.conj = None
                
        self.zeros_conj.clear()
        self.poles_conj.clear()
        self.circle.figure.canvas.draw()
        self.response_plot()  

    def delete_point(self , point):
        point.point.remove()
        if point.conj != None:
            point.conj.point.remove()
            if point.conj in self.zeros:
                self.zeros.remove(point.conj) 
            elif point.conj in self.poles:
                self.poles.remove(point.conj) 
            elif point.conj in self.zeros_conj:
                self.zeros_conj.remove(point.conj) 
            elif point.conj in self.poles_conj:
                self.poles_conj.remove(point.conj) 
            


        if point in self.zeros:
            self.zeros.remove(point) 
        elif point in self.poles:
            self.poles.remove(point) 
        elif point in self.zeros_conj:
            self.zeros_conj.remove(point) 
        elif point in self.poles_conj:
            self.poles_conj.remove(point) 
            
        self.circle.figure.canvas.draw()

    def on_double_click(self, event):
        x, y = event.xdata, event.ydata
        if event.inaxes == self.c.axes and event.button == Qt.LeftButton and event.dblclick:
            if self.ui.combx_zero_pole.currentText() =="add zero":
                marker = 'o'
                self.zeros.append(DraggablePoint(self.c.axes,self ,  x, y ,marker ))
                if self.ui.checkBox_conj.isChecked():
                    self.zeros[-1].create_conjgate()
                    self.zeros_conj.append(self.zeros[-1].conj)

            else:
                marker = "x"
                self.poles.append(DraggablePoint(self.c.axes,self ,  x, y ,marker ))
                if self.ui.checkBox_conj.isChecked():
                    self.poles[-1].create_conjgate()
                    self.poles_conj.append(self.poles[-1].conj)
            self.response_plot()

            
            # if self.ui.checkBox_conj.isChecked():
            #     self.add_conj()

    def print(self):
        print("zeros")
        for zero in self.zeros:
            
            print(zero.x , zero.y)
        print("________")

        print("poles")
        for pole in self.poles:
            
            print(pole.x , pole.y)
        print("________")
        
        print("poles_conj")
        for pole_conj in self.poles_conj:
            
            print(pole_conj.x , pole_conj.y)
        print("________")
        
        print("zeros_conj")
        for zero_conj in self.zeros_conj:
            
            print(zero_conj.x , zero_conj.y)
        print("________")

    def clear_all_zeros(self):
        for zero in self.zeros:
            zero.point.remove()
            if zero.conj != None:
                zero.conj.point.remove()
                self.zeros_conj.remove(zero.conj)
        self.zeros.clear()
        self.zeros_conj.clear()
        self.circle.figure.canvas.draw()
        self.response_plot()
        
    def clear_all_poles(self):
        for pole in self.poles:
            pole.point.remove()
            if pole.conj != None:
                pole.conj.point.remove()
                self.poles_conj.remove(pole.conj)
        self.poles.clear()
        self.poles_conj.clear()
        self.circle.figure.canvas.draw()
        self.response_plot()
        
    def clear_all(self):
        self.clear_all_poles()
        self.clear_all_zeros()
        
    def convert_to_complex(self , points , conjgate):
        points_c = points + conjgate
        numbers = [(point.x , point.y ) for point in points_c]
        print(numbers)
        return [complex(real, imag) for (real, imag) in numbers ]

    def clear_mag_phase_grph(self):
        self.ui.grph_mag_response.clear()
        self.ui.grph_phase_response.clear()
    
    def get_zeros_poles(self):
        print("zeros")
        print(self.zeros)
        zeros = self.convert_to_complex(self.zeros , self.zeros_conj)
        poles = self.convert_to_complex(self.poles , self.poles_conj)
        return zeros , poles
    
    def response_plot(self):
        self.clear_mag_phase_grph()
        zeros , poles = self.get_zeros_poles()
        print("here")
        print(zeros)
        print(poles)
        print("here")
        system = signal.TransferFunction(np.poly(zeros), np.poly(poles))
        frequencies, response = signal.freqz(system.num, system.den)

        magnitude_plot = self.ui.grph_mag_response.plot(frequencies, 20 * np.log10(np.abs(response)))
        magnitude_plot.setPen('b')

        phase_plot = self.ui.grph_phase_response.plot(frequencies, np.angle(response, deg=True))
        phase_plot.setPen('r')
        
    def all_pass_zero_poles_plot(self , zeros , poles):
        self.clear_all()
        for zero in zeros:
            self.zeros.append(DraggablePoint(self.c.axes,self ,  zero.x, zero.y ,'o' ))
        for pole in poles:
            self.poles.append(DraggablePoint(self.c.axes,self ,  pole.x, pole.y ,'x' ))

    def play_animation(self):
        self.ui.grph_2.clear()
        self.ui.grph_1.clear()
        print("animation playing")
        self.animation_timer.timeout.connect(lambda:self.update_plot_with_time(self.data_y))
        self.data_line = self.ui.grph_1.plotItem.plot( pen="r")
        self.data_line_filter = self.ui.grph_2.plotItem.plot(pen = 'r')
        self.animation_timer.start(30)
        # self.is_animation_running = True
        self.current_index = 0
        self.create_filter_from_z_p()
        
    def update_plot_with_time(self , data):
        # self.animation_speed = 1
        
        self.data_line.setData(self.data_x[0:self.current_index] , self.data_y[0:self.current_index])
        self.data_line_filter.setData(self.data_x[0:self.current_index] , self.filtered_signal[0:self.current_index])
        self.ui.grph_1.autoRange()
        self.ui.grph_1.autoRange()
       
        if self.current_index >= len(data)-1:
            self.is_signal_ended = True
            
        
        self.current_index += self.animation_speed # Convert the speed value to integer
        # QApplication.processEvents()
            
    def open_file(self):
        file_path  , _ = QFileDialog.getOpenFileName( self , "open file", "" ,"(*.csv) ")
        # df = pd.read_csv(file_path)
        df = np.genfromtxt(file_path, delimiter = ',')
        self.data_x = df[:, 0].tolist()
        self.data_y = df[:, 1].tolist()
        self.ui.grph_1.clear()
        self.ui.grph_2.clear()
        self.ui.grph_1.plot(self.data_x[0:self.current_index],  self.data_y[0:self.current_index])

        self.play_animation()
    
    # def signal_gen_via_mouse(self):
    #     self.signal_gen = self.ui.padding_area.mouseMoveEvent()
        
def main():
    app = QApplication(sys.argv)
    window = MyWindow() 
   
   
    window.showMaximized()
    window.show()
    
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()