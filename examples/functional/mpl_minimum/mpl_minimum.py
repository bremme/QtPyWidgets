#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import modules
import sys
import os
from qtpy.QtWidgets import QApplication, QMainWindow
# at root qtpy examples folder to path
sys.path.append(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        os.path.pardir, os.path.pardir
    )
)
from widgets.mplwidget import QtMplWidget   # noqa: E402


def main():
    # create the application
    app = QApplication(sys.argv)
    # create the main window
    window = QMainWindow()
    # create a matplotlib widget and set the window as its parent
    mpl = QtMplWidget(window)
    # set the plot as the central widget of the window
    window.setCentralWidget(mpl)
    # add a simple line (y = x^2) to the plot
    xdata = list(range(1, 100 + 1))
    ydata = [x ** 2 for x in xdata]
    mpl.axes.plot(xdata, ydata)
    # display the main window
    window.show()
    # start the Qt main loop execution
    sys.exit(app.exec_())


if __name__ == '__main__':
    # execute the main function
    main()
