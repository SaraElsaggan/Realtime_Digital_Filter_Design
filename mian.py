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
        self.zeros_allpass = []
        self.poles_allpass = []
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

        self.animation_timer = QTimer()
        
        self.c.mpl_connect('button_press_event', self.on_double_click)

        self.all_pass_coff = ['1' , '-1' , '.45' , '.345' , '-.9' , '0']
        self.checked_coeff = []
        self.ui.tbl_allpass_list.setColumnCount(1)  # Set column count to 1 for a single column
        # self.ui.tbl_allpass_list.setRowCount(7) 
        self.ui.tbl_allpass_list.verticalHeader().setVisible(False)

        # Hide column headers
        self.ui.tbl_allpass_list.horizontalHeader().setVisible(False)
        self.ui.tbl_allpass_list.setShowGrid(False)


        for coff in self.all_pass_coff:
            row_position = self.ui.tbl_allpass_list.rowCount()
            self.ui.tbl_allpass_list.insertRow(row_position)
            item = QTableWidgetItem(coff)
            item.setFlags(item.flags() | 2)  # Enable ItemIsUserCheckable
            item.setCheckState(0)  # Set default state to unchecked
            self.ui.tbl_allpass_list.setItem(row_position, 0, item)


        self.ui.tbl_allpass_list.setColumnWidth(0, 50000)

        last_row_index = self.ui.tbl_allpass_list.rowCount() - 1

        # Set the text in the last cell of the last row
        self.ui.tbl_allpass_list.setItem(last_row_index, self.ui.tbl_allpass_list.columnCount() - 1, QTableWidgetItem("-------------------------------------Your custom_built all pass-------------------------------------"))
        self.ui.tbl_allpass_list.itemChanged.connect(self.allpass_response)

        
            
            
        # self.ui.tbl_allpass_list.setColumnCount(1)  # Set column count to 1 for a single column
        # self.ui.tbl_allpass_list.setRowCount(1) 
        # item =  QTableWidgetItem('Item')
        # item.setFlags(item.flags() | 2)  # Enable ItemIsUserCheckable
        # item.setCheckState(1)  # Set default state to unchecked
        # self.ui.tbl_allpass_list.setItem(0, 0, item)

        self.animation_speed = 1

        self.x_positions = []
        self.y_positions = []
        self.counter = 1
        self.gen_data = []
        self.data_y = None
        self.data_x = None
        
        self.ui.slider_process_speed.valueChanged.connect(self.handle_slider_speed)

        self.ui.btn_add_coeff.clicked.connect(self.add_coustom_coff)
        # self.ui.tbl_allpass_list.it

    # def calc_allpass_zeros_poles(self):
    #     coffs = [] /
    #     for 
    def add_coustom_coff(self):
        real = self.ui.input_real.value()
        img = self.ui.input_imag.value()
        coff = f"{real}+{img}j"
        row_position = self.ui.tbl_allpass_list.rowCount()
        self.ui.tbl_allpass_list.insertRow(row_position)
        item = QTableWidgetItem(coff)
        item.setFlags(item.flags() | 2)  # Enable ItemIsUserCheckable
        item.setCheckState(0)  # Set default state to unchecked
        self.ui.tbl_allpass_list.setItem(row_position, 0, item)
        # coff = complex(coff)
        
        
        
    def handle_slider_speed(self):
          self.animation_speed = int(self.ui.slider_process_speed.value())
          
    def handle_gen_checkbox(self):
        if  self.ui.checkBox.isChecked():
            self.animation_timer.stop()
            self.data_x = 0
            self.data_y = []
            self.ui.grph_input_sig.clear()     
            self.ui.grph_output_sig.clear()     
            
    def genrate_signal_with_mouse(self , event):
        if self.ui.checkBox.isChecked():
            x = event.x()
            y = event.y()
            self.x_positions.append(x)
            self.y_positions.append(y)
            self.ui.grph_input_sig.clear()
            self.counter += 1
            self.gen_data.append(self.counter)
            self.data_y = self.x_positions
            self.ui.grph_input_sig.plot( self.x_positions)
            self.ui.grph_input_sig.autoRange()
            print(self.x_positions)
            # self.
            self.create_filter_from_z_p()
            self.ui.grph_output_sig.clear()

            self.ui.grph_output_sig.plot(self.gen_data , self.filtered_signal)
            self.ui.grph_output_sig.autoRange()

        print("_____")
    
    def create_filter_from_z_p(self ):
        # self.ui.grph_output_sig.clear()
        zeros , poles = self.get_zeros_poles()
        allpass_zeros , allpass_poles = self.allpass_z_p()
        a, b = signal.zpk2tf(zeros+allpass_zeros, poles+allpass_poles, 1)
        self.filtered_signal = np.real(signal.lfilter(a, b, self.data_y))
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
        
    # def all_pass_zero_poles_plot(self , zeros , poles):
    #     self.clear_all()
    #     for zero in zeros:
    #         self.zeros.append(DraggablePoint(self.c.axes,self ,  zero.x, zero.y ,'o' ))
    #     for pole in poles:
    #         self.poles.append(DraggablePoint(self.c.axes,self ,  pole.x, pole.y ,'x' ))

    def play_animation(self):
        self.ui.grph_output_sig.clear()
        self.ui.grph_input_sig.clear()
        print("animation playing")
        self.animation_timer.timeout.connect(lambda:self.update_plot_with_time(self.data_y))
        self.data_line = self.ui.grph_input_sig.plotItem.plot( pen="r")
        self.data_line_filter = self.ui.grph_output_sig.plotItem.plot(pen = 'r')
        self.animation_timer.start(30)
        # self.is_animation_running = True
        self.current_index = 0
        # self.create_filter_from_z_p()
        self.filtered_signal_new = []
        z = self.apply_filter()
    
    def apply_filter(self ):
        zeros , poles = self.get_zeros_poles()
        allpass_zeros , allpass_poles = self.allpass_z_p()
        a, b = signal.zpk2tf(zeros+allpass_zeros, poles+allpass_poles, 1)
        self.filtered_signal = np.real(signal.lfilter(a, b, self.data_y))
        # return np.real(signal.lfilter(a, b, points))
    
    def update_plot_with_time(self , data):
        # self.animation_speed = 1
        
        # self.data_line.setData(self.data_x[0:self.current_index] , self.data_y[0:self.current_index])
        # self.data_line_filter.setData(self.data_x[0:self.current_index] , self.filtered_signal[0:self.current_index])
        # self.ui.grph_output_sig.plot( self.filtered_signal[0:self.current_index])
        self.ui.grph_input_sig.plot( self.data_y[0:self.current_index])
        # self.create_filter_from_z_p()
        # filtered = self.apply_filter(self.data_y[self.current_index :self.current_index+5])
        # self.filtered_signal_new.extend(filtered)
        self.ui.grph_output_sig.plot( self.filtered_signal[0:self.current_index])
        # self.ui.grph_output_sig.plot( self.filtered_signal_new)
        # self.ui.grph_input_sig.autoRange()
        # self.ui.grph_output_sig.autoRange()
       
        if self.current_index >= len(data)-1:
            self.is_signal_ended = True
            
        
        self.current_index += 5 # Convert the speed value to integer
        # self.current_index += self.animation_speed # Convert the speed value to integer
        # QApplication.processEvents()
            
    def open_file(self):
        file_path  , _ = QFileDialog.getOpenFileName( self , "open file", "" ,"(*.csv) ")
        # df = pd.read_csv(file_path)
        df = np.genfromtxt(file_path, delimiter = ',')
        self.data_x = df[:, 0].tolist()
        self.data_y = df[:, 1].tolist()
        self.ui.grph_input_sig.clear()
        self.ui.grph_output_sig.clear()
        # self.ui.grph_input_sig.plot(self.data_x[0:self.current_index],  self.data_y[0:self.current_index])

        self.play_animation()
    
    def allpass_z_p(self ):
        zeros=[]
        poles=[]
        checked_coeff = self.get_coffs()
        for a in checked_coeff:
            a = complex(a)
            # a.real = np.abs(a.real)
            # x = np.abs(a)
            if a ==1:
                continue
            poles.append(a)
            zero=(1/np.abs(a))*np.exp(1j*np.angle(a))
            # zero = a.conjugate()
            # zero = complex(np.real(a)-np.imag(a))
            zeros.append(complex(zero))
        return zeros, poles
        
        
        # zeros=[]
        # poles=[]
        # checked_coeff = self.get_coffs()
        # w, all_pass_phs = 0, 0

        # for a in checked_coeff:
        #     if a ==1:
        #         a= 0.99999999
        #     a = complex(a, 0)
            
            
        #     # Check if denominator is not zero before performing division
        #     if np.abs(a.real) > 0:
        #         a_conj = 1 / np.conj(a)

        #         w, h = signal.freqz([-np.conj(a), 1.0], [1.0, -a])
        #         all_pass_phs = np.add(np.angle(h), all_pass_phs)
                
        #         # Add points to lists
        #         poles.append(complex(a.real+ a.imag))
        #         zeros.append(complex(a_conj.real+ a_conj.imag))
        # return zeros , poles
        #         # self.all_pass_poles.append(pg.Point(a.real, a.imag))
                # self.all_pass_zeros.append(pg.Point(a_conj.real, a_conj.imag))
                
        
        
        
        
        
    
    def allpass_response(self):
        self.plot_allpass_zeros_poles()
        zeros , poles = self.allpass_z_p()
      
        system = signal.TransferFunction(np.poly(zeros), np.poly(poles))
        frequencies, response = signal.freqz(system.num, system.den)
        self.ui.grph_4.clear()
        phase_plot = self.ui.grph_4.plot(frequencies, np.angle(response, deg=True))
        phase_plot.setPen('r')
        
    def plot_allpass_zeros_poles(self):
        zeros , poles = self.allpass_z_p()
        for point in self.zeros_allpass:
            if point  != None:
                point.point.remove()
        for point in self.poles_allpass:
            if point  != None:
                point.point.remove()
        self.zeros_allpass.clear()
        self.poles_allpass.clear()
        # self.zeros_allpass.append(DraggablePoint(self.c.axes, self, 0 , 0 , 'o').on_release())
        for zero in zeros:
            self.zeros_allpass.append(DraggablePoint(self.c.axes, self, np.real(zero) , np.imag(zero) , 'o'))
        for pole in poles:
            self.poles_allpass.append(DraggablePoint(self.c.axes, self, np.imag(pole) , np.real(pole) , 'x'))
        # self.zeros_allpass[0].on_release()
        self.circle.figure.canvas.draw()

    
    def get_coffs(self):
        checked_coeff=[]
        for row in range(self.ui.tbl_allpass_list.rowCount()):
            if row == 5:
                continue
            item = self.ui.tbl_allpass_list.item(row, 0)  # Get item in the first column of the current row
            coff = complex(item.text())
            if item.checkState() == Qt.Checked:
                checked_coeff.append(coff)
            
        print(checked_coeff)
        return checked_coeff
        
            
            # if item is not None:
    
def main():
    app = QApplication(sys.argv)
    window = MyWindow() 
   
   
    window.showMaximized()
    window.show()
    
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()