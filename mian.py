from matplotlib.patches import ConnectionPatch
from matplotlib.lines import Line2D

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PyQt5.QtWidgets import  QApplication, QMainWindow, QShortcut, QFileDialog , QSplitter , QFrame , QSlider
from scipy.signal import spectrogram
from scipy.signal import resample
import sys
from PyQt5.QtGui import QIcon, QKeySequence
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


class DraggableCircle(patches.Circle):
    def __init__(self, canvas, xy, radius=0.1, **kwargs):
        super().__init__(xy, radius, **kwargs)
        self.canvas = canvas
        self.press = None

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.axes:
            return
        contains, attrd = self.contains(event)
        if not contains:
            return
        self.press = (self.center), event.xdata, event.ydata

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None:
            return
        if event.inaxes != self.axes:
            return
        dx = event.xdata - self.press[1]
        dy = event.ydata - self.press[2]
        self.center = (self.press[0][0] + dx, self.press[0][1] + dy)
        self.canvas.draw()
        
        print(self.get_position())

    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.canvas.draw()

    def get_position(self):
        return self.center
    
    
class DraggableX(Line2D):
    def __init__(self, canvas, xy, size=0.1, **kwargs):
        x, y = xy
        xdata, ydata = canvas.axes.transData.transform((x, y))
        xsize, ysize = canvas.axes.transData.transform((x + size, y + size))
        super().__init__([xdata - size, xdata + size], [ydata - size, ydata + size], **kwargs)
        self.canvas = canvas
        self.press = None

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.axes:
            return
        contains, attrd = self.contains(event)
        if not contains:
            return
        self.press = (self._x[0], self._y[0]), event.xdata, event.ydata

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None:
            return
        if event.inaxes != self.axes:
            return
        dx = event.xdata - self.press[1]
        dy = event.ydata - self.press[2]
        self.set_xdata([self.press[0][0] + dx - 0.1, self.press[0][0] + dx + 0.1])
        self.set_ydata([self.press[0][1] + dy - 0.1, self.press[0][1] + dy + 0.1])
        self.canvas.draw()

    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.canvas.draw()

    def get_position(self):
        x_center = (self._x[0] + self._x[1]) / 2
        y_center = (self._y[0] + self._y[1]) / 2
        return x_center, y_center

class DraggablePoint:
    def __init__(self, ax, x, y):
        self.ax = ax
        self.point, = ax.plot(x, y, 'x', markersize=10, color='r', markeredgewidth=2)
        self.cpid = self.point.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cmid = self.point.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.ceid = self.point.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.press = None

    def on_press(self, event):
        if event.inaxes == self.ax:
            contains, _ = self.point.contains(event)
            if contains:
                self.press = self.point.get_data(), event.xdata, event.ydata

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
        self.press = None
        self.point.figure.canvas.draw()

    def print_position(self, position):
        print(f"New Position: x={position[0]}, y={position[1]}")

    def draw_point(self, x, y):
        self.point.set_data(x, y)
        self.point.figure.canvas.draw()

    def delete_point(self):
        self.point.remove()
        self.point.figure.canvas.draw()

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
        
        self.zeros = {}
          
        # self.ui.grph_zero_plot.plot(x, y, pen='b')
        self.c.axes.add_patch(plt.Circle((0, 0), 1, color='b', fill=False))
        self.ui.horizontalLayout_2.addWidget(self.c)
        self.c.axes.set_xlim(-1.5, 1.5)
        self.c.axes.set_ylim(-1.5, 1.5)

        self.draggable_point = DraggablePoint(self.c.axes, 0, 0 )

        # zero = DraggableCircle(self.c, (0.5, 0.5), 0.05, color='r')
        # pole = DraggableX(self.c, (0.5, 0.5), size=0.05, color='g')
        # zero.connect()
        # pole.connect()
        # self.c.axes.add_patch(zero)
        # self.c.axes.add_line(pole)
    

        
        
    

def main():
    app = QApplication(sys.argv)
    window = MyWindow() 
   
   
    window.showMaximized()
    window.show()
    
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()