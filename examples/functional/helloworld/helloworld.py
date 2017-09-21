#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from qtpy.QtWidgets import QApplication, QMainWindow, QLabel
from qtpy import QtCore


def main():
    # create the application
    app = QApplication(sys.argv)
    # create the main window
    window = QMainWindow()
    # create a label to hold our text
    label = QLabel(text="hello world!", )
    # set the label to align in the center
    label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    # add our label to the central widget of the window
    window.setCentralWidget(label)
    # display the main window
    window.show()
    # start the Qt main loop execution
    sys.exit(app.exec_())


if __name__ == '__main__':
    # execute the main function
    main()
