from scipy import signal

from PyQt5.QtCore import Qt

from matplotlib.patches import ConnectionPatch
from matplotlib.lines import Line2D

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PyQt5.QtWidgets import  QApplication, QMainWindow, QShortcut, QFileDialog , QSplitter , QFrame , QSlider , QMenu 
from scipy.signal import spectrogram
from scipy.signal import resample
import sys
from PyQt5.QtGui import QIcon, QKeySequence , QCursor
from mainwindow import Ui_MainWindow  
from pyqtgraph import PlotWidget, ROI

import numpy as np
import pandas as pd
from scipy.io import wavfile
import pyqtgraph as pg
from scipy.fftpack import rfft, rfftfreq, irfft , fft , fftfreq
from PyQt5.QtCore import pyqtSlot
import sounddevice as sd
import librosa
from pyqtgraph import PlotWidget, PlotDataItem


# class DraggableCircle(patches.Circle):
#     def __init__(self, canvas, xy, radius=0.1, **kwargs):
#         super().__init__(xy, radius, **kwargs)
#         self.canvas = canvas
#         self.press = None

#     def connect(self):
#         'connect to all the events we need'
#         self.cidpress = self.canvas.mpl_connect('button_press_event', self.on_press)
#         self.cidrelease = self.canvas.mpl_connect('button_release_event', self.on_release)
#         self.cidmotion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        

#     def on_press(self, event):
#         'on button press we will see if the mouse is over us and store some data'
#         if event.inaxes != self.axes:
#             return
#         contains, attrd = self.contains(event)
#         if not contains:
#             return
#         self.press = (self.center), event.xdata, event.ydata

#     def on_motion(self, event):
#         'on motion we will move the rect if the mouse is over us'
#         if self.press is None:
#             return
#         if event.inaxes != self.axes:
#             return
#         dx = event.xdata - self.press[1]
#         dy = event.ydata - self.press[2]
#         self.center = (self.press[0][0] + dx, self.press[0][1] + dy)
#         self.canvas.draw()
        
#         print(self.get_position())

#     def on_release(self, event):
#         'on release we reset the press data'
#         self.press = None
#         self.canvas.draw()

#     def get_position(self):
#         return self.center
    
    
# class DraggableX(Line2D):
#     def __init__(self, canvas, xy, size=0.1, **kwargs):
#         x, y = xy
#         xdata, ydata = canvas.axes.transData.transform((x, y))
#         xsize, ysize = canvas.axes.transData.transform((x + size, y + size))
#         super().__init__([xdata - size, xdata + size], [ydata - size, ydata + size], **kwargs)
#         self.canvas = canvas
#         self.press = None

#     def connect(self):
#         'connect to all the events we need'
#         self.cidpress = self.canvas.mpl_connect('button_press_event', self.on_press)
#         self.cidrelease = self.canvas.mpl_connect('button_release_event', self.on_release)
#         self.cidmotion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)

#     def on_press(self, event):
#         'on button press we will see if the mouse is over us and store some data'
#         if event.inaxes != self.axes:
#             return
#         contains, attrd = self.contains(event)
#         if not contains:
#             return
#         self.press = (self._x[0], self._y[0]), event.xdata, event.ydata

#     def on_motion(self, event):
#         'on motion we will move the rect if the mouse is over us'
#         if self.press is None:
#             return
#         if event.inaxes != self.axes:
#             return
#         dx = event.xdata - self.press[1]
#         dy = event.ydata - self.press[2]
#         self.set_xdata([self.press[0][0] + dx - 0.1, self.press[0][0] + dx + 0.1])
#         self.set_ydata([self.press[0][1] + dy - 0.1, self.press[0][1] + dy + 0.1])
#         self.canvas.draw()

#     def on_release(self, event):
#         'on release we reset the press data'
#         self.press = None
#         self.canvas.draw()

