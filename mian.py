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
 
class MyWindow(QMainWindow):   
    
    def __init__(self ):
        super(MyWindow , self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  
        
        
        self.c = MplCanvas(self)
        
        self.zeros = []
        self.poles = []
        self.zeros_conj = []
        self.poles_conj = []

        self.ui.checkBox_conj.stateChanged.connect(self.handle_checkbox_change)
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

        # self.

        self.animation_timer = QTimer()
        # self.animation_timer.timeout.connect(self.update_plot_with_time)
        
        self.c.mpl_connect('button_press_event', self.on_double_click)
        
    def plot_signal(self  , data) :
        # p = 0
        # for signal in self.signals_1:
        data_line = self.ui.grph_1.plotItem.plot()
        # signal["data_lines"].append(data_line)
        # signal["data_indices"].append(0)
            # p += 20                 
        # legend_1 = pg.LegendItem((10, 10), offset=(40 ,  p ))
        # legend_1.setParentItem(self.ui.graphicsView.getPlotItem())
        # legend_1.addItem(data_line, signal["name"])
        # self.legend_1.append(legend_1)
        
        
        # self.fun()
        
        self.ui.grph_1.plotItem.getViewBox().setAutoPan(x=True,y=True)
        self.timer_1.timeout.connect(lambda:self.update_plot_data_grph_1(self.signals_1))
        self.timer_1.start()
        # max_y , min_y = self.find_max_min_y_grph_1()
        # self.ui.grph_1.plotItem.vb.setLimits(xMin=0, xMax=max(signal["x"]), yMin=min_y-.5, yMax=max_y+.5)
        # self.ui.grph_1.setXRange(0 , 0.002*len(signal["data"]))
        # self.ui.grph_1.addLegend(offset=(50, 30))
        
        # self.update_legends_1()
        # legends = self.ui.grph_1.plotItem.legend.items
        # print(legends)
        
        # icon = QtGui.QPixmap("pause.png")
        # self.ui.btn_play_pasuse_viewer_1.setIcon(QtGui.QIcon(icon))
        # self.ui.grph_1.plotItem.addLegend()
        
        self.ui.grph_1.show()
        
    def update_plot_data_grph_1(self,signals):
        for signal in signals:
            for i in range(len(signal["data_lines"])):
                x = signal["x"][:signal["data_indices"][i]]
                y = signal["y"][:signal["data_indices"][i]]
                signal["data_indices"][i] += 5 
                signal["data_lines"][i].setData(x, y)
                
    def combo_switch(self , index):
        self.ui.combx_zero_pole.setCurrentIndex(index)
    
    def check_switch(self ):
        if self.ui.checkBox_conj.isChecked():
            self.ui.checkBox_conj.setChecked(False)
        else:
            self.ui.checkBox_conj.setChecked(True)
        
    def handle_checkbox_change(self, state):
        pass
        # if state == 2:  # Checked
        #     self.add_conj()
        # else:
        #     self.remove_all_cong()

    # def add_conj(self ):
    #     self.remove_all_cong()
    #     for zero in self.zeros :
    #             zero.create_conjgate()
    #             self.zeros_conj.append(zero.conj)
    #     for pole in self.poles:
    #             pole.create_conjgate()
    #             self.poles_conj.append(pole.conj)
    #     self.response_plot()  

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
        zeros = self.convert_to_complex(self.zeros , self.zeros_conj)
        poles = self.convert_to_complex(self.poles , self.poles_conj)
        return zeros , poles
    
    def response_plot(self):
        self.clear_mag_phase_grph()
        zeros , poles = self.get_zeros_poles()
        print("here")
        print(zeros)
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
        # self.orignal_data  = np.linspace(0 , 1000 , 1)
        # if self.is_signal_ended:
        #     print("Signal Ended")
        #     self.current_index = 0
        #     self.reset_viewport_range()
        #     self.is_signal_ended = False
        print("animation playing")
        self.animation_timer.timeout.connect(lambda:self.update_plot_with_time(self.data_y))
        # self.animation_timer.timeout.connect(lambda:self.update_plot_with_time(self.orignal_data))
        self.data_line = self.ui.grph_1.plotItem.plot( pen="r")
        self.animation_timer.start(30)
        self.is_animation_running = True
        # self.set_play_button_state()
        
    def update_plot_with_time(self , data):
        self.animation_speed = 1
        # x_min , x_max = self.ui.grph_1.viewRange()[0]
        # self.ui.grph_1.plot(self.data_x[0:self.current_index] , self.data_y[0:self.current_index] , pen = 'r')
        self.data_line.setData(self.data_x[0:self.current_index] , self.data_y[0:self.current_index])
        self.ui.grph_1.autoRange()
        # self.ui.grph_2.setData(self.data_modified[0:self.current_index])

        # if self.current_index > x_max:   
        #     for viewport in [self.ui.grph_1, self.ui.grph_2]:
        #         viewport.setLimits(xMax = self.current_index)
        #         viewport.getViewBox().translateBy(x = self.animation_speed)
       
        if self.current_index >= len(data)-1:
            # self.stop_animation()
            self.is_signal_ended = True
        
        self.current_index += self.animation_speed # Convert the speed value to integer
        # QApplication.processEvents()
            
    def open_file(self):
        file_path  , _ = QFileDialog.getOpenFileName( self , "open file", "" ,"(*.csv) ")
        # df = pd.read_csv(file_path)
        df = np.genfromtxt(file_path, delimiter = ',')
        self.data_x = df[:, 0].tolist()
        self.data_y = df[:, 1].tolist()
        self.ui.grph_1.plot(self.data_x[0:self.current_index],  self.data_y[0:self.current_index])
        self.play_animation()
        
        
def main():
    app = QApplication(sys.argv)
    window = MyWindow() 
   
   
    window.showMaximized()
    window.show()
    
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()