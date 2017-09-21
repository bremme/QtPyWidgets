#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from qtpy.QtWidgets import QApplication, QMainWindow


class Application(QApplication):

    def __init__(self, argv):
        super().__init__(argv)
        # create the main window
        self.window = QMainWindow()
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