#     def get_position(self):
#         x_center = (self._x[0] + self._x[1]) / 2
#         y_center = (self._y[0] + self._y[1]) / 2
#         return x_center, y_center

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
        if event.inaxes == self.ax and event.button == 3:  # Check for right-click
            # self.parent.deleted = self
            contains, _ = self.point.contains(event)
            if contains:
                self.delete_point()
        self.parent.response_plot()
        
                
                
    # def on_press(self, event):
    #     if event.button == 3:  # Right mouse button
    #         self.show_context_menu(event)
    #     if event.inaxes == self.ax:
    #         # else:
    #         contains, _ = self.point.contains(event)
    #         if contains:
    #             self.press = self.point.get_data(), event.xdata, event.ydata


    def on_motion(self, event):
        if self.press is None:
            return
        if event.inaxes == self.ax:
            prev_data, xpress, ypress = self.press
            dx = event.xdata - xpress
            dy = event.ydata - ypress
            self.x , self.y = (prev_data[0] + dx, prev_data[1] + dy)

            self.point.set_data(self.x , self.y)
            self.point.figure.canvas.draw()
            # self.print_position((self.x , self.y))
            if self.conj != None:
                self.conj.x, self.conj.y = self.x, -self.y
                self.conj.point.set_data(self.conj.x, self.conj.y)
                self.conj.point.figure.canvas.draw()
        self.parent.response_plot()
            # if self.orig != None:
            #     self.orig.x, self.orig.y = self.x, -self.y
            #     self.orig.point.set_data(self.orig.x, self.orig.y)
            #     self.orig.point.figure.canvas.draw()

    def on_release(self, event):
        # if event.button != 3:  # Check for right-click
        # self.
        
        self.press = None
        self.parent.pls.figure.canvas.draw()

    def show_context_menu(self, event):
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec_(QCursor.pos())
        if action == delete_action:
            self.delete_point()

    def print_position(self, position):
        print(f"New Position: x={position[0]}, y={position[1]}")

    def draw_point(self, x, y):
        self.point.set_data(x, y)
        self.point.figure.canvas.draw()

    def delete_point(self):
        # self.point.figure.canvas.draw()
        # self.point.remove()
        # self.point.figure.canvas.draw_idle()  # Update the plot
        self.parent.on_right_click(self)

        # self.ax.lines.remove(self.point)

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=1, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        # self.draggable_point = DraggablePoint(self.axes, 0, 0 , 'x')


# class MplCanvas(FigureCanvasQTAgg):
    
