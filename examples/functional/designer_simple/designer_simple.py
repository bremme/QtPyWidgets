#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import modules
import sys
import os
from qtpy.QtWidgets import QApplication, QMainWindow
from qtpy.QtCore import Slot
from qtpy import uic


# define some file scoped/global variables ####################################
textOutput = None
textInput = None

# define Qt Slots #############################################################


@Slot()
def button_one_clicked():
    textOutput.setText("Button 1 clicked")


@Slot()
def button_two_clicked():
    textOutput.setText("Button 2 clicked")


@Slot()
def button_clear_clicked():
    textOutput.clear()
    textInput.clear()


# define helper functions #####################################################

def setup_ui(window):
    """Setup the userinterface.
    """
    global textOutput, textInput
    # build UI pfile path
    ui_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "mainwindow.ui"
    )
    # load the UI
    uic.loadUi(ui_file_path, window)
    # set a window title
    window.setWindowTitle("Qt Designer Simple example")
    # bind window textOutput object to global textOutput
    textOutput = window.textOutput
    textInput = window.textInput


def connect_signals_to_slots(window):
    """Connect Qt Signals to Qt Slots
    """
    window.buttonOne.clicked.connect(button_one_clicked)
    window.buttonTwo.clicked.connect(button_two_clicked)
    window.clearButton.clicked.connect(button_clear_clicked)
    window.textInput.textChanged.connect(window.textOutput.setText)


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
