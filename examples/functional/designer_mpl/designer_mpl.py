#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import modules
import sys
import os
from qtpy.QtWidgets import QApplication, QMainWindow
from qtpy.QtCore import QObject, Slot, Signal
from qtpy import uic
import math


# allthough this is a functianal (not oop) example, there is no way to use Qt
# Signals without an object derived from QObject
class UpdateSignal(QObject):
    updated = Signal()


# define some file scoped/global variables ####################################
sinewave_amplitude = 1
sinewave_frequency = 1
mpl = None
sinewave_settings_signal = UpdateSignal()


# define Qt Slots #############################################################

@Slot(float)
def set_sinewave_amplitude(amplitude):
    # obtain access to the global amplitude (since we are changing it)
    global sinewave_amplitude
    print("Update sinewave amplitude: {}".format(amplitude))
    # update the (global) value of sinewave amplitude
    sinewave_amplitude = amplitude
    # fire the sinewave settings updated signal
    sinewave_settings_signal.updated.emit()


@Slot(float)
def set_sinewave_frequency(frequency):
    # obtain access to the global frequency (since we are changing it)
    global sinewave_frequency
    print("Update sinewave frequency: {}".format(frequency))
    # update the (global) value of sinewave frequency
    sinewave_frequency = frequency
    # fire the sinewave settings updated signal
    sinewave_settings_signal.updated.emit()


@Slot()
def plot_sinewave():
    print("Plot sinewave: y = {} sin(2*pi*{}*t)".format(
        sinewave_amplitude,
        sinewave_frequency
    ))
    mpl.removeLines()
    xdata = [x / 1000.0 for x in list(range(0, 10000 + 1))]
    ydata = [
        sinewave_amplitude * math.sin(
            2 * math.pi * sinewave_frequency * t
        ) for t in xdata
    ]
    mpl.axes.plot(xdata, ydata, color="#1f77b4")
    mpl.canvas.draw()


# define helper functions #####################################################

def setup_ui(window):
    """Setup the userinterface.
    """
    # obtain access to the global mpl (since we are changing it)
    global mpl
    # build UI pfile path
    ui_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "mainwindow.ui"
    )
    # load the UI
    uic.loadUi(ui_file_path, window)
    # set a window title
    window.setWindowTitle("Qt Designer Matplotlib example")
    # set values to amplitude and frequency spinboxes
    window.sineAmplitudeSpinBox.setValue(sinewave_amplitude)
    window.sineFrequencySpinBox.setValue(sinewave_frequency)
    # setup matplotlib
    window.mpl.axes.grid()
    window.mpl.fig.set_tight_layout(True)
    # bind window matplotlib object to global mpl
    mpl = window.mpl


def connect_signals_to_slots(window):
    """Connect Qt Signals to Qt Slots
    """
    # connect amplitude spinbox changed to set amplitude
    window.sineAmplitudeSpinBox.valueChanged.connect(
        set_sinewave_amplitude
    )
    # connect frequency spinbox changed to set frequency
    window.sineFrequencySpinBox.valueChanged.connect(
        set_sinewave_frequency
    )
    # connect the plot sinewave button to plot sinwave method
    window.plotSineButton.clicked.connect(
        plot_sinewave
    )
    # connect the clear sinewave plot button to remove lines
    window.clearSineButton.clicked.connect(
        window.mpl.removeLines
    )
    # connect the sinewave settings updated signal to plot sinewave method
    sinewave_settings_signal.updated.connect(
        plot_sinewave
    )


def main():
    # create the application
    app = QApplication(sys.argv)
    # create the main window
    window = QMainWindow()
    # setup the UI
    setup_ui(window)
    # wire signals to slots
    connect_signals_to_slots(window)
    # show the window
    window.show()
    # start the Qt main loop execution
    sys.exit(app.exec_())


if __name__ == '__main__':
    # execute the main function
    main()