#     def __init__(self, parent=None, width=5, height=1, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)
#         super(MplCanvas, self).__init__(fig)
    

 
class MyWindow(QMainWindow):   
    
    def __init__(self ):
        super(MyWindow , self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  
        
        
        self.c = MplCanvas(self)
        
        self.points = []
        self.zeros = []
        self.poles = []
        self.zeros_conj = []
        self.poles_conj = []

        # self.ui.checkBox.stateChanged.connect(lambda state: self.add_conj if state == 2 else self.remove_all_cong)
        self.ui.checkBox.stateChanged.connect(self.handle_checkbox_change)




        # self.ui.grph_zero_plot.plot(x, y, pen='b')
        self.pls = self.c.axes.add_patch(plt.Circle((0, 0), 1, color='b', fill=False))
        self.ui.horizontalLayout_2.addWidget(self.c)
        self.c.axes.set_xlim(-1.5, 1.5)
        self.c.axes.set_ylim(-1.5, 1.5)
        
        self.ui.btn_clr_zero.clicked.connect(self.clear_all_zeros)
        self.ui.btn_clr_pole.clicked.connect(self.clear_all_poles)
        self.ui.btn_clr_all.clicked.connect(self.clear_all)

        # self.draggable_point = DraggablePoint(self.c.axes, 0, 0 )
        # self.draggable_point_1 = DraggablePoint(self.c.axes, 1, 0 )
        # self.draggable_point_2 = DraggablePoint(self.c.axes, 2, 0 )
        # self.draggable_point_3 = DraggablePoint(self.c.axes, 3, 0 )
        # # self.draggable_point.delete_point()
        # self.draggable_point.delete_point()

        # zero = DraggableCircle(self.c, (0.5, 0.5), 0.05, color='r')
        # pole = DraggableX(self.c, (0.5, 0.5), size=0.05, color='g')
        # zero.connect()
        # pole.connect()
        # self.c.axes.add_patch(zero)
        # self.c.axes.add_line(pole)
        
        self.c.mpl_connect('button_press_event', self.on_double_click)
        # self.ui.btn_add_pole.clicked.connect(self.add_conj)
        # self.c.draw_idle
        # self.c.mpl_connect('button_release_event', self.on_right_click)
        
    # def on_right_click(self , event):
    def handle_checkbox_change(self, state):
        if state == 2:  # Checked
            self.add_conj()
        else:
            self.remove_all_cong()
    def add_conj(self ):
        for zero in self.zeros :
            # if zero.conj == None:
                zero.create_conjgate()
                self.zeros_conj.append(zero.conj)
        for pole in self.poles:
            # if pole.conj == None:
                pole.create_conjgate()
                self.poles_conj.append(pole.conj)
            
    def remove_all_cong(self):
        # pass
        for zero in self.zeros_conj :
            if zero != None:
                zero.point.remove()
        for pole in self.poles_conj:
            if pole != None:
                pole.point.remove()
        self.zeros_conj.clear()
        self.poles_conj.clear()
        self.pls.figure.canvas.draw()

        # for zero , pole in zip(self.zeros , self.poles):

        #     self.on_right_click(zero.conj)
        #     self.on_right_click(pole.conj)
        
        
    def on_right_click(self , point):
        point.point.remove()
        if self.ui.checkBox.isChecked():
            point.conj.point.remove()
            
        if point.marker == 'o':
            if point in self.zeros:
                self.zeros.remove(point)
                self.zeros_conj.remove(point.conj)
            elif point in self.zeros_conj:
                self.zeros_conj.remove(point)
                self.zeros.remove(point.conj)
        else:
            if point in self.poles:
                self.poles.remove(point)
                self.poles_conj.remove(point.conj)
            elif point in self.poles_conj:
                self.poles_conj.remove(point)
                self.poles.remove(point.conj)
            # point.point.remove()
            
        self.pls.figure.canvas.draw()
        
        # for zero in self.zeros:
        #     zero.point.figure.canvas.draw()

    def on_double_click(self, event):
        x, y = event.xdata, event.ydata
      
        if event.inaxes == self.c.axes and event.button == Qt.LeftButton and event.dblclick:
            if self.ui.comboBox.currentText() =="add zero":
                marker = 'o'
                self.zeros.append(DraggablePoint(self.c.axes,self ,  x, y ,marker ))
                    # self.zeros[-1].create_conjgate()
            else:
                marker = "x"
                self.poles.append(DraggablePoint(self.c.axes,self ,  x, y ,marker ))
            print("zeros")
            for zero in self.zeros:
                
                print(zero.x , zero.y)
            print("________")

            print("poles")
            for pole in self.poles:
                
                print(pole.x , pole.y)
            print("________")
            if self.ui.checkBox.isChecked():
                self.add_conj()
            # self.points.append((x , y))
            # print(self.points)
            self.response_plot()
    
    def clear_all_zeros(self):
        for zero in self.zeros:
            zero.point.remove()
            # self.zeros.remove(zero)
            
        if self.ui.checkBox.isChecked():
            for zero_conj in self.zeros_conj:
                zero_conj.point.remove()
                # self.zeros_conj.remove(zero_conj)
        self.zeros.clear()
        self.zeros_conj.clear()
        self.pls.figure.canvas.draw()
        self.clear_mag_phase_grph()
        
        
        
    def clear_all_poles(self):
        for pole in self.poles:
            pole.point.remove()
            
        if self.ui.checkBox.isChecked():
            for pole_conj in self.poles_conj:
                pole_conj.point.remove()
        self.poles.clear()
        self.poles_conj.clear()
        self.pls.figure.canvas.draw()
        self.clear_mag_phase_grph()
        
        
    def clear_all(self):
        self.clear_all_poles()
        self.clear_all_zeros()
        
    def convert_to_complex(self , points):
        numbers = [(point.x , point.y ) for point in points]
        return [complex(real, imag) for (real, imag) in numbers ]

    def clear_mag_phase_grph(self):
        self.ui.grph_mag_response.clear()
        self.ui.grph_phase_response.clear()

    def response_plot(self):
        self.clear_mag_phase_grph()
        zeros = self.convert_to_complex(self.zeros)
        poles = self.convert_to_complex(self.poles)
        system = signal.TransferFunction(np.poly(zeros), np.poly(poles))
        frequencies, response = signal.freqz(system.num, system.den)

        # Magnitude response
        magnitude_plot = self.ui.grph_mag_response.plot(frequencies, 20 * np.log10(np.abs(response)))
        magnitude_plot.setPen('b')

        # Phase response
        phase_plot = self.ui.grph_phase_response.plot(frequencies, np.angle(response, deg=True))
        phase_plot.setPen('r')
        
        # self.ui.grph_mag_response.plot()

        
        
    

def main():
    app = QApplication(sys.argv)
    window = MyWindow() 
   
   
    window.showMaximized()
    window.show()
    
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()