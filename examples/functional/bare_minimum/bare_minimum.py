#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from qtpy.QtWidgets import QApplication, QMainWindow


def main():
    # create the application
    app = QApplication(sys.argv)
    # create the main window
    window = QMainWindow()
    # display the main window
    window.show()
    # start the Qt main loop execution
    sys.exit(app.exec_())


if __name__ == '__main__':
    # execute the main function
    main()
