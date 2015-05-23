"""
RawMyo.py

jdaly
5/20/2015

Raw Myo data acquisition and display
"""

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg 

import myo as libmyo #; libmyo.init()
from myo_listener import Listener

import numpy as np

import sys, time

#class RawWindow(QtGui.QWidget):
class RawWindow(QtGui.QMainWindow):
    def __init__(self):
        super(RawWindow, self).__init__()
        self.setWindowTitle('Myo Data Acquirer')
        self.resize(800,480)
        cw = QtGui.QWidget()
        self.setCentralWidget(cw)
        l = QtGui.QGridLayout()
        cw.setLayout(l)
        
        titleLabel = QtGui.QLabel('Myo Data Acquirer')       
        l.addWidget(titleLabel, 0, 0, 2, 1)

        self.emgplot = pg.PlotWidget(name='EMGplot')
        self.emgplot.setRange(QtCore.QRectF(-50,-200,1000,1400))
        self.emgplot.disableAutoRange()
        l.addWidget(self.emgplot, 0, 1, 1, 2)

        self.accplot = pg.PlotWidget(name='ACCplot')
        #self.accplot.setRange(QtCore.QRectF(0,-2,1000,2))
        l.addWidget(self.accplot, 1, 1, 1, 1)

        self.oriplot = pg.PlotWidget(name='ORIplot')
        #self.oriplot.setRange(QtCore.QRectF(0,0,1,1))
        l.addWidget(self.oriplot, 1,2,1,1)

        self.refreshRate = 0.05
        
        self.emgcurve = []
        for i in range(8):
            c = self.emgplot.plot(pen=(i,10))
            c.setPos(0,i*150)
            self.emgcurve.append(c)

        self.oricurve = []
        for i in range(4):
            c = self.oriplot.plot(pen=(i,5))
            c.setPos(0,i*2)
            self.oricurve.append(c)

        self.acccurve = []
        for i in range(4):
            c = self.accplot.plot(pen=(i,5))
            c.setPos(0,i*2)
            self.acccurve.append(c)
        
        self.lastUpdateTime = time.time()
        self.show()
        self.start_listening()

    def start_listening(self):
        self.listener = Listener(self)
        self.hub = libmyo.Hub()
        self.hub.set_locking_policy(libmyo.LockingPolicy.none)
        self.hub.run(1000, self.listener)

    def update_plots(self):
        ctime = time.time()
        if (ctime - self.lastUpdateTime) >= self.refreshRate:
            for i in range(8):
                self.emgcurve[i].setData(self.listener.emg.data[i,:])
            for i in range(4):
                self.oricurve[i].setData(self.listener.orientation.data[i,:])
            for i in range(3):
                self.acccurve[i].setData(self.listener.acc.data[i,:])
            self.lastUpdateTime = ctime

            app.processEvents()

    def closeEvent(self, event):
        print "Closing..."
        self.hub.shutdown()	



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = RawWindow()
    sys.exit(app.exec_())