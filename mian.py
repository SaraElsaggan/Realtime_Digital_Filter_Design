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
    def __init__(self, ax, x, y , marker):
        self.ax = ax
        self.point, = ax.plot(x, y, marker, markersize=7, color='r', markeredgewidth=1)
        self.cpid = self.point.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cmid = self.point.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.ceid = self.point.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.crid = self.point.figure.canvas.mpl_connect('button_release_event', self.on_right_click)

        self.press = None

    def on_press(self, event):
        if event.inaxes == self.ax:
            contains, _ = self.point.contains(event)
            if contains:
                self.press = self.point.get_data(), event.xdata, event.ydata

    def on_right_click(self, event):
        if event.inaxes == self.ax and event.button == 3:  # Check for right-click
            contains, _ = self.point.contains(event)
            if contains:
                self.delete_point()
                
                
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
            new_data = (prev_data[0] + dx, prev_data[1] + dy)
            self.point.set_data(new_data)
            self.point.figure.canvas.draw()
            self.print_position(new_data)

    def on_release(self, event):
        if event.button != 3:  # Check for right-click
        
            self.press = None
            self.point.figure.canvas.draw()

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
        self.point.figure.canvas.draw_idle()  # Update the plot
        self.point.remove()

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
        
        self.zeros = []
          
        # self.ui.grph_zero_plot.plot(x, y, pen='b')
        self.c.axes.add_patch(plt.Circle((0, 0), 1, color='b', fill=False))
        self.ui.horizontalLayout_2.addWidget(self.c)
        self.c.axes.set_xlim(-1.5, 1.5)
        self.c.axes.set_ylim(-1.5, 1.5)

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
        # self.c.mpl_connect('button_release_event', self.on_right_click)
        
    # def on_right_click(self):
        
        

    def on_double_click(self, event):
        if event.inaxes == self.c.axes and event.button == Qt.LeftButton and event.dblclick:
            if self.ui.comboBox.currentText() =="zero":
                marker = 'o'
            else:
                marker = "x"
            x, y = event.xdata, event.ydata
            self.zeros.append(DraggablePoint(self.c.axes, x, y ,marker ))
            print(self.zeros)
    
        
    def response_plot(self):
        system = signal.TransferFunction(np.poly(self.zeros), np.poly(self.poles))
        frequencies, response = signal.freqz(system.num, system.den)

        # Magnitude response
        magnitude_plot = self.ui.grph_mag_response.plot(frequencies, 20 * np.log10(np.abs(response)))
        magnitude_plot.setPen('b')

        # Phase response
        phase_plot = self.ui.grph_phase_response.plot(frequencies, np.angle(response, deg=True))
        phase_plot.setPen('r')

        
        
    

def main():
    app = QApplication(sys.argv)
    window = MyWindow() 
   
   
    window.showMaximized()
    window.show()
    
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()