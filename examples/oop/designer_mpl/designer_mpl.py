#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import modules
import sys
import os

from qtpy.QtWidgets import QApplication, QMainWindow
from qtpy.QtCore import QObject, Slot, Signal
from qtpy import uic
import math


class Application(QApplication):

    def __init__(self, argv):
        super().__init__(argv)
        self.window = MainWindow()
        self.window.show()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # create object to hold our sinewave settings
        self.sinewave_settings = SineWaveSettings()
        # wire up the userinterface
        self._setup_ui()
        # wire up the signals and slots
        self._connect_slots_signals()

    def _setup_ui(self):
        # build UI pfile path
        ui_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "mainwindow.ui"
        )
        # load the UI
        uic.loadUi(ui_file_path, self)
        # set a window title
        self.setWindowTitle("Qt Designer Matplotlib example")
        # set values to amplitude and frequency spinboxes
        self.sineAmplitudeSpinBox.setValue(self.sinewave_settings.amplitude)
        self.sineFrequencySpinBox.setValue(self.sinewave_settings.frequency)
        # setup matplotlib
        self.mpl.axes.grid()
        self.mpl.fig.set_tight_layout(True)

    def _connect_slots_signals(self):
        # connect amplitude spinbox changed to set amplitude
        self.sineAmplitudeSpinBox.valueChanged.connect(
            self.sinewave_settings.setAmplitude
        )
        # connect frequency spinbox changed to set frequency
        self.sineFrequencySpinBox.valueChanged.connect(
            self.sinewave_settings.setFrequency
        )
        # connect the plot sinewave button to plot sinwave method
        self.plotSineButton.clicked.connect(
            self.plot_sinewave
        )
        # connect the clear sinewave plot button to remove lines
        self.clearSineButton.clicked.connect(
            self.mpl.removeLines
        )
        # connect the sinewave settings updated signal to plot sinewave method
        self.sinewave_settings.settingsUpdated.connect(
            self.plot_sinewave
        )

    @Slot()
    def plot_sinewave(self):
        print("Plot sinewave: y = {} sin(2*pi*{}*t)".format(
            self.sinewave_settings.amplitude,
            self.sinewave_settings.frequency
        ))
        self.mpl.removeLines()
        xdata = [x / 1000.0 for x in list(range(0, 10000 + 1))]
        ydata = [
            self.sinewave_settings.amplitude * math.sin(
                2 * math.pi * self.sinewave_settings.frequency * t
            ) for t in xdata
        ]
        self.mpl.axes.plot(xdata, ydata, color="#1f77b4")
        self.mpl.canvas.draw()


class SineWaveSettings(QObject):

    settingsUpdated = Signal()

    def __init__(self, amplitude=1, frequency=1):
        super().__init__()
        self.amplitude = amplitude
        self.frequency = frequency

    @Slot(float)
    def setAmplitude(self, amplitude):
        print("Update sinewave amplitude: {}".format(amplitude))
        self.amplitude = amplitude
        self.settingsUpdated.emit()

    @Slot(float)
    def setFrequency(self, frequency):
        print("Update sinewave frequency: {}".format(frequency))
        self.frequency = frequency
        self.settingsUpdated.emit()


def main():
    # create the application
    app = Application(sys.argv)
    # start the Qt main loop execution
    sys.exit(app.exec_())


if __name__ == '__main__':
    # execute the main function
    main()
