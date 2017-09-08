#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import modules
import os
from qtpy.QtWidgets import QMainWindow
from qtpy import uic


class QPyMainWindow(QMainWindow):

    def __init__(self, uiFile=None, windowTitle="QPyMainWindow"):
        super().__init__()
        # wire up the userinterface
        self.__setup_ui(uiFile, windowTitle)

    def __setup_ui(self, uiFile, windowTitle):
        """Setup the userinterface.
        """
        # build UI file path
        if uiFile is None:
            uiFile = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "mainwindow.ui"
            )
        # load the UI
        uic.loadUi(uiFile, self)
        # set a window title
        self.setWindowTitle(windowTitle)
