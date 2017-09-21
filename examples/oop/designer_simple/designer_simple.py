#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import modules
import sys
import os
from qtpy.QtWidgets import QApplication, QMainWindow
from qtpy.QtCore import Slot
from qtpy import uic


class Application(QApplication):

    def __init__(self, argv):
        super().__init__(argv)
        # create the main window
        self.window = MainWindow()
        self.window.show()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # wire up the userinterface
        self._setup_ui()
        # wire up the signals and slots
        self._connect_signals_to_slots()

    def _setup_ui(self):
        """Setup the userinterface.
        """
        # build UI pfile path
        ui_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "mainwindow.ui"
        )
        # load the UI
        uic.loadUi(ui_file_path, self)
        # set a window title
        self.setWindowTitle("Qt Designer Simple example")

    def _connect_signals_to_slots(self):
        """Connect Qt Signals to Qt Slots
        """
        self.buttonOne.clicked.connect(self.button_one_clicked)
        self.buttonTwo.clicked.connect(self.button_two_clicked)
        self.clearButton.clicked.connect(self.textOutput.clear)
        self.clearButton.clicked.connect(self.textInput.clear)
        self.textInput.textChanged.connect(self.textOutput.setText)

    # define Qt Slots #########################################################
    @Slot()
    def button_one_clicked(self):
        self.textOutput.setText("Button 1 clicked")

    @Slot()
    def button_two_clicked(self):
        self.textOutput.setText("Button 2 clicked")

    @Slot()
    def button_clear_clicked(self):
        self.textOutput.clear()


def main():
    # create the application
    app = Application(sys.argv)
    # start the Qt main loop execution
    sys.exit(app.exec_())


if __name__ == '__main__':
    # execute the main function
    main()
