#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import modules
import sys
import os
import logging
# import third-party modules
from qtpy.QtWidgets import QApplication, QMainWindow
from qtpy.QtCore import Slot, QTimer
# extend path
sys.path.append(os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    os.path.pardir, os.path.pardir, os.path.pardir
))
# import user modules
from QtPyWidgets import QtLogHandler    # noqa: E402


class Application(QApplication):

    def __init__(self, argv):
        super().__init__(argv)
        self.window = MainWindow()
        self.window.show()
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeoutOccured)
        self.timer.start(250)
        self.logger = logging.getLogger("Main")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.window.log_handler.handler)
        self.counter = 0
        self.level = logging.DEBUG

    @Slot()
    def timeoutOccured(self):
        if self.level > logging.CRITICAL:
            self.level = logging.DEBUG
        self.logger.log(self.level, "Message %d", self.counter)
        self.counter += 1
        self.level += 10


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        # wire up the userinterface
        self.__setup_ui()

    def __setup_ui(self):
        self.log_handler = QtLogHandler(parent=self)
        self.setCentralWidget(self.log_handler)


def main():
    app = Application(sys.argv)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
