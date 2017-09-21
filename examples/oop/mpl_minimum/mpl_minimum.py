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
))
from widgets.mplwidget import QtMplWidget   # noqa: E402


class Application(QApplication):

    def __init__(self, argv):
        # call the parent (QApplication) constructor
        super().__init__(argv)
        # create the main window
        self.window = QMainWindow()
        # create a matplotlib widget and set the window as its parent
        self.mpl = QtMplWidget(self.window)
        # add our label to the central widget of the window
        self.window.setCentralWidget(self.mpl)
        # add a simple line (y = x^2) to the plot
        xdata = list(range(1, 100 + 1))
        ydata = [x ** 2 for x in xdata]
        self.mpl.axes.plot(xdata, ydata)
        # display the main window
        self.window.show()


def main():
    # create the application
    app = Application(sys.argv)
    # start the Qt main loop execution
    sys.exit(app.exec_())


if __name__ == '__main__':
    # execute the main function
    main()
