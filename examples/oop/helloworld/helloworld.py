#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from qtpy.QtWidgets import QApplication, QMainWindow, QLabel
from qtpy import QtCore


class Application(QApplication):

    def __init__(self, argv):
        # call the parent (QApplication) constructor
        super().__init__(argv)
        # create the main window
        self.window = QMainWindow()
        # create a label to hold our text
        self.label = QLabel(text="Hello world!", )
        # set the label to align in the center
        self.label.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )
        # get the current font and make it a little bigger
        font = self.label.font()
        font.setPointSize(24)
        # reapply the font to the label
        self.label.setFont(font)
        # add our label to the central widget of the window
        self.window.setCentralWidget(self.label)
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
