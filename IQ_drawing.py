# -*- coding: utf-8 -*-
"""
Copyright (C) 2016  Colin Ford

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys, math, signal
from PyQt4 import QtGui, QtCore

class IQ(QtGui.QWidget):
    
    def __init__(self):
        super(IQ, self).__init__()
        self.width = 170
        self.height = 280
        self.time = 0
        self.amplitude = 100        
        self.amplitude_i = self.amplitude
        self.amplitude_q = self.amplitude
        self.time_internal = 0.1
        self.frequency = 5
        self.frequency_q = 5
        self.phase = 0
        self.phase_q = 0
        self.initUI()
        
    def initUI(self):
        self.setGeometry(300, 300, self.height, self.width)
        self.setWindowTitle('Signals')
        self.show()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawIQ(qp)
        qp.end()
        
    def drawIQ(self, qp):      
        size = self.size()
        frequency = self.frequency / size.width()
        frequency_q = self.frequency_q / size.width()
        x = 0
        for i in range(int(size.width()/self.time_internal)):
            self.time += self.time_internal
            x = math.fmod(self.time, size.width())
            I = (self.amplitude_i * math.cos(((2*math.pi*frequency*x) + self.phase)))        
            Q = (self.amplitude_q * math.sin(((2*math.pi*frequency_q*x) + self.phase_q)))
            IQ = I + Q
            #print("I",I*I)
            #print("Q",Q*Q)
            #print(x, math.sqrt(I*I + Q*Q))
            I += size.height() / 2
            Q += size.height() / 2
            IQ += size.height() / 2
            qp.setPen(QtCore.Qt.blue)        # I - cosin
            qp.drawPoint(int(x), I)
            qp.setPen(QtCore.Qt.red)         # Q - sin
            qp.drawPoint(int(x), Q)     
            qp.setPen(QtCore.Qt.black)        # Added
            qp.drawPoint(int(x), IQ)     
            qp.setPen(QtCore.Qt.green)
            qp.drawPoint(int(x), size.height()/2)            
                
    def setIfreq(self,value):
        self.frequency = value
        self.repaint()              

    def setQfreq(self,value):
        self.frequency_q = value
        self.repaint()   
        
    def setIamp(self,value):
        self.amplitude_i = value
        self.repaint()              

    def setQamp(self,value):
        self.amplitude_q = value
        self.repaint()           

    def setIphase(self,value):
        self.phase = value
        self.repaint()              

    def setQphase(self,value):
        self.phase_q = value
        self.repaint()           

    def sampleInterval(self,value):
        self.time_internal = value
        self.repaint()   
      
                
class IQControl(QtGui.QWidget):
    
    def __init__(self, parent=None):
        super(IQControl, self).__init__(parent)
        self.signals = parent
        
        self.sample_lab = QtGui.QLabel("Sample Interval")
        self.sample = QtGui.QDoubleSpinBox()
        self.sample.setValue(0.1)
        self.sample.setRange(0.0,5.0)
        self.sample.setSingleStep(0.01)
        self.sample.valueChanged.connect(self.sample_change)        
        
        self.ifreq_lab = QtGui.QLabel("I Frequency")
        self.ifreq = QtGui.QSpinBox()
        self.ifreq.setValue(5)
        self.ifreq.setRange(0,500)
        self.ifreq.valueChanged.connect(self.ifreq_change)

        self.qfreq_lab = QtGui.QLabel("Q Frequency")
        self.qfreq = QtGui.QSpinBox()
        self.qfreq.setValue(5)
        self.qfreq.setRange(0,500)
        self.qfreq.valueChanged.connect(self.qfreq_change)

        self.iamp_lab = QtGui.QLabel("I Amplitude")
        self.iamp = QtGui.QSpinBox()
        self.iamp.setValue(100)
        self.iamp.setRange(0,1000)
        self.iamp.valueChanged.connect(self.iamp_change)

        self.qamp_lab = QtGui.QLabel("Q Amplitude")
        self.qamp = QtGui.QSpinBox()
        self.qamp.setValue(100)
        self.qamp.setRange(0,1000)
        self.qamp.valueChanged.connect(self.qamp_change)

        self.iphase_lab = QtGui.QLabel("I Phase")
        self.iphase = QtGui.QSpinBox()
        self.iphase.setValue(0)
        self.iphase.setRange(0,1000)
        self.iphase.valueChanged.connect(self.iphase_change)

        self.qphase_lab = QtGui.QLabel("Q Phase")
        self.qphase = QtGui.QSpinBox()
        self.qphase.setValue(0)
        self.qphase.setRange(0,1000)
        self.qphase.valueChanged.connect(self.qphase_change)

        layout = QtGui.QHBoxLayout()

        layout.addWidget(self.sample_lab)
        layout.addWidget(self.sample)        
        layout.addWidget(self.ifreq_lab)
        layout.addWidget(self.ifreq)
        layout.addWidget(self.qfreq_lab)
        layout.addWidget(self.qfreq)
        layout.addWidget(self.iamp_lab)
        layout.addWidget(self.iamp)
        layout.addWidget(self.qamp_lab)
        layout.addWidget(self.qamp)
        layout.addWidget(self.iphase_lab)
        layout.addWidget(self.iphase)
        layout.addWidget(self.qphase_lab)
        layout.addWidget(self.qphase)
        
        self.setLayout(layout)

    def sample_change(self,value):
        self.signals.sampleInterval(value)
        
    def ifreq_change(self,value):
        self.signals.setIfreq(value)

    def qfreq_change(self,value):
        self.signals.setQfreq(value)

    def iamp_change(self,value):
        self.signals.setIamp(value)

    def qamp_change(self,value):
        self.signals.setQamp(value)

    def iphase_change(self,value):
        self.signals.setIphase(value)

    def qphase_change(self,value):
        self.signals.setQphase(value)        

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    iq_signal = IQ()
    iq_control = IQControl(iq_signal)
    iq_control.show()
    app.exec_()

if __name__ == '__main__':
    main()
 
